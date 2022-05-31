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


def create_url(user_id, token, type=None):
    '''
    Creates the url to request the followers of one account (id in input), their location (if available) and their public metrics.
    Each request returns 1000 followers, uses the pagination token (in input) to retrieve all the followers of the user
    '''
    if type==None:
        if token:
            return "https://api.twitter.com/2/users/{}/followers?&user.fields=location,public_metrics&max_results=1000&pagination_token={}".format(user_id, token)
        else:
            return "https://api.twitter.com/2/users/{}/followers?&user.fields=location,public_metrics&max_results=1000".format(user_id)
    if type=='lookup':
        return 'https://api.twitter.com/1.1/users/lookup.json?user_id={}&max_result=1'.format(user_id)
    if type=='big':
        if token:
            return 'https://api.twitter.com/1.1/followers/ids.json?user_id={}&count=5000&cursor={}'.format(user_id, token)
        else:
            return 'https://api.twitter.com/1.1/followers/ids.json?user_id={}&count=5000'.format(user_id)
    
def get_params():
    return {"user.fields": ["created_at", "location"]}

def bearer_oauth(r):
    """
    Method required by bearer token authentication. Needs the bearer token as env variable (Var name:BEARER_TOKEN))
    """
    bearer_token = os.environ.get('BEARER_TOKEN')
    if bearer_token==None:
        raise ValueError("Please set the Bearer Token of your Twitter Application as env variable")
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "Twitter Analysis"
    return r

def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def retrieve_small(user_id, count, followers):
    '''
    Gets as input an user id and saves to a JSON file (in the data directory) data regading all the followers of the user. Retrieves 15k followers and then sleeps 15 minutes. 
    '''
    next_token= None
    if count == None:
        count=0
    response_lst= []
    while count*1000<followers:
        if count%15==0 and count!=0:
            retrieved = len(response_lst)
            missing = followers - retrieved 
            print(str(datetime.datetime.now()),'Sleeping, I retrieved information about {} accounts. I still need to retrieve information about {} accounts'.format(retrieved, missing))
            time.sleep(905)             #sleeps for 15 mins and 5 seconds to respect the Twitter limitation of 15 requests x 15 minutes https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers
        url = create_url(user_id, next_token)
        json_response = connect_to_endpoint(url)
        count+=1
        response_lst.append(json_response)
        if 'next_token' in json_response['meta'].keys():
            next_token = json_response['meta']['next_token']
        else: 
            next_token=None
        if next_token==None:
            with open("data/response{}.json".format(user_id), "w") as f:
                f.write(json.dumps(response_lst,indent=4))
    print("Following for user {} saved at \"data/response{}.json\"".format(user_id, user_id))
    return count 



def retrieve_big(user_id, count, followers):
    '''
    Gets as input an user id and saves to a JSON file (in the data directory) data regading all the followers of the user. Retrieves 15k followers and then sleeps 15 minutes. 
    '''
    next_token= None
    if count == None:
        count = 0
    response_lst= []
    while count*5000<followers:  
        if count%15==0 and count!=0:
            retrieved = count*5000
            missing = followers - retrieved
            with open("data/response{}.json".format(user_id), "a") as f:
                f.write(json.dumps(response_lst))
                next_token = None
                response_lst=[] 
            print(str(datetime.datetime.now()),'Sleeping, I retrieved the ids for {} accounts. \nI still need to retrieve the ids for {} accounts'.format(retrieved, missing))
            time.sleep(905)             #sleeps for 15 mins and 5 seconds to respect the Twitter limitation of 15 requests x 15 minutes https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers
        url = create_url(user_id, next_token, 'big')
        json_response = connect_to_endpoint(url)
        count+=1
        response_lst.append(json_response['ids'])
        if 'next_cursor_str' in json_response:
            next_token = json_response['next_cursor_str']
    print("Ids of the followers of user {} saved at \"data/response{}.json\"".format(user_id, user_id))
    return count


def account_type(user_id):
    url = create_url(user_id, token=None, type='lookup')
    json_response = connect_to_endpoint(url)
    return json_response[0]['followers_count']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Twitter-followers',
    description='''This scripts retrieves information about the Twitter followers of the account(s) provided as id in the args.
                        \nThe IDs must be provided (-l --list) as a string with comma-separated values i.e. "2244994945, 1334200897081987072".
                        \nBy deafault, if the account(s) provided have less than 75K of followers, several information about the followers ( as number of posted tweets, username, location (if available) and number of followers) will be retrieved, 
                        but this process is quite long, it will retrieve information about 15K followers and then stop for 15minutes.
                        \nFor accounts that have more than 75K followers just the ids of the followers account will be retrieved, this process obtains 75K of IDs each 15minutes. 
                        \nThis treshold of 75K can be changed with the optional parameter -t --treshold
                        ''')

    parser.add_argument('-l', '--list', help='List of IDs', type=str, required=True)
    parser.add_argument('-t', '--treshold', help='Treshold to define if an account is big or small. Default value = 75K', type=int,required=False)

    args = parser.parse_args()

    ids = [int(item)for item in args.list.split(',')]
    treshold = args.treshold    
    if treshold==None:
        treshold=75000
    count_small = None
    count_big =None
    for user_id in ids:
        followers = account_type(user_id)
        if int(followers) <treshold:
            print('I will retrieve a lot of information about the followers of account {}'.format(user_id))
            count_small = retrieve_small(user_id, count_small, followers)
        else: 
            print('I will retrieve the IDs of the followers of account {}'.format(user_id))
            count_big = retrieve_big(user_id, count_big, followers)
