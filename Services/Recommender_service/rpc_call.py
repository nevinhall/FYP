#!/usr/bin/env python
import pika
import uuid
import json


class rpc_call(object):

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

    def get_user_profile(self, user_id):
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
            body=data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response
