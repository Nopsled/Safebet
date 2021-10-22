#!/usr/bin/python
import requests
import os
import json
from difflib import SequenceMatcher


###################TODO#########################
#	Made with love and stress during 2019	   #
################################################

################################################

BANNER = """
#####################################################
############## - - - MATCH FINDER - - - #############
#####################################################

#	Supported websites: Nordicbet, Betway
#	In development: Fotball
#	Created with love and stress during summer 2019
#	Version 0.5 (JSON)
#	Author: XXX.

#####################################################
#####################################################
#####################################################
"""

BETWAY_URL = "https://sports.betway.se/api/Events/V2/GetEvents?t=62cbdb81-5a3a-4ff5-935b-c89ef5211091"

BETWAY_PAYLOAD = {
"LanguageId": 2,
"ClientTypeId": 2,
"BrandId": 3,
"JurisdictionId": 6,
"ClientIntegratorId":1,
"ExternalIds":[4130816,4130819,4139699,4139230,4139231,4139242,4139247],
"MarketCName": "total-goals-2-5",
"ScoreboardRequest": { "ScoreboardType": 3, "IncidentRequest": {} },
"ApplicationId": 5,
"BrowserId": 3,
"OsId": 4,
"ApplicationVersion": "",
'BrowserVersion': "74.0.3729.169","OsVersion": "10.14.6","SessionId": 'null',"TerritoryId": 254, "CorrelationId": "4fa8dafc-0196-48a8-81b2-f534e8cb2e68","ViewName":"sports"
}

BETWAY_HEADERS = {
		"Content-Type": "application/json; charset=utf-8",
		"Origin": "https://sports.betway.se",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept": "application/json; charset=UTF-8",
		"Referer": "https://sports.betway.se/sv/sports/cat/soccer",
		"Accept-Language": "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
		"Cookie": "btag=0dbe099b-7f9c-471e-9790-a211f8e82a4c; TrackingVisitId=0dbe099b-7f9c-471e-9790-a211f8e82a4c; SpinSportVisitId=0a637f2c-1765-431f-9c8b-d4c7735a6d56; userLanguage=sv; TS01274dd2=01955136d73a14b020d11807518f2a7e2b3985aec02f01172d6c188375b391fdd371cdb195692c54823ba70d8254032487eb17f108f29fd0319684c388aeb6b461dcc22ff81f96806b8e734ef1d1808ae91045c975; TS017040ab=01955136d7e02a8b6596d89687f678aeac0cdc045f2f01172d6c188375b391fdd371cdb195692c54823ba70d8254032487eb17f108faa488f1ef755f263f5f8c65bda6cfc22b4f94bd3e4cff0deeca9da37140e86c48718e284199d15f239b046a9482017d; _ga=GA1.2.867753266.1558941609; _gid=GA1.2.418187462.1558941609; _fbp=fb.1.1558941611167.1542515829; TimezoneOffset=120; TS01cb28e0=01955136d7e421ea8173ebd187cbe2561f7c8d8b6e98f82ab72ed77fd8ffd6b98ab1bb18b4b6f88c268150045081124549419b95c2a363acb1ed7a389cbd1b4f01a120e8acbde54d2afb5c317e3159384dcd2fd4656c043fa5744e272c5509bb8f7a9a97c8",
		"Connection": "keep-alive"
}



NORDICBET_URL = "https://obgapi.bpsgameserver.com/api/sb/v1/widgets/events-table/v2?eventPhase=Prematch&maxMarketCount=500&startsOnOrAfter=2019-05-28T18:00:00Z&startsBefore=2019-05-29T18:00:00Z&eventSortBy=StartDate"
NORDICBET_HEADERS = {
'brandId': '3a487f61-ef61-4a3a-af38-cd0eb89519ce',
'marketCode': 'en'
}

class Match:
	def __init__(self, match_id, match_name, match_date, match_time, website):
		self.match_id = match_id
		self.match_name = match_name
		self.match_date = match_date
		self.match_time = match_time
		self.website = website

		self.high_odds = 0
		self.low_odds = 0

		self.betting_options_list = []

class BettingOption:
	def __init__(self, match_id, option, odds):
		self.match_id = match_id
		self.option = option
		self.odds = odds



# Compare similarity in string 0 - 1 (0 - 100%)
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Flip the match strings to compare
def flip_string_by_minus(name):
	return '{0} - {1}'.format(name.split(" - ")[1], name.split(" - ")[0])

def compare_fotball(match1=Match, match2=Match):

	high_odds = match1.high_odds
	low_odds = match2.low_odds_found

	match1_share = float(high_odds) / ( float(high_odds) + float(low_odds) )
	match2_share = 1 - float(match1_share)
	profit = float(low_odds) * float(match1_share)

	if(profit > 0):
		print()
		print("Match: " + str(match1.match_name) + " | " + str(match2.match_name))
		print("Fördelning: " + str(match1_share) + " @ " + match1.website + " | Över 2.5 mål: " + str(high_odds) )
		print("Fördelning: " + str(match2_share) + " @ " + match2.website + " | Under 2.5 mål: " + str(low_odds) )
		print("Retur: " + str(profit) + "%")


	low_odds = match1.low_odds
	high_odds = match2.high_odds

	match1_share = float(high_odds) / ( float(high_odds) + float(low_odds) )
	match2_share = 1 - float(match1_share)

	profit = float(low_odds) * float(match1_share)

	if(profit > 0):
		print("=====================================================================")
		print("Match: " + str(match1.match_name) + " | " + str(match2.match_name))
		print("Fördelning: " + str(match1_share) + " @ " + str(match1.website) + " | Under 2.5 mål: " + str(low_odds) )
		print("Fördelning: " + str(match2_share) + " @ " + str(match2.website) + " | Över 2.5 mål: " + str(high_odds) )
		print("Retur: " + str(profit) + "%")
		print()


