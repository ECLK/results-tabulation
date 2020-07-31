import MySQLdb
import sys

# validate arguments (dbconfig and sql source file)
if len(sys.argv) < 7:
    print("not enough arguments. dbconfig file and source sql file path required.")
    sys.exit()

hostname = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
database = sys.argv[4]
port = int(sys.argv[5])

# Load the mysql source file
with open(sys.argv[6]) as f:
    mysql_queries = f.read()

# connect to the db
conn = MySQLdb.connect(hostname, username, password, database, port)
cursor = conn.cursor()

# execute query
query_array = mysql_queries.split(";")
for query in query_array:
    if query != "\n":
        cursor.execute(query)
        conn.commit()
