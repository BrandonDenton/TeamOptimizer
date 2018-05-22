#!/opt/local/bin/python3.3
#
# Module for GroupSort
#
# ---------------------
#
# This module includes:
#
# Class "pool" of all users to be sorted and pool demographic info
# Class "subgroup" for each subgroup created from users in pool class
# Class "member" with boolean value for E/I, S/N, T/F, J/P corresponding to type
#
# Function "initialize" which reads in information about the pool and stores it in pool class
# Function "lsort" which will be written as the first kind of sort (LAYERS of types - explain elegantly later)
# Function "ssort" which will be written as the second kind (SWAP users to match pool stats)
# Function "print" to show current state of the groups
#
# *** Temporary function "genusers" which generates random member dataset based on user input ***
#
#----------------------
#
# Question about return data? Maybe return an array with data as follows:
#
# [0] Total number of members
# [1] Number of groups
# [2] Group 0 member 0
# [3] Group 0 member 1
# ...
# [n] Group i member j
#
# With each array value being an integer 0-15 that corresponds to an MBTI type:
# To be replaced later with userids in a struct elsewhere in database
#
# *** Anything missing? ***
#
# Also might be fun to later do matplotlib stuff and make some fancy graphs, haha

import time
import pymysql
from numpy import array,arange
from random import randint as rand
import random
#import matplotlib.pyplot as plt





#******************** TO INITIALIZE USERS -- GENERATE OR IMPORT ***********************


#Randomizes a list of numbers from range(low,high)
def randomlist(low,high):
  retlist = []
  for n in range(low,high):
    retlist.append(n)

  i = high - low - 1
  random.seed(10) # random generator seeded to 10 for easy debugging during coding process
  while(i>0):
    index = rand(0,i)
    swap = retlist[i]
    retlist[i] = retlist[index]
    retlist[index] = swap

    i = i - 1

  return retlist

#Generates a list of users (amount "total" and "group" with numE extroverts, numS sensors, etc...with randomized list
#assigning values for each. Randomizes order of people for each, then sets first section of list from range(0,numX)
#in randomized list to that value trait. Sets later values to opposite trait. Prints to text file "Userfile.txt".
def genusers(total, group, numE, numS, numT, numJ):
  allusers = []

  for n in range(0,total):
    allusers.append(Member(n, 0,0,0,0))

  Eorder = randomlist(0,total)
  Sorder = randomlist(0,total)
  Torder = randomlist(0,total)
  Jorder = randomlist(0,total)

  for person in range(0,numE):
    allusers[Eorder[person]].ei = 'e'
  for person in range(numE,total):
    allusers[Eorder[person]].ei = 'i'
  for person in range(0,numS):
    allusers[Sorder[person]].sn = 's'
  for person in range(numS,total):
    allusers[Sorder[person]].sn = 'n'
  for person in range(0,numT):
    allusers[Torder[person]].tf = 't'
  for person in range(numT,total):
    allusers[Torder[person]].tf = 'f'
  for person in range(0,numJ):
    allusers[Jorder[person]].jp = 'j'
  for person in range(numJ,total):
    allusers[Jorder[person]].jp = 'p'
   
  # connect to database
  db = pymysql.connect(host = "173.194.110.138", user = "dbtest", passwd = "d4nkm3m3s", db = "team09" )
  cur = db.cursor()
  
  # insert into db group named 'test' with groupid = '2' 
  numPPG = total/group
  cur.execute("INSERT INTO groups (groupid, admin, groupname, nummembers, numPerGroup, dateCreated) SELECT * FROM (SELECT '2', '0', 'test', %s, %s, CURDATE()) AS tmp WHERE NOT EXISTS (SELECT groupid FROM groups WHERE groupid = '2') LIMIT 1", (total, numPPG))
  
  # insert into db users randomly generated in allusers[] and set these users' pairs, create an array of userids called 'testUsers' for deletion later
  testUsers = []
  for user in allusers:
    testUsers.append(int(user.memnum))
    t = user.ei + user.sn + user.tf + user.jp
    em = "@test.com"
    cur.execute("INSERT INTO users (userid, name, email, type, password) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE userid = %s", (user.memnum, t + str(user.memnum), t + str(user.memnum) + em, t, t, user.memnum))
    cur.execute("INSERT INTO pairs (userid, groupid, admin) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE userid = %s", (user.memnum, '2', '0', user.memnum))

  '''
  # prints out all groups, users, and pairs in current database
  print("current database groups (groupid, admin, groupname, nummembers, numPerGroup, dateCreated):")
  cur.execute("SELECT * FROM groups ORDER BY groupid")
  for group in cur.fetchall():
    print(group)
  print("\n")
  print("current database users (userid, name, email, type, password):")
  cur.execute("SELECT * FROM users ORDER BY userid")
  for user in cur.fetchall():
    print(user)
  print("\n")
  print("current database pairs (userid, groupid, admin):")
  cur.execute("SELECT * FROM pairs ORDER BY userid")
  for pair in cur.fetchall():
    print(pair)
  print("\n")
  '''

  # uncomment code below to delete randomly generated test users, test group, and test pairs from database
  #for test in testUsers:
  #  print("deleting userid = %d" % test)
  #  cur.execute("DELETE FROM users WHERE userid = %s", (test))
  #  cur.execute("DELETE FROM pairs WHERE userid = %s", (test))
  #cur.execute("DELETE FROM groups WHERE groupid = '2'")

  #commit and close database
  db.commit()
  db.close()

