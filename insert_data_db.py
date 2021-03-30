from re import M
import re
from pymongo import MongoClient
import json
from numpy import random
import numpy as np

"""
Connect to MongoDB Database.
"""
client = MongoClient('mongodb://127.0.0.1:27017')
db = client.meal



"""
Avergae Macro breakdown of  meal, this will be used to 
as a condition when retrieving data from the database.
"""
carbs_avg = 0.40
protein_avg = 0.20 
fats_avg = 0.10



"""
Retrieve data for a given macro. Append the results
into respectes arrays.
"""
def find_meals(macro,macro_avg,diet_restrictions = "null",allergies = []):
    meals = []
    meals_ids = []
    meal_calories = []
    meal_macro_preference  = []

    if diet_restrictions != "null":
            for meal in db.meals.find({"$and":[{macro: {"$gte": macro_avg}},{"Category": {"$eq":"Vegetarian"}}]}):
                meals_ids.append(meal['idMeal'])
                meal_calories.append(meal['calories'])
                meal_macro_preference.append(meal[macro])

    for meal in db.meals.find({macro: {"$gte": macro_avg}}):
        meals.append(meal)
        meals_ids.append(meal['idMeal'])
        meal_calories.append(meal['calories'])
        meal_macro_preference.append(meal[macro])

    return meals, meals_ids,meal_calories ,meal_macro_preference


protein_heavy_meal,protein_heavy_meal_ids ,protein_heavy_meal_calories,protein_heavy_meal_macro_preference = find_meals("Protein",protein_avg,"Vegetarian")
carb_heavy_meal ,carb_heavy_meal_ids ,carb_heavy_meal_calories ,carb_heavy_meal_macro_preference = find_meals("Carbs",carbs_avg)
fats_heavy_meal,fats_heavy_meal_ids,fats_heavy_meal_calories,fats_heavy_meal_macro_preference = find_meals("Fats",fats_avg)



"""
This code is responsible for generating an array of meals based on a macronutrient
the function returns an array of optiaml meals containing the highest nutrient value 
for the calorie number provided.

@params: Array nutritional_preference_value,Array meal_calories, Int total_calories,Array macro_heavy_meal_ids.
@returns: Array of Ids of optimal meals.
"""
def solve_knapsack(nutritional_preference_value, meal_calories, total_calories,macro_heavy_meal_ids):
    includes_meal_ids = []
    n = len(nutritional_preference_value) 
    if total_calories <= 0 or n == 0 or len(meal_calories) != n:
        return 0
    
    dp = [[0 for x in range(total_calories+1)] for y in range(n)]
    
    # populate the total_calories = 0 columns, with '0' total_calories we have '0' profit
    for i in range(0, n):
        dp[i][0] = 0
    
    # if we have only one weight, we will take it if it is not more than the total_calories
    for c in range(0, total_calories+1):
        if meal_calories[0] <= c:
            dp[0][c] = nutritional_preference_value[0]
    
    for i in range(1, n):
        for c in range(1, total_calories+1):
            profit1, profit2 = 0, 0
            if meal_calories[i] <= c:
                profit1 = nutritional_preference_value[i] + dp[i-1][c-meal_calories[i]]
            profit2 = dp[i-1][c]
            dp[i][c] = max(profit1, profit2)

    col = total_calories 

    for row in range(n-1,0,-1):
        if( dp[row][col] !=  dp[row-1][col]):
            # print(dp[row][col] , '!=',  dp[row-1][col])
            includes_meal_ids.append(macro_heavy_meal_ids[row])
            print("Value added",nutritional_preference_value[row])
            col =  col - meal_calories[row]
            print("New Backpack weight", col)


    print(dp[0][total_calories])
    
    # maximum profit will be at the bottom-right corner.
    print(includes_meal_ids)
    return includes_meal_ids


total_calories = 1500


# print("res",solve_knapsack(carb_heavy_meal_macro_preference ,  carb_heavy_meal_calories, total_calories,carb_heavy_meal_ids))
meal_plan_protein = []
meal_plan_carbs = []
meal_plan_fats = []

meal_plan_final = []

macro_predictions1 = {
    "protein_prediction": 0.455,
    "carbs_prediction": 0.455,
    "fats_prediction": 0.19
    }




