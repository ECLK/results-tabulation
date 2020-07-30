import MySQLdb
import sys
import configparser
import io

# validate arguments (dbconfig and sql source file)
if len(sys.argv) < 3:
    print("not enough arguments. dbconfig file and source sql file path required.")
    sys.exit()

# Load the configuration file
config = configparser.ConfigParser()
config.read(sys.argv[1])

hostname = config['mysql']['DATABASE_HOST'].replace("\"", "")
username = config['mysql']['DATABASE_USERNAME'].replace("\"", "")
password = config['mysql']['DATABASE_PASSWORD'].replace("\"", "")
database = config['mysql']['DATABASE_NAME'].replace("\"", "")
portnumb = int(config['mysql']['DATABASE_PORT'].replace("\"", ""))

# Load the mysql source file
with open(sys.argv[2]) as f:
    mysql_queries = f.read()
# connect to the db
conn = MySQLdb.connect(hostname, username, password, database, portnumb)
cursor = conn.cursor()

# execute query
query_array = mysql_queries.split(";")
for query in query_array:
    if query != "\n":
        cursor.execute(query)
        conn.commit()
