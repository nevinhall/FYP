from .login_rpc import login_rpc
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



    #set FLASK_APP=hello.
    #$env:FLASK_APP = "hello.py"
    #flask run