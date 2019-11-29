import mysql.connector

# connector for DB...
class DBConnection:
	def __init__(self, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD):
		self.host = DB_HOST
		self.database = DB_NAME
		self.user = DB_USER
		self.password = DB_PASSWORD
		self.conn = None


	def get_conn(self):
		if self.conn is None:
			self.conn = mysql.connector.connect(host=self.host,
										database=self.database,
										user=self.user,
										passwd=self.password)
		return self.conn



#mydbconnobj = DBConnection("localhost","testdb","root","yourpasswordhere")
#mydbconn = mydbconnobj.get_conn()

# create DB with your own name
class CreateDB:
	def create(self):
		mydb = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="yourpasswordhere!"
		)
		mycursor = mydb.cursor()
		mycursor.execute("CREATE DATABASE kraken")
#la = CreateDB()
#la.create()
