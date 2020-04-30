import sqlite3
import pandas as pd

# Read in the processed data file
data = pd.read_csv('Files/Final.csv')
# Create a database connection
conn = sqlite3.connect('fifa_rm.db')
c = conn.cursor()

# Req Columns
nongk_rs_cols = ['potential', 'skill_moves', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
gk_rs_cols = ['gk_diving','gk_handling','gk_kicking','gk_reflexes','gk_speed','gk_positioning']
gen_cols = ['sofifa_id', 'short_name', 'long_name', 'nationality', 'club', 'value_eur', 'team_position', 'GroupCol']
req_cols = gen_cols + nongk_rs_cols + gk_rs_cols

#Main Table
data = data[req_cols]
data.to_sql('all_player_data', con=conn, index=False, if_exists='replace')

# Attacker Players Table
att_data = data[gen_cols + nongk_rs_cols]
att_data = att_data[att_data['GroupCol'] == 'Attacker']
att_data.to_sql('att_player_data', con=conn, index=False, if_exists='replace')

# Mid-Fielder Players Table
mid_data = data[gen_cols + nongk_rs_cols]
mid_data = mid_data[mid_data['GroupCol'] == 'Mid-Fielder']
mid_data.to_sql('mid_player_data', con=conn, index=False, if_exists='replace')

# Defender Players Table
def_data = data[gen_cols + nongk_rs_cols]
def_data = def_data[def_data['GroupCol'] == 'Defender']
def_data.to_sql('def_player_data', con=conn, index=False, if_exists='replace')

# Goalkeeper Players Table
gk_data = data[gen_cols + [nongk_rs_cols[0]] + gk_rs_cols]
gk_data = gk_data[gk_data['GroupCol'] == 'Goalkeeper']
gk_data.to_sql('gk_player_data', con=conn, index=False, if_exists='replace')


conn.close()
