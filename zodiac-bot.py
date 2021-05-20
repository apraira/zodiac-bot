from tweepy import (Stream, OAuthHandler)
from tweepy.streaming import StreamListener
import time
from os import environ
import tweepy
from urllib3.exceptions import ProtocolError
import random
import pyaztro

# V1
#tes
#sekarang lagi make piku
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class StreamListener(tweepy.StreamListener):
    tweet_counter = 0
    nkata = 0
    total_predict = 0
    
    
    
    def on_status(self, status):
        # Static variable
        maks = 10
        print('starting prediction')
        
        
        #Dynamic Variabel
        target_user_id = status.user.id
        target_user = api.get_user(target_user_id)
        
        user = api.me()
        
        user_a = user.id
        user_b = target_user_id
        
        #to check apakah dah follow apa belum
        stats = api.show_friendship(source_id=user_a, source_screen_name=user.screen_name, target_id=user_b, target_screen_name=target_user.screen_name)
        
        #ngecek jumlah followers
        nfolls = status.user.followers_count
        
        #horoscope
        zodiac = status.text
        zodiac = zodiac.lower()
        zodiac = zodiac.replace(".","")
        zodiac = zodiac.replace(",","")
        zodiac = zodiac.split()
        zodiac = zodiac[1]
        
        
        horoskop = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces' ]
        #list kata0
        
        #jika jumlah tweet yang di reply < 5
        
        if StreamListener.tweet_counter < maks:
            
            #jika dia follow akun
            if stats[0].followed_by == True:

                if status.is_quote_status == True:
                    
                    print("> (is quoted)" + status.user.screen_name +
                               ": " + status.text + " ( skipped )")

                elif 'RT' in status.text:
                    
                    print("> (is retweeted)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                elif status.in_reply_to_status_id != None:
                    
                    print("> (is replyied)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")
                    
                elif zodiac not in horoskop: 
                    time.sleep(10)
                    api.update_status("@" + status.user.screen_name + " " + 'hi, please do check our format (on pinned) correctly' , in_reply_to_status_id=status.id)
                    print("> (wrong format)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                #kalo followers kurang dari 40
                elif nfolls < 10:
                    
                    time.sleep(10)
                    api.update_status("@" + status.user.screen_name + " " + 'Sorry, your followers must be more than 10.', in_reply_to_status_id=status.id)
                    print(str(StreamListener.tweet_counter) + ". (less than 10 followers)" + status.user.screen_name +
                                  ": " + status.text + " ( replied )")

                else:
                    #get zodiac features
                    horoscope = pyaztro.Aztro(sign=zodiac)
                    username = status.user.screen_name
                    mood = horoscope.mood
                    luckytime = horoscope.lucky_time
                    description = horoscope.description
                    color = horoscope.color
                    jodoh = horoscope.compatibility
                    luckynumber = horoscope.lucky_number


                    kata2 = 'Hello, ' + username + "!" + '\n\n' + description + '\n\n' + 'we post different messages per-day, see you  tomorrow. :)'
                    
                                   
                    time.sleep(10)
                    api.update_status("@" + status.user.screen_name + " " + kata2, in_reply_to_status_id=status.id)


                    StreamListener.tweet_counter += 1
                    StreamListener.total_predict += 1

                    #logs
                    print(str(StreamListener.tweet_counter) + ".  " +
                    status.user.screen_name + ": " + status.text + " ( replied )")

            #Jika dia belom follow akun
            else:

                if status.is_quote_status == True:
                    
                    print("> (is quoted)" + status.user.screen_name +
                               ": " + status.text + " ( skipped )")

                elif 'RT' in status.text:
                    
                    print("> (is retweeted)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                elif status.in_reply_to_status_id != None:
                    
                    print("> (is replyied)" + status.user.screen_name +
                                  ": " + status.text + " ( skipped )")

                #reply suruh follow dulu
                else:
                    time.sleep(10)
                    api.update_status("@" + status.user.screen_name + " " + 'Please follow us first, then try again', in_reply_to_status_id=status.id)
                   
                    print(">"  +
                        status.user.screen_name + ": must follow first"  + " ( replied )") 
            
            
            
        #jika jumlah tweet yang di reply > 5
        else:
            print('Max num reached = ' +
                              str(StreamListener.tweet_counter))
            StreamListener.tweet_counter = 0
            print('Istirahat 5 Menit')
            time.sleep(60*5)
            print ("starting prediction again")
            
        
        print('============================')
        print('max number: ' + str(StreamListener.tweet_counter))
        print('total zodiac today: ' + str(StreamListener.total_predict))
        print('============================')
            
        
             
        
                      
                      
        
            
    def on_limit(self,track):
        print ("Horrors, we lost %d tweets!" % track)
        
    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

while True:
    try:
        stream.filter(track=["@zodiacperday"], stall_warnings=True)

    except Exception as e:
        print (e)
        time.sleep(1)  # to avoid craziness with Twitter
        continue

