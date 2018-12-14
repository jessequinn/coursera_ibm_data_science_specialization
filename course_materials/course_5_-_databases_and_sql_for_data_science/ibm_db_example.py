'''
Set DYLD_LIBRARY_PATH in bash_profile for ibm_db module to work
as per https://github.com/ibmdb/python-ibmdb/tree/master/IBM_DB/ibm_db

export DYLD_LIBRARY_PATH=/Users/jessequinn/.pyenv/versions/3.6.0/lib/python3.6/site-packages/clidriver/lib:$DYLD_LIBRARY_PATH
'''


import ibm_db
import ibm_db_dbi
import pandas as pd

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_hostname = "dashdb-entry-yp-dal10-01.services.dal.bluemix.net"
dsn_port = "50000"
dsn_protocol = "TCPIP"
dsn_uid = "USERNAME"
dsn_pwd = "PASSWORD"

# Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)

# print the connection string to check correct values are specified
# print(dsn)

# Create database connection

try:
    conn = ibm_db.connect(dsn, "", "")
    print("Connected!")

except:
    print("Unable to connect to database")

try:
  stmt = ibm_db.exec_immediate(
      conn, "CREATE TABLE trucks(serial_no VARCHAR(20) PRIMARY KEY NOT NULL, model VARCHAR(20) NOT NULL, manufacturer VARCHAR(20) NOT NULL, engine_size VARCHAR(20) NOT NULL, truck_class VARCHAR(20) NOT NULL)")
  
  print('Created table.')
except:
  print('Error: Unable to add table.')

try:
  stmt = ibm_db.exec_immediate(conn, "INSERT INTO trucks(serial_no, model, manufacturer, engine_size, truck_class) VALUES('A1234','Lonestar','International Trucks','Cummins ISX15', 'Class 8');")

  print('Inserted data.')
except:
  print('Error: Cannot insert data.')

try:
  stmt = ibm_db.exec_immediate(conn, "INSERT INTO trucks(serial_no, model, manufacturer, engine_size, truck_class) VALUES('B5432','Volvo VN','Volvo Trucks','Volvo D11', 'Heavy Duty Class 8');")

  print('Inserted data.')
except:
  print('Error: Cannot insert data.')

try:
  stmt = ibm_db.exec_immediate(conn, "INSERT INTO trucks(serial_no, model, manufacturer, engine_size, truck_class) VALUES('C5674','Kenworth W900','Kenworth Truck Co','Caterpillar C9', 'Class 8');")

  print('Inserted data.')
except:
  print('Error: Cannot insert data.')

try:
  stmt = ibm_db.exec_immediate(conn, "SELECT * FROM trucks")
  res = ibm_db.fetch_both(stmt)
  
  # print(res)
except:
  print("Error: Select statement failed.")

pconn = ibm_db_dbi.Connection(conn)

df = pd.read_sql('SELECT * FROM trucks', pconn)
print(df.head())

ibm_db.close(conn)
