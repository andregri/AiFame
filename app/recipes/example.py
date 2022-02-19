from EdamamAPI import Edamam

appID = 'appID'
recipeID = 'recipeID'

e = Edamam(appID,recipeID)

r = e.get_recipes("chicken, eggs, cabbages")
print([rec.label for rec in r])