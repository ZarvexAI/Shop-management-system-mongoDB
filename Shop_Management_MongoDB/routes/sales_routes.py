from fastapi import APIRouter
from config.db_connection import sales_collection, product_collection
from validations.SchemaSales import SchemaCreateSale
from bson.objectid import ObjectId
from datetime import datetime

salesRoutes= APIRouter()

@salesRoutes.post("/create")
def CreateSale(sale_request: SchemaCreateSale):
    try:
        sale_lines = []   
        total_amount = 0  

        for sale_item in sale_request.items:
            try:
                product_object_id = ObjectId(sale_item.product_id)
            except Exception:
                return {"status": "error",
                        "data": [],
                        "message": "Invalid product id"
                        }

            db_product = product_collection.find_one({"_id": product_object_id})
            if db_product is None:
                return {"status": "error",
                        "data": [],
                        "message": "Product not found"
                        }
            
            if sale_item.quantity > db_product["product_stock"]:
                return {
                    "status": "error",
                    "data": [],
                    "message": "Not enough stock for " + db_product["product_name"]
                     }

            line_total = db_product["product_price"] * sale_item.quantity

            sale_lines.append({
                "product_id": str(db_product["_id"]),
                "product_name": db_product["product_name"],
                "price": db_product["product_price"],
                "quantity": sale_item.quantity,
                "line_total": line_total
            })
            total_amount = total_amount + line_total

        for line in sale_lines:
            product_collection.update_one(
                {"_id": ObjectId(line["product_id"])},
                {"$inc": {"product_stock": -line["quantity"]}}
            )

        customer_name = sale_request.customer_name
        if customer_name is None or customer_name.strip() == "":
            customer_name = "Walk-in customer"

        saved_sale = sales_collection.insert_one({
            "customer_name": customer_name.strip(),
            "items": sale_lines,
            "total_amount": total_amount,
            "created_at": datetime.now()
        })


        return {
            "status": "success",
            "data": {
                "sale_id": str(saved_sale.inserted_id),
                 "total_amount": total_amount
                    },
            "message": "Sale completed"
        }

    except Exception as e:
        return {
            "status": "error",
            "data": [],
            "message": str(e)
               }


@salesRoutes.get("/getall")
def GetAllSales():
     try:
         all_sales=list(sales_collection.find().sort("created_at",-1))
         if len(all_sales)==0:
          return{
              "message":"No sales Found"
                }
         else:
           for var in all_sales:
             var["_id"]= str(var["_id"])
    
         return{
               "status":"success",
               "data":all_sales,
               "message":"All Sales Fetched Successfuly"
              }
                
     except Exception as e:
         return{
              "status":"error",
              "data":[],
              "message": str(e)
               }


@salesRoutes.get("/getbyid/{id}")
def GetById(id:str):
    try:
        try:
            sales_id= ObjectId(id)
        except Exception as e:
            return{"message" : "invalid id"}

        req_sale=sales_collection.find_one({"_id":sales_id})
        if not req_sale:
            return {"message":"Sale not found"}
        req_sale["_id"] = str(req_sale["_id"])

        return{
            "status":"success",
            "data": req_sale,
            "message":"Sale fetched successfuly"
        }
    except Exception as e:
        return{
                "status":"success",
                "data":[],
                "message":"Sale fetched successfuly"
                }


@salesRoutes.get("/getbyname/{name}")
def GetbyName(name:str):
    try:
      name_check=name.strip().lower()
      all_sales=list(sales_collection.find())
      by_name=[]
      for single_sale in all_sales:
          if name_check in single_sale["customer_name"].lower().strip():
              single_sale["_id"] = str(single_sale["_id"])
              by_name.append(single_sale)
      if by_name is []:
          return{"message":"Name not found in our record"}
      return{
                "status":"success",
                "data":by_name,
                "message":"Sale fetched successfuly"
            }       

          
    except Exception as e:
         return{
                "status":"success",
                "data":[],
                "message":str(e)
                }


@salesRoutes.delete("/delete/{id}")
def CancelSale (id:str):
    try:
        try:
            sale_id= ObjectId(id)
        except :
            return{"message":"invalid id"}

        sale_check= sales_collection.find_one({"_id":sale_id})
        if not sale_check:
            return{"message":"Sale not found"}

        for line in sale_check["items"]:
          product_collection.update_one(
            {"_id": ObjectId(line["product_id"])},
            {"$inc": {"product_stock": +line["quantity"]}}
                )
          
        sales_collection.delete_one({"_id":sale_id})


        return{
            "status":"success",
            "data":[],
            "message":"Sale cancelled  successfuly"
        }
    
    except Exception as e:
        return{
            "status":"error",
            "data":[],
            "message":str(e)
        }