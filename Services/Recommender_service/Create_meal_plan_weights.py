import re
import pandas as pd
import random
class Create_meal_plan_weights():


    def create_meal_plan_weights(self,user_profile):

        diets_matrix_factorization = pd.read_csv("C:/Users/R00165035/Desktop/FYP/Services/Recommender_service/diets.csv")
        user_profile =  pd.read_json(user_profile)

        print(user_profile)
        print(diets_matrix_factorization)

        diets_matrix_factorization.columns = diets_matrix_factorization.columns.str.replace(' ', '')
        diets_matrix_factorization[['protein','carbs','fats']] = diets_matrix_factorization[['protein','carbs','fats']].astype(float)

        diets_recommender = diets_matrix_factorization.copy()

        diets_recommender.drop(['title', 'dietID'], axis=1, inplace=True)
        diets_matrix_factorization.drop(['title', 'dietID'], axis=1, inplace=True)

        print("*****just before error******")
        print(user_profile)
        print(diets_matrix_factorization)

        generated_user_intrests = diets_matrix_factorization.T.dot(user_profile.rating) 

        result_recommendations = (diets_recommender.dot(generated_user_intrests)) / generated_user_intrests.sum() 

        macro_predictions = {
        "protein_prediction": 0.0,
        "carbs_prediction": 0.0,
        "fats_prediction ": 0.0
        }

        activity_level_prediction = generated_user_intrests.iloc[3]/15

        i = 0
        for key in macro_predictions:
            macro_predictions[key]  = round(generated_user_intrests.iloc[i]/ (generated_user_intrests.sum() - generated_user_intrests.iloc[3]), 2)
            i = i+1


        print(generated_user_intrests)
        #percentage of ethe meal plan ie 45% should be carbs
        print("Ratio of Macros")
        print("p:",  list(macro_predictions.values())[0])
        print("c:",  list(macro_predictions.values())[1])
        print("f:",  list(macro_predictions.values())[2])

        print(activity_level_prediction)
       



        return generated_user_intrests




    def combinatorial_optimisation(self,generated_user_intrests):
        generated_user_intrests = generated_user_intrests.to_dict()
        nutritional_preference = max(generated_user_intrests, key=generated_user_intrests.get)

        #Incase the highest weight is the same in more than one element alternate by choosing at random
        temp = generated_user_intrests.copy()

        print(generated_user_intrests)
        del temp[nutritional_preference]
        temp_nutritional_preference = max(temp, key=temp.get)

        print(nutritional_preference)
        print(temp_nutritional_preference)

        print(generated_user_intrests)

        if(temp[temp_nutritional_preference] == generated_user_intrests[nutritional_preference]):
            print("inside the date")
            if(random.randint(0, 1) == 0):
                nutritional_preference = temp_nutritional_preference

        
        # A naive recursive implementation
        # of 0-1 Knapsack Problem
        
        # Returns the maximum value that
        # can be put in a knapsack of
        # capacity W
        
        
      
        return("soon a meal plan will be created with a preference on", nutritional_preference  )
    
