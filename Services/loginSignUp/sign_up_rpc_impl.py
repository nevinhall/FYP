import re
import pika
import json
from validate_email import validate_email

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='sign_up_rpc_gueue')




def sign_up(email,password):
    return("sign up")
    if(valid_email(email)):
        """
        write to database
        re-direct to login
        """
    """
    re-direct to login
    """

    pass

def valid_email(email):
    return validate_email(email)

def on_request_sign_up(ch, method, props, body):
    
    body = json.loads(body)
    print(body)

    response = sign_up(body["email"],body["password"])

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)





channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='sign_up_rpc_gueue', on_message_callback=on_request_sign_up)


print(" [x] Awaiting RPC requests")
channel.start_consuming()