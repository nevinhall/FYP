import pika
import json
from pika.connection import PRODUCT
import pymysql

connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq',port="5672"))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')
channel.queue_declare(queue='forgot_password_rpc_queue')



def login(email,password): 
    connection = pymysql.connect(host="mysqldb",user="root",passwd="",database="users" )
    cursor = connection.cursor()
    
    if(valid_email(email) and valid_password(email,password)):
        sql = "SELECT user_id FROM users WHERE email =%s"
        cursor.execute(sql,email)
        result = cursor.fetchall()


        return(result[0][0])
    return("failure")



def valid_email(email):
    connection = pymysql.connect(host="mysqldb",user="root",passwd="",database="users" )
    cursor = connection.cursor()

    sql = "SELECT * FROM users WHERE email =%s"
    cursor.execute(sql,email)
    result = cursor.fetchone()
    print("LOGIN IMPL, FUNC:valid_email ->  Valid email",result,flush=True)

    if(result == None):
        return False


    return True



def valid_password(email,password):
    connection = pymysql.connect(host="mysqldb",user="root",passwd="",database="users" )
    cursor = connection.cursor()

    cursor.execute("""SELECT password FROM users WHERE email = %s AND password = %s""" ,(email, password))
    result = cursor.fetchone()

    print("LOGIN IMPL, FUNC:valid_password -> Valid password", result,flush=True)

    if(result == None):
        return False


    return True



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

print("Login Service Awaiting RPC requests")
channel.start_consuming()