
import re
import pika
import json
import pymysql
from validate_email import validate_email
import uuid

class rpc_call(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def get_user_profile(self, user_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_user_profile_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=user_id)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='generate_meal_meal_rpc_queue')
channel.queue_declare(queue='get_user_profile_rpc_queue')


def on_request_retrieve_user_details(ch, method, props, body):
    print("on_request_retrieve_user_details", body)

    response = retrieve_user_details(body)
    print("final", response)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


"""
React app calls this first to determine what page to render 
"""


# def user_profile_exist(user_id):
#     #database connection
#     connection = pymysql.connect(host="localhost",user="root",passwd="",database="user_profiles" )
#     cursor = connection.cursor()

#     print("here",user_id)
#     sql = "SELECT user_id FROM user_profiles WHERE user_id =%s"
#     cursor.execute(sql,user_id)
#     result = cursor.fetchone()
#     print(result)

#     if(result == None):
#              #executing the quires
#         try:
#             cursor.execute("INSERT INTO user_profiles (user_id) VALUES (%s)", (user_id))
#                 # cursor.execute("INSERT INTO user_profiles VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (user_id))
#         except:
#             return("failed to create profile")


#         #commiting the connection then closing it.
#         connection.commit()
#         connection.close()

#         return("profile created")
#     connection.close()
#     return("profile already exits")

def retrieve_user_details(user_id):
    user_profile = rpc_call().get_user_profile(user_id)
    print("This is the user profile", user_profile)
    return user_profile


def normalise_data(response):
    print("reponse in gen meal plan") 
    print("normaise_data", response)

    return "retrieving data for", response


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='generate_meal_meal_rpc_queue', on_message_callback=on_request_retrieve_user_details)

print(" GenMealPlan Awaiting RPC requests")
channel.start_consuming()





