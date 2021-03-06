#! /usr/bin/env python3

import sys
import re
import base64
from urllib.request import urlopen
import json

def write_dbc_points(points):
    out_str = '    <string name="ZGJjUG9pbnRzVGhpc1dlZWs=">'
    id_str = str(points)
    id_str = base64.b64encode(bytes(id_str, 'utf-8')).decode("utf-8")
    out_str += id_str
    out_str += '</string>\n'
    out_f.write(out_str)  

if(len(sys.argv) != 2):
    print("ERROR: Need one arg")
    print("Use:",sys.argv[0],"file")
    sys.exit(1)

try:
    input_f = open(sys.argv[1],'r')
except FileNotFoundError:
    print ("ERROR: File '",sys.argv[1],"' does not exist")
    sys.exit(1)
    
try:
    out_f  = open('HACKED_'+sys.argv[1],'w')
except:
    print ('ERROR opening ','HACKED_'+sys.argv[1], ' for writing!')
    sys.exit(1)
        
try:
    players_f = open('players.json','r')
except FileNotFoundError:
    print ("Players json file does not exist, downloading...")
    # url="https://www.easports.com/fifa/ultimate-team/web-app/content/B1BA185F-AD7C-4128-8A64-746DE4EC5A82/2018/fut/items/web/players_meta.json"
    url="https://www.easports.com/fifa/ultimate-team/web-app/content/20C1B296-B15C-4F72-AF0F-882F187EC2C9/2020/fut/items/web/players.json"
    response = urlopen(url)
    players_f = open('players.json', 'a+b')
    players_f.write(response.read())
    players_f.seek(0)

exclude_icons=[1041,166124,5419,1025,240,248146] # icons not in the game (prime)
extra_cards=[-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,67266887020]
id_set=set()
out_str=""
id_str=""

json_data = json.load(players_f)

###
#for player in json_data["Players"]:
#    if player["r"] > 74:
#        print(player)
#sys.exit(0)    
###

for player in json_data["LegendsPlayers"]:
    if player["id"] not in exclude_icons:
        id_set.add(player["id"])
        
for player in json_data["Players"]: # All gold players
    if player["r"] >= 75:
        id_set.add(player["id"])
        
for player in json_data["Players"]: # All silver players
    if player["r"] >= 72 and player["r"] < 75 :
        id_set.add(player["id"])         
        
for player in extra_cards:
    id_set.add(player)
        
#for player in id_set:
#    print(player)
#sys.exit(0)

regex_coins_line      = re.compile(r'^    <string name="Y29pbnM=">.*')
regex_club_name_line  = re.compile(r'^    <string name="Y2x1Yk5hbWU=">.*')
regex_xp_line         = re.compile(r'^    <string name="eHA=">.*')
regex_players_line    = re.compile(r'^    <string name="bXlJZHM=">.*')
regex_dbc_points_line = re.compile(r'^    <string name="ZGJjUG9pbnRzVGhpc1dlZWs=">.*')

for line in input_f:
    if regex_coins_line.match(line):
        out_str = '    <string name="Y29pbnM=">'
        id_str = '100000000' # seems to be the max
        id_str = base64.b64encode(bytes(id_str, 'utf-8')).decode("utf-8")
        out_str += id_str
        out_str += '</string>\n'
        out_f.write(out_str)
        
    elif regex_club_name_line.match(line):
        out_str = '    <string name="Y2x1Yk5hbWU=">'
        id_str = 'HackedByDrNoob'
        id_str = base64.b64encode(bytes(id_str, 'utf-8')).decode("utf-8")
        out_str += id_str
        out_str += '</string>\n'
        out_f.write(out_str)
        
    elif regex_dbc_points_line.match(line):
        write_dbc_points(15000)                  
        
    elif regex_xp_line.match(line):
        out_str = '    <string name="eHA=">'
        id_str = '100'
        id_str = base64.b64encode(bytes(id_str, 'utf-8')).decode("utf-8")
        out_str += id_str
        out_str += '</string>\n'
        out_f.write(out_str)

    elif regex_players_line.match(line):
        #write to player db
        
        out_str = '    <string name="bXlJZHM=">'
        id_str = '{'
        for player_id in id_set:
            id_str += '"id'
            id_str += str(player_id)
            id_str += '":80,'
            
        id_str = id_str[:-1]
        id_str += '}'
        id_str = base64.b64encode(bytes(id_str, 'utf-8')).decode("utf-8") # write IDs as base64!!
        out_str += id_str
        out_str += '</string>\n'
        
        out_f.write(out_str) 

    else:
        out_f.write(line)  