def main():

	print()
	print(BANNER)
	print()

	match_list_betway = []
	match_betting_list_betway = []

	r = requests.post(BETWAY_URL, data=json.dumps(BETWAY_PAYLOAD), headers=BETWAY_HEADERS)
	for element in r.json()['Events']:
		match_id = element['Id']
		match_name = element['EventName']
		match_group_name = element['GroupName']
		match_time = element['Time']
		match_date = element['Date']

		#print()
		#print("Match ID: ", match_id)
		#print("Grupp: ", match_group_name)
		#print("Match: ", match_name)
		#print("Tid: ", match_time)
		#print("Datum: ", match_date)

		match = Match(match_id, match_name, match_date, match_time, "Betway")
		match_list_betway.append(match)


	# Find all odds for betway matches
	for element in r.json()['Outcomes']:
		match_id = element['EventId']
		betting_option = element['BetName']
		betting_odds = element['OddsDecimal']

		betting_option = BettingOption(match_id, betting_option, betting_odds)
		match_betting_list_betway.append(betting_option)

	# Connect matches with betting odds
	for match in match_list_betway:
		for betting_option in match_betting_list_betway:
			if str(match.match_id) in str(betting_option.match_id):
				match.betting_options_list.append(betting_option)


	# Display all located odds and matches
	for match in match_list_betway:
		print("Match: ", match.match_name)
		print("Datum: ", match.match_date)
		print("Tid: ", match.match_time)
		for betting_option in match.betting_options_list:
			print("===================================")
			print("Betting option: ", betting_option.option)
			print("Betting odds: ", betting_option.odds)
		print()









	match_list_nordicbet = []
	match_betting_list_nordicbet = []

	r = requests.get(NORDICBET_URL, headers=NORDICBET_HEADERS)

	# Grab all matches and find id and additional information
	for element in r.json()['data']['events']:
		match_id = element['id']
		match_category = element['categoryName']
		match_name = element['label']
		match_date = element['startDate']
		match_time = 0
		
		match = Match(match_id, match_name, match_date, match_time, "Nordicbet")
		match_list_nordicbet.append(match)

		#print(match_id)
		#print(match_category)
		#print(match_name)
		#print(match_time)
		#print()

	# Locate all the odds of the match and save it in list
	for element in r.json()['data']['selections']:
		match_id = element['id']
		match_odds = element['odds']
		match_betting_option = element['alternateLabel']

		betting_option = BettingOption(match_id, match_betting_option, match_odds)
		match_betting_list_nordicbet.append(betting_option)


	# Connect the correct matches with correct odds
	for match in match_list_nordicbet:
		for betting_option in match_betting_list_nordicbet:
			if match.match_id in betting_option.match_id:
				match.betting_options_list.append(betting_option)


	# Display all matches and odds
	for match in match_list_nordicbet:
		print("===================================")
		print("Match: ", match.match_name)
		print("Datum: ", match.match_date)
		print("Tid: ", match.match_time)
		for betting_option in match.betting_options_list:
			print("----------------------------------------")
			print("Betting option: ", betting_option.option)
			print("Betting odds: ", betting_option.odds)
		print("==================================")
		print()







	compareable_matches_list = []
	DETECTION_TRESHHOLD = 0.7

	# Check which matches names matches over DETECTION_TRESHHOLD
	for match_betway in match_list_betway:
		for match_nordicbet in match_list_nordicbet:

			match_betway_flipped = flip_string_by_minus(match_betway.match_name)
			match_nordicbet_flipped = flip_string_by_minus(match_nordicbet.match_name)

			if (
			similar( match_nordicbet.match_name, match_betway.match_name ) > DETECTION_TRESHHOLD or
			similar( match_nordicbet.match_name, match_betway_flipped) > DETECTION_TRESHHOLD or
			similar( match_nordicbet_flipped, match_betway_flipped) > DETECTION_TRESHHOLD or
			similar( match_nordicbet_flipped, match_betway.match_name) > DETECTION_TRESHHOLD
			):
				compareable_matches_list.append([match_betway, match_nordicbet])
				print("Match hittad för jämförelse: ", match_betway.match_name, "|", match_nordicbet.match_name)


	print()

	for match_pair in compareable_matches_list:

		match_betway = match_pair[0]
		match_nordicbet = match_pair[1] 

		#print("Match: ", match_betway.match_name, "|", match_nordicbet.match_name)
		#print("Tid: ", match_betway.match_time)
		#print("Datum: ", match_betway.match_date)

		#print("- - - - - - - - - - - - - - - - - - - - - -")
		#print("Betway: ", match_betway.betting_options_list[0].option, ":", match_betway.betting_options_list[0].odds )
		#print("Betway: ", match_betway.betting_options_list[1].option, ":", match_betway.betting_options_list[1].odds )
		#print("- - - - - - - - - - - - - - - - - - - - - -")

		for betting_option_nordicbet in match_nordicbet.betting_options_list:
			for betting_option_betway in match_betway.betting_options_list:
				if betting_option_nordicbet.option == betting_option_betway.option:
					print("Betting option found")
					print("Nordicbet: ", betting_option_nordicbet.option, " | ", betting_option_nordicbet.odds)
					print("Betway: ", betting_option_betway.option, " | ", betting_option_betway.odds)


		#compare_fotball(match_betway, match_nordicbet)




if __name__ == '__main__':
	main()















