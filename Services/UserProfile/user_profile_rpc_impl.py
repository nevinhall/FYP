from math import log
import re
import pika
import json
from pika.frame import Body
import pymysql
from validate_email import validate_email
from pymongo import MongoClient
from bson.json_util import dumps

connection = pika.BlockingConnection(
     pika.ConnectionParameters(host='rabbitmq',port="5672"))

channel = connection.channel()

channel.queue_declare(queue='user_exits_rpc_queue')
channel.queue_declare(queue='create_user_profile_rpc_queue')
channel.queue_declare(queue='get_user_profile_rpc_queue')
channel.queue_declare(queue='del_user_profile_rpc_queue')
channel.queue_declare(queue='get_user_meal_plan_rpc_queue')
channel.queue_declare(queue='get_user_exercise_plan_rpc_queue')
channel.queue_declare(queue='set_current_user_exercise_plan_rpc_queue')
channel.queue_declare(queue='set_current_user_meal_plan_rpc_queue')
channel.queue_declare(queue='get_current_user_meal_plan_rpc_queue')
channel.queue_declare(queue='get_current_user_exercise_plan_rpc_queue')




def on_request_del_user_profile(ch, method, props, body):
 
    body = json.loads(body)
    user_id = body['user_id']


    response = del_user_profile(user_id)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)



def on_request_get_user_profile(ch, method, props, body):
    print("THIS IS BODY",body)

   
    body = json.loads(body)
    user_id = body['user_id']


    response = get_user_profile(user_id)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)



def on_request_get_user_meal_plan(ch, method, props, body):
    print("THIS CORRECT BODY",  body)
    body = json.loads(body)
    user_id = body['user_id']

    response = get_user_meal_plan(user_id)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)



def on_request_get_user_exercise_plan(ch, method, props, body):

    body = json.loads(body)
    user_id = body['user_id']


    response = get_user_exercise_plan(user_id)

    ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)



def on_request_set_current_user_exercise_plan(ch, method, props, body):
    body = json.loads(body)
    user_id = body['user_id']
    exercise_plan_id = body['exercise_plan_id']
    
    response = set_current_user_exercise_plan(user_id,exercise_plan_id)

    ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)




def on_request_set_current_user_meal_plan(ch, method, props, body):
    body = json.loads(body)
    user_id = body['user_id']
    meal_plan_id = body['meal_plan_id']

    response = set_current_user_meal_plan(user_id,meal_plan_id)

    ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)




def on_request_get_current_user_exercise_plan(ch, method, props, body):
    body = json.loads(body)
    user_id = body['user_id']

    response = get_current_user_exercise_plan(user_id)

    ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)




def on_request_get_current_user_meal_plan(ch, method, props, body):
    body = json.loads(body)
    user_id = body['user_id']


    response = get_current_user_meal_plan(user_id)

    ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def on_request_get_user(ch, method, props, body):
    body = json.loads(body)
    user_id = body['user_id']

    response = get_user_profile(user_id)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)



def on_request_user_exists(ch, method, props, body):
    body = json.loads(body)
    user_id = body['user_id']

    response = user_profile_exist(user_id)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def on_request_create_user_profile(ch, method, props, body):
    body = json.loads(body)
 
    print(body['user_id'], body['height'],body['weight'],body['activity_level'],body['age'],body['dietray_options'], body['allergies'])

    response = create_user_profile(body['user_id'], body['height'],body['weight'],body['activity_level'],body['allergies'],body['age'],body['dietray_options'],body['gender'])

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

'''
This method is responisbe for checking to see if a user profile exists
if so it returns an acknowledgement message if no proifle is found for 
the given ID an empty profile is created.

@Params: String user ID

@returns string result.
'''
def del_user_profile(user_id):
    #database connection
    connection = pymysql.connect(host="mysqldb",user="root",passwd="",database="user_profiles" )
    cursor = connection.cursor()

    sql = "DELETE  FROM user_profiles WHERE user_id =%s"
    cursor.execute(sql,user_id)
    result = cursor.fetchone()
    print(result)

    #commiting the connection then closing it.
    connection.commit()
    connection.close()

    client = MongoClient('mongodb://host.docker.internal:27017')

    db = client.workouts
    print("USER PROFILE IMPLC: FUNC:del_user_profile ->Deleting",user_id,flush=True)

    db[f"{user_id}"].drop()

    db = client.meal
    db[f"{user_id}"].drop()


    return("delete failed")
  


