# Twitter network
Python code based on the example provided by [TwitterDev](https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Follows-Lookup/followers_lookup.py) to retrieve a Twitter network. 

The idea is to define some target accounts, retrieve their followers (retreieve_followers0.py) and the other accounts that are followed by the previously retrieved ones. 

## Requirements 
- Twitter project's BEARER_TOKEN set as environmental variable. 

- List of the IDs of the accounts whose followers we want to get. You can use this [tool](https://tweeterid.com/) to retrive the IDs of one account starting from its username. 

## Usage 
### Followers
To obtain the followers of the account(s) provided in the list (examples):
````
pip install requests
python retrievefollowers0.py -l "2244994945,1334200897081987072"  
python retrievefollowers0.py -l "2244994945,1334200897081987072" -t 100000 
````
`-l --list` required parameter: list of the ids 

`-t --treshold` optional parameter: changes the treshold to define an account as big (default 75000)

`-c --cursor` optional parameter: to start the search from a certain token (given by Twitter in the previous request and saved to the log file)

When there's interest about just one accont the commas can be omitted: 

````
python retrievefollowers0.py -l 2244994945
````

The scripts retrieves 15000 followers and enriched information about them (number of posts, number of followers, location if available, username...) each 15minutes for small accounts (default <=75K followers) and 75000 ids each 15 minutes for the the followers for big accounts (default >75K followers)

Results are then saved in a newly created 'data' directory as JSON files (one for each of the accounts provided in the call). 

### Following
Once retrieved the followers of the target account the script retrieve_following can be used to search for other accounts, other than the target ones, that the retrieved account follows. 

The script needs a json file target_requests.json located in the folder 'data/database_ids/' containing the requests formatted as https://api.twitter.com/2/users/{user_id}/following?user.fields={desired user fileds}'. The script will retrieve information about 1000 accounts followed by each of the accounts in input. Performs 15 requests each 15 minutes then sleeps not to exceed Twitter limits. 

````
python retrieve_following.py
````
