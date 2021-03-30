import json
"""
This responsible for normalising the data for use in the recommender system.
This achieved by determing a rating for each of the diet plan types.

@params: user_porfile this the user profile that requires normalising.
@return: user_profile_converted JSON string containg ratings for each diet type.

"""
def normalise_data(user_profile):

    user_profile = user_profile.decode()

    user_profile = user_profile.strip().replace('\'','').replace(',','').replace('(','').replace(')','').split()
    print("just before error", user_profile)
    user_id =  user_profile[0]
    height = user_profile[1]
    weight =user_profile[2]
    bmi =user_profile[3]
    activity_level =user_profile[4]
    dietary_options = user_profile[5]
    allergies = user_profile[6]
    age = user_profile[7]

    weight_gain = 0
    weight_lose = 0
    weight_maintaince = 0


    if(float(bmi) < 18.):
        weight_gain = weight_gain + 3
    
    elif(float(bmi) > 25):
        weight_lose = weight_lose +3
    else:
        weight_maintaince = weight_maintaince +3

    

    if(float(bmi) < 18.5 and activity_level == 'high'):
        weight_gain  = weight_gain + 1

    elif(float(bmi) > 25 and activity_level == 'low'):
        weight_lose  = weight_lose + 1
    
    else:
        weight_maintaince = weight_maintaince +1


    if(float(bmi) < 18.5 and int(age) < 25):
            weight_gain  = weight_gain + 1

    elif(float(bmi) > 25 and int(age) < 25):
        weight_lose  = weight_lose + 1
    
    else:
        weight_maintaince = weight_maintaince +1

    print("weight_maintaince", weight_maintaince)
    print("weight_gain", weight_gain)
    print("weight_lose", weight_lose)

    """
    Prep the data for use in the recommneder system, convert to json.
    """
    user_profile_converted = {"userID":{"0":user_id,"1":user_id,"2":user_id},"title":{"0":"weight lose","1":"weight gain","2":"maintaince"},"dietID":{"0":0,"1":1,"2":2},"rating":{"0":weight_lose,"1":weight_gain,"2":weight_maintaince}}
    user_profile_converted =  json.dumps( user_profile_converted )
    


    return  user_profile_converted


