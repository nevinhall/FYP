import re
import pika
import json
import pymysql
from validate_email import validate_email

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='user_exits_rpc_queue')








def on_request_sign_up(ch, method, props, body):
  
 
    print(body)

    response = user_profile_exist(body)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


"""
React app calls this first to determine what page to render 
"""
def user_profile_exist(user_id):
    #database connection
    connection = pymysql.connect(host="localhost",user="root",passwd="",database="user_profiles" )
    cursor = connection.cursor()
    
    print("here",user_id)
    sql = "SELECT user_id FROM user_profiles WHERE user_id =%s"
    cursor.execute(sql,user_id)
    result = cursor.fetchone()
    print(result)

    if(result == None):
             #executing the quires
        try:
            cursor.execute("INSERT INTO user_profiles VALUES (%s)", (user_id))
        except:
            return("failed to sign up")
       

        #commiting the connection then closing it.
        connection.commit()
        connection.close()

        return("profile created")
    connection.close()
    return("profile already exits")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='user_exits_rpc_queue', on_message_callback=on_request_sign_up)


print(" [x] Awaiting RPC requests")
channel.start_consuming()