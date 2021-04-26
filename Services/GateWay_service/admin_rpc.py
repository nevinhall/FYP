#!/usr/bin/env python
import pika
import uuid
import json

"""
This class acts as en entry point for all functionality relating to 
loging up.
"""
class admin_rpc(object):

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


    def get_num_users(self):

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_num_users_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= "data")
        while self.response is None:
            self.connection.process_data_events()
        return self.response



    def get_num_users_gender(self,gender):

        data = { 
            "gender": gender
        }

        data  = json.dumps(data)

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_num_users_gender_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


    def get_all_meals(self):

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_all_meals_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= "data")
        while self.response is None:
            self.connection.process_data_events()
        return self.response


    
    def get_all_exercises(self):

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='get_all_exercises_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= "data")
        while self.response is None:
            self.connection.process_data_events()
        return self.response


        
    def del_meal(self,meal_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='del_meal_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= meal_id)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


        
    def del_exercise(self,exercise_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='del_exercise_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= exercise_id)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



    
    def create_meal(self,Meal,Protein,Carbs,Fats,calories,Category,strArea,strInstructions,strYoutube):

        data = {
            "Meal" :Meal,
            "Protein": int(Protein),
            "Carbs": int(Carbs),
            "Fats": int(Fats),
            "calories": calories,
            "Category": Category,
            "strArea": strArea,
            "strInstructions":strInstructions,
            "strYoutube": strYoutube,
        }

        data  = json.dumps(data)

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='create_meal_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



     
    def create_exercise(self,name,desciption,type,reps):

        data = {
            "name" : name,
            "desciption": desciption,
            "type": type,
            "reps": reps
        }

        data  = json.dumps(data)

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='create_exercise_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response



