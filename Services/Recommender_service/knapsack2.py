def solve_knapsack(profits, weights, capacity):
    saved_ids = []
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
            profit2 = dp[i][c]

           
            dp[i][c] = max(profit1, profit2)

       
            # print(weights[i])
        
        print(dp[i-1][c-1])
        # saved_ids = 
    
    # maximum profit will be at the bottom-right corner.

    print(dp)
    return dp[n-1][capacity]



# ids= ["id1","id2","id3","id4"]
# val = [60, 100, 120,110]
# wt = [10, 20, 30,5]
# total_cals = 50
# n = len(val)

items = ["A","B","C","D"]
weights = [2,3,1,4]
profits = [4,5,3,7]

capacity = 5
print(solve_knapsack(profits, weights, capacity))

