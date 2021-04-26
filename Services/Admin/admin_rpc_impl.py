import pika
import json
import pymysql

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='get_num_users_rpc_queue')


#database connection
connection = pymysql.connect(host="localhost",user="root",passwd="",database="users" )
cursor = connection.cursor()



def get_num_users(): 
    
    try:
        sql = "SELECT COUNT(user_id) FROM users"
        cursor.execute(sql)
        result = cursor.fetchall()
        result = result[0][0]
    except:
        result = ("failure")


    return(result)




    
    

def on_request_get_num_users(ch, method, props, body):
 

    response = get_num_users()

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)



channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='get_num_users_rpc_queue', on_message_callback=on_request_get_num_users)


print("Admin service")
channel.start_consuming()