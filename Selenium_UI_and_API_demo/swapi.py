# -*- coding: UTF-8 -*-
import requests

# This script demonstrates basic API handling using the requests module.
# If Python is not available for some reason, then the API calls can be handled by an external tool (e.g. cURL) and basic programing can be done with any available language.
#
# I am using a public API 'https://swapi.dev/api/' that gets information about (the first 6 films of) the Star Wars universe. For details check the base URL. Sive this is a public API the data can not be modified by the user (POST and DELETE requests are not supported) and there is a daily 10k limit of requests. The requests module supports all CRUD (Create, Read, Update, Delete) operations via the post, get, put and delete methods. These methods can be used in a "real world" scenario similar to the usage of the get method here.

BASE_URL = 'https://swapi.dev/api/'

def get_total_num_of(resource):
	resp = requests.get(BASE_URL + resource)
	try:
		return int(resp.json()['count'])
	except Exception as e:
		print(e,f'\nCould not find resource: "{resource}"')		

def get_all(resource):
	results = []
	resp = requests.get(BASE_URL + resource)
	try:
		while resp.json()['next'] != None:
			results += resp.json()['results']
			resp = requests.get(resp.json()['next'])
		results += resp.json()['results']
		return results
	except Exception as e:
		print(e)

def get_homeplanet_of_chars_from_film(film_num):
	results = {}
	resp = requests.get(BASE_URL + 'films/' + str(film_num))
	try:
		for char in resp.json()['characters']:
			homeplanet_url, char_name = requests.get(char).json()['homeworld'], requests.get(char).json()['name']
			results[char_name] = requests.get(homeplanet_url).json()['name']
		return results
	except Exception as e:
		print(e)

def test_num_of_total_characters():
	assert get_total_num_of('people') == 82 # as of 15th March,2021

def test_all_planets_are_retreived():
	assert get_total_num_of('planets') == len(get_all('planets'))

def test_jar_jar_from_Naboo():
	assert get_homeplanet_of_chars_from_film(4)['Jar Jar Binks'] == 'Naboo'

if __name__ == '__main__':
	test_num_of_total_characters()
	test_all_planets_are_retreived()
	test_jar_jar_from_Naboo()
	
	print('The homeplanets of the characters in "The Empire Strikes Back" are the following:')
	for k,v in get_homeplanet_of_chars_from_film(2).items():
		print(f'- the homeplanet of {k} is {v}.')

	print('Did you know? The wookie name of planet "Bespin" is {}.'.format(requests.get(BASE_URL + 'planets/6/?format=wookiee').json()['whrascwo']))