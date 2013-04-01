import datetime
import logging

import models
import will
    
def getTestData():
    data = []
    menu = {'diningHall': 'Butler',
            'breakfast': []}
    data.append(menu)
    return data
    
def load():
    #data = will.getData()
    data = getTestData()
    meals = []
    entrees = []
    
    for menu in data:
        
        print 'menu'
        
        (menuMeals, menuEntrees) = constructMenu(menu)
        meals = menuMeals #meals + menuMeals
        entrees = menuEntrees #entrees + menuEntrees
    return (meals, entrees)
    #db.put(meals)
    #db.put(entrees)

def constructMenu(menu):
    menuMeals = []
    menuEntrees = []
    names = ['breakfast', 'lunch', 'dinner']
    for name in names:
        if name in menu:
            (meal, mealEntrees) = constructMeal(menu, name)
            menuMeals.append(meal)
            menuEntrees.append(mealEntrees)
    return (menuMeals, menuEntrees)
    
def constructMeal(menu, name):
    data = menu[name]
    meal = models.Meal()
    #meal.date = 
    mealEntrees = []
    #meal.diningHall = menu.diningHall
    meal.name = name
    return (meal, mealEntrees)