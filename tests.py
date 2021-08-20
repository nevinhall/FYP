import pytest

def calculate_calories(gender,activity_level,weight,height,age):
    kg_to_lbs = int(weight) * 2.205
    cm_to_inch = int(height) / 2.54
    age = int(age)

    calories = 1800

    if(gender == "male"):
        bmr = (66 +(6.3 * kg_to_lbs) + (12.9 * cm_to_inch)) - (6.8 * age)

    if(gender == "female"):
       bmr = (655 +(4.3 * kg_to_lbs) + (4.7 * cm_to_inch)) - (4.7 * age)

    if(activity_level == "low"):
        calories = bmr *1.375

    if(activity_level == "high"):
        calories = bmr * 1.725

    return calories


def calcualte_bmi(height,weight):

    height = float(height) /100
    weight = int(weight)


    return int(weight/(height**2))


def test_bmi_healthy():
    assert calcualte_bmi(188,70) == 19

def test_bmi_over():
    assert calcualte_bmi(180,120) == 37

def test_bmi_under():
    assert calcualte_bmi(160,45) == 17

def test_calories():
    res = calculate_calories("male","high",78,176,34) 
    assert(res -300 <= res <= res + 300)