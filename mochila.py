import urllib.request
import csv
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.request import urlretrieve 


# Python3 program to solve fractional  
# Knapsack Problem 
class ItemValue: 
      
    """Item Value DataClass"""
    def __init__(self, wt, val, ind): 
        self.wt = wt 
        self.val = val 
        self.ind = ind 
        self.cost = val // wt 
  
    def __lt__(self, other): 
        return self.cost < other.cost 
  
# Greedy Approach 
class FractionalKnapSack: 
      
    """Time Complexity O(n log n)"""
    @staticmethod
    def getMaxValue(wt, val, capacity,ind): 
          
        """function to get maximum value """
        iVal = [] 
        for i in range(len(wt)): 
            iVal.append(ItemValue(wt[i], val[i], ind[i])) 
  
        # sorting items by value 
        iVal.sort(reverse = True) 
        totalValue = 0
        print(len(iVal))
        curItems = []
        for i in iVal: 
            curWt = int(i.wt) 
            curVal = int(i.val) 
            if capacity - curWt >= 0: 
                capacity -= curWt 
                totalValue += curVal 
                curItems.append(i.ind)
            #else: 
              #  fraction = capacity / curWt 
               # totalValue += curVal * fraction 
                #capacity = int(capacity - (curWt * fraction)) 
                #curItems.append(i.ind)
                #break           
        return totalValue, curItems 

wt = []
val = []
ind = []
capacity = 100000


with open('tablas/Paris.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
        	ind.append(row[0])	
        	wt.append(int(row[3].replace('$','').replace('.','')))
	        val.append(abs(int(row[4].replace('$','').replace('.',''))-int(row[3].replace('$','').replace('.',''))))
	        line_count += 1
    print(f'Processed {line_count} lines.')

maxValue = FractionalKnapSack.getMaxValue(wt, val, capacity,ind)[0] 
print("items =",FractionalKnapSack.getMaxValue(wt, val, capacity,ind)[1] )
print("Maximum value in Knapsack =", maxValue)	        