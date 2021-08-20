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
                pika.ConnectionParameters(host='rabbitmq',port="5672"))

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
        
        data = {
        "user_id": user_id
         }
        data  = json.dumps(data)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='user_exits_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response
    


    def get_user_profile(self,user_id):
        data = {
            "user_id": user_id
        }
        data  = json.dumps(data)
        
            
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_user_profile_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



    def get_user_meal_plan(self,user_id):
        data = {
             "user_id": user_id
         }

        data  = json.dumps(data)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_user_meal_plan_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



    def get_user_exercise_plan(self,user_id):


        data = {
            "user_id": user_id
        }
        data  = json.dumps(data)

     
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_user_exercise_plan_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



    def get_user_current_exercise_plan(self,user_id):
        data = {
            "user_id": user_id
        }
        data  = json.dumps(data)



        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_current_user_exercise_plan_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



    def set_user_current_exercise_plan(self,user_id,exercise_plan_id):
        data = {
            "user_id": user_id,
            "exercise_plan_id" : exercise_plan_id 
        }
        data  = json.dumps(data)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='set_current_user_exercise_plan_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


    
    def set_user_current_meal_plan(self,user_id,meal_plan_id):
        data = {
            "user_id": user_id,
            "meal_plan_id" : meal_plan_id 
        }
        data  = json.dumps(data)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='set_current_user_meal_plan_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



    def get_user_current_meal_plan(self,user_id):
        data = {
            "user_id": user_id
            }
        data  = json.dumps(data)

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_current_user_meal_plan_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


    
    def del_user(self,user_id):
        data = {
        "user_id": user_id
        }
        data  = json.dumps(data)


        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='del_user_profile_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



    def create_user_profile(self,user_id, height,weight,activity_level,allergies,age,dietray_options,gender):
        data = {
           "user_id" :user_id,
           "height" :height,
           "weight" :weight,
           "activity_level" :activity_level,
           "allergies":allergies,
           "age":age,
           "dietray_options": dietray_options,
           "gender":gender
        
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
   
        