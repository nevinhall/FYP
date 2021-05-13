import pika
import json
import pymysql
import uuid
from pymongo import MongoClient
from bson.json_util import dumps

connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq',port="5672"))

channel = connection.channel()

channel.queue_declare(queue='get_num_users_rpc_queue')
channel.queue_declare(queue='get_num_users_gender_rpc_queue')
channel.queue_declare(queue='get_all_meals_rpc_queue')
channel.queue_declare(queue='get_all_exercises_rpc_queue')
channel.queue_declare(queue='create_meal_rpc_queue')
channel.queue_declare(queue='create_exercise_rpc_queue')
channel.queue_declare(queue='del_meal_rpc_queue')
channel.queue_declare(queue='del_exercise_rpc_queue')


#database connection
connection_user = pymysql.connect(host="mysqldb",user="root",passwd="",database="users" )
cursor_user = connection_user.cursor()






def get_num_users():
    connection_user_profiles = pymysql.connect(host="mysqldb",user="root",passwd="",database="user_profiles" )
    cursor_user_profiles = connection_user_profiles.cursor()

    try:
        sql = "SELECT COUNT(user_id) FROM user_profiles"
        cursor_user_profiles.execute(sql)
        result = cursor_user_profiles.fetchall()
        result = result[0][0]

        connection_user_profiles.commit()
      
    except:
        result = ("failure")

    connection_user_profiles.close()
    return(result)


def get_num_user_gender(gender):
    connection_user_profiles = pymysql.connect(host="mysqldb",user="root",passwd="",database="user_profiles" )
    cursor_user_profiles = connection_user_profiles.cursor()
    
    try:
        sql = "SELECT COUNT(user_id) FROM user_profiles WHERE gender =%s"
        cursor_user_profiles.execute(sql,gender)
        result = cursor_user_profiles.fetchall()
        result = result[0][0]
    except:
        result = ("failure")


    return(result)


def get_all_meals():
    print("Request Made for all meals")
    client = MongoClient('mongodb://host.docker.internal:27017')
    db =client.meal
 
    meals= []
    for meal in db["meals"].find():
        meals.append(meal)
        
    return(dumps(meals))


def get_all_exercises():

    client = MongoClient('mongodb://host.docker.internal:27017')
    db =client.workouts
 
    workouts = []
    for workout in db["workout"].find():
        workouts.append(workout)
        
    return(dumps(workouts))


def creat_meal(Meal,Protein,Carbs,Fats,calories,Category,strArea,strInstructions,strYoutube):
    client = MongoClient('mongodb://host.docker.internal:27017')
    db =client.meal
    id =  str(uuid.uuid4())

    values = {
        "idMeal": id,
        "Meal": Meal,
        "Protein": Protein,
        "Carbs":Carbs,
        "Fats":Fats,
        "calories":calories,
        "Category":Category,
        "strArea":strArea,
        "strInstructions":strInstructions,
        "strYoutube":strYoutube

    }
  

    db["meals"].insert_one(values)
    return("done")



def create_exercise(name,desciption,type,reps):
    client = MongoClient('mongodb://host.docker.internal:27017')
    db =client.workouts
  

    values = {
        "name": name,
        "deciption": desciption,
        "type":type,
        "reps":int(reps)
    }
  

    db["workout"].insert_one(values)
    return("done")



def del_meal(meal_id):
    client = MongoClient('mongodb://host.docker.internal:27017')
    print("deleting",meal_id)
    db = client.meal
    db["meals"].delete_one({"idMeal":meal_id})

    return("deleted")
  

def del_exercise(exercise_name):
    client = MongoClient('mongodb://host.docker.internal:27017')
    print("Deleting exercise: ",exercise_name,flush=True)

    db = client.workouts
    deletWhere = { "name": exercise_name}
    db["workout"].delete_one(deletWhere)

    return("deleted")
  



def on_request_del_meal(ch, method, props, body):
    
    body = json.loads(body)
    response = del_meal(body["meal_id"])

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)




def on_request_del_exercise(ch, method, props, body):

    body = json.loads(body)
    response = del_exercise(body["name"])

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)




def on_request_create_exercise(ch, method, props, body):
    body = json.loads(body)

    response = create_exercise(body["name"],body["deciption"],body["type"],body["reps"])

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    



def on_request_create_meal(ch, method, props, body):
    body = json.loads(body)

    response = creat_meal(body["Meal"],body["Protein"],body["Carbs"],body["Fats"],body["calories"],body["Category"],body["strArea"],body["strInstructions"],body["strYoutube"])

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    


def on_request_get_all_exercises(ch, method, props, body):
 
    response = get_all_exercises()

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)



def on_request_get_all_meals(ch, method, props, body):
 
    response = get_all_meals()

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

    

def on_request_get_num_users_gender(ch, method, props, body):
    body = json.loads(body)

    response = get_num_user_gender(body["gender"])

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    




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
channel.basic_consume(queue='get_num_users_gender_rpc_queue', on_message_callback=on_request_get_num_users_gender)
channel.basic_consume(queue='get_all_meals_rpc_queue', on_message_callback=on_request_get_all_meals)
channel.basic_consume(queue='get_all_exercises_rpc_queue', on_message_callback=on_request_get_all_exercises)
channel.basic_consume(queue='create_meal_rpc_queue', on_message_callback=on_request_create_meal)
channel.basic_consume(queue='create_exercise_rpc_queue', on_message_callback=on_request_create_exercise)
channel.basic_consume(queue='del_meal_rpc_queue', on_message_callback=on_request_del_meal)
channel.basic_consume(queue='del_exercise_rpc_queue', on_message_callback=on_request_del_exercise)


print("Admin service")
channel.start_consuming()