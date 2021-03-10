# -*- coding: UTF-8 -*-
import requests, re


# this function needs additional work: has problems when strings containi characters that should be escaped, maybe some encoding can help
qs_regex = lambda s: re.compile('.*?'+'.*?'.join(s.replace('+','\+').split()),re.IGNORECASE) # generate regex from query string


# this needs to be updated, only first 12 communities added
def get_communities(qs):
    '''
    Returns all communities  as a dict given the query string qs as the text entered
    in the search field. All other filters (category, location, language, online) are empty.
    '''
    response = requests.get(f'https://community-z.com/api/v2/communities.json?start=0&order=most_popular&search={qs}')
##    comm = []
##    total_comms = int(response.json()['total'])
##    while total > 0: get other responce with start+=12, add comms, total -= 12
    try:
        comm = response.json()['communities']
    except:
        comm = []
    return comm


def get_categories(_id): # using _id since id is a builtin function
    '''
    Returns all categories as a list given the id of a community.
    An empty list is returned if categories could not be found.
    '''
    responce = requests.get(f'https://community-z.com/api/v2/communities/{_id}/pages/home')
    try:
        cats = responce.json()[0]['properties']['details']['categories']
    except:
        cats = []
    return cats

def is_valid_search(qs):
    '''
    Returns a boolean value depending on the validity of a search with qs entered in the search field.
    A search is considered valid if the following is True:
    - No communities are found for the search
    - For all communities that are results of the search:
        either
        - the regular expression generated from qs matches the title
        or
        - the regular expression generated from qs matches one of the categories associated with the community

        Messages are also printed to the terminal to check progress.
    '''
    comms = get_communities(qs)
    if not comms:
        print(f'\n\n---------\nNo communities found for "{qs}"')
        return True
    rqs = qs_regex(qs)
    print(f'\n\n---------\n{len(comms)} communities found as results for search string "{qs}"')
    for c in comms:
        print('\nVerifying search validity for community with title="{}"'.format(c['title']))
        if re.findall(rqs,c['title']):
            print('"{}" is a valid result: {} is part of the title'.format(c['title'],re.findall(rqs,c['title'])))
            continue
        cats = get_categories(c['id'])
        if not cats:
            print('No match in title and no categories found. Search is invalid.')
            return False
        for cat in cats:
            if re.findall(rqs,cat):
                print('"{}" is a valid result: {} is part of the category "{}"'.format(c['title'],re.findall(rqs,cat),cat))
                break
            
            
cases = ['EPAM', 'bRest it', 'IT BreST', 'aWs', 'AWS', 'python', 'x', 'noresults']                

[is_valid_search(case) for case in cases]
