# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 10:20:39 2021

@author: Nevin Hall
"""
import pandas as pd


diets_matrix_factorization = pd.read_csv("diets.csv")
user_profile = pd.read_csv("user_profile.csv")

diets_matrix_factorization.columns = diets_matrix_factorization.columns.str.replace(' ', '')
diets_matrix_factorization[['protein','carbs','fats']] = diets_matrix_factorization[['protein','carbs','fats']].astype(float)

diets_recommender = diets_matrix_factorization.copy()

diets_recommender.drop(['title', 'dietID'], axis=1, inplace=True)
diets_matrix_factorization.drop(['title', 'dietID'], axis=1, inplace=True)

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

print("Ratio of Macros")
print("p:",  list(macro_predictions.values())[0])
print("c:",  list(macro_predictions.values())[1])
print("f:",  list(macro_predictions.values())[2])

print(activity_level_prediction)