#  for user in allusers:
#    print ("%d %s%s%s%s" % (int(user.memnum), user.ei, user.sn, user.tf, user.jp))
#  print("\n")
#  f = open("Userfile.txt", "w")
#  f.write("USERFILE %d %d\n"%(total, group))

#  for person in allusers:
#    f.write("%d %s%s%s%s\n"%(int(person.memnum), person.ei,person.sn,person.tf,person.jp))

#  f.close()


#Reads in users from Userfile.txt, where format is:
# USERFILE totalmembers totalgroups
# userid type
# userid type
# ...
#
#Makes a "Member" object for each and appends to list, returns full list of users at the end

#def importusers(filename):

#  allusers = []

#  f = open(filename, 'r')

#  i = 0

#  for line in f:
#    token = line.split()
#    if(i == 0):
#      totalmembers = int(token[1])
#      totalgroups = int(token[2])
#    else:
#      allusers.append(Member(int(token[0]), token[1][0],token[1][1],token[1][2],token[1][3]))
#    i = i + 1
#
#  f.close()
#
#  return totalmembers, totalgroups, allusers

# connect to database and select groupid = 'test' to sort
def importusers():
  allusers = []
  db = pymysql.connect(host = "173.194.110.138", user = "dbtest", passwd = "d4nkm3m3s", db = "team09" )
  cur = db.cursor()
  cur.execute("SELECT pairs.userid, users.name, pairs.groupid, groups.groupname, users.type, groups.numPerGroup FROM pairs INNER JOIN groups on groups.groupid = pairs.groupid INNER JOIN users on users.userid = pairs.userid WHERE groups.groupname = 'test' ORDER BY groups.groupname")
  i = 0
  numStudentsPerGroup = 0
  members = {}
  for user in cur.fetchall():
    #print(user)
    members[user[0]] = user[1]
    allusers.append(Member((user[0]), user[4][0], user[4][1], user[4][2], user[4][3]))
    if (i == 0):
      numStudentsPerGroup = user[5]
    i = i + 1
  db.close()

  numStudents = i
  numGroups = int(numStudents/numStudentsPerGroup)
  #print("members ID/Name dictionary (userid: name):")
  #print("%s" % members.items())
  #print("\n")
  
  return numStudents, numGroups, allusers, members


#****************************** BEGIN MEMBER CLASS DEFINITION *********************


class Member:

  def __init__(self, mn, ei, sn, tf, jp):
    self.memnum = mn
    self.ei = ei
    self.sn = sn
    self.tf = tf
    self.jp = jp

  # setters for E, S, T, and J
  def setE(self, val):
    self.ei = val
  def setS(self, val):
    self.sn = val
  def setT(self, val):
    self.tf = val
  def setJ(self, val):
    self.jp = val


#******************************** BEGIN POOL DEFINITION ***************************


class Pool:

