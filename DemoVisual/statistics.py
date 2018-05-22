#!/usr/bin/env python3
#
#Annika Jusino, CS370, HW 10

from numpy import *
import matplotlib.pyplot as plt
from GroupSort import *
import sys

'''

This program runs x amount of tests (user input) and shows the average difference
between the randomized and sorted data. It also shows a side-by-side comparison
of sorted/unsorted/ideal group composition data for the first thread to complete.


'''

# The code that the thread executes goes here:
def test(total, numgroup, E, S, T, J) :
# nE = number of E, nS = number of S ... each index corresponds to statistics, where [0] is ideal, [1 - m] is random groups (i.e "pre-sort"), [m+1 - n] is groups after sort
     nE = []
     nS = []
     nT = []
     nJ = []

#in the future, will query and count total users -- currently generates and imports users from text file

     genusers(total, numgroup, E, S, T, J)

     members,groups,userlist = importusers("Userfile.txt")

     x = Pool(0, members, groups, userlist)
         
     x.calcTargetTypes()
         
     nE.append(x.targetNumE)
     nS.append(x.targetNumS)
     nT.append(x.targetNumT)
     nJ.append(x.targetNumJ)

     x.calcGroupComposition()

     for subgroup in x.grouplist:
          nE.append(subgroup.GroupNumE)
          nS.append(subgroup.GroupNumS)
          nT.append(subgroup.GroupNumT)
          nJ.append(subgroup.GroupNumJ)

     x.balance()

     for subgroup in x.grouplist:
          nE.append(subgroup.GroupNumE)
          nS.append(subgroup.GroupNumS)
          nT.append(subgroup.GroupNumT)
          nJ.append(subgroup.GroupNumJ)

     f=open("Userfile.txt","w")
     f.write("")
     f.close()

     return (nE, nS, nT, nJ)



if(len(sys.argv) < 7):
     print("Usage: 'python statistics.py TotalGroupMembers NumberOfGroups NumberE NumberS NumberT NumberJ'")
     exit(0)

total = int(sys.argv[1])
ngroups = int(sys.argv[2])
e = int(sys.argv[3])
s = int(sys.argv[4])
t = int(sys.argv[5])
j = int(sys.argv[6])

arrE, arrS, arrT, arrJ = test(total, ngroups, e, s, t, j)

print(arrE)
print(arrS)
print(arrT)
print(arrJ)

arrI = []
arrN = []
arrF = []
arrP = []

for n in range(0,len(arrE)):
     arrI.append(int(total/ngroups) - arrE[n])
     arrN.append(int(total/ngroups) - arrS[n])
     arrF.append(int(total/ngroups) - arrT[n])
     arrP.append(int(total/ngroups) - arrJ[n])
     
print(arrE)
print(arrS)
print(arrT)
print(arrJ)
print(arrI)
print(arrN)
print(arrF)
print(arrP)


N = 1 +(ngroups * 2)

indices = arange(N)
width = 1

p1 = plt.bar(indices, arrE, width, color = 'red', label = 'E')
p2 = plt.bar(indices, arrI, width, color = 'pink', label = 'I',bottom = arrE)
p3 = plt.bar(indices, arrS, width, color = 'orange', label = 'S',bottom = [arrE[j] +arrI[j] for j in range(len(arrE))])
p4 = plt.bar(indices, arrN, width, color = 'yellow', label = 'N',bottom = [arrE[j] +arrI[j] +arrS[j] for j in range(len(arrE))])
p5 = plt.bar(indices, arrT, width, color = 'green', label = 'T',bottom = [arrE[j] +arrI[j] +arrS[j] +arrN[j] for j in range(len(arrE))])
p6 = plt.bar(indices, arrF, width, color = 'lawngreen', label = 'F',bottom = [arrE[j] +arrI[j] +arrS[j] +arrN[j] +arrT[j] for j in range(len(arrE))])
p7 = plt.bar(indices, arrJ, width, color = 'blue', label = 'J',bottom = [arrE[j] +arrI[j] +arrS[j] +arrN[j] +arrT[j] + arrF[j] for j in range(len(arrE))])
p8 = plt.bar(indices, arrP, width, color = 'cyan', label = 'P',bottom = [arrE[j] +arrI[j] +arrS[j] +arrN[j] +arrT[j] + arrF[j] +arrJ[j] for j in range(len(arrE))])


plt.ylabel("Number of each type")
plt.title("Group composition: ideal, before sort, after sort")
plt.legend(bbox_to_anchor=(1,1),loc = 'upper left', fontsize = 12)
plt.xlim(0,N)

plt.show()

