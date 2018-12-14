'''
https://www.periscopedata.com/blog/python-create-table
'''

import csv
import ast
import ibm_db
import ibm_db_dbi
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def dataType(val, current_type):
    try:
        # Evaluates numbers to an appropriate type, and strings an error
        t = ast.literal_eval(val)
    except ValueError:
        return 'varchar'
    except SyntaxError:
        return 'varchar'

    if type(t) in [int, float]:
        if (type(t) in [int]) and current_type not in ['float', 'varchar']:
            if (-32768 < t < 32767) and current_type not in ['int', 'bigint']:
                return 'smallint'
            elif (-2147483648 < t < 2147483647) and current_type not in ['bigint']:
                return 'int'
            else:
                return 'bigint'
        if type(t) is float and current_type not in ['varchar']:
            return 'decimal'
    else:
        return 'varchar'


def createTable(fn, tablename):
    f = open(
        fn, 'r')
    reader = csv.reader(f)

    longest, headers, type_list = [], [], []

    for row in reader:
        if len(headers) == 0:
            headers = row
            for col in row:
                # set default varchar length to 20
                longest.append(20)
                type_list.append('')
        else:
            for i in range(len(row)):
                # NA is the csv null value
                if type_list[i] == 'varchar' or row[i] == 'NA':
                    pass
                else:
                    var_type = dataType(row[i], type_list[i])
                    type_list[i] = var_type
            if len(row[i]) > longest[i]:
                longest[i] = len(row[i])

    f.close()

    statement = 'CREATE TABLE ' + tablename + ' ('
    for i in range(len(headers)):
        if type_list[i] == 'varchar':
            statement = (
                statement + '\n{} varchar({}),').format(headers[i].lower(), str(longest[i]))
        else:
            statement = (statement + '\n' + '{} {}' +
                         ',').format(headers[i].lower(), type_list[i])

    statement = statement[:-1] + ');'

    return statement


# database info
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

# Create database connection
try:
    conn = ibm_db.connect(dsn, "", "")
    print('Connected!')

except:
    print('Unable to connect to database')

# # remove tables
# try:
#   stmt = ibm_db.exec_immediate(conn, 'DROP TABLE CENSUS_DATA')
#   print('Dropped table')
# except:
#     print('Unable to drop table.')

# try:
#   stmt = ibm_db.exec_immediate(conn, 'DROP TABLE CHICAGO_PUBLIC_SCHOOLS')
#   print('Dropped table')
# except:
#     print('Unable to drop table.')

# try:
#   stmt = ibm_db.exec_immediate(conn, 'DROP TABLE CHICAGO_CRIME_DATA')
#   print('Dropped table')
# except:
#     print('Unable to drop table.')

# # create tables
# try:
#     stmt = ibm_db.exec_immediate(
#         conn, createTable(
#             './Census_Data_-_Selected_socioeconomic_indicators_in_Chicago__2008___2012.csv', 'CENSUS_DATA'))

#     print('Created table.')
# except:
#     print('Error: Unable to add table.')

# try:
#     stmt = ibm_db.exec_immediate(
#         conn, createTable(
#             './Chicago_Public_Schools_-_Progress_Report_Cards__2011-2012_.csv', 'CHICAGO_PUBLIC_SCHOOLS'))

#     print('Created table.')
# except:
#     print('Error: Unable to add table.')

# try:
#     stmt = ibm_db.exec_immediate(
#         conn, createTable('./Chicago_Crime_Data.csv', 'CHICAGO_CRIME_DATA'))

#     print('Created table.')
# except:
#     print('Error: Unable to add table.')


pconn = ibm_db_dbi.Connection(conn)

df1 = pd.read_sql('SELECT COUNT(*) FROM CENSUS_DATA', pconn)
df2 = pd.read_sql('SELECT COUNT(*) FROM CHICAGO_PUBLIC_SCHOOLS', pconn)
df3 = pd.read_sql('SELECT COUNT(*) FROM CHICAGO_CRIME_DATA', pconn)

print(df1)
print(df2)
print(df3)

df2 = pd.read_sql('SELECT AVG("College_Enrollment__number_of_students_") AS "Average_College_Enrollment", "Community_Area_Name" FROM CHICAGO_PUBLIC_SCHOOLS GROUP BY "Community_Area_Name"', pconn)

print(df2)

df2 = pd.read_sql('SELECT COUNT("Healthy_Schools_Certified_") FROM CHICAGO_PUBLIC_SCHOOLS WHERE "Healthy_Schools_Certified_" = "Yes"', pconn)

print(df2)

df2 = pd.read_sql('SELECT COUNT("Location_Description") FROM CHICAGO_CRIME_DATA WHERE "Location_Description" = "GAS STATION"', pconn)

print(df2)

df2 = pd.read_sql('SELECT COUNT("Community_Area_Name") AS "Number_of_Schools", "Community_Area_Name" FROM CHICAGO_PUBLIC_SCHOOLS GROUP BY "Community_Area_Name" ORDER BY COUNT("Community_Area_Name") DESC LIMIT 10', pconn)

print(df2)

df2 = pd.read_sql('SELECT COUNT("Primary_Type") FROM CHICAGO_CRIME_DATA WHERE "Primary_Type" = "MOTOR VEHICLE THEFT"', pconn)

print(df2)

df2 = pd.read_sql('SELECT MIN(a."Average_Student_Attendance") AS "Minimum_Value_for_Attendance", a."Community_Area_Name" FROM CHICAGO_PUBLIC_SCHOOLS a INNER JOIN CENSUS_DATA b ON a."Community_Area_Number" = b."Community_Area_Number" WHERE b.hardship_index = 96 GROUP BY a."Community_Area_Name"', pconn)

print(df2)

ibm_db.close(conn)
