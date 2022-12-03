# Importing Libraries
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import os
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Creating list to append tweet data to
complete_tweets_list = []
dict_tweets_keywords={}

#creating keywords list
keyword_list = ["CovidVaccine", "Covid19vaccine", "Covid_19vaccine", "COVIDVaccines", "COVIDVaccination", "Johnson & Johnson", "Johnson and Johnson", "Pfizer", "Moderna", "Comirnaty", "Spikevax", "Janssen"]
#creating list of cities
cities_list = ["Huntsville", "Anchorage", "Tafuna", "Phoenix", "Springdale", "Fresno", "Denver", "Bridgeport", "Wilmington", "Jacksonville", "Atlanta", 
                "Honolulu", "Boise", "Chicago", "Indianapolis", "Evansville", "Wichita", "Louisville", "Shreveport" ,"Portland", "Baltimore", "Boston",
                "Detroit", "Minneapolis", "Jackson", "Springfield", "Billings", "Omaha", "Reno", "Manchester", "Newark", "Albuquerque", "Yonkers", "Charlotte", "Fargo", "Saipan", "Columbus","Norman",
                "Portland", "Philadelphia", "Carolina", "Providence", "Charleston", "Aberdeen", "Houston", "Provo", "Burlington", "Northside", "Chesapeake", "Norfolk", "Northside", "Rutland", "Orem",
                "Dallas", "Memphis", "Brookings", "Columbia", "Cranston", "Ponce", "Pittsburgh", "Salem", "Tulsa", "Cleveland", "Tinian", "Bismarck", "Raleigh", "Buffalo", "Roswell", "Paterson"
                "Nashua", "Henderson", "Lincoln", "Missoula", "Gulfport", "Rochester", "Warren", "Worcester", "Lewiston", "Lafayette", "Lexington", "Olathe", "Carmel", "Evansville", "Aurora", "Meridian"
                "Hilo", "Yigo", "Columbus", "Miami", "Dover", "Stamford", "Aurora", "San Diego", "San-Diego", "SanDiego", "Fayetteville", "Tucson", "Juneau"]
years_list = [2020,2021]

for key in keyword_list:
    print("keyword: ",key)
    all_tweet_key_list = []
    #creating directories

    #directory for search keyword
    current_directory = os.getcwd()
    directory = key
    path = os.path.join(current_directory,directory)
    if not os.path.exists(path):
        os.mkdir(path)
        
    
    for city in cities_list:
        tweet_city_list = []

        #directory for city
        city_directory = city
        city_path = os.path.join(path,city_directory)
        if not os.path.exists(city_path):
            os.mkdir(city_path)

        #directory for json files
        json_directory = "json"
        json_path = os.path.join(city_path,json_directory)
        if not os.path.exists(json_path):
            os.mkdir(json_path)
        
        #directory for csv files
        csv_directory = "csv"
        csv_path = os.path.join(city_path,csv_directory)
        if not os.path.exists(csv_path):
            os.mkdir(csv_path)

        for year in years_list:
            if year == 2020:
                #setting up month for dates
                month = 10
                end_month = 13
            if year == 2021:
                #setting up month for dates
                month = 1
                end_month = 8
            while month < end_month:
                #setting up complete date
                day = 2
                cuurrent_date = str(year)+"-"+str(month)+"-"+"01"
                last_date = str(year)+"-"+str(month)+"-"+str(day)

                while day < 31:
                    date_tweets_list = []
                    print("current_date: ",cuurrent_date)
                    print("current_date: ",last_date)

                    #directories based on dates for json files  
                    date_json_dir = os.path.join(json_path,cuurrent_date+'to'+last_date)
                    if not os.path.exists(date_json_dir):
                        os.mkdir(date_json_dir) 

                    #directories based on dates for csv files  
                    date_csv_dir = os.path.join(csv_path,cuurrent_date+'to'+last_date)
                    if not os.path.exists(date_csv_dir):
                        os.mkdir(date_csv_dir) 

                    #getting tweets:    
                    # Using TwitterSearchScraper to scrape data and append tweets to list
                    #searchterm: Term that we want to search
                    #since: time since we want to search
                    #until: time until we want to search
                    #near: Near a location(place city) we want to search
                    #within: within a certain radius
                    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('{searchterm} since:{currentdate} until:{lastdate} near:{location} within:50km'.format(
                            searchterm = key, currentdate = cuurrent_date, lastdate=last_date, location = city)).get_items()):
                        if i>1000:
                            continue

                        #appending tweets to different lists
                        date_tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.user.location])
                        tweet_city_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.user.location])
                        all_tweet_key_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.user.location])
                        complete_tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.user.location])
                    
                    #incrementing day
                    day += 1
                    #setting up new search dates
                    cuurrent_date = last_date
                    last_date = str(year)+"-"+str(month)+"-"+str(day)

                    # Creating a dataframe from the tweets list above
                    date_tweets_df2 = pd.DataFrame(date_tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'Location'])

                    #creting file names
                    csv_filename = cuurrent_date+'to'+last_date+'.csv'
                    json_filename = cuurrent_date+'to'+last_date+'.json'

                    #saving files
                    date_tweets_df2.to_json(r""+date_json_dir+"\\"+json_filename)
                    date_tweets_df2.to_csv(r""+date_csv_dir+"\\"+csv_filename)

                #increment month
                month +=1

        #saving tweets based on key and city to csv file        
        city_tweets_df2 = pd.DataFrame(tweet_city_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'Location'])
        city_tweets_df2.to_csv(r""+city_path+"\\"+key+'_'+city+'.csv')
        city_tweets_df2.to_json(r""+city_path+"\\"+key+'_'+city+'.json')
        
    #saving tweets based on key to a file
    all_tweet_key_df2 = pd.DataFrame(all_tweet_key_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'Location'])
    all_tweet_key_df2.to_csv(r""+path+"\\"+key+'.csv')
    all_tweet_key_df2.to_json(r""+path+"\\"+key+'.json')

#combining all tweets based on key, city,date and saving them
complete_tweets_df2 = pd.DataFrame(complete_tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'Location'])
complete_tweets_df2.to_json(r"all_keys_tweets.json")
complete_tweets_df2.to_csv(r"all_keys_tweets.csv")