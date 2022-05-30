# Twitter followers
Python code based on the example provided by [TwitterDev](https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Follows-Lookup/followers_lookup.py) to retrieve followers of a Twitter account based on its ID.

## Requirements 
- Twitter project's BEARER_TOKEN set as environmental variable. 

- List of the IDs of the accounts whose followers we want to get. You can use this [tool](https://tweeterid.com/) to retrive the IDs of one account starting from its username. 

## Usage 
To obtain the followers of the account(s) provided in the list (examples):
````
pip install requests
python retrievefollowers0.py -l "2244994945,1334200897081987072"  
python retrievefollowers0.py -l "2244994945,1334200897081987072" -t 100000 
````
`-l --list` required parameter: list of the ids 

`-t --treshold` optional parameter: changes the treshold to define an account as big (default 75000)

The scripts retrieves 15000 followers and enriched information about them (number of posts, number of followers, location if available, username...) each 15minutes for small accounts (default <=75K followers) and 75000 ids each 15 minutes for the the followers for big accounts (default >75K followers)

Results are then saved in a newly created 'data' directory as JSON files (one for each of the accounts provided in the call). 