'''
This method is responisbe for checking to see if a user profile exists
if so it returns an acknowledgement message if no proifle is found for 
the given ID an empty profile is created.

@Params: String user ID

@returns string result.
'''
def user_profile_exist(user_id):
    #database connection
    connection = pymysql.connect(host="mysqldb",user="root",passwd="",database="user_profiles" )
    cursor = connection.cursor()
    
    sql = "SELECT user_id FROM user_profiles WHERE user_id =%s"
    cursor.execute(sql,user_id)
    result = cursor.fetchone()
  

    if(result == None):
             #executing the quires
        try:
            cursor.execute("INSERT INTO user_profiles (user_id) VALUES (%s)", (user_id))
                # cursor.execute("INSERT INTO user_profiles VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (user_id))
        except Exception as e:
            print(e,flush=True)
            print("failed to create profile",flush=True)
            return("failed to create profile")
       

        #commiting the connection then closing it.
        connection.commit()
        connection.close()


        return("profile created")
    connection.close()


    return("profile already exits")
  
'''
This method is responisbe for inserting values into a given
user profile. The previous function must be ran in order for 
this function to populate the row. 

@Params: String user_id, height,weight,activity_level,allergies,age,dietray_options 

@returns string result 
'''
def create_user_profile(user_id, height,weight,activity_level,allergies,age,dietray_options,gender):
    user_profile_exist(user_id)

    print(user_id,flush=True)
    print(height,flush=True)
    print(weight,flush=True)
    print(activity_level,flush=True)
    print(allergies,flush=True)
    print(age,flush=True)
    print(dietray_options,flush=True)

    bmi = calcualte_bmi(height,weight)
    calories = calculate_calories(gender,activity_level,weight,height,age)
   
    #database connection
    connection = pymysql.connect(host="mysqldb",user="root",passwd="",database="user_profiles" )
    cursor = connection.cursor()

    
    #executing the quires
    try:
        cursor.execute("UPDATE user_profiles SET height = %s , weight = %s, bmi = %s, activity_level = %s, dietary_options = %s, allergies = %s,age = %s,calories = %s, gender = %s WHERE user_id = %s",(
        height,weight,bmi,activity_level,dietray_options,allergies,age,calories,gender,user_id))
    except(Exception):
        

        return("failed to populate user profile")
    

    #commiting the connection then closing it.
    connection.commit()
    connection.close()
    print("USER PROFILE IMPL: FUNC:create_user_profile ->sent to db",flush=True)



    return("updated profile")


'''
This method is responisbe for getting a generatating
the BMI for a given user. The users height is formatted
from a centemeters to meters.

@Params: String height and weight.

@returns integer BMI Value.
'''
def calcualte_bmi(height,weight):

    height = float(height) /100
    weight = int(weight)


    return int(weight/(height**2))



def calculate_calories(gender,activity_level,weight,height,age):
    kg_to_lbs = int(weight) * 2.205
    cm_to_inch = int(height) / 2.54
    age = int(age)

    calories = 1800

    if(gender == "male"):
        bmr = (66 +(6.3 * kg_to_lbs) + (12.9 * cm_to_inch)) - (6.8 * age)

    if(gender == "female"):
       bmr = (655 +(4.3 * kg_to_lbs) + (4.7 * cm_to_inch)) - (4.7 * age)

    if(activity_level == "low"):
        calories = bmr *1.375

    if(activity_level == "high"):
        calories = bmr * 1.725

    return calories


'''
This method is responisbe for getting a user profile given an ID
the retrieved user profile is returned.

@Params: String user_Id

@returns user_profile
'''
def get_user_profile(user_id):
    #database connection
    connection = pymysql.connect(host="mysqldb",user="root",passwd="",database="user_profiles" )
    cursor = connection.cursor()

    sql = "SELECT * FROM user_profiles WHERE user_id =%s"
    cursor.execute(sql,user_id)
    user_profile = cursor.fetchone()
   
 
    return(dumps(user_profile))



