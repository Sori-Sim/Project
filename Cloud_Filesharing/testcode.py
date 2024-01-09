import pymysql

ENDPOINT="appdb.cfavunhs5tsa.us-east-1.rds.amazonaws.com"
PORT="3306"
USR="admin"
PASSWORD="password1"
DBNAME="appdb"


print("INITIALIZING DATABASE")
conn = pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
cur = conn.cursor()
try:
        cur.execute("DROP TABLE userdetails;") 
        print ("table deleted")
except Exception as e:
    print("cannot delete table")
    cur.execute("CREATE TABLE userdetails(email VARCHAR (20) , password VARCHAR (20), description VARCHAR(50), imagelocation VARCHAR (50));")
    print ("table created" )
    cur.execute("INSERT INTO userdetails(email, password, description, imagelocation) VALUES('test1@gmail.com', 'password', 'this is a desc', 'Default.png');") 
    print ("Insert Success")
    cur.execute("INSERT INTO userdetails(email, password, description, imagelocation) VALUES('test2@gmail.com', 'password', 'this is a desc', 'Default.png');")
    print("Insert Success")
    cur.execute("INSERT INTO userdetails(email, password, description, imagelocation) VALUES('test3@gmail.com', 'password', 'this is a desc', 'Default.png');")
    print("Insert Success")
    cur.execute("INSERT INTO userdetails(email, password, description, imagelocation) VALUES('test4@gmail.com', 'password', 'this is a desc', 'Default.png');") 
    print("Insert Success") 
    conn.commit()
    
    cur.execute ("SELECT * FROM userdetails;")
    query_results = cur.fetchall()
    print(query_results[0][3])