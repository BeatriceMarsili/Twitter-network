"""
Created on 17/05/2022
original code @TwitterDev
adaptation @BeatriceMarsili
"""

from urllib import response
import requests
import os
import json 
import time
import argparse
import datetime
import logging
from keyboard import press

def print_time():
    return str(datetime.datetime.now())

def est_time(req):
    time = req   
    days = round(time / 1440, 0)     
    leftover_minutes = time % 1440
    hours = leftover_minutes / 60
    return (str(days) + " days, " + str(hours) + " hours.")

def bearer_oauth(r):
    """
    Method required by bearer token authentication. Needs the bearer token as env variable (Var name:BEARER_TOKEN))
    """
    bearer_token = os.environ.get('BEARER_TOKEN')
    if bearer_token==None:
        raise ValueError("Please set the Bearer Token of your Twitter Application as env variable")
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "UnMappers Analysis"
    return r

def connect_to_endpoint(url, count):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        print(print_time(),'Sleeping for error on twitter.', response.status_code, response.text, 'Last index:', count)
        time.sleep(905)
        response = requests.request("GET", url, auth=bearer_oauth)
    return response.json()


def retrieve_ids():
    count = 0
    logger = logging.getLogger()
    handler = logging.FileHandler("data/following_grade0/logs/logfile{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f")))
    logger.addHandler(handler)
    while count < 10055: 
        with open('data/database_ids/target_requests.json', 'rb') as fp:
            lines = json.load(fp)
            target = lines[count+1:count+16]
            del lines 
            fp.close()
        missing = 10055 - count
        for line in target: 
            press('enter')
            if count % 15 ==0 and count !=0: 
                time_left = est_time(missing)
                message= print_time()+'Sleeping, I retrieved the ids for {} accounts. I still need to retrieve the ids for {} accounts.'.format(count, missing)     
                logger.error(message)
                print(print_time(),'Sleeping, I retrieved the ids for {} accounts. \nI still need to retrieve the ids for {} accounts. \nEstimated time left: {}'.format(count, missing, time_left))
                time.sleep(905) 
                press('enter')
            user_id = line.split('/')[5]
            json_response = connect_to_endpoint(line, count)
            count +=1 
            missing -= 1 
            with open("data/following_grade0/response{}.json".format(user_id), "w") as f:
                f.write(json.dumps(json_response))
                f.close()
                print("Ids of the account that user {} follows saved at \"data/response{}.json\"".format(user_id, user_id))
                
    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Twitter-followers',
    description='''This scripts retrieves the ids of the accounts followed by the accounts in input.
                        \nThe IDs must be provided in a .txt file containing the requests to the Twitter api, assumes the accounts follow less than 800 other accounts, therefore doens't need the parameter max_results.
                        \nExpects a file in data/database_ids/target_requests.json containing the list of the requests to be made. Format: 'https://api.twitter.com/2/users/$user_id$/following?user.fields=$desired user fileds$\'''')
    log_dir = '/data/following_grade0/logs'
    if not os.path.exists(os.getcwd()+log_dir):
        os.makedirs(os.getcwd()+log_dir)
    retrieve_ids()
    print("Process finished")
    


