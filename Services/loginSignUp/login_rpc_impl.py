import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')
channel.queue_declare(queue='forgot_password_rpc_queue')


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

def valid_email(email):
    '''
    check email is in database

    if(response):
        return true
    else:
        return false 

    '''
    pass

def valid_password(email,password):
    '''
    check password is in database

    if(response):
        return true
    else:
        return false 

    '''
    pass

def forgot_password(email,new_password):
    '''
    if(valid_email):
        send email to reset password 
        create temp server send link in email use timer 
    ''' 
    return("sending new password")

    
    

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



def on_request_forgot_password(ch, method, props, body):
    print("password reset 2")
    print(body)
    body = json.loads(body)

    response = forgot_password(body["email"],body["new_password"])

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)



channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
channel.basic_consume(queue='forgot_password_rpc_queue', on_message_callback = on_request_forgot_password)

print(" [x] Awaiting RPC requests")
channel.start_consuming()