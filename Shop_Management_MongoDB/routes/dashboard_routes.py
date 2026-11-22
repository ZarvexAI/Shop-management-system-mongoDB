from fastapi import APIRouter
import datetime
from config.db_connection import sales_collection, product_collection, category_collection
dashboardRoutes= APIRouter()

@dashboardRoutes.get("/summary")
def getsummary():
    try:
        product_list=(list(product_collection.find()))
        total_product_count=len(product_list)

        stock_value= 0
        low_stock_count= 0

        for item in product_list:
            stock_result =item["product_price"] * item["product_stock"]
            stock_value = stock_value + stock_result
            if item["product_stock"] <= item["product_low_stock_limit"]:
                low_stock_count = low_stock_count + 1

        today_sales_count=0
        today_sales_total=0
        todays_date= datetime.datetime.now().date()
        for item in list(sales_collection.find()): 
            if item["created_at"].date() == todays_date:
                today_sales_count= today_sales_count + 1
                today_sales_total= today_sales_total + item["total_amount"]

        return{
            "status":"success",
            "data":{
                    "Total_product":total_product_count,
                    "Total_stock_value":stock_value,
                    "Low_stock_count":low_stock_count,
                    "Todays_sales":today_sales_count,
                    "Today_sales_total":today_sales_total
                    },
            "message":"Summary fetched succesfuly"
            }

    except Exception as e:
        return{
            "status":"error",
            "data":[],
            "message":str(e)
        }