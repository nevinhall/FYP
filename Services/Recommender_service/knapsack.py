  
from typing import ValuesView


class knap():

  def __init__(self):
      self.saved_ids = []
      self.old_max_vals = 0

      
  def knapSack(self,total_cals, wt, val, n,ids):
        
            # Base Case
            if n == 0 or total_cals == 0:
                return 0

            
        
            # If weight of the nth item is
            # more than Knapsack of capacity W,
            # then this item cannot be included
            # in the optimal solution
            if (wt[n-1] > total_cals):
                return self.knapSack(total_cals, wt, val, n-1,ids)

            
        
            # return the maximum of two cases:
            # (1) nth item included
            # (2) not included
            else:
                #add to the ids here

                
             
                # item_included = self.knapSack(
                #         total_cals-wt[n-1], wt, val, n-1,ids)
                
                  
                # item_not_included = val[n-1] + self.knapSack(total_cals, wt, val, n-1,ids)


                # if(max(item_included,item_not_included) > self.old_max_vals):
                #     print("*******current item values*****************")
                #     print(max(item_included,item_not_included))
                #     self.saved_ids.append(ids[n-1])
                #     print(self.saved_ids)
             
                self.old_max_vals = max(item_included,item_not_included)
                return max(item_included,item_not_included)



        
        # end of function knapSack
        
            
#Driver Code

ids= ["id1","id2","id3","id4"]
val = [60, 100, 120,110]
wt = [10, 20, 30,5]
total_cals = 50
n = len(val)
ks = knap()
print (ks.knapSack(total_cals, wt, val, n,ids))
print

    

