# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json,request

class BarApp(http.Controller):
     

     @http.route('/bar_app/bar_app', auth='public')
     def index(self, **kw):
         return "Hello, world"

        #Get All products
     @http.route('/bar_app/products', auth='public',type="http")
     def getProducts(self, **kw):
        productdata= http.request.env["bar_app.product_model"].sudo().search_read([],["id","name","description","category","ingredients","price"])
        data={  "status":200,
                "data":productdata }
        
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")

        #Get all categories
     @http.route('/bar_app/category', auth='public',type="http")
     def getCategories(self, **kw):
        categorydata= http.request.env["bar_app.category_model"].sudo().search_read([],["id","name","description","products","parent_id"])
        data={  "status":200,
                "data":categorydata }
        
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")


        #Get all categories Robert
     @http.route('/bar_app/GetAllCategories', auth='public',type="http")
     def getCategoriesWithoutStatus(self, **kw):
        categorydata= http.request.env["bar_app.category_model"].sudo().search_read([],["id","name","description","products"])
        categorydata 
        
        return http.Response(json.dumps(categorydata).encode("utf8"),mimetype="application/json")
        #Get All ingredients
     @http.route('/bar_app/ingredient', auth='public',type="http")
     def getIngredients(self, **kw):
        ingredientdata= http.request.env["bar_app.ingredient_model"].sudo().search_read([],["id","name","observation","products"])
        data={  "status":200,
                "data":ingredientdata }
        
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")

     #GET ONE product BY ID
     @http.route('/bar_app/getProduct/<int:id>',auth="public",type="http")
     def getProduct(self,id, **kw):
        if id:
            domain = [("id","=",id)]
        else:
            domain = []
        prouctdata = http.request.env["bar_app.product_model"].sudo().search_read(domain,["id","name","description","category","ingredients","price"])
        data = { "status":200, "data":prouctdata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")

        #GET ONE ingredient BY ID
     @http.route('/bar_app/getIngredient/<int:id>',auth="public",type="http")
     def getIngredient(self,id, **kw):
        if id:
            domain = [("id","=",id)]
        else:
            domain = []
        ingredientdata = http.request.env["bar_app.ingredient_model"].sudo().search_read(domain,["id","name","observation","products"])
        data = { "status":200, "data":ingredientdata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")

     #GET ONE Category BY ID
     @http.route('/bar_app/getCategory/<int:id>',auth="public",type="http")
     def getCategory(self,id, **kw):
        if id:
            domain = [("id","=",id)]
        else:
            domain = []
        categorydata = http.request.env["bar_app.category_model"].sudo().search_read(domain,["id","name","description","products"])
        data = { "status":200, "data":categorydata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")


        
        #Category Data
     @http.route(['/bar_app/getAllCategoryData','/bar_app/getAllCategoryData/<int:catid>'], auth='public', type="http")
     def getDatCategories(self,catid=None, recurse=False,**kw):
        if catid:
            domain=[("id","=",catid)]
        else:
            domain=[]
        catdata = http.request.env["bar_app.category_model"].sudo().search_read(domain,["name","description","products","parent_id","child_ids"])
        for rec in catdata:
            if rec["parent_id"]:
                detdata = self.getDatCategories(catid=rec["parent_id"][0],recurse=True)
                rec["parent_id"] = detdata
                if recurse:
                    return rec 
            else:
                if recurse:
                    return catdata 
                
        
        return http.Response(json.dumps(catdata).encode("utf8"),mimetype ="application/json")        
                                
    
     #ADD PRODUCT
     @http.route('/bar_app/addProduct', auth='public', type="json",method="POST")
     def addProduct(self, **kw):
        response = request.jsonrequest
        try:
                result= http.request.env["bar_app.product_model"].sudo().create(response)
                data={
                        "status":201,
                        "id":result.id
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data

        #ADD Ingredient
     @http.route('/bar_app/addIngredient', auth='public', type="json",method="POST")
     def addIngredient(self, **kw):
        response = request.jsonrequest
        try:
                result= http.request.env["bar_app.ingredient_model"].sudo().create(response)
                data={
                        "status":201,
                        "id":result.id
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data

        #ADD Category
     @http.route('/bar_app/addCategory', auth='public', type="json",method="POST")
     def addCategory(self, **kw):
        response = request.jsonrequest
        try:
                result= http.request.env["bar_app.category_model"].sudo().create(response)
                data={
                        "status":201,
                        "id":result.id
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data

        #ADD Table
     @http.route('/bar_app/newTable', auth='public', type="json",method="POST")
     def addTable(self, **kw):
        response = request.jsonrequest
        try:
                order = {}
                order["num"]=response["num"]
                order["client"]=response["client"]
                order["waiter"]=response["waiter"]
                result= http.request.env["bar_app.table_model"].sudo().create(order)
                for rec in response["lineOrders"]:
                        lineOrder={}
                        lineOrder["numTable"]=result.id
                        lineOrder["product"]=rec["product"]
                        lineOrder["quantity"]=rec["quantity"]
                        lineOrder["price"]=rec["price"]
                        http.request.env["bar_app.order_model"].sudo().create(lineOrder)
                data={
                        "status":201,
                        "id":result.id
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data
        
        #UPDATE PRODUCT
     @http.route('/bar_app/updateProduct', auth='public', type="json",method="PUT")
     def updateProduct(self, **kw):
        response = request.jsonrequest
        try:
                productdata= http.request.env["bar_app.product_model"].sudo().search([("id","=",response["id"])])
                productdata.sudo().write(response)
                data={
                        "status":201,
                        "id":productdata.id
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data

          #UPDATE INGREDIENT
     @http.route('/bar_app/updateIngredient', auth='public', type="json",method="PUT")
     def updateIngredient(self, **kw):
        response = request.jsonrequest
        try:
                ingredientdata= http.request.env["bar_app.ingredient_model"].sudo().search([("id","=",response["id"])])
                ingredientdata.sudo().write(response)
                data={
                        "status":201,
                        "id":ingredientdata.id
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data

              #UPDATE Category
     @http.route('/bar_app/updateCategory', auth='public', type="json",method="PUT")
     def updateCategory(self, **kw):
        response = request.jsonrequest
        try:
                categorydata= http.request.env["bar_app.category_model"].sudo().search([("id","=",response["id"])])
                categorydata.sudo().write(response)
                data={
                        "status":201,
                        "id":categorydata.id
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data

        #Confirm Table
     @http.route('/bar_app/confirmTable', auth='public', type="json",method="PUT")
     def confirmTable(self, **kw):
        response = request.jsonrequest
        try:
                productdata= http.request.env["bar_app.table_model"].sudo().search([("num","=",response["num"])])
                productdata.changeStateToConfirm()
                data={
                        "status":201,
                        "id":productdata.id
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data

        #DELETE Product 
     @http.route('/bar_app/deleteProduct', auth='public', type="json",method="DELETE")
     def deleteProduct(self, **kw):
        response = request.jsonrequest
        try:
                productdata= http.request.env["bar_app.product_model"].sudo().search([("id","=",response["id"])])
                productdata.sudo().unlink()
                data={
                        "status":200,
                        
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data

        #DELETE CATEGORY 
     @http.route('/bar_app/deleteCategory', auth='public', type="json",method="DELETE")
     def deleteCategory(self, **kw):
        response = request.jsonrequest
        try:
                categorydata= http.request.env["bar_app.category_model"].sudo().search([("id","=",response["id"])])
                categorydata.sudo().unlink()
                data={
                        "status":200,
                        
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data

        #DELETE INGREDIENT 
     @http.route('/bar_app/deleteIngredient', auth='public', type="json",method="DELETE")
     def deleteIngredient(self, **kw):
        response = request.jsonrequest
        try:
                ingredientdata= http.request.env["bar_app.ingredient_model"].sudo().search([("id","=",response["id"])])
                ingredientdata.sudo().unlink()
                data={
                        "status":200,
                        
                }
                return data
        except Exception as e:
                data={
                        "status":404,
                        "error":e
                }
                return data


        
        