def generate_meal_plan(
    protein_heavy_meal,protein_heavy_meal_ids,protein_heavy_meal_calories,protein_heavy_meal_macro_preference,
 
    carb_heavy_meal,
    carb_heavy_meal_ids,
    carb_heavy_meal_calories,
    carb_heavy_meal_macro_preference,
    
    fats_heavy_meal,
    fats_heavy_meal_ids,
    fats_heavy_meal_calories,
    fats_heavy_meal_macro_preference,

    is_Optimal

):

    """
    This code is responsible for deleting random meals to ensure uniqueness if the user chooses
    the non optiaml approach

    @params: Array meals,meals_ids, Array meals_calories, Array meal_macro_preferences
    @return: Array meals,meals_ids, Array meals_calories, Array meal_macro_preferences  
    """
    def shuffle_arrays(meals,meals_ids, meals_calories, meal_macro_preferences):
        print("m",len(meals))
        print("mi",len(meals_ids))
        print("mc",len(meals_calories))
        print("mmp",len(meal_macro_preferences))
        print("************************")
        indexes =random.randint((len(meals)), size=(int(len(meals)/2)))

     
        indexes = list(dict.fromkeys(indexes))

        print(indexes)
        for index in sorted(indexes, reverse=True):
            print("index:", index)
            del meals[index]
            del meals_ids[index]
            del meals_calories[index]
            del meal_macro_preferences[index]

        return meals,meals_ids, meals_calories, meal_macro_preferences


    def generate_meal_plan(mealId,meal_macro_preferences,meals_calories,calorie_ratio,meals_ids,meal_plan,meals):
        for mealId in solve_knapsack(meal_macro_preferences ,meals_calories, calorie_ratio ,meals_ids):
                      for item in meals:
                        if item["idMeal"] == mealId and item not in meal_plan:
                            meal_plan.append(item)


    """
    Filter any duplicate meals.
    """
    meal_plan = []
    for key in macro_predictions1:
    
        prediction_ratio = macro_predictions1[key]
        calorie_ratio = int(total_calories * prediction_ratio)
        print(key,calorie_ratio)

        if(not is_Optimal):
            print("protein shuffle")
            protein_heavy_meal, protein_heavy_meal_ids, protein_heavy_meal_calories, protein_heavy_meal_macro_preference  = shuffle_arrays(  protein_heavy_meal, protein_heavy_meal_ids, protein_heavy_meal_calories, protein_heavy_meal_macro_preference )
            print("carbs shuffle")
            carb_heavy_meal, carb_heavy_meal_ids, carb_heavy_meal_calories, carb_heavy_meal_macro_preference= shuffle_arrays( carb_heavy_meal, carb_heavy_meal_ids, carb_heavy_meal_calories, carb_heavy_meal_macro_preference)
            print("fat shuffle")
            fats_heavy_meal, fats_heavy_meal_ids,fats_heavy_meal_calories ,fats_heavy_meal_macro_preference= shuffle_arrays( fats_heavy_meal, fats_heavy_meal_ids,fats_heavy_meal_calories ,fats_heavy_meal_macro_preference)
            
        
        if  calorie_ratio != 0:
            if key == "protein_prediction" and calorie_ratio != 0:
                   generate_meal_plan(protein_heavy_meal_ids, protein_heavy_meal_macro_preference,protein_heavy_meal_calories,calorie_ratio,protein_heavy_meal_ids,meal_plan,protein_heavy_meal)

            if key == "carbs_prediction":
                  generate_meal_plan(carb_heavy_meal_ids, carb_heavy_meal_macro_preference,carb_heavy_meal_calories,calorie_ratio,carb_heavy_meal_ids,meal_plan,carb_heavy_meal)

            if key == "fats_prediction":
                    generate_meal_plan(fats_heavy_meal_ids, fats_heavy_meal_macro_preference,fats_heavy_meal_calories,calorie_ratio,fats_heavy_meal_ids,meal_plan,fats_heavy_meal)
                 
               

    return meal_plan


is_Optimal = False
meal_plan_final = generate_meal_plan(protein_heavy_meal,protein_heavy_meal_ids,protein_heavy_meal_calories,protein_heavy_meal_macro_preference,

    carb_heavy_meal,
    carb_heavy_meal_ids,
    carb_heavy_meal_calories,
    carb_heavy_meal_macro_preference,
    
    fats_heavy_meal,
    fats_heavy_meal_ids,
    fats_heavy_meal_calories,
    fats_heavy_meal_macro_preference,

    is_Optimal
)


print(len(meal_plan_final))
