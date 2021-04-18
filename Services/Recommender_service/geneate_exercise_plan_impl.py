from pymongo import MongoClient
import re
import pika
import json
import pymysql
from validate_email import validate_email
import uuid
import io
import random
import pandas as pd
import rpc_call
from recommender_system import Create_meal_plan_weights
import prep_data



"""
Setup neccessary communication for rabbitMQ
"""
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='generate_exercise_plan_rpc_queue')
channel.queue_declare(queue='get_user_profile_rpc_queue')



"""
Service driver code, Once the user makes the request to 
generate a meal plan the system first retrieves the users details
onece this has been completed the data is normailsied.
The function then creates the macro ratios for the given user profile

@returns: completed meal plan
"""
def on_request_retrieve_user_details(ch, method, props, body):

    user_profile = retrieve_user_details(body)
    user_profile_normalised = prep_data.normalise_data(user_profile)
    user_profile_weights = Create_meal_plan_weights.Create_meal_plan_weights().create_meal_plan_weights(user_profile_normalised)
    response = generate_exercise_plan(user_profile_weights)
    write_exercise_plan_to_database(response,body)

    
    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


"""
This code is responsible for communicating with the user service
the function retrieves a user profile for the given ID.

@params: string user_id.
@returns: user profile.
"""
def retrieve_user_details(user_id):
    user_profile = rpc_call.rpc_call().get_user_profile(user_id)


    return user_profile

def retrieve_workouts(user_profile_weights):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.workouts

    workouts_cardio = []
    workouts_strength = []
  
    """
    Retrive documents for the different exercise types
    """
    for workout in db.workout.find({'type': 'cardio'}):
        workouts_cardio.append(workout)

    for workout in db.workout.find({'type': 'strength'}):
        workouts_strength.append(workout)



    return(workouts_cardio,workouts_strength)

"""

"""
def generate_exercise_plan(user_profile_weights):
    user_workout_plan = []
    workouts_cardio,workouts_strength = retrieve_workouts(user_profile_weights)
 

    if user_profile_weights[1] == "weight gain":
       user_workout_plan.append(random.sample(workouts_strength, 2))
       user_workout_plan.append(random.choice(workouts_cardio))


       return user_workout_plan



    if user_profile_weights[1] == "weight lose":
          user_workout_plan.append(random.sample(workouts_cardio, 2))
          user_workout_plan.append(random.choice(workouts_strength))
          

          return user_workout_plan

    #develop futher
    # else:
    #       user_workout_plan.append(random.sample(group_of_items, num_to_select))
    #       user_workout_plan.append(random.choice(foo))


def write_exercise_plan_to_database(exercise_plan,user_id):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.workouts
    # db[f"{user_id}"].drop()
    db[f"{user_id}"].insert_one({"ID":str(uuid.uuid4()),"inUse":1,"favourited":0,"exercise_plan":exercise_plan})

    print(db[f"{user_id}"].find_one())


        
"""
Make service open to recieve requests.
"""
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='generate_exercise_plan_rpc_queue', on_message_callback=on_request_retrieve_user_details)

print(" GenExerciselPlan Awaiting RPC requests")
channel.start_consuming()





