import requests
import os
import time
import pickle
import datetime
import logging
from keyboard import press

def print_time():
    return str(datetime.datetime.now())

def create_url(users):
    return "https://api.twitter.com/2/users?ids={}".format(users)

def get_params():
    return {"user.fields": ["public_metrics"]}

def bearer_oauth(r):
    """
    Method required by bearer token authentication. Needs that the bearer token is set as env variable (Var name:BEARER_TOKEN))
    """
    bearer_token = os.environ.get('BEARER_TOKEN')

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "Twitter Analysis"
    return r

def connect_to_endpoint(url):
    params = get_params()
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        print('sleeping for error on twitter', response.status_code, response.text)
        time.sleep(905)
        response = requests.request("GET", url, auth=bearer_oauth, params=params)
    return response.json()

def format_ids(ids_lst):
    return ','.join(ids_lst)

        
if __name__ == '__main__':
    path = os.getcwd()
    if not os.path.exists('Twitter_Analysis/data/n_followers/logs'):
        os.makedirs('Twitter_Analysis/data/n_followers/logs')    
    logger = logging.getLogger()
    handler = logging.FileHandler("Twitter_Analysis/data/n_followers/logs/{}.json".format(datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f")))
    logger.addHandler(handler)    
    counter = 0
    idx=0
    with open('Twitter_Analysis/data/database_ids/ids.json', "rb") as f:
        ids_lst =  pickle.load(f)
        tot = len(ids_lst)
        del ids_lst
    if not os.path.exists('Twitter_Analysis/data/n_followers'):
        os.makedirs('Twitter_Analysis/data/n_followers')
    while counter <=tot:
        #provide here the file containing the list of ids
        with open('Twitter_Analysis/data/database_ids/ids.json', "rb") as f:
            ids_lst =  pickle.load(f)
            to_search= ids_lst[idx:idx+100]
            del ids_lst
            ids_form = format_ids(to_search)
            f.close()
        if counter%75==0 and counter!=0:
            retrieved=counter*100
            missing = tot - retrieved
            message= print_time(),'Sleeping, I retrieved the number of followers for {} accounts. \nI still need to retrieve the ids for {} accounts. Last index: {}'.format(retrieved, missing, idx)     
            logger.error(message)
            print(print_time(),'Sleeping, I retrieved the number of followers for {} accounts. \nI still need to retrieve the ids for {} accounts. Last index: {}'.format(retrieved, missing, idx))
            time.sleep(905)
            press('enter')

        url = create_url(ids_form)
        json_response = connect_to_endpoint(url)
        counter+=1
        idx+=100
        with open('Twitter_Analysis/data/n_followers/request{}.json'.format(counter), 'wb') as fp:
            pickle.dump(json_response, fp)
            fp.close()
        print(print_time(), counter, 'saved. Last index:{}'.format(idx))   