#Initializes Pool object with groupid, total members, total group, and a list of users.
#Afterwards, analyzes data to pick up total number of E, S, T, and J, as well as percentages
#Also initializes the subgroups from the memberlist after the Pool has been initialized

  def __init__(self, gid, tmem, tgp, usrs, nameMap):

    self.groupid = gid            #initializes variables
    self.totmem = tmem
    self.totgroup = tgp

    self.memlist = usrs           #initializes all memlist
    self.IDNameMap = nameMap

    self.CalcOverallComposition() #analyzes userdata input

    self.grouplist = []


    lorder = randomlist(0,tmem)   #randomly picks user order and splits them into subgroups
    u = 0                         #number of users sorted into current subgroup
    g = gid + 1                   #subgroup's userid
    ng = 0                        #number of subgroups already created
    mg = tmem//tgp                #(members per group = total members // total groups) {// denotes integer divide}
    self.mg = mg

    for sub in range(0,tgp):
      subusers = []               #creates empty subgroup users list

      u = 0
      while(u < mg):              #while fewer than number of members per group
        subusers.append(self.memlist[lorder[ng * mg + u]]) #append memlist[lorder[number group we are on * members per group + members currently in subgroup]]
        u = u + 1                 #add one to users total in subgroup
      self.grouplist.append(Subgroup(g,mg,subusers))  #once done, append to grouplist in Pool object
      g = g + 1                   #increment subgroup id
      ng = ng + 1                 #increment number of groups filled



#************ INITIALIZATION SUBFUNCTIONS HERE ************************


  # calculates the number of target types per group (number of each type per group is
  # to be as close to the class average for that type); it prints to stdout the target
  # numbers afterwards
  def calcTargetTypes(self):
    #print "Percent of E is %f" % self.perE
    i = 1
    while (i < self.mg) and ( float(float(i)/self.mg) < self.perE ):
      i = i + 1
    self.targetNumE = i
    self.targetNumI = self.mg - i
    print ("targetNumE = %d and targetNumI = %d" % (self.targetNumE, self.targetNumI))

    #print "Percent of S is %f" % self.perS
    i = 1
    while (i < self.mg) and ( float(float(i)/self.mg) < self.perS ):
      i = i + 1
    self.targetNumS = i
    self.targetNumN = self.mg - i
    print ("targetNumS = %d and targetNumN = %d" % (self.targetNumS, self.targetNumN))

    #print "Percent of T is %f" % self.perT
    i = 1
    while (i < self.mg) and ( float(float(i)/self.mg) < self.perT ):
      i = i + 1
    self.targetNumT = i
    self.targetNumF = self.mg - i
    print ("targetNumT = %d and targetNumF = %d" % (self.targetNumT, self.targetNumF))

    #print "Percent of J is %f" % self.perJ
    i = 1
    while (i < self.mg) and ( float(float(i)/self.mg) < self.perJ ):
      i = i + 1
    self.targetNumJ = i
    self.targetNumP = self.mg - i
    print ("targetNumJ = %d and targetNumP = %d\n" % (self.targetNumJ, self.targetNumP))

  def CalcOverallComposition(self):
    countE = countS = countT = countJ = 0
    i = 0
    for person in self.memlist:
      if person.ei == 'e':
          countE = countE + 1
      if person.sn == 's':
          countS = countS + 1
      if person.tf == 't':
          countT = countT + 1
      if person.jp == 'j':
          countJ = countJ + 1
      i = i + 1

    self.SetInitialCount(i,countE,countS,countT,countJ)

  def SetInitialCount(self, totalmembers, E, S, T, J):
    self.totmem = totalmembers
    self.e = E
    self.s = S
    self.t = T
    self.j = J
    self.perE = float(float(E)/totalmembers) #next 4 calc with actual vals, currently "percentage extrovert"
    self.perS = float(float(S)/totalmembers)
    self.perT = float(float(T)/totalmembers)
    self.perJ = float(float(J)/totalmembers)


#*********************************** SUBGROUP ANALYSIS HERE ************************************

  # calculates the number of each types in groups formed; it prints to stdout each group's
  # number of types and whether or not each group has met its goal or not (1 for yes, 0 for no,
  # 2 for exceeding target count) as it calculates
  def calcGroupComposition(self):
    i = j = 0
    for subgroup in self.grouplist:
      countE = countS = countT = countJ = 0
      for person in subgroup.memlist:
        #print ("%s%s%s%s" % (person.ei, person.sn, person.tf, person.jp))
        if person.ei == 'e':
          countE = countE + 1
        if person.sn == 's':
          countS = countS + 1
        if person.tf == 't':
          countT = countT + 1
        if person.jp == 'j':
          countJ = countJ + 1
        i = i + 1
        if (i == self.mg):
          print ("group %d" % j)
          subgroup.setTypeNums(countE, self.mg-countE, countS, self.mg-countS, countT, self.mg-countT, countJ, self.mg-countJ)
          subgroup.targetCheck(self.targetNumE, self.targetNumI, self.targetNumS, self.targetNumN, self.targetNumT, self.targetNumF, self.targetNumJ, self.targetNumP)
          print ("groupE = %d; groupI = %d; E/I goal met? %d" % (subgroup.GroupNumE, subgroup.GroupNumI, subgroup.boolEI))
          print ("groupS = %d; groupN = %d; S/N goal met? %d" % (subgroup.GroupNumS, subgroup.GroupNumN, subgroup.boolSN))
          print ("groupT = %d; groupF = %d; T/F goal met? %d" % (subgroup.GroupNumT, subgroup.GroupNumF, subgroup.boolTF))
          print ("groupJ = %d; groupP = %d; J/P goal met? %d" % (subgroup.GroupNumJ, subgroup.GroupNumP, subgroup.boolJP))
          countE = countS = countT = countJ = 0
          i = 0
          j = j + 1


