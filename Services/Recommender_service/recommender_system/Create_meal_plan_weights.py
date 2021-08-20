import re
import pandas as pd
import random
class Create_meal_plan_weights():

    '''
    This method is responisbe for recommending values for the combinatorial 
    algorithm based on the user profile containg the ratings for each of the 
    diet types.

    @Params: user profile: json object containing values for userID, title
    dietId and rating.

    @returns the diet type and the ratio of macro nutrients.
    '''
    def create_meal_plan_weights(self,user_profile):
        '''
        Prepare data for matrix factorisation
        '''

        diets_matrix_factorization = pd.read_csv("./recommender_system/diets.csv")
        user_profile =  pd.read_json(user_profile)

        diet_plan_type_index = user_profile["rating"].idxmax()

        diet_plan_type = user_profile.iloc[diet_plan_type_index]
        diet_plan_type = diet_plan_type["title"]

        diets_matrix_factorization.columns = diets_matrix_factorization.columns.str.replace(' ', '')
        diets_matrix_factorization[['protein','carbs','fats']] = diets_matrix_factorization[['protein','carbs','fats']].astype(float)

        diets_recommender = diets_matrix_factorization.copy()

        diets_recommender.drop(['title', 'dietID'], axis=1, inplace=True)
        diets_matrix_factorization.drop(['title', 'dietID'], axis=1, inplace=True)



        """
        Use matrix factorisation to generate a recommendation for each macro group
        """
        print("CREATE WEIGHTS: FUNC: create_weights -> user matrix =",user_profile.rating,flush=True)
        print("CREATE WEIGHTS: FUNC: create_weights -> diets matrix=", diets_matrix_factorization,flush=True)
        generated_user_intrests = diets_matrix_factorization.T.dot(user_profile.rating) 
        print("CREATE WEIGHTS: FUNC: create_weights -> result matrix=", generated_user_intrests,flush=True)


     
        macro_predictions = {
        "protein_prediction": 0.0,
        "carbs_prediction": 0.0,
        "fats_prediction ": 0.0
        }

        """
        Populate previously decalared dictioanry with respective macro values
        """
        i = 0
        for key in macro_predictions:
            macro_predictions[key]  = round(generated_user_intrests.iloc[i]/ (generated_user_intrests.sum() - generated_user_intrests.iloc[3]), 3)
            i = i+1
  
        print("Create Meal Plan Weights: FUNC: create_meal_plan_weights -> Ratio of Macros",flush=True)
        print("p:",  list(macro_predictions.values())[0])
        print("c:",  list(macro_predictions.values())[1])
        print("f:",  list(macro_predictions.values())[2])
        print("Diet Type",diet_plan_type, flush=True)
       
       

    
        return macro_predictions, diet_plan_type


    
    '''
        This method is responisbe for

        @Params: 

        @returns t
    '''
    
    def combinatorial_optimisation(self,predictions):
        
        generated_user_intrests = predictions[0]
        nutritional_preference = max(generated_user_intrests, key=generated_user_intrests.get)

        
      
        return("soon a meal plan will be created with a preference on", nutritional_preference,predictions[1],predictions)
    
