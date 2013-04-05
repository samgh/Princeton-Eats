import datetime

from google.appengine.ext import db

# Entree data type, keyed by name
class Entree(db.Model):
    allergens = db.StringListProperty()
    ingredients = db.StringListProperty()
    name = db.StringProperty()
    def html_string(self):
        html = '<div>'
        html = html + '<p><b>%s</b></p>' % self.name
        html = html + '<p>%s</p>' % self.allergens
        html = html + '<p>%s</p>' % self.ingredients
        html = html + '</div>'
        return html

# Meal data type
class Meal(db.Model):
    date = db.StringProperty()
    entreeKeys = db.StringListProperty()
    hall = db.StringProperty()
    type = db.StringProperty()
    def html_string(self):
        html = '<div>'
        html = html + '<p><b>%s, %s, %s</b></p>' % (self.hall, self.type, self.date)
        html = html + '<p>%s</p>' % self.entreeKeys
        html = html + '</div>'
        return html
    
# Return all meals and entrees
def getMealsAndEntrees():
    meals = Meal.all().run()
    entrees = Entree.all().run()
    return (meals, entrees)

# Return menus for home page
def getHomeMenus():
    menus = {}
    q = db.GqlQuery("SELECT * FROM Meal " +
                    "WHERE date = :1 " +
                    "AND type = :2 ",
                    "Friday, April 05", "dinner")
    for meal in q.run():
        if meal.hall in menus:
            continue
        menus[meal.hall] = meal.entreeKeys
    return menus