#************************* PRINT FUNCTIONS ************************

  def Print(self, printName):                #prints all members in the object
    if (printName):
      print ("USERID %-10s MB-TYPE" % "NAME")
      for person in self.memlist:
        if person.memnum in IDNameMap:
          print ("%-6d %-10s %s%s%s%s"%(person.memnum, IDNameMap[person.memnum], person.ei, person.sn, person.tf, person.jp))
    else:
      print("USERID MB-TYPE")
      for person in self.memlist:
        print ("%-6d %s%s%s%s"%(person.memnum, person.ei, person.sn, person.tf, person.jp))
        


  def printsub(self, printName):             #calls print on each subgroup, which is same as Print() -- prints all members in object
    itr = 3
    for subgroup in self.grouplist:
      print("Group %d"%itr)
      subgroup.Print(printName)
      itr = itr + 1


#******************************* GROUP BALANCING FUNCTIONS ****************

  def swap(self,g1,g2,u1,u2): #swaps group1[user1] with group2[user2]
    hold = self.grouplist[g1].memlist[u1]
    self.grouplist[g1].memlist[u1] = self.grouplist[g2].memlist[u2]
    self.grouplist[g2].memlist[u2] = hold
    self.calcGroupComposition()
#    self.printsub()


  def jpclean(self):
    print("working on jpclean")
#Figures out cycles to balance j/p issues, i.e.:

#can't swap any in g2 and g3

#swap g1 infp with g3 infj, 1(lowp), 3(balanced), then can swap g1 istj with g2 istp so all balanced

#g1 (balanced)

#infp
#entj
#istj
#esfp

#g2 (lowj)

#enfp
#infj
#estp
#istp

#g3 (lowp)

#esfj
#estp
#infj
#intj


  def balance(self):

    for group1 in range(0,self.totgroup): #iterate through sublists
#      print("GROUP 1 = %d" % group1);
#      match = ""
#      match = match + str(self.grouplist[group1].boolEI)
#      match = match + str(self.grouplist[group1].boolSN)
#      match = match + str(self.grouplist[group1].boolTF)
#      match = match + str(self.grouplist[group1].boolJP)
#      print(match)

      if(self.grouplist[group1].boolEI == 0):  #if current sublist too few E
        print("low E:%d" % group1)
        for group2 in range(0, self.totgroup): #analyze everything further
#          print("GROUP 2 = %d" % group2)
          if(group1 != group2):
            if(self.grouplist[group2].boolEI == 2):  #to find one with too many E
              print("high E:%d" % group2)
              # iterate through members in "under-represented" and "over-represented" subgroups to swap members
              for user1 in range(0, self.mg):
                if(self.grouplist[group1].memlist[user1].ei == 'i'):
                  print("group %d user %d is introvert: %s" % (group1,user1,self.grouplist[group1].memlist[user1].ei))
                  for user2 in range(0, self.mg):
                    if(self.grouplist[group2].memlist[user2].ei == 'e'):
                      print("group %d user %d is extrovert: %s" % (group2,user2,self.grouplist[group2].memlist[user2].ei))
                      if(self.grouplist[group1].boolEI != 1):
                         self.swap(group1,group2,user1,user2)
                      if(self.grouplist[group1].boolEI == 1):
                        print("BALANCED")
                      if((self.grouplist[group1].memlist[user1].ei == 'e') or (self.grouplist[group1].boolEI == 1)):
                        break
                    if((self.grouplist[group1].memlist[user1].ei == 'e') or (self.grouplist[group1].boolEI == 1)):
                      break
                  if((self.grouplist[group1].memlist[user1].ei == 'e') or (self.grouplist[group1].boolEI == 1)):
                    break

      if(self.grouplist[group1].boolEI == 2):  #if current sublist too many E
        print("high E:%d" % group1)
        for group2 in range(0, self.totgroup):               #analyze everything further
