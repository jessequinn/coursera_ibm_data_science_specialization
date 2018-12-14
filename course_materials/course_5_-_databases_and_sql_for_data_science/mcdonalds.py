'''
https://www.kaggle.com/mcdonalds/nutrition-facts#menu.csv
'''


import ibm_db
import ibm_db_dbi
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    print('Connected!')

except:
    print('Unable to connect to database')

pconn = ibm_db_dbi.Connection(conn)

df = pd.read_sql('SELECT * FROM MCDONALDS_NUTRITION', pconn)
# print(df.head())

# print(df.describe(include='all'))

print(df['Sodium'].describe())
print(df['Sodium'].idxmax())
print(df.at[82, 'Item'])

f, ax = plt.subplots(2, figsize=(10, 8))


plot = sns.swarmplot(x='Category', y='Sodium', data=df, ax=ax[0])
plt.setp(plot.get_xticklabels(), rotation=70)
plt.title('Sodium Content')

# plot = sns.jointplot(x='Protein', y='Total Fat', data=df)

plot = sns.set_style('whitegrid')
ax = sns.boxplot(x=df['Sugars'], ax=ax[1])

ibm_db.close(conn)
plt.tight_layout()
plt.savefig('mcdonalds.png')
# plt.show()
