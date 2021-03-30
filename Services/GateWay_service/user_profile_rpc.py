#!/usr/bin/env python
import pika
import uuid
import json

"""
This class acts as en entry point for all functionality relating to 
the user profile.
"""
class user_profile_rpc(object):

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

    def user_exists(self,user_id):
        print(user_id)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='user_exits_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= user_id)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


    
    def del_user(self,user_id):
        print(user_id)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='del_user_profile_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= user_id)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


    def create_user_profile(self,user_id, height,weight,activity_level,allergies,age,dietray_options):
        data = {
           "user_id" :user_id,
           "height" :height,
           "weight" :weight,
           "activity_level" :activity_level,
           "allergies":allergies,
           "age":age,
           "dietray_options": dietray_options
        
        }

        data  = json.dumps(data)

  

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='create_user_profile_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response
   
        