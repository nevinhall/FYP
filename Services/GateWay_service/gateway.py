#!/usr/bin/env python
from pika.spec import methods
from .generate_exercise_plan_rpc import generate_exercise_plan_rpc
import re
from .user_profile_rpc import user_profile_rpc
from .login_rpc import login_rpc
from.sign_up_rpc import sign_up_rpc
from .generate_meal_plan_rpc import generate_meal_plan_rpc


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



@app.route('/get_user_current_meal_plan', methods=['Post'])
def get_user_current_meal_plan_rpc_call():
    user_id = request.form.get('user_id')
  
    return(user_profile_rpc().get_user_current_meal_plan(user_id))


@app.route('/get_user_current_exercise_plan', methods=['Post'])
def get_user_current_exercise_plan_rpc_call():
    user_id = request.form.get('user_id')
  
    return(user_profile_rpc().get_user_current_exercise_plan(user_id))