from .user_profile_rpc import user_profile_rpc
from .login_rpc import login_rpc
from.sign_up_rpc import sign_up_rpc
from flask import Flask, request

import pika

app = Flask(__name__)

@app.route('/login',methods=['POST'])
def login_rpc_call():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)

        return(login_rpc().call(email, password))

    return("login failed")

    
@app.route('/login/forgotpassword',methods=['POST'])
def forgot_password_rpc_call():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)

        return(login_rpc().forgot_password(email, password))

    return("login failed")

@app.route('/signup',methods=['POST'])
def sign_up_rpc_call():
      email = request.form.get('email')
      password = request.form.get('password')
      return(sign_up_rpc().sign_up(email,password))
     
@app.route('/userexists', methods=['POST'])
def uses_exists_rpc_call():
    user_id = request.form.get('user_id')
    return(user_profile_rpc().user_exists(user_id))

@app.route('/createuserprofile', methods=['Post'])
def create_user_profile_rpc_call():
        pass

    #set FLASK_APP=gateway.py
    #$env:FLASK_APP = "gateway.py"
    #flask run

      #set FLASK_APP=gateway && $env:FLASK_APP = "gateway.py" && flask run