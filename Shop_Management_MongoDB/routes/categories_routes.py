from fastapi import APIRouter
from validations.SchemaCategories import SchemaCategories
from config.db_connection import category_collection ,product_collection
from bson.objectid import ObjectId
categoryRoutes= APIRouter()


@categoryRoutes.post("/create")
def CreateCategory(category_data:SchemaCategories):
    try:   
          new_name = category_data.category_name.strip().lower()

          all_categories = list(category_collection.find())

          for check in all_categories:
           if check["category_name"].strip().lower() == new_name:
               return {
                    "status": "error",
                    "data": [],
                    "message": "Category already exists"
               }
               
          created_data= category_collection.insert_one({
            "category_name":category_data.category_name,
            "category_description":category_data.category_description
            })

          return{
              "status":"success",
              "data": {
                   "_id":str(created_data.inserted_id),
                   "category_name":category_data.category_name,
                   "category_description":category_data.category_description
                      },
             "message":"Category created successfuly"
                   }
    except Exception as e:
         return{
              "status":"error",
              "data":[],
              "message": str(e)
               }


@categoryRoutes.get("/getall")
def GetAllCategories():
    try:
          all_categories=list(category_collection.find())
          if len(all_categories)==0:
              return{
                  "status":"error",
                  "data":[],
                  "message":"No Category Found"
              }
          else:
               for var in all_categories:
                   var["_id"]= str(var["_id"])

          return{
                  "status":"success",
                  "data":all_categories,
                  "message":"All Categories Fetched Successfuly"
              }
            
    except Exception as e:
         return{
              "status":"error",
              "data":[],
              "message": str(e)
               }


@categoryRoutes.get("/search/{id}")
def SearchById (id:str):
    try:      
       search_category=category_collection.find_one({"_id":ObjectId(id)})
       if search_category is None:
           return{
               "status":"error",
               "data":[],
               "message":"Category Not Found"
           }
       search_category["_id"] = str(search_category["_id"])

       return{
           "status":"success",
           "data":search_category, 
           "message":"Category Fetched Successfuly"
             }

    except Exception as e:
         return{
              "status":"error",
              "data":[],
              "message": str(e)
               }


@categoryRoutes.put("/update/{id}")
def UpdateCategory(id: str, updated_data: SchemaCategories):
    try:
        try:
            categoryid = ObjectId(id)
        except Exception:
            return {"status": "error",
                    "data": [],
                    "message": "Invalid category id"
                    }

        req_category = category_collection.find_one({"_id": categoryid})
        if req_category is None:
            return {"status": "error", "data": [], "message": "Category not found"}

        old_name = req_category["category_name"]
        new_name = updated_data.category_name.strip()


        for cat in category_collection.find():
            if cat["_id"] != categoryid and cat["category_name"].strip().lower() == new_name.lower():
                return {"status": "error", "data": [], "message": "Category already exists"}


        update_data = dict(updated_data)
        update_data["category_name"] = new_name
        category_collection.update_one({"_id": categoryid}, {"$set": update_data})

        if old_name != new_name:
            product_collection.update_many(
                {"product_category": old_name},
                {"$set": {"product_category": new_name}}
            )

        result = category_collection.find_one({"_id": categoryid})
        result["_id"] = str(result["_id"])

        return {"status": "success",
                "data": result,
                "message": "Category updated successfully"
                }


    except Exception as e:
        return{
                 "status":"error",
                 "data":[],
                 "message": str(e)
          }


@categoryRoutes.delete("/delete/{id}")
def DeleteCategory (id:str):
     try:
        try:
            category_id = ObjectId(id)
        except Exception:
            return {
                "status": "error",
                "data": [],
                "message": "Invalid product id"
            }
        req_category = category_collection.find_one({"_id": category_id})
        if req_category is None:
            return {
                "status": "error",
                "data": [],
                "message": "Product not found"
            }

        category_name=req_category["category_name"].strip().lower()
        for products in product_collection.find():
            if products["product_category"].lower().strip()==category_name:
                  return {
                    "status": "error",
                    "data": [],
                    "message": "Category is used by products, cannot delete"
                }
       
        category_collection.delete_one({"_id":category_id}) 
          
        return{
                  "status":"success",
                  "data":[],
                  "message":"Category deleted successfuly"
                  }

     except Exception as e:
         return{
                 "status":"error",
                 "data":[],
                 "message": str(e)
         }