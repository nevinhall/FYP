import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def login(email,password): 
    return("login function")
    """
        if(valid_email(self,email)):
            if(valid_password(self,email,password)):
               return("response: succesful login")
            else:
                return("response:password not valid")
        else:
            return("response:email not valid")
    """

def on_request(ch, method, props, body):
    print(body)
    body = json.loads(body)

    response = login(body["email"],body["password"])

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()