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
        self.qsname = ''
        self.club = ''
        self.nationality = ''
        self.mval = -1
        self.teampos = ''
        self.k = values
        self.gcolList = ['Attacker', 'Mid-Fielder', 'Defender', 'Goalkeeper']
        self.nongk_rs_cols = ['potential', 'skill_moves', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
        self.gk_rs_cols = ['potential','gk_diving','gk_handling','gk_kicking','gk_reflexes','gk_speed','gk_positioning']
        self.conn = sqlite3.connect(os.path.join(ROOT,"fifa_rm.db"))
        self.c = self.conn.cursor()
        self.resultsList = {}
        print("Connected to database succesfully")

    
    # def getPlayerNames(self, name):
    #     self.queryResult = self.c.execute("SELECT sofifa_id, GroupCol FROM all_player_data WHERE instr(long_name, {} LIMIT 5) > 0".format("'" + name + "'")).fetchall()
    #     self._id = self.queryResult[0]
    #     self.grp = self.queryResult[1]


    def getTopKSimilar(self, name, mval=-1):

        self.queryResult = self.c.execute("SELECT sofifa_id, short_name, nationality, club, value_eur, team_position, GroupCol FROM all_player_data WHERE short_name LIKE '%{}%' LIMIT 5".format(name)).fetchone()
        print(self.queryResult)
        if self.queryResult is not None:
            self._id = self.queryResult[0]
            self.qsname = self.queryResult[1]
            self.nationality = self.queryResult[2]
            self.club = self.queryResult[3]
            self.mval = self.queryResult[4]
            self.teampos = self.queryResult[5]
            self.grp = self.queryResult[6]

            self.resultsList = [self.queryResult]
            for self.gcolvalue in self.gcolList:
                print(self.gcolvalue)
                if self.gcolvalue == "Attacker":
                    self.query = "SELECT * FROM att_player_data WHERE sofifa_id != {}".format(self._id)
                    self.temp_df = pd.read_sql(sql=self.query, con=self.conn)
                elif self.gcolvalue == "Mid-Fielder":
                    self.query = "SELECT * FROM mid_player_data WHERE sofifa_id != {}".format(self._id)
                    self.temp_df = pd.read_sql(sql=self.query, con=self.conn)
                elif self.gcolvalue == "Defender":
                    self.query = "SELECT * FROM def_player_data WHERE sofifa_id != {}".format(self._id)
                    self.temp_df = pd.read_sql(sql=self.query, con=self.conn)
                else:
                    self.query = "SELECT * FROM gk_player_data WHERE sofifa_id != {}".format(self._id)
                    self.temp_df = pd.read_sql(sql=self.query, con=self.conn)
                    
                if self.temp_df is not None:
                    self.tColList = self.temp_df["sofifa_id"].tolist()
                    self.tColList.append(self._id)

                    if self.gcolvalue != "Goalkeeper" and self.grp != "Goalkeeper":
                        self.temp_df = self.temp_df[self.nongk_rs_cols].append(pd.read_sql("SELECT potential, skill_moves, shooting, passing, dribbling, defending, physic from all_player_data WHERE sofifa_id = {}".format(self._id),con=self.conn))
                    elif self.gcolvalue == "Goalkeeper" and self.grp != "Goalkeeper":
                        self.temp_df = self.temp_df[self.gk_rs_cols].append(pd.read_sql("SELECT  potential, gk_diving, gk_handling, gk_kicking, gk_reflexes, gk_speed, gk_positioning from all_player_data WHERE sofifa_id = {}".format(self._id),con=self.conn))

                    # elif self.gcolvalue == "Goalkeeper" and self.grp == "Goalkeeper":
                    #     self.temp_df = self.temp_df[self.gk_rs_cols].append(pd.read_sql("SELECT  potential, gk_diving, gk_handling, gk_kicking, gk_reflexes, gk_speed, gk_positioning from all_player_data WHERE sofifa_id = {}".format(self._id),con=self.conn))

                    
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
                        self.rcms = self.c.execute("SELECT sofifa_id, short_name, club, nationality, value_eur, team_position, GroupCol from all_player_data WHERE sofifa_id in {0}".format(self.req_ids)).fetchall()
                        self.resultsList.append(self.rcms)
                      
                        # self.rcms.append(self.qsname)
                        # for self.val in self.rcms:
                        #     print(self.val[0])
                        # print(self.rcms)
                        
                    except:
                        print("Player id not present in matrix")
                        print(4)
                    
                
                else:
                    print("No data found for your query")
                    return [self.qsname]
            print(self.resultsList)
            print(len(self.resultsList))                        
            return self.resultsList
        else:
            print("Player does not exist in database!")
            self.c.close()
            self.conn.close()
            return