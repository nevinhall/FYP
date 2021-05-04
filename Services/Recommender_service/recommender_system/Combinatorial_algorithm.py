from re import M
import re
from pymongo import MongoClient
import json
from numpy import log, random
import numpy as np
from pymongo.common import validate_driver_or_none

class Combinatorial_algorithm():
  
    """
    Diver code.
    """
    def __init__(self,dietary_needs = "null"):
        """
        Connect to MongoDB Database.
        """
        client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = client.meal

        
        """
        Avergae Macro breakdown of  meal, this will be used to 
        as a condition when retrieving data from the database.
        """
        self.carbs_avg = 0.40
        self.protein_avg = 0.20 
        self.fats_avg = 0.10

        self.dietary_needs = dietary_needs

        self.protein_heavy_meal,self.protein_heavy_meal_ids ,self.protein_heavy_meal_calories,self.protein_heavy_meal_macro_preference = self.find_meals("Protein",self.protein_avg,self.dietary_needs)
        self.carb_heavy_meal ,self.carb_heavy_meal_ids ,self.carb_heavy_meal_calories ,self.carb_heavy_meal_macro_preference = self.find_meals("Carbs",self.carbs_avg,self.dietary_needs)
        self.fats_heavy_meal,self.fats_heavy_meal_ids,self.fats_heavy_meal_calories,self.fats_heavy_meal_macro_preference = self.find_meals("Fats",self.fats_avg,self.dietary_needs)

    """
    Retrieve data for a given macro. Append the results
    into respectes arrays.
    """
    def find_meals(self,macro,macro_avg,diet_restrictions = "null",allergies = []):
        meals = []
        meals_ids = []
        meal_calories = []
        meal_macro_preference  = []

        if diet_restrictions == "Vegetarian":
                for meal in self.db.meals.find({"$and":[{macro: {"$gte": macro_avg}},{"Category": {"$eq":"Vegetarian"}}]}):
                    meals.append(meal)
                    meals_ids.append(meal['idMeal'])
                    meal_calories.append(meal['calories'])
                    meal_macro_preference.append(meal[macro])

        else:
            for meal in self.db.meals.find():
                meals.append(meal)
                meals_ids.append(meal['idMeal'])
                meal_calories.append(meal['calories'])
                meal_macro_preference.append(meal[macro])

      
        return meals, meals_ids,meal_calories ,meal_macro_preference


    """
    This code is responsible for generating an array of meals based on a macronutrient
    the function returns an array of optiaml meals containing the highest nutrient value 
    for the calorie number provided.

    @params: Array nutritional_preference_value,Array meal_calories, Int total_calories,Array macro_heavy_meal_ids.
    @returns: Array of Ids of optimal meals.
    """
    def solve_knapsack(self,nutritional_preference_value, meal_calories, total_calories,macro_heavy_meal_ids):
        includes_meal_ids = []
        n = len(nutritional_preference_value) 
        if total_calories <= 0 or n == 0 or len(meal_calories) != n:
            return []
        
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
                # print("Value added",nutritional_preference_value[row])
                col =  col - meal_calories[row]
                # print("New Backpack weight", col)


        print(dp[0][total_calories])
        
        # maximum profit will be at the bottom-right corner.
        print(includes_meal_ids)


        return includes_meal_ids


    """
    This code is responsible for deleting random meals to ensure uniqueness if the user chooses
    the non optiaml approach

    @params: Array meals,meals_ids, Array meals_calories, Array meal_macro_preferences
    @return: Array meals,meals_ids, Array meals_calories, Array meal_macro_preferences  
    """
    def shuffle_arrays(self,meals,meals_ids, meals_calories, meal_macro_preferences):
        print("************************")
        indexes =random.randint((len(meals)), size=(int(len(meals)/2)))
        indexes = list(dict.fromkeys(indexes))

        for index in sorted(indexes, reverse=True):
            del meals[index]
            del meals_ids[index]
            del meals_calories[index]
            del meal_macro_preferences[index]

        return meals,meals_ids, meals_calories, meal_macro_preferences

    #TOD0: MAKING UNIQUE DROPS CALORIES
    """
    This code is responsible for generating a meal plan for a given macro group and ensuring it there
    are no duplicates.
    @params: self,mealId,meal_macro_preferences,meals_calories,calorie_ratio,meals_ids,meal_plan,meals
    @return: The Final array of meals  
    """
    def generate_meal_plan(self,mealId,meal_macro_preferences,meals_calories,calorie_ratio,meals_ids,meal_plan,meals):
                for mealId in self.solve_knapsack(meal_macro_preferences ,meals_calories, calorie_ratio ,meals_ids):
                            for item in meals:
                                if item["idMeal"] == mealId and item not in meal_plan:
                                    meal_plan.append(item)



    def create_meal_plan(self,is_Optimal,user_profile_weights, total_calories):
        meal_plan = []
        for key in user_profile_weights:
        
            prediction_ratio = user_profile_weights[key]
            calorie_ratio = int(total_calories * prediction_ratio)
            print(key,calorie_ratio)

            if(is_Optimal == "false"):
                print("Generating non optimal meal plan")
                protein_heavy_meal, protein_heavy_meal_ids, protein_heavy_meal_calories, protein_heavy_meal_macro_preference  = self.shuffle_arrays(self.protein_heavy_meal, self.protein_heavy_meal_ids, self.protein_heavy_meal_calories, self.protein_heavy_meal_macro_preference )
                carb_heavy_meal, carb_heavy_meal_ids, carb_heavy_meal_calories, carb_heavy_meal_macro_preference= self.shuffle_arrays(self.carb_heavy_meal, self.carb_heavy_meal_ids, self.carb_heavy_meal_calories, self.carb_heavy_meal_macro_preference)
                fats_heavy_meal, fats_heavy_meal_ids,fats_heavy_meal_calories ,fats_heavy_meal_macro_preference= self.shuffle_arrays(self.fats_heavy_meal, self.fats_heavy_meal_ids,self.fats_heavy_meal_calories ,self.fats_heavy_meal_macro_preference)

                if  calorie_ratio != 0:
                    if key == "protein_prediction" and calorie_ratio != 0:
                        self.generate_meal_plan(protein_heavy_meal_ids, protein_heavy_meal_macro_preference,protein_heavy_meal_calories,calorie_ratio,protein_heavy_meal_ids,meal_plan,protein_heavy_meal)

                    if key == "carbs_prediction":
                        self.generate_meal_plan(carb_heavy_meal_ids, carb_heavy_meal_macro_preference, carb_heavy_meal_calories,calorie_ratio,self.carb_heavy_meal_ids,meal_plan,carb_heavy_meal)

                    if key == "fats_prediction":
                        self.generate_meal_plan(fats_heavy_meal_ids, fats_heavy_meal_macro_preference,fats_heavy_meal_calories,calorie_ratio,fats_heavy_meal_ids,meal_plan,fats_heavy_meal)
                
            else:
            
                if  calorie_ratio != 0:
                    if key == "protein_prediction" and calorie_ratio != 0:
                        self.generate_meal_plan(self.protein_heavy_meal_ids, self.protein_heavy_meal_macro_preference,self.protein_heavy_meal_calories,calorie_ratio,self.protein_heavy_meal_ids,meal_plan,self.protein_heavy_meal)

                    if key == "carbs_prediction":
                        self.generate_meal_plan(self.carb_heavy_meal_ids, self.carb_heavy_meal_macro_preference,self.carb_heavy_meal_calories,calorie_ratio,self.carb_heavy_meal_ids,meal_plan,self.carb_heavy_meal)

                    if key == "fats_prediction":
                        self.generate_meal_plan(self.fats_heavy_meal_ids, self.fats_heavy_meal_macro_preference,self.fats_heavy_meal_calories,calorie_ratio,self.fats_heavy_meal_ids,meal_plan,self.fats_heavy_meal)
                        
        
        return meal_plan


