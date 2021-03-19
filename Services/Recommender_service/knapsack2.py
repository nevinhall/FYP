import numpy as np

def solve_knapsack(profits, weights, capacity):
    n = len(profits) 
    if capacity <= 0 or n == 0 or len(weights) != n:
        return 0
    
    dp = [[0 for x in range(capacity+1)] for y in range(n)]
    
    # populate the capacity = 0 columns, with '0' capacity we have '0' profit
    for i in range(0, n):
        dp[i][0] = 0
    
    # if we have only one weight, we will take it if it is not more than the capacity
    for c in range(0, capacity+1):
        if weights[0] <= c:
            dp[0][c] = profits[0]
    
    for i in range(1, n):
        for c in range(1, capacity+1):
            profit1, profit2 = 0, 0
            if weights[i] <= c:
                profit1 = profits[i] + dp[i-1][c-weights[i]]
            profit2 = dp[i-1][c]
            dp[i][c] = max(profit1, profit2)

    col = capacity 

    for row in range(n-1,0,-1):
        if( dp[row][col] !=  dp[row-1][col]):
            # print(dp[row][col] , '!=',  dp[row-1][col])
            print("Value added",profits[row])
            col =  col - weights[row]
            print("New Backpack weight", col)

    print(dp[0][capacity])
    
    # maximum profit will be at the bottom-right corner.
    print(np.matrix(dp))
    return dp[n-1][capacity]
items = ["A","B","C","D"]
weights = [2,3,1,4]
profits = [100,5,3,7]

capacity = 150
print(solve_knapsack(profits, weights, capacity))

