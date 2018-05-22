#############################################################
# SURVEY PARSER FOR MYSQL DATABASE ENTRY
# AUTHOR: BRANDON DENTON
#
# The following script parses questions and responses for a
# MBTI survey and populates a database of these questions 
# for use by our website, Team Optimizer, to generate MBTI
# scores for its users. This script is meant to generically
# handle survey questions and answers and can parse any set
# of questions written to a file in the following format:
#
# (question starts with integer)  1.    At a party do you:
# (answer starts with a-z) a. Interact with a few
#    b. Interact with a few, known to you 
#    2. Are you more: 
#    a. Realistic than speculative 
#    b. Speculative than realistic 
#    ....
#############################################################
import os
import re
import pymysql
import time
from flask import request, redirect    # I may need this for client calling/automation idk

## Prepare to populate the DB. ##
try:  # attempt to connect
  conn = pymysql.connect(host='173.194.242.125', user='dbtest', password='d4nkm3m3s', db='team09')
except:
  print("Could not contact the database")
  exit(1)
try:
  print("Building questions table....")
  cur.execute('CREATE TABLE questions (text VARCHAR(1024), r1 VARCHAR(1024), r2 VARCHAR(1024), r3 VARCHAR(1024), r4 VARCHAR(1024), id INT(4))')
except:
  cur = conn.cursor()
  cur.execute('DELETE FROM questions')

## Now, actually parse the file. ##
os.chdir("C:/Users/bdenton4/team09/server")
filepath = "questionlist.txt"
with open(filepath, 'r') as qfile:
  i = 0
  for line in qfile:
    slist = re.split('\s+', line)
    if(any(char.isdigit() for char in slist[0])):
      if(questRecord):    # create record from question info
        cur.execute('INSERT INTO questions (text, r1, r2, r3, r4, id) VALUES ("%s", "%s", "%s", "%s", "%s", %s)', questRecord[0], questRecord[1], questRecord[2], questRecord[3], questRecord[4], int(questRecord[5]))
        cur.commit()    # make sure the query executes
        questRecord = []
      questRecord = []
      questRecord[5] = i    # id value
      i += 1
      quest = ""
      for t in range(1, len(slist)):
        quest += slist[i]
        quest += " "
      questRecord[0] = quest    # question text
    if(slist[0] == "a."):
      quest = ""
      for t in range(1, len(slist)):
        quest += slist[i]
        quest += " "
      questRecord[1] = quest    # response a
    if(slist[0] == "b."):
      quest = ""
      for t in range(1, len(slist)):
        quest += slist[i]
        quest += " "
      questRecord[2] = quest    # response b
    if(slist[0] == "c."):
      quest = ""
      for t in range(1, len(slist)):
        quest += slist[i]
        quest += " "
      questRecord[3] = quest    # response c
    if(slist[0] == "d."):
      quest = ""
      for t in range(1, len(slist)):
        quest += slist[i]
        quest += " "
      questRecord[4] = quest    # response d
      
print("Parsing Complete")