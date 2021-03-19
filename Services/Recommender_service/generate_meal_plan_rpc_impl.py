
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
import prep_data


"""
Setup neccessary communication for rabbitMQ
"""
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='generate_meal_meal_rpc_queue')
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
    response = Create_meal_plan_weights.Create_meal_plan_weights().combinatorial_optimisation(user_profile_weights)

    
    
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





"""
Make service open to recieve requests.
"""
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='generate_meal_meal_rpc_queue', on_message_callback=on_request_retrieve_user_details)

print(" GenMealPlan Awaiting RPC requests")
channel.start_consuming()





