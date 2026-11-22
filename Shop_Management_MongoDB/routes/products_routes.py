from fastapi import APIRouter
from validations.SchemaProducts import SchemaProducts, SchemaRestock
from config.db_connection import product_collection, category_collection
from bson.objectid import ObjectId
import datetime

productsRoutes= APIRouter()

@productsRoutes.post("/create")
def CreateProduct(productData:SchemaProducts):
    try:
        new_name = productData.product_name.strip().lower()
        
        all_products = list(product_collection.find())
        
        for check in all_products:
            if check["product_name"].strip().lower() == new_name:
             return {
                        "status": "error",
                        "data": [],
                        "message": "Product already exists"
                    }

        category_check= False
        for var in list(category_collection.find ()):
         if var["category_name"].strip().lower()== productData.product_category.strip().lower():
             category_check= True
             real_product_category= var["category_name"]

        if category_check ==  False:
          return{"message":"Category does not exist yet",
                 "status":"error",
                 "data":[]}

        created_data= product_collection.insert_one({
                    "product_name": productData.product_name.strip().lower(),
                    "product_category": real_product_category,
                    "product_price": productData.product_price,
                    "product_stock": productData.product_stock,
                    "product_low_stock_limit": productData.product_low_stock_limit,
                    "product_description": productData.product_description,
                    "created_at": datetime.datetime.now()
                })
        return{
                "status": "success",
                "data":{
                   "_id": str(created_data.inserted_id),
                     "product_name": productData.product_name,
                     "product_category": real_product_category,
                     "product_price": productData.product_price,
                     "product_stock": productData.product_stock,
                     "product_low_stock_limit": productData.product_low_stock_limit,
                     "product_description": productData.product_description
                }, 
                "message": "Product created successfully"
            }
    except Exception as e: 
        return{
                "status": "error",
                "data": [],
                "message": str(e)
            }


@productsRoutes.get("/getall")
def GetAllProducts():
   try:
    all_products=list(product_collection.find())
    for cat in all_products:
        cat["_id"]= str(cat["_id"])
    return{
       "status":"success",
       "data":all_products,
       "message":"All products fetched"
    }
   except Exception as e:
      return{
         "status":"error",
         "data":[],
         "message":str(e)
      }


@productsRoutes.get("/getby/{category}")
def GetAllProducts(category:str):
   try:
    check_category = category.strip().lower()
    allproducts=list(product_collection.find())
    byCategory=[]
    for item in allproducts:
       item["_id"]=str(item["_id"])
       if item["product_category"].strip().lower() == check_category:
          byCategory.append(item)
    if byCategory == []:
       return{"message":"category is not in our record"}      

    return{
       "status":"success",
       "data": byCategory,
       "message":"All records fetched on basis of category"
    }
    
   except Exception as e:
      return{
         "status":"error",
         "data":[],
         "message":str(e)
      }


@productsRoutes.get("/getbyname/{name}")
def GetAllProducts(name:str):
   try:
    
    check_name = name.strip().lower()
    allproducts=list(product_collection.find())
    byname=[]
    for item in allproducts:
       item["_id"]=str(item["_id"])
       if check_name in item["product_name"].strip().lower():
          byname.append(item)
    if byname == []:
       return{"message":"name is not in our record"}
          
    return{
       "status":"success",
       "data": byname,
       "message":"All records fetched on basis of name"
    }
    
   except Exception as e:
      return{
         "status":"error",
         "data":[],
         "message":str(e)
      }
   

@productsRoutes.get("/low-stock")
def GetLowStockList():
   try:
      full_list= list(product_collection.find())
      low_stock_list= []
      for var in full_list:
         if var["product_stock"] <= var["product_low_stock_limit"]:
            var["_id"] = str(var["_id"])
            low_stock_list.append(var)

      if low_stock_list is []:
         return{"message" : "No stock is low limit right now"}

      return{
         "status":"success",
         "data":low_stock_list,
         "message":"Low stock list fetched successfuly"
      }
   
   except Exception as e:
      return{
         "status":"error",
         "data":[],
         "message":str(e)
      }


@productsRoutes.get("/getbyid/{id}")
def GetById (id:str):
    try:
        try:
            product_id = ObjectId(id)
        except Exception:
            return {
                "status": "error",
                "data": [],
                "message": "Invalid product id"
            }
        req_product = product_collection.find_one({"_id": product_id})
        if req_product is None:
            return {
                "status": "error",
                "data": [],
                "message": "Product not found"
            }
        req_product["_id"] = str(req_product["_id"])
        return {
            "status": "success",
            "data": req_product,
            "message": "Product fetched successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "data": [],
            "message": str(e)
        }


@productsRoutes.put("/update/{id}")
def productUpdate (id:str, updated_data:SchemaProducts):
   try:
      try:
         productid= ObjectId(id)

      except Exception as e:
         return {"message":"Invalid product id"}

      req_product= product_collection.find_one({"_id":productid})

      if req_product is None:
         return{"message":"Product not found"}
      
      name_check = updated_data.product_name.strip().lower()
        
      all_products = list(product_collection.find())
        
      for check in all_products:
       if check["product_name"].strip().lower() == name_check:
         return {
                  "status": "error",
                  "data": [],
                  "message": "Product already exists"
                    }
      category_check= False
      for var in list(category_collection.find ()):
          if var["category_name"].strip().lower()== updated_data.product_category.strip().lower():
             category_check= True
             real_product_category= var["category_name"]
      
      if category_check ==  False:
       return{"message":"Category does not exist yet",
              "status":"error",
              "data":[]}
      
      
      var= dict(updated_data)
      var["product_category"]= real_product_category
      product_collection.update_one({"_id":productid},{"$set":var})
      req_updated_data=product_collection.find_one({"_id":productid})
      req_updated_data["_id"]= str(req_updated_data["_id"])
           
      return{
         "status":"success",
         "data":req_updated_data,
         "message":"Product updated successfuly"
      }

   except Exception as e:
      return{
         "status":"error",
         "data":[],
         "message":str(e)
      }


@productsRoutes.patch("/restock/{id}")
def RestockProduct(id:str, restock_value:SchemaRestock):
   try:
      try:
         productid= ObjectId(id)
   
      except Exception as e:
         return {"message":"Invalid product id"}
   
      req_product= product_collection.find_one({"_id":productid})
   
      if req_product is None:
       return{"message":"Product not found"}

      restocking_data= product_collection.update_one({"_id":productid},{"$inc":{"product_stock":restock_value.restock_quantity}})
      restocked_data=product_collection.find_one({"_id":productid})
      restocked_data["_id"]=str(restocked_data["_id"])
      return{
         "status":"success",
         "data":restocked_data,
         "message":"Product restocked successfuly"
      }
   except Exception as e:
      return{
               "status":"error",
               "data":[],
               "message":str(e)
            }


@productsRoutes.delete("/delete/{id}")
def DeleteProduct(id:str):
   try:
      try:
         productid= ObjectId(id)
      
      except Exception as e:
         return {"message":"Invalid product id"}
      
      req_product= product_collection.find_one({"_id":productid})
      
      if req_product is None:
       return{"message":"Product not found"}

      product_collection.delete_one({"_id":productid})


      return{
         "status":"success",
         "data":[],
         "message":"product deleted successfuly"
      }

   except Exception as e:
      return{
         "status":"error",
         "data":[],
         "message":str(e)
      }