#          print("GROUP 2 = %d" % group2)
          if(group1 != group2):
            if(self.grouplist[group2].boolEI == 0):  #to find one with too few E
              print("low E:%d" % group2)
              for user1 in range(0,self.mg):
                if(self.grouplist[group1].memlist[user1].ei == 'e'):
                  print("group %d user %d is extrovert: %s" % (group1,user1,self.grouplist[group1].memlist[user1].ei))
                  for user2 in range(0,self.mg):
                    if(self.grouplist[group2].memlist[user2].ei == 'i'):
                      print("group %d user %d is introvert: %s" % (group2,user2,self.grouplist[group2].memlist[user2].ei))
                      if(self.grouplist[group1].boolEI != 1):
                         self.swap(group1,group2,user1,user2)
                      if(self.grouplist[group1].boolEI == 1):
                        print("BALANCED")
                      if((self.grouplist[group1].memlist[user1].ei == 'i') or (self.grouplist[group1].boolEI == 1)):
                        break
                    if((self.grouplist[group1].memlist[user1].ei == 'i') or (self.grouplist[group1].boolEI == 1)):
                      break
                  if((self.grouplist[group1].memlist[user1].ei == 'i') or (self.grouplist[group1].boolEI == 1)):
                    break
#      print("\n");


    for group1 in range(0,self.totgroup): #iterate through sublists
#      print("GROUP 1 = %d" % group1)
#      match = ""
#      match = match + str(self.grouplist[group1].boolEI)
#      match = match + str(self.grouplist[group1].boolSN)
#      match = match + str(self.grouplist[group1].boolTF)
#      match = match + str(self.grouplist[group1].boolJP)
#      print(match)

      if(self.grouplist[group1].boolSN == 0):
        print("low S:%d" % group1)
        for group2 in range(0, self.totgroup):               #analyze everything further
#          print("GROUP 2 = %d" % group2)
          if(group1 != group2):
            if(self.grouplist[group2].boolSN == 2):
              print("high S:%d" % group2)
              for user1 in range(0,self.mg):
                if(self.grouplist[group1].memlist[user1].sn == 'n'):
                  print("group %d user %d is intuitive: %s" % (group1,user1,self.grouplist[group1].memlist[user1].sn))
                  for user2 in range(0,self.mg):
                    if(self.grouplist[group2].memlist[user2].sn == 's'):
                      print("group %d user %d is sensor: %s" % (group2,user2,self.grouplist[group2].memlist[user2].sn))
                      if(self.grouplist[group1].boolSN != 1) and (self.grouplist[group1].memlist[user1].ei == self.grouplist[group2].memlist[user2].ei):
                         self.swap(group1,group2,user1,user2)
                      if(self.grouplist[group1].boolSN == 1):
                        print("BALANCED")
                      if((self.grouplist[group1].memlist[user1].sn == 's') or (self.grouplist[group1].boolSN == 1)):
                        break
                    if((self.grouplist[group1].memlist[user1].sn == 's') or (self.grouplist[group1].boolSN == 1)):
                      break
                  if((self.grouplist[group1].memlist[user1].sn == 's') or (self.grouplist[group1].boolSN == 1)):
                    break

      if(self.grouplist[group1].boolSN == 2):
        print("high S:%d" % group1)
        for group2 in range(0, self.totgroup):               #analyze everything further
#          print("GROUP 2 = %d" % group2)
          if(group1 != group2):               #analyze everything further
            if(self.grouplist[group2].boolSN == 0):
              print("low S:%d" % group2)
              for user1 in range(0,self.mg):
                if(self.grouplist[group1].memlist[user1].sn == 's'):
                  print("group %d user %d is sensor: %s" % (group1,user1,self.grouplist[group1].memlist[user1].sn))
                  for user2 in range(0,self.mg):
                    if(self.grouplist[group2].memlist[user2].sn == 'n'):
                      print("group %d user %d is intuitive: %s" % (group2,user2,self.grouplist[group2].memlist[user2].sn))
                      if(self.grouplist[group1].boolSN != 1) and (self.grouplist[group1].memlist[user1].ei == self.grouplist[group2].memlist[user2].ei):
                         self.swap(group1,group2,user1,user2)
                      if(self.grouplist[group1].boolSN == 1):
                        print("BALANCED")
                      if((self.grouplist[group1].memlist[user1].sn == 'n') or (self.grouplist[group1].boolSN == 1)):
                        break
                    if((self.grouplist[group1].memlist[user1].sn == 'n') or (self.grouplist[group1].boolSN == 1)):
                      break
                  if((self.grouplist[group1].memlist[user1].sn == 'n') or (self.grouplist[group1].boolSN == 1)):
                    break
#      print("\n");

    for group1 in range(0,self.totgroup): #iterate through sublists
#      print("GROUP 1 = %d" % group1)
#      match = ""
#      match = match + str(self.grouplist[group1].boolEI)
#      match = match + str(self.grouplist[group1].boolSN)
#      match = match + str(self.grouplist[group1].boolTF)
#      match = match + str(self.grouplist[group1].boolJP)
#      print(match)

      if(self.grouplist[group1].boolTF == 0):
        print("low T:%d" % group1)
        for group2 in range(0, self.totgroup):               #analyze everything further
#          print("GROUP 2 = %d" % group2)
          if(group1 != group2):               #analyze everything further
            if(self.grouplist[group2].boolTF == 2):
              print("high T:%d" % group2)
              for user1 in range(0,self.mg):
                if(self.grouplist[group1].memlist[user1].tf == 'f'):
                  print("group %d user %d is feeler: %s" % (group1,user1,self.grouplist[group1].memlist[user1].tf))
                  for user2 in range(0,self.mg):
                    if(self.grouplist[group2].memlist[user2].tf == 't'):
                      print("group %d user %d is thinker: %s" % (group2,user2,self.grouplist[group2].memlist[user2].tf))
                      if(self.grouplist[group1].boolTF != 1) and (self.grouplist[group1].memlist[user1].ei == self.grouplist[group2].memlist[user2].ei) and (self.grouplist[group1].memlist[user1].sn == self.grouplist[group2].memlist[user2].sn):
                         self.swap(group1,group2,user1,user2)
                      if(self.grouplist[group1].boolTF == 1):
                        print("BALANCED")
                      if((self.grouplist[group1].memlist[user1].tf == 't') or (self.grouplist[group1].boolTF == 1)):
                        break
                    if((self.grouplist[group1].memlist[user1].tf == 't') or (self.grouplist[group1].boolTF == 1)):
                      break
                  if((self.grouplist[group1].memlist[user1].tf == 't') or (self.grouplist[group1].boolTF == 1)):
                    break

      if(self.grouplist[group1].boolTF == 2):
        print("high T:%d" % group1)
        for group2 in range(0, self.totgroup):               #analyze everything further
#          print("GROUP 2 = %d" % group2)
          if(group1 != group2):
            if(self.grouplist[group2].boolTF == 0):
              print("low T:%d" % group2)
              for user1 in range(0,self.mg):
                if(self.grouplist[group1].memlist[user1].tf == 't'):
                  print("group %d user %d is thinker: %s" % (group1,user1,self.grouplist[group1].memlist[user1].tf))
                  for user2 in range(0,self.mg):
                    if(self.grouplist[group2].memlist[user2].tf == 'f'):
                      print("group %d user %d is feeler: %s" % (group2,user2,self.grouplist[group2].memlist[user2].tf))
                      if(self.grouplist[group1].boolTF != 1) and (self.grouplist[group1].memlist[user1].ei == self.grouplist[group2].memlist[user2].ei) and (self.grouplist[group1].memlist[user1].sn == self.grouplist[group2].memlist[user2].sn):
                         self.swap(group1,group2,user1,user2)
                      if(self.grouplist[group1].boolTF == 1):
                        print("BALANCED")
                      if((self.grouplist[group1].memlist[user1].tf == 'f') or (self.grouplist[group1].boolTF == 1)):
                        break
                    if((self.grouplist[group1].memlist[user1].tf == 'f') or (self.grouplist[group1].boolTF == 1)):
                      break
                  if((self.grouplist[group1].memlist[user1].tf == 'f') or (self.grouplist[group1].boolTF == 1)):
                    break
#      print("\n");

    for group1 in range(0,self.totgroup): #iterate through sublists
