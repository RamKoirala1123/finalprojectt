from urllib.parse import quote_plus
import pymongo
username = quote_plus('kshitizbhatta0')
password = quote_plus('Bhatta@123')
cluster = quote_plus('sweetstore.1jgsnjp.mongodb.net')
url = 'mongodb+srv://' + username + ':' + password + '@' + cluster

my_client = pymongo.MongoClient(url)
# First define the database name
# dbname = my_client['Cluster0']

