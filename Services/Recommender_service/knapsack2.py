import numpy as np

def solve_knapsack(nutritional_preference_value, meal_calories, total_calories):
    n = len(nutritional_preference_value) 
    if total_calories <= 0 or n == 0 or len(meal_calories) != n:
        return 0
    
    dp = [[0 for x in range(total_calories+1)] for y in range(n)]
    
    # populate the total_calories = 0 columns, with '0' total_calories we have '0' profit
    for i in range(0, n):
        dp[i][0] = 0
    
    # if we have only one weight, we will take it if it is not more than the total_calories
    for c in range(0, total_calories+1):
        if meal_calories[0] <= c:
            dp[0][c] = nutritional_preference_value[0]
    
    for i in range(1, n):
        for c in range(1, total_calories+1):
            profit1, profit2 = 0, 0
            if meal_calories[i] <= c:
                profit1 = nutritional_preference_value[i] + dp[i-1][c-meal_calories[i]]
            profit2 = dp[i-1][c]
            dp[i][c] = max(profit1, profit2)

    col = total_calories 

    for row in range(n-1,0,-1):
        if( dp[row][col] !=  dp[row-1][col]):
            # print(dp[row][col] , '!=',  dp[row-1][col])
            print("Value added",nutritional_preference_value[row])
            col =  col - meal_calories[row]
            print("New Backpack weight", col)

    print(dp[0][total_calories])
    
    # maximum profit will be at the bottom-right corner.
    print(np.matrix(dp))
    return dp[n-1][total_calories]
meal_ids = ["A","B","C","D"]
meal_calories = [2,3,1,4]
nutritional_preference_value = [100,5,3,7]

total_calories = 150
print(solve_knapsack(nutritional_preference_value, meal_calories, total_calories))

