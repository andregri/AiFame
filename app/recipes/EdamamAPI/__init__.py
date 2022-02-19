import requests
import json


class Edamam():

    def __init__(self,
                
                #nutrition_appid,
                #nutrition_appkey,
                recipes_appid, 
                recipes_appkey#,
                #food_appid,
                #food_appkey
                ):

        """
        Edamam api auth
        """
        #self.nutrition_appid = nutrition_appid
       # self.nutrition_appkey = nutrition_appkey
        self.recipes_appid = recipes_appid
        self.recipes_appkey = recipes_appkey
        #self.food_appid = food_appid
        #self.food_appkey = food_appkey


    def get_recipes(self, ingredients=None):
        """
        Search for recipes from list of ingredients given in natural language 
        Get string of ingredients in 
        Return list of Recipe 
        """
        if ingredients != None and type(ingredients) is str:
            url = 'https://api.edamam.com/search?q=' + ingredients + '&app_id=' + self.recipes_appid + '&app_key=' + self.recipes_appkey

            r = requests.get(url)
            if r.status_code == 401:
                return None

            r = r.json()
            data = r['hits']

            recipes = []

            for c in data:
                #Extract information from response data, for other info see recipesApi.json
                label = c["recipe"]["label"] #Name of the recipes
                icon = c["recipe"]["image"] #Image, 
                link = c["recipe"]["url"] #Link from Serious Eats
                dietLabel = c["recipe"]["dietLabels"] #Diet Type
                ingredientLines = c["recipe"]["ingredientLines"] #Ingredients in natural languages with quantities and descriptions
                ingredients = [i["food"] for i in c["recipe"]["ingredients"]] #List of ingredients
                
                recipes.append(Recipe(
                label, 
                icon=icon,
                link=link, 
                dietLabel=dietLabel,
                ingredients=ingredients,
                ingredientLines=ingredientLines))

            
            return recipes
        return None

class Recipe():
    def __init__(self, label, icon, link, dietLabel, ingredientLines, ingredients):
        self.label = label
        self.icon = icon
        self.link = link
        self.dietLabel = dietLabel
        self.ingredientLines = ingredientLines
        self.ingredients = ingredients


    