#      print("GROUP 1 = %d" % group1)
#      match = ""
#      match = match + str(self.grouplist[group1].boolEI)
#      match = match + str(self.grouplist[group1].boolSN)
#      match = match + str(self.grouplist[group1].boolTF)
#      match = match + str(self.grouplist[group1].boolJP)
#      print(match)

      if(self.grouplist[group1].boolJP == 0):
        print("low j :%d" % group1)
        for group2 in range(0, self.totgroup):               #analyze everything further
#          print("GROUP 2 = %d" % group2)
          if(group1 != group2):
            if(self.grouplist[group2].boolJP == 2):
              print("high j :%d" % group2)
              for user1 in range(0,self.mg):
                if(self.grouplist[group1].memlist[user1].jp == 'p'):
                  print("group %d user %d is perceiver: %s" % (group1,user1,self.grouplist[group1].memlist[user1].jp))
                  for user2 in range(0,self.mg):
                    if(self.grouplist[group2].memlist[user2].jp == 'j'):
                      print("group %d user %d is judger: %s" % (group2,user2,self.grouplist[group2].memlist[user2].jp))
                      if(self.grouplist[group1].boolJP != 1) and (self.grouplist[group1].memlist[user1].ei == self.grouplist[group2].memlist[user2].ei) and (self.grouplist[group1].memlist[user1].sn == self.grouplist[group2].memlist[user2].sn) and (self.grouplist[group1].memlist[user1].tf == self.grouplist[group2].memlist[user2].tf):
                         self.swap(group1,group2,user1,user2)
                      if(self.grouplist[group1].boolJP == 1):
                        print("BALANCED")
                      if((self.grouplist[group1].memlist[user1].jp == 'j') or (self.grouplist[group1].boolJP == 1)):
                        break
                    if((self.grouplist[group1].memlist[user1].jp == 'j') or (self.grouplist[group1].boolJP == 1)):
                      break
                  if((self.grouplist[group1].memlist[user1].jp == 'j') or (self.grouplist[group1].boolJP == 1)):
                    break

      if(self.grouplist[group1].boolJP == 2):
        print("high j :%d" % group1)
        for group2 in range(0, self.totgroup):               #analyze everything further
#          print("GROUP 2 = %d" % group2)
          if(group1 != group2):
            if(self.grouplist[group2].boolJP == 0):
              print("low j :%d" % group2)
              for user1 in range(0,self.mg):
                if(self.grouplist[group1].memlist[user1].jp == 'j'):
                  print("group %d user %d is judger: %s" % (group1,user1,self.grouplist[group1].memlist[user1].jp))
                  for user2 in range(0,self.mg):
                    if(self.grouplist[group2].memlist[user2].jp == 'p'):
                      print("group %d user %d is perceiver: %s" % (group2,user2,self.grouplist[group2].memlist[user2].jp))
                      if(self.grouplist[group1].boolJP != 1) and (self.grouplist[group1].memlist[user1].ei == self.grouplist[group2].memlist[user2].ei) and (self.grouplist[group1].memlist[user1].sn == self.grouplist[group2].memlist[user2].sn) and (self.grouplist[group1].memlist[user1].tf == self.grouplist[group2].memlist[user2].tf):
                         self.swap(group1,group2,user1,user2)
                      if(self.grouplist[group1].boolJP == 1):
                        print("BALANCED")
                      if((self.grouplist[group1].memlist[user1].jp == 'p') or (self.grouplist[group1].boolJP == 1)):
                        break
                    if((self.grouplist[group1].memlist[user1].jp == 'p') or (self.grouplist[group1].boolJP == 1)):
                       break
                  if((self.grouplist[group1].memlist[user1].jp == 'p') or (self.grouplist[group1].boolJP == 1)):
                    break
