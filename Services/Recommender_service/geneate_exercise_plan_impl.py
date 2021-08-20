from math import log
from bson.json_util import dumps
from pymongo import MongoClient
import re
import pika
import json
from validate_email import validate_email
import uuid
import random
import pandas as pd
import rpc_call
from recommender_system import Create_meal_plan_weights
import prep_data
from bson.json_util import dumps
import random



"""
Setup neccessary communication for rabbitMQ
"""
connection = pika.BlockingConnection(
         pika.ConnectionParameters(host='rabbitmq',port="5672"))

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
    
    user_id = str(body)
    user_id = user_id.strip("'")
    user_id = user_id[2:]

    print("GEN EXERCISE: Fetching profile with ID",user_id,flush=True)
    user_profile = retrieve_user_details(user_id)
    print("GEN EXERCISE: Fetched profile result",user_profile,flush=True)
   
    user_profile_normalised,calories,activity_level  = prep_data.normalise_data(user_profile)
    user_profile_weights = Create_meal_plan_weights.Create_meal_plan_weights().create_meal_plan_weights(user_profile_normalised)

    response = generate_exercise_plan(user_profile_weights,activity_level)
    response = write_exercise_plan_to_database(response,user_id)

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
 
    print("GEN EXERCISE PLAN: FUNC: retrieve_user_details ->",str(user_id),flush=True)
    user_profile = rpc_call.rpc_call().get_user_profile(user_id)


    return user_profile

    

def retrieve_workouts(user_profile_weights):
    client = MongoClient('mongodb://host.docker.internal:27017')
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
def generate_exercise_plan(user_profile_weights,activity_level):

    user_workout_plan = []
    workouts_cardio,workouts_strength = retrieve_workouts(user_profile_weights)
    exercise_type =  user_profile_weights[1] 


    for workout in workouts_cardio:
        if "low" in activity_level:
            workout["reps"] = "30 seconds"
        else:
             workout["reps"] = "1 min"


    for workout in workouts_strength:
        if "low" in activity_level:
            workout["reps"] = "8"
        else:
            workout["reps"] = "12"

    

    if user_profile_weights[1] == "maintaince":
        alternateType = ["weight gain","weight lose"]
        exercise_type  =  alternateType[random.randint(0, 1)]
     


    if  exercise_type  == "weight gain":
       user_workout_plan.append(random.sample(workouts_strength, 2))
       user_workout_plan.append(random.choice(workouts_cardio))



    if  exercise_type  == "weight lose":
          user_workout_plan.append(random.sample(workouts_cardio, 2))
          user_workout_plan.append(random.choice(workouts_strength))

    
    return user_workout_plan



def write_exercise_plan_to_database(exercise_plan,user_id):
    client = MongoClient('mongodb://host.docker.internal:27017')
 
    print("GEN EXERCISE PLAN: FUNC: write_exercise_plan_to_database -> writing to user", user_id,flush=True)
  
    db = client.workouts
    planID = str(uuid.uuid4())
    db[f"{user_id}"].insert_one({"ID":planID,"inUse":1,"favourited":0,"exercise_plan":exercise_plan})
   

    return(dumps(db[f"{user_id}"].find_one( {"ID": {"$eq":planID}})))


        
"""
Make service open to recieve requests.
"""
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='generate_exercise_plan_rpc_queue', on_message_callback=on_request_retrieve_user_details)

print(" GenExerciselPlan Awaiting RPC requests",flush=True)
channel.start_consuming()





