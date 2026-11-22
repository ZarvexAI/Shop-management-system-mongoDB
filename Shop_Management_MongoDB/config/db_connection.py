from pymongo import MongoClient
import os 

def db_connection ():
    try:
        output=MongoClient(os.getenv("DB_URI"))
        print("DB connected successfuly")
        return output
    except Exception as e:
           print("DB connection failed",e)


client=db_connection()
database=client["Shop_Management"]
category_collection= database["Categories"]
product_collection=database["Products"]
sales_collection=database["Sales"]