#      print("\n");

    for group1 in range(0,self.totgroup): #iterate through sublists
      if(self.grouplist[group1].boolJP != 1):
        print("Need jpclean %d"%group1)
        self.jpclean()


  def updateUserGroups(self):
    db = pymysql.connect(host = "173.194.110.138", user = "dbtest", passwd = "d4nkm3m3s", db = "team09" )
    cur = db.cursor()

    # insert individuals into sorted groups in database (update groups and pairs table)
    groupNum = 3
    t = "team"
    for subgroup in self.grouplist:
      name = t + str(groupNum)
      cur.execute("INSERT INTO groups (groupid, admin, groupname, nummembers, dateCreated) VALUES(%s, '0', %s, %s, CURDATE()) ON DUPLICATE KEY UPDATE groupid = %s", (groupNum, name, self.totmem/self.totgroup, groupNum))
      for person in subgroup.memlist:
        #print("GROUP %d: %d %s%s%s%s" % (groupNum, person.memnum, person.ei, person.sn, person.tf, person.jp))
        cur.execute("INSERT INTO pairs (userid, groupid, admin) VALUES(%s, %s, '0') ON DUPLICATE KEY UPDATE groupid = %s", (person.memnum, groupNum, groupNum))
      groupNum = groupNum + 1
    
    # prints out all groups and pairs in current database
    #print("current database groups (groupid, admin, groupname, nummembes, numPerGroup, dateCreated):")
    #cur.execute("SELECT * FROM groups ORDER BY groupid")
    #for group in cur.fetchall():
    #  print(group)
    #print("\n")
    #cur.execute("SELECT * FROM pairs ORDER BY userid")
    #for pair in cur.fetchall():
    #  print(pair)
    #print("\n")
    
    # commit and close database
    db.commit()
    db.close()

#****************** RUN ************************************************


  # calls on other functions in class Pool to sort groups
  def runSort(self):

    #initialize pool with number of groups
    self.Print(0)
    self.printsub(0)
    print ("\n")
    print ("Target number of each types are:")
    self.calcTargetTypes()
    print ("\n")
    print ("Initial group has the following composition ('boolean value' 1 if target is met, 2 if target has surpassed, and 0 if not met):")
    self.calcGroupComposition()
    print ("\n")
    self.balance()
    self.printsub(1)
    self.updateUserGroups()

#******************************** SUBGROUP DEFINITION *************************


# class for a group, initialized with gorup ID, number of students per team, and array of students in the team
# also contains current number of E/I, S/N, T/F, J/P (to be updated as sorting occurs)
class Subgroup(Pool):
  def __init__(self,gid,tmem,userlist):
    self.groupid = gid
    self.totmem = tmem
    self.memlist = userlist

  # iterates through one group formed to count the number of each types in the group; it generates 8 integers
  # containing count for each type
  def setTypeNums(self, NE, NI, NS, NN, NT, NF, NJ, NP):
    self.GroupNumE = NE
    self.GroupNumI = NI
    self.GroupNumS = NS
    self.GroupNumN = NN
    self.GroupNumT = NT
    self.GroupNumF = NF
    self.GroupNumJ = NJ
    self.GroupNumP = NP

  # given the target number of types per group, this function interates through a group to see if the number of types
  # in the group match the targets. it generates 4 'boolean' values for each type pair, 1 for target met, 2 if target
  # has surpassed, and 0 if target has not been met
  def targetCheck(self, targetE, targetI, targetS, targetN, targetT, targetF, targetJ, targetP):
    self.boolEI = self.boolSN = self.boolTF = self.boolJP = 0
    if (self.GroupNumE == targetE):
      self.boolEI = 1
    elif (self.GroupNumE > targetE):
      self.boolEI = 2
    if (self.GroupNumS == targetS):
      self.boolSN = 1
    elif (self.GroupNumS > targetS):
      self.boolSN = 2
    if (self.GroupNumT == targetT):
      self.boolTF = 1
    elif (self.GroupNumT > targetT):
      self.boolTF = 2
    if (self.GroupNumJ == targetJ):
      self.boolJP = 1
    elif (self.GroupNumJ > targetJ):
      self.boolJP = 2

#need to handle uneven groups, including nE<ngroups


#********************** MAIN *******************

#Initializes pool with subgroups and run
students = 40
numGroups = 5
numExtroverts = 20
numSensing = 20
numThinking = 20
numJudging = 20
print ("Number of students = %d" % students)
print ("Number of groups = %d" % numGroups)
print ("Number of extroverts = %d" % numExtroverts)
print ("Number of sensing = %d" % numSensing)
print ("Number of thinking = %d" % numThinking)
print ("Number of judging = %d\n" % numJudging)

#genusers(40,5,20,20,20,20)
genusers(students, numGroups, numExtroverts, numSensing, numThinking, numJudging)
#members,groups,userlist = importusers("Userfile.txt")
members, groups, userlist, IDNameMap= importusers()
x = Pool(0,members,groups,userlist, IDNameMap)
x.runSort()
#f=open("Userfile.txt","w")
#f.write("")
#f.close()


