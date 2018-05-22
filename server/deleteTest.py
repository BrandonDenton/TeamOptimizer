import pymysql

db = pymysql.connect(host = "173.194.110.138", user = "dbtest", passwd = "d4nkm3m3s", db = "team09" )
cur = db.cursor()
cur.execute("SELECT groupid FROM groups WHERE groupname = 'test'")
gid = cur.fetchone();
cur.execute("SELECT userid FROM pairs WHERE groupid = %s", (gid))
groupToDelete = [];
usersToDelete = [];
for pairUID in cur.fetchall():
  cur.execute("SELECT groupid FROM pairs WHERE userid = %s", (pairUID))
  usersToDelete.append(pairUID)
  for groupid in cur.fetchall():
    groupToDelete.append(groupid)
groupToDelete = list(set(groupToDelete))
usersToDelete = list(set(usersToDelete))
for group in groupToDelete:
  cur.execute("DELETE FROM groups WHERE groupid = %s", (group))
  cur.execute("DELETE FROM pairs WHERE groupid = %s", (group))
for user in usersToDelete:
  cur.execute("DELETE FROM users WHERE userid = %s", (user))
'''
print("current groups:")
cur.execute("SELECT * FROM groups")
for group in cur.fetchall():
  print(group)
print("current users:")
cur.execute("SELECT * FROM users")
for user in cur.fetchall():
  print(user)
print("current pairs:")
cur.execute("SELECT * FROM pairs")
for pair in cur.fetchall():
  print(pair)
'''
db.commit()
db.close()
