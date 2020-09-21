import pymysql
conn=pymysql.connect(host='localhost',user='root',passwd='WWWangenei1998!@#',db='www',charset='utf8')
cursor=conn.cursor()
sql="INSERT INTO usertb(username,age)values('hzh',21)"
cursor.execute(sql)
conn.commit()
cursor.execute("SELECT VERSION()")
data=cursor.fetchone()
print("version:%s" %data)
conn.close()