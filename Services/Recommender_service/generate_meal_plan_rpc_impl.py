

import re
import pika
import json
import pymysql
from validate_email import validate_email
import uuid
import io
import pandas as pd
import rpc_call
import Create_meal_plan_weights




connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='generate_meal_meal_rpc_queue')
channel.queue_declare(queue='get_user_profile_rpc_queue')


def on_request_retrieve_user_details(ch, method, props, body):
    print("on_request_retrieve_user_details", body)

    user_profile = retrieve_user_details(body)
    user_profile = normalise_data(user_profile)
    user_profile_weights = Create_meal_plan_weights.Create_meal_plan_weights().create_meal_plan_weights(user_profile)
    response = Create_meal_plan_weights.Create_meal_plan_weights().combinatorial_optimisation(user_profile_weights)

    
    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)



def retrieve_user_details(user_id):
    user_profile = rpc_call.rpc_call().get_user_profile(user_id)
    print("This is the user profile", user_profile)
    return user_profile


def normalise_data(response):
    print("reponse in gen meal plan") 
    user_profile = response.decode()

    user_profile = user_profile.strip().replace('\'','').replace(',','').replace('(','').replace(')','').split()
    user_id =  user_profile[0]
    height = user_profile[1]
    weight =user_profile[2]
    bmi =user_profile[3]
    activity_level =user_profile[4]
    dietary_options = user_profile[5]
    allergies = user_profile[6]
    age = user_profile[7]

    weight_gain = 0
    weight_lose = 0
    weight_maintaince = 0


    if(float(bmi) < 18.):
        weight_gain = weight_gain + 3
    
    elif(float(bmi) > 25):
        weight_lose = weight_lose +3
    else:
        weight_maintaince = weight_maintaince +3

    

    if(float(bmi) < 18.5 and activity_level == 'high'):
        weight_gain  = weight_gain + 1

    elif(float(bmi) > 25 and activity_level == 'low'):
        weight_lose  = weight_lose + 1
    
    else:
        weight_maintaince = weight_maintaince +1


    if(float(bmi) < 18.5 and int(age) < 25):
            weight_gain  = weight_gain + 1

    elif(float(bmi) > 25 and int(age) < 25):
        weight_lose  = weight_lose + 1
    
    else:
        weight_maintaince = weight_maintaince +1

    print("weight_maintaince", weight_maintaince)
    print("weight_gain", weight_gain)
    print("weight_lose", weight_lose)

    user_id =1
    user_profile = {"userID":{"0":user_id,"1":user_id,"2":user_id},"title":{"0":"weight lose","1":"weight gain","2":"maintaince"},"dietID":{"0":0,"1":1,"2":2},"rating":{"0":weight_lose,"1":weight_gain,"2":weight_maintaince}}
    # [{"userID":1,"title":"weight loss","dietID":0,"rating":0},{"userID":1,"title":"weight gain","dietID":2,"rating":5},{"userID":1,"title":"maintaince ","dietID":4,"rating":0}]
    user_profile =  json.dumps(user_profile)
    
    print(user_profile)

    return user_profile






channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='generate_meal_meal_rpc_queue', on_message_callback=on_request_retrieve_user_details)

print(" GenMealPlan Awaiting RPC requests")
channel.start_consuming()





