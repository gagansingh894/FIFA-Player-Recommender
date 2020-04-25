import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import sigmoid_kernel
import sqlite3
import os

ROOT = os.path.dirname(os.path.relpath(__file__))

class Recommendations:

    def __init__(self, values=5):
        self._id = -1
        self.grp = ''
        # self.name = ''
        # self.club = ''
        # self.nationality = ''
        # self.mval = -1
        self.k = values
        self.nongk_rs_cols = ['potential', 'skill_moves', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
        self.gk_rs_cols = ['potential','gk_diving','gk_handling','gk_kicking','gk_reflexes','gk_speed','gk_positioning']
        self.conn = sqlite3.connect(os.path.join(ROOT,"fifa_rm.db"))
        self.c = self.conn.cursor()
        print("Connected to database succesfully")

    def getTopKSimilar(self, name, club='', nationality='', mval=-1):

        self.queryResult = self.c.execute("SELECT sofifa_id, GroupCol FROM player_data WHERE short_name = {}".format("'" + name + "'")).fetchone()
        if self.queryResult is not None:
            self._id = self.queryResult[0]
            self.grp = self.queryResult[1]

            if club == '' and nationality == '' and mval == -1:
                self.query = "SELECT * FROM player_data WHERE GroupCol = {}".format("'" + self.grp + "'") # DEFAULT QUERY
            elif club != '' and nationality == '' and mval == -1:
                self.query = "SELECT * FROM player_data WHERE GroupCol = {} AND club = {} OR sofifa_id = {}".format("'" + self.grp + "'", "'" + club + "'", self._id)
            elif club == '' and nationality != '' and mval == -1:
                self.query = "SELECT * FROM player_data WHERE GroupCol = {} AND nationality = {} OR sofifa_id = {}".format("'" + self.grp + "'", "'" + nationality + "'", self._id)
            elif club != '' and nationality != '' and mval == -1:
                self.query = "SELECT * FROM player_data WHERE GroupCol = {} AND club = {} AND nationality = {} OR sofifa_id = {}".format("'" + self.grp + "'", "'" + club + "'", "'" + nationality + "'", self._id)
            elif club == '' and nationality == '' and mval != -1:
                self.query = "SELECT * FROM player_data WHERE GroupCol = {} AND value_eur <= {} OR sofifa_id = {}".format("'" + self.grp + "'", mval, self._id)
            elif club != '' and nationality == '' and mval != -1:
                self.query = "SELECT * FROM player_data WHERE GroupCol = {} AND club = {} AND value_eur <= {} OR sofifa_id = {}".format("'" + self.grp + "'", "'" + club + "'", mval, self._id)
            elif club == '' and nationality == '' and mval != -1:
                self.query = "SELECT * FROM player_data WHERE GroupCol = {} AND nationality = {} AND value_eur <= {} OR sofifa_id = {}".format("'" + self.grp + "'", "'" + nationality + "'", mval, self._id)
            else:
                self.query = "SELECT * FROM player_data WHERE GroupCol = {} AND club = {} AND nationality = {} AND value_eur <= {} OR sofifa_id = {}".format("'" + self.grp + "'", "'" + club + "'", "'" + nationality + "'", mval, self._id)


            self.temp_df = pd.read_sql(sql=self.query, con=self.conn)
            if self.temp_df is not None:
                self.tColList = self.temp_df["sofifa_id"].tolist()
           

                if self.grp != "Goalkeeper":
                    self.temp_df = self.temp_df[self.nongk_rs_cols]
                else:
                    self.temp_df = self.temp_df[self.gk_rs_cols]

                
                self.sc = StandardScaler()
                self.temp_df = self.sc.fit_transform(self.temp_df)
                self.temp_df = sigmoid_kernel(self.temp_df,self.temp_df)
                self.temp_df = pd.DataFrame(self.temp_df, columns=self.tColList, index=self.tColList)
                del self.sc, self.tColList

                try:
                    self.tempDict = self.temp_df[self._id].to_dict()
                    self.tempList = list({k: v for k, v in sorted(self.tempDict.items(), key=lambda item: item[1], reverse=True)}.keys())
                    self.tempList.remove(self._id)
                    self.req_ids = tuple(self.tempList[0:self.k])
                    self.rcms = self.c.execute("SELECT short_name FROM player_data WHERE sofifa_id in {0}".format(self.req_ids)).fetchall()
                    # for self.val in self.rcms:
                    #     print(self.val[0])
                    return self.rcms
                except:
                    print("Player id not present in matrix")

            else:
                print("No data found for your query")
                return

        else:
            print("Player does not exist in database!")
            self.c.close()
            self.conn.close()
            return