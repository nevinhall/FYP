import re
import pika
import json
import pymysql
from validate_email import validate_email

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='user_exits_rpc_queue')
channel.queue_declare(queue='create_user_profile_rpc_queue')





def on_request_user_exists(ch, method, props, body):
    print(body)

    response = user_profile_exist(body)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def on_request_create_user_profile(ch, method, props, body):
    body = json.loads(body)
 
    print(body['user_id'], body['height'],body['weight'],body['activity_level'],body['age'],body['dietray_options'], body['allergies'])

    response = create_user_profile(body['user_id'], body['height'],body['weight'],body['activity_level'],body['allergies'],body['age'],body['dietray_options'])

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
            cursor.execute("INSERT INTO user_profiles (user_id) VALUES (%s)", (user_id))
                # cursor.execute("INSERT INTO user_profiles VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (user_id))
        except:
            return("failed to create profile")
       

        #commiting the connection then closing it.
        connection.commit()
        connection.close()

        return("profile created")
    connection.close()
    return("profile already exits")

def create_user_profile(user_id, height,weight,activity_level,allergies,age,dietray_options):
    bmi = calcualte_bmi(height,weight)
   
    
    #database connection
    connection = pymysql.connect(host="localhost",user="root",passwd="",database="user_profiles" )
    cursor = connection.cursor()
    # some other statements  with the help of cursor
    

    #executing the quires
    try:
        cursor.execute("UPDATE user_profiles SET height = %s , weight = %s, bmi = %s, activity_level = %s, dietary_options = %s, allergies = %s, age = %s WHERE user_id = %s",(
        height,weight,bmi,activity_level,dietray_options,allergies,age,user_id))
    except:
        return("failed to populate user profile")
    

    #commiting the connection then closing it.
    connection.commit()
    connection.close()
    print("sent to db")


    return("updated profile")

def calcualte_bmi(height,weight):
    return weight/(height**2) 

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='user_exits_rpc_queue', on_message_callback=on_request_user_exists)
channel.basic_consume(queue='create_user_profile_rpc_queue', on_message_callback=on_request_create_user_profile)



print(" [x] Awaiting RPC requests")
channel.start_consuming()