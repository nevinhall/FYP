#!/usr/bin/env python
import pika
import uuid
import json

class login_rpc(object):

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

    def call(self, email,password):

        data = { 
            "email": email,
            "password": password
        }

        data  = json.dumps(data)

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


    def forgot_password(self, email,password):
        print("password reset 1")

        data = { 
            "email": email,
            "password": password
        }

        data  = json.dumps(data)

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='forgot_password_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body= data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response
