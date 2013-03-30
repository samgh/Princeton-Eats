import datetime

import models
import will
    
def load():
    data = will.getData()
    for menu in data:
        insertMenu(menu)

def insertMenu(menu):
    meals = []
    entrees = []
    if menu.breakfast:
        (meal, mealEntrees) = constructMeal(menu, 'breakfast', menu.breakfast)
        meals.append(meal)
        entrees.append(mealEntrees)
    if menu.lunch:
        (meal, mealEntrees) = constructMeal(menu, 'lunch', menu.lunch)
        meals.append(meal)
        entrees.append(mealEntrees)    
    if menu.dinner:
        (meal, mealEntrees) = constructMeal(menu, 'dinner', menu.dinner)
        meals.append(meal)
        entrees.append(mealEntrees)
    db.put(meals)
    db.put(entrees)
    
def constructMeal(menu, name, data):
    meal = models.Meal()
    #meal.date = 
    meal.diningHall = menu.diningHall
    meal.name = name
    return (meal, mealEntrees)