def get_user_meal_plan(user_id):
    print("USER PROFILE IMPL: FUNC:  get_user_meal_plan-> getting all meal plans",user_id ,flush=True)
    client = MongoClient('mongodb://host.docker.internal:27017')
    db =client.meal
 
    user_meal_plans = []
    for meal_plan in db[f"{user_id}"].find():
        user_meal_plans.append(meal_plan)
        
    return(dumps(user_meal_plans))



def get_user_exercise_plan(user_id):
    user_workouts = []
    print("USER PROFILE IMPL: FUNC: get_user_exercise_plan -> getting all exercise plan",flush=True) 
    client = MongoClient('mongodb://host.docker.internal:27017')
    db = client.workouts
    
    for workout_plan in db[f"{user_id}"].find():
        user_workouts.append(workout_plan)
        
    return(dumps(user_workouts))



def get_current_user_meal_plan(user_id):
    print("USER PROFILE IMPL: FUNC: get_current_user_meal_plan -> getting meal plan for user",user_id,flush=True)
    client = MongoClient('mongodb://host.docker.internal:27017')
    db =client.meal
 
    return(dumps(db[f"{user_id}"].find_one({"inUse": {"$eq":1}})))




def get_current_user_exercise_plan(user_id):
    print("USER PROFILE IMPL: FUNC: get_current_user_exercise_plan-> getting exercise plan current",flush=True)
    client = MongoClient('mongodb://host.docker.internal:27017')
    db = client.workouts
    

    return(dumps(db[f"{user_id}"].find_one({"inUse": {"$eq":1}})))




def set_current_user_meal_plan(user_id,meal_plan_id):
   
    print("USER PROFILE IMPL: FUNC: set_current_user_meal_plan -> setting meal plan for user", user_id,flush=True)
    client = MongoClient('mongodb://host.docker.internal:27017')
    db =client.meal
 
    myquery =  {"inUse": {"$eq":1}}
    newvalues = { "$set": {"inUse": 0} }

    db[f"{user_id}"].update_many(myquery, newvalues)
 

    myquery =  {"ID": {"$eq":meal_plan_id}}
    newvalues = { "$set": {"inUse": 1} }

   
    return(db[f"{user_id}"].update_one(myquery, newvalues))

  

def set_current_user_exercise_plan(user_id,exercise_plan_id):
    print("USER PROFILE IMPL: FUNC: set_current_user_exercise_plan -> setting exercise plan",flush=True)
    client = MongoClient('mongodb://host.docker.internal:27017')
    db = client.workouts
    

    myquery =  {"inUse": {"$eq":1}}
    newvalues = { "$set": {"inUse": 0} }

    db[f"{user_id}"].update_many(myquery, newvalues)


    myquery =  {"ID": {"$eq":exercise_plan_id}}
    newvalues = { "$set": {"inUse": 1} }

   
    return(db[f"{user_id}"].update_one(myquery, newvalues))



"""
Make service open to recieve requests.
"""
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='user_exits_rpc_queue', on_message_callback=on_request_user_exists)
channel.basic_consume(queue='create_user_profile_rpc_queue', on_message_callback=on_request_create_user_profile)
channel.basic_consume(queue='get_user_profile_rpc_queue', on_message_callback=on_request_get_user_profile)
channel.basic_consume(queue='del_user_profile_rpc_queue', on_message_callback=on_request_del_user_profile)
channel.basic_consume(queue='get_user_meal_plan_rpc_queue', on_message_callback=on_request_get_user_meal_plan)
channel.basic_consume(queue='get_user_exercise_plan_rpc_queue', on_message_callback=on_request_get_user_exercise_plan)
channel.basic_consume(queue='set_current_user_meal_plan_rpc_queue', on_message_callback=on_request_set_current_user_meal_plan)
channel.basic_consume(queue='set_current_user_exercise_plan_rpc_queue', on_message_callback=on_request_set_current_user_exercise_plan)
channel.basic_consume(queue='get_current_user_meal_plan_rpc_queue', on_message_callback=on_request_get_current_user_meal_plan)
channel.basic_consume(queue='get_current_user_exercise_plan_rpc_queue', on_message_callback=on_request_get_current_user_exercise_plan)



print(" User Profile Awaiting RPC requests",flush=True)
channel.start_consuming()