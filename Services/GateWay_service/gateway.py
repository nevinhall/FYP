#!/usr/bin/env python
from flask_cors.core import FLASK_CORS_EVALUATED
from pika.spec import methods
from .generate_exercise_plan_rpc import generate_exercise_plan_rpc
import re
from .user_profile_rpc import user_profile_rpc
from .login_rpc import login_rpc
from.sign_up_rpc import sign_up_rpc
from .generate_meal_plan_rpc import generate_meal_plan_rpc
from .admin_rpc import admin_rpc


from flask import Flask, request
from flask_cors import CORS

"""
This is file responsible for defining all the API
endpoints. It is the webserver and therefore the 
gateway to the application.
"""
import pika

app = Flask(__name__)
CORS(app)

@app.route('/login',methods=['POST'])
def login_rpc_call():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        return(login_rpc().call(email, password))


    return("failure")

    

@app.route('/login/forgotpassword',methods=['POST'])
def forgot_password_rpc_call():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        return(login_rpc().forgot_password(email, password))



    return("login failed")


@app.route("/getuserprofile",methods=['POST'])
def get_user_profile_rpc_call():
    uuid =  request.form.get('user_id')

    return user_profile_rpc().get_user_profile(uuid)



@app.route('/signup',methods=['POST'])
def sign_up_rpc_call():
    email = request.form.get('email')
    password = request.form.get('password')

 
    return(sign_up_rpc().sign_up(email,password))
     


@app.route('/userexists', methods=['POST'])
def uses_exists_rpc_call():
    user_id = request.form.get('user_id')


    return(user_profile_rpc().user_exists(user_id))



@app.route('/deluser', methods=['POST'])
def del_user_rpc_call():
    user_id = request.form.get('user_id')


    return(user_profile_rpc().del_user(user_id))




@app.route('/createuserprofile', methods=['Post'])
def create_user_profile_rpc_call():
        user_id =  request.form.get('user_id')
        height =  request.form.get('height')
        weight =  request.form.get('weight')
        activity_level =  request.form.get('activity_level')
        allergies =  request.form.get('allergies')
        age =  request.form.get('age')
        dietray_options =  request.form.get('dietray_options')
        gender = request.form.get('gender')
      

        return(user_profile_rpc().create_user_profile(user_id, height, weight, activity_level, allergies, age,dietray_options,gender))



@app.route('/generatemealplan', methods=['Post'])
def generate_meal_plan_rpc_call():
      user_id =  request.form.get('user_id')


      return(generate_meal_plan_rpc().generate_meal_plan_rpc(user_id))
    #set FLASK_APP=gateway.py
    #$env:FLASK_APP = "gateway.py"
    #flask run

      #set FLASK_APP=gateway && $env:FLASK_APP = "gateway.py" && flask run

@app.route('/generateexerciseplan', methods=['Post'])
def generate_exercise_plan_rpc_call():
    user_id =  request.form.get('user_id')
    return(generate_exercise_plan_rpc().generate_exercise_plan_rpc(user_id))

@app.route('/get_exercise_plan', methods=['Post'])
def get_exercise_plan_rpc_call():
    user_id = request.form.get('user_id')
    return(user_profile_rpc().get_user_exercise_plan(user_id))


@app.route('/get_meal_plan', methods=['Post'])
def get_meal_plan_rpc_call():
    user_id = request.form.get('user_id')
    return(user_profile_rpc().get_user_meal_plan(user_id))


@app.route('/set_current_user_exercise_plan', methods=['Post'])
def set_current_user_exercise_plan_rpc_call():
    user_id = request.form.get('user_id')
    exercise_plan_id =request.form.get('exercise_plan_id')


    return(user_profile_rpc().set_user_current_exercise_plan(user_id,exercise_plan_id))




@app.route('/set_current_user_meal_plan', methods=['Post'])
def set_current_user_meal_plan_rpc_call():
    user_id = request.form.get('user_id')
    meal_plan_id =request.form.get('meal_plan_id')


    return(user_profile_rpc().set_user_current_meal_plan(user_id,meal_plan_id))



@app.route('/get_user_current_meal_plan', methods=['Post'])
def get_user_current_meal_plan_rpc_call():
    user_id = request.form.get('user_id')
  
    return(user_profile_rpc().get_user_current_meal_plan(user_id))


@app.route('/get_user_current_exercise_plan', methods=['Post'])
def get_user_current_exercise_plan_rpc_call():
    user_id = request.form.get('user_id')
  
    return(user_profile_rpc().get_user_current_exercise_plan(user_id))




@app.route('/get_num_users', methods=['Get'])
def get_num_users(): 
    return(admin_rpc().get_num_users())


@app.route('/get_num_users_gender', methods=['Post'])
def get_num_users_gender():  
      gender = request.form.get('gender')
      return(admin_rpc().get_num_users_gender(gender))


@app.route('/get_all_meals', methods=['Get'])
def get_all_meals():  
      return(admin_rpc().get_all_meals())


@app.route('/get_all_exercises', methods=['Get'])
def get_all_exercises():  
      return(admin_rpc().get_all_exercises())


@app.route('/del_meal', methods=['POST'])
def del_meal_rpc_call():
    meal_id = request.form.get('meal_id')
    return(admin_rpc().del_meal(meal_id))


@app.route('/del_exercise', methods=['POST'])
def del_exercise_rpc_call():
    exercise_id = request.form.get('exercise_id')
    return(admin_rpc().del_exercise(exercise_id))


@app.route('/create_meal', methods=['POST'])
def create_meal_rpc_call():
    Meal = request.form.get('meal')
    Protein = request.form.get('protein')
    Carbs = request.form.get('carbs')
    Fats = request.form.get('fats')
    calories = request.form.get('calories')
    Category = request.form.get('category')
    strArea = request.form.get('strArea')
    strInstructions = request.form.get('strInstructions')
    strYoutube = request.form.get('strYoutube')
    return(admin_rpc().create_meal(Meal,Protein,Carbs,Fats,calories,Category,strArea,strInstructions,strYoutube))


@app.route('/create_exercise', methods=['POST'])
def create_exercise_rpc_call():
    name = request.form.get('name')
    desciption = request.form.get('deciption')
    type = request.form.get('type')
    reps = request.form.get('reps')

    return(admin_rpc().create_exercise(name,desciption,type,reps))
