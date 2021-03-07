import pandas as pd
import csv
from scipy.spatial.distance import cosine

data = pd.read_csv("Databases/Small_Data_Groceries.csv")
data["Quantity"] = 1

print(data.head(100)) # First 100 Values
len(pd.unique(data.item)) # Unique values

dataWide = data.pivot("Person", "item", "Quantity") # Converting data from long to wide format
dataWide.fillna(0, inplace=True) # Fill NA with 0
dataWide.head(100) # First 100 Values

data_ib = dataWide.copy() # For Item Based collaborative filtering
data_ib = data_ib.reset_index()
data_ib = data_ib.drop("Person", axis=1)

data_ibs = pd.DataFrame(index=data_ib.columns,columns=data_ib.columns) # Creating Place holder frame

# Similarity Measure
for i in range(0,len(data_ibs.columns)) :
    for j in range(0,len(data_ibs.columns)) :
      # Fill in placeholder with cosine similarities
      data_ibs.iloc[i,j] = 1-cosine(data_ib.iloc[:,i],data_ib.iloc[:,j])

data_ibs.head(100) # First 100 Similarity Values

data_neighbours = pd.DataFrame(index=data_ibs.columns,columns=range(1,11))
 
# Loop through our similarity dataframe and fill in neighbouring item names
for i in range(0,len(data_ibs.columns)):
    data_neighbours.iloc[i,:10] = data_ibs.iloc[0:,i].sort_values(ascending=False)[:10].index
    
data_neighbours  # Printing Data Neighbours

# For User Based Collaborating Filtering
def getScore(history, similarities):
   return sum(history*similarities)/sum(similarities)

data_sims1 = dataWide.reset_index()

# Create a place holder matrix for similarities, and fill in the user name column
data_sims = pd.DataFrame(index=data_sims1.index,columns=data_sims1.columns)
data_sims.iloc[:,:1] = data_sims1.iloc[:,:1]

data_sims12 = data_sims1.iloc[:100,] # Copying first 100 Values
data_sims11 = data_sims.iloc[:100,] # Copying first 100 Values

# Need to run this for only limited users, Might be slow beyond that.
for i in range(0,len(data_sims11.index)):
    for j in range(1,len(data_sims11.columns)):
        user = data_sims11.index[i]
        product = data_sims11.columns[j]
 
        if data_sims12.iloc[i][j] == 1:
            data_sims11.iloc[i][j] = 2 # Preorders value
        else:
            product_top_names = data_neighbours.loc[product][1:]
            product_top_sims = data_ibs.loc[product].sort_values(ascending=False)[1:]
            user_purchases = data_ib.loc[user,product_top_names]
 
            data_sims11.iloc[i][j] = getScore(user_purchases,product_top_sims)

data_sims11.head(100) # After Collaborative filtering Values

# Get the top products
data_recommend = pd.DataFrame(index=data_sims.index, columns=['Person','Prior 1','Prior 2','Prior 3','Prior 4','Prior 5','Prior 6','Prior 7'])
data_recommend.iloc[0:,0] = data_sims.iloc[:,0]

# Instead of top product scores, we want to see names
for i in range(0,len(data_sims.index)):
    data_recommend.iloc[i,1:] = data_sims.iloc[i,1:].sort_values(ascending=False).iloc[0:7,].index.transpose()

# newuser to add new user in csv file
def newuser():  
    x=None
    x=input("Enter the Product(Item) Name: ")
    with open("Databases/Small_Data_Groceries.csv","a") as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow([user_id,x])

# GUI:
print('\n--Welcome in Groceries Recommendation Engine--\n')
print('Select follwing option:- \n1.Add New user\n2.Search Previous user(by there id)\n3.Show recommendation for all users\n0.Exit')
option=-1
data_recommend.index.name='Ind'
option=int(input('Choose your option:-'))
while option>0:
    if(option==1):
        user_id=int(input('Create new user ID:- '))
        A=int(input('No. Purchased items: '))
        for q in range(A):
            newuser() 
        break
    elif(option==2):
        user=int(input("Enter the user ID:- "))
        user=user-1
        print ('n',data_recommend.iloc[user,])
        break
    elif(option==3):
        print ('\n',data_recommend.head(100))
        break
    else:
        print('\nPlease Enter Valid option')
        break
print ('\nThank you')