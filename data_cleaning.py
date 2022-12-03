#Importing Libraries
import pandas as pd

#Reading the Tweets File
#insert the file path
File = pd.read_csv(r'C:\Parhai Mahool\2nd Semester\Research Seminar\final\run6\all_keys_tweets.csv')

#Creating Dataframe
Dataframe = pd.DataFrame(File, columns=['Datetime','Text','Tweet Id','Username'])

#Checking and removing duplicate values from the dataframe
Dataframe = Dataframe.drop_duplicates()

# Extracting DataFrame's Test column to list
Tweet_list = Dataframe['Text'].tolist()

#Saving Dataset/Dataframe to an excel file
Dataframe.to_csv(r'Dataset.csv', sep=',')