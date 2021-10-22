#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from difflib import SequenceMatcher
import time
import os


###################TODO#########################
#	Made with love and stress during 2019	   #
################################################
# 	- Proxy support
#	- Additional websites
#	- Additional sports
#	- Support for SMS notification
# 	- Run script each x minutes
#	- Performance information
#	- Run it fully headless
#	- Multiple tabs / windows
################################################

BANNER = """
#####################################################
############## - - - MATCH FINDER - - - #############
#####################################################

#	Supported websites: Nordicbet, Betway
#	Supported sports: Fotball
#	In development: Icehockey
#	Created with love and stress during summer 2019
#	Version 1.6
#	Author: G/L.

#####################################################
#####################################################
#####################################################
"""


# Compare similarity in string 0 - 1 (0 - 100%)
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class FotballMatch:
	def __init__(self, website, name, time, odds_over_25_goals, odds_under_25_goals):
		self.website = website
		self.name = name
		self.time = time
		self.odds_over_25_goals = odds_over_25_goals
		self.odds_under_25_goals = odds_under_25_goals
class IcehockeyMatch:
	def __init__(self, website, name, time, odds_over_55_goal, odds_under_55_goal):
		self.website = website
		self.name = name
		self.time = time
		self.odds_over_55_goal = odds_over_55_goal
		self.odds_under_55_goal = odds_under_55_goal
class MatchManager:
	@staticmethod
	def compare_fotball(match1=FotballMatch, match2=FotballMatch):

		odds_under_25_goals = match1.odds_under_25_goals
		odds_over_25_goals = match2.odds_over_25_goals

		match1_share = float(odds_over_25_goals) / ( float(odds_over_25_goals) + float(odds_under_25_goals) )
		match2_share = 1 - float(match1_share)

		profit = float(odds_under_25_goals) * float(match1_share)

		if(profit > 0):
			print("Match: " + str(match1.name) + " | " + str(match2.name))
			print("Fördelning: " + str(match1_share) + " @ " + str(match1.website) + " | Under 2.5 mål: " + str(odds_under_25_goals) )
			print("Fördelning: " + str(match2_share) + " @ " + str(match2.website) + " | Över 2.5 mål: " + str(odds_over_25_goals) )
			print("Retur: " + str(profit) + "%")
			print("=======================================")


		odds_over_25_goals = match1.odds_over_25_goals
		odds_under_25_goals = match2.odds_under_25_goals


		match1_share = float(odds_over_25_goals) / ( float(odds_over_25_goals) + float(odds_under_25_goals) )
		match2_share = 1 - float(match1_share)

		profit = float(odds_under_25_goals) * float(match1_share)

		if(profit > 0):
			print("Match: " + str(match1.name) + " | " + str(match2.name))
			print("Fördelning: " + str(match1_share) + " @ " + str(match1.website) + " | Över 2.5 mål: " + str(odds_over_25_goals) )
			print("Fördelning: " + str(match2_share) + " @ " + str(match2.website) + " | Under 2.5 mål: " + str(odds_under_25_goals) )
			print("Retur: " + str(profit) + "%")


	@staticmethod
	def compare_icehockey(match1=IcehockeyMatch, match2=IcehockeyMatch):

		odds_under_55_goal = float(match1.odds_under_55_goal.replace("," , ".") )
		odds_over_55_goal = float(match2.odds_over_55_goal.replace("," , ".") )

		match1_share = odds_over_55_goal / (odds_over_55_goal + odds_under_55_goal)
		match2_share = 1 - match1_share

		profit = odds_under_55_goal * match1_share

		if(profit > 1):
			print("Match: " + str(match1.name) + " | " + str(match2.name) )
			print("Tid: " + str(match1.time) + " | " + str(match2.time) )
			print("Fördelning: " + str(match1_share) + " @ " + str(match1.website) + " | Under 5.5 mål: " + str(odds_under_55_goal) )
			print("Fördelning: " + str(match2_share) + " @ " + str(match2.website) + " | Över 5.5 mål: " + str(odds_over_55_goal) )
			print("Retur: " + str(profit) + "%")

		print("#############################################")

		odds_over_55_goal = float(match1.odds_over_55_goal.replace("," , ".") )
		odds_under_55_goal = float(match2.odds_under_55_goal.replace("," , ".") )

		match1_share = odds_over_55_goal / (odds_over_55_goal + odds_under_55_goal)
		match2_share = 1 - match1_share

		profit = odds_under_55_goal * match1_share

		if(profit > 1):
			print("Match: " + str(match1.name) + " | " + str(match2.name) )
			print("Tid: " + str(match1.time) + " | " + str(match2.time) )
			print("Fördelning: " + str(match1_share) + " @ " + str(match1.website) + " | Över 5.5 mål: " + str(odds_over_55_goal) )
			print("Fördelning: " + str(match2_share) + " @ " + str(match2.website) + " | Under 5.5 mål: " + str(odds_under_55_goal) )
			print("Retur: " + str(profit) + "%")

t = time

class Betway:
	def __init__(self, driver):
		self.icehockey_matches = []
		self.fotball_matches = []
		self.driver = driver
		self.TIMEOUT = 10

	def get_icehockey(self):
		URL = "https://sports.betway.se/sv/sports/sct/ice-hockey/north-america"
		self.driver.get(URL)

		try:
			element_present = EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "1X2")]'))
			WebDriverWait(self.driver, self.TIMEOUT).until(element_present)
			self.driver.find_element_by_xpath("//div[contains(text(), '1X2')]").click()
		except TimeoutException:
			print ("Timed out")

		try:
		    element_present = EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "icehockey-total-goals")]'))
		    WebDriverWait(self.driver, self.TIMEOUT).until(element_present)
		    self.driver.find_element_by_xpath("//div[contains(text(), 'icehockey-total-goals')]").click()
		except TimeoutException:
		    print ("Timed out")



		c = 0
		cc = 0
		for match in self.driver.find_elements_by_css_selector('.scoreboardInfoNames'):

			try:
				name = match.text
				time = self.driver.find_elements_by_class_name("oneLineDateTime")[c].text
				odds_over_55_goal = self.driver.find_elements_by_class_name("odds")[1 + cc].text
				odds_under_55_goal = self.driver.find_elements_by_class_name("odds")[2 + cc].text

				print(name)
				print(time)
				print(odds_over_55_goal)
				print(odds_under_55_goal)

				icehockeyMatch = IcehockeyMatch("Betway", name, time, odds_over_55_goal, odds_under_55_goal)
				self.icehockey_matches.append(icehockeyMatch)

			except Exception as exception:
				print(exception)

			c += 1
			cc += 2


	def get_fotball(self):
		URL = "https://sports.betway.se/sv/sports/cpn/soccer/376"
		self.driver.get(URL)
		self.driver.implicitly_wait(10)

		# Expand all todays fotball matches
		rows = len(self.driver.find_elements_by_css_selector("div.collapsableHeader"))
		for c in range(rows - 1, 5, -1):
			t.sleep(0.1)
			try:
				element = self.driver.find_elements_by_css_selector("div.collapsableHeader")[c]

				# Scroll to element
				self.driver.execute_script('arguments[0].scrollIntoView(true);', element)
				self.driver.execute_script("window.scrollBy(0, -450);")
				
				# Click element to make it visible
				element.click()
			except Exception as exception:
				print(exception)

		# collect match link to all matches

		matches_url_list = []
		for match_link in self.driver.find_elements_by_css_selector('.scoreboardInfoNames'):
			match_link = match_link.get_attribute("href")
			matches_url_list.append(match_link)
			print("New match found: ", match_link)

		print("[Betway] Matches found: ", len(matches_url_list) )

		# open each match url
		for match_url in matches_url_list:
			self.driver.get(match_url)

			# Find match name
			try:
				match_name = self.driver.find_elements_by_css_selector("div.titleAndIconWrapper > div.titleWidgetWrapper > div > div > h1")[0].text
			except Exception as e:
				print("Error, match name not found, continue...")

				# Continue to next match if match name not found
				continue

			# Find element "Mål" and click
			try:
				for element in self.driver.find_elements_by_css_selector("div[collectionitem='goals'"):
					print("Searching for element Mål... ", element.text)
					if element.text == "Mål":
						element.click()
						print(" --- Located element Mål, clicked it")

						# Grab all possible betting alternatives and find the correct one, add to matches if found total 2.5 goals
						try: 
							c = 1
							for betting_option in self.driver.find_elements_by_css_selector("div.collapsableHeader > div.marketTitleWrapper > div.titleText > span"):
								print(" ------ Searching for betting alternative... ", betting_option.text)
								if betting_option.text == "Totalt antal mål 2.5":
									print(" --------- Betting alternative located")

									# Find odds at total goals 2.5
									try: 
										match_time = "0"
										try:

											
											match_odds_over_25_goals = self.driver.find_elements_by_css_selector("div.marketListWidgetContainer > div > div:nth-child(" + str(c) + ") > div.collapsableContent > div > div.outcomeEntryCollection > div > div.outcomeItemCollection > div:nth-child(1) > div.outcomeItemContainer.baseOutcomeItem > div > div.oddsDisplay > div")[0].text
											match_odds_under_25_goals = self.driver.find_elements_by_css_selector("div.marketListWidgetContainer > div > div:nth-child(" + str(c) + ") > div.collapsableContent > div > div.outcomeEntryCollection > div > div.outcomeItemCollection > div:nth-child(2) > div.outcomeItemContainer.baseOutcomeItem > div > div.oddsDisplay > div")[0].text
										except Exception as e:
											print(e)
											continue

										# Replace "," with "."
										match_odds_over_25_goals = match_odds_over_25_goals.replace(",", ".")
										match_odds_under_25_goals = match_odds_under_25_goals.replace(",", ".")

										print()
										print("###############################################################")
										print("#################### - - - BETWAY - - - #######################")
										print("#################### Match: ", match_name)
										print("#################### Tid: ", match_time)
										print("#################### Odds över 2.5 mål: ", match_odds_over_25_goals)
										print("#################### Odds under 2.5 mål: ", match_odds_under_25_goals)
										print("###############################################################")
										print()

										fotballMatch = FotballMatch("Betway", match_name, match_time, match_odds_over_25_goals, match_odds_under_25_goals)
										self.fotball_matches.append(fotballMatch)

									except Exception as e:
										print (e.message, e.args)
								c += 1

						except Exception as e:
							print (e.message, e.args)
			
			except Exception as e:
				print(e.message, e.args)

		print("[Betway] Valid matches added to be compared: ", len(self.fotball_matches) )


class Nordicbet:
	def __init__(self, driver):
		self.icehockey_matches = []
		self.fotball_matches = []
		self.driver = driver
		self.TIMEOUT = 10

	def get_icehockey(self):
		
		self.driver.get("https://www-beta.nordicbet.com/sv/odds/ishockey/nhl")
		self.driver.implicitly_wait(10)

		match_links_list = []


		name = self.driver.find_elements_by_css_selector("div.obg-event-info-participant-label")[1].text
		name += " - "
		name += self.driver.find_elements_by_css_selector("div.obg-event-info-participant-label")[0].text


		for match in self.driver.find_elements_by_css_selector(".obg-event-row-details"):
			try:
				match_link = match.get_attribute("href")
				match_links_list.append(match_link)

			except Exception as exception:
				print(exception)

		for link in match_links_list:
			self.driver.get(link)	

		self.driver.implicitly_wait(10)		
		
		try:
			time = "0"
			odds_over_55_goal = self.driver.find_elements_by_css_selector(".obg-selection-content")[19].text.split("\n")[1]
			odds_under_55_goal = self.driver.find_elements_by_css_selector(".obg-selection-content")[20].text.split("\n")[1]

			print(name)
			#print(time)
			print(odds_over_55_goal)
			print(odds_under_55_goal)

			icehockeyMatch = IcehockeyMatch("Nordicbet", name, time, odds_over_55_goal, odds_under_55_goal)
			self.icehockey_matches.append(icehockeyMatch)

		except Exception as exception:
			print(exception)

	def get_fotball(self):
		URL = "https://www-beta.nordicbet.com/sv/odds/fotboll"
		self.driver.get(URL)
		self.driver.implicitly_wait(10)

		rows = len(self.driver.find_elements_by_css_selector("span.obg-events-master-detail-header-toggle"))

		for c in range(rows - 1, 0, -1):
			try:
		 		t.sleep(1.5)
		 		self.driver.find_elements_by_css_selector("span.obg-events-master-detail-header-toggle")[c].click()
			except Exception as e:
				print(e.message, e.args)

		self.driver.find_elements_by_css_selector("span.obg-events-master-detail-header-toggle")[0].click()
		t.sleep(1)

		matches_found_url_list = []
		for match_link in self.driver.find_elements_by_css_selector(".obg-event-row-details"):
			match_link = match_link.get_attribute("href")
			matches_found_url_list.append(match_link)
			print("Match found: ", match_link)

		print("[Nordicbet] Matches found: ", len(matches_found_url_list))

		for match_url in matches_found_url_list:	
			self.driver.get(match_url)
			t.sleep(1)

			# Find "Mål" element and click it
			for element in self.driver.find_elements_by_css_selector("obg-tab-label > div > span"):

				# Find match name
				match_name = self.driver.find_elements_by_css_selector("div.obg-m-event-participant")[0].text.replace("\n", " ")
				match_name = match_name.replace("–", "-")

				print("Searching for element Mål... ", element.text)
				if element.text == "Mål":
					element.click()
					print(" --- Mål element located, clicked it")

					t.sleep(0.4)

					# Search for header name = 'Antal mål' or 'Antal mål i matchen'
					for row_header in self.driver.find_elements_by_css_selector("obg-event-market-group-component:nth-child(1) > div > div:nth-child(1)"):
						print(" --- Searching for row header...: ", row_header.text)

						if (row_header.text == 'Antal mål' or 'Antal mål i matchen'):
							print(" ------ Correct row header located: ", row_header.text)

							# Search for betting option of 2.5 goals
							match_odds_over_25_goals = 0
							match_odds_under_25_goals = 0
							for row in self.driver.find_elements_by_css_selector("div.obg-selection-content"):

								t.sleep(0.35)
								try:
									print(" --------- Searching for correct betting alternative...", row.text.split("\n")[0])
								except Exception as e:
									print(e.message, e.args)

								# Check if row.text is over 2.5 goals
								if row.text.split("\n")[0] == "över 2.5" and row.text.split("\n")[1] != "-":
									print(" ------------ Betting odds 'över 2.5' located for 2.5 goals")
									try:
										match_odds_over_25_goals = float(row.text.split("\n")[1])
									except Exception as e:
										print(e.message, e.args)

								# Check if row.text is under 2.5 goals
								if row.text.split("\n")[0] == "under 2.5" and row.text.split("\n")[1] != "-":
									print(" ------------ Betting odds 'under 2.5' located for 2.5 goals")
									try:
										match_odds_under_25_goals = float(row.text.split("\n")[1])
									except Exception as e:
										print(e.message, e.args)

								# Check if odds found, if so then valid match
								if match_odds_over_25_goals > 0 and match_odds_under_25_goals > 0:

									match_time = "0"
									print()
									print("#############################################################")
									print("#################### - - - NORDICBET - - - ##################")
									print("#################### Match: ", match_name)
									print("#################### Tid: ", match_time)
									print("#################### Odds över 2.5 mål totalt: ", match_odds_over_25_goals)
									print("#################### Odds under 2.5 mål totalt: ", match_odds_under_25_goals)
									print("#############################################################")
									print()

									fotballMatch = FotballMatch("Nordicbet", match_name, match_time, match_odds_over_25_goals, match_odds_under_25_goals)
									self.fotball_matches.append(fotballMatch)

									# Break out of loop if correct odds are found
									break

							# Break out of loop if correct row_header_text are found
							break

		print("[Nordicbet] Valid matches added to be compared: ", len(self.fotball_matches) )



def flip_string_by_minus(name):
	return '{0} — {1}'.format(name.split(" - ")[1], name.split(" - ")[0])

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

def main():

	print()
	print(BANNER)
	print()

	options = Options()  
	#options.add_argument("--headless")
	#options.add_argument("--window-size=1920x1080") 

	driver = webdriver.Chrome(executable_path = DRIVER_BIN, options = options)
	driver.maximize_window()

	betway = Betway(driver)
	betway.get_fotball()
	#betway.get_icehockey()

	nordicbet = Nordicbet(driver)
	nordicbet.get_fotball()
	#nordicbet.get_icehockey()

	########################### ICEHOCKEY ############################
	# icehockey_match_list = []
	# for match_nordicbet in nordicbet.icehockey_matches:
	# 	for match_betway in betway.icehockey_matches:
	# 		if (similar(match_nordicbet.name, match_betway.name) > 0.75):
	# 			print("Match found: ", match_betway.name, " | ", match_nordicbet.name)
	# 			print()
	# 			icehockey_match_list.append([match_nordicbet, match_betway])

	# for match_pair in icehockey_match_list:
	# 	MatchManager.compare_icehockey(match_pair[0], match_pair[1])
	# 	print()
	# 	print()
	############## ////////////ICEHOCKEY ############################


	########################### FOTBALL ############################
	print()
	print("=================================================================")
	print("Matches found @ Nordicbet: ", len (nordicbet.fotball_matches) )
	print("Matches found @ Betway: ", len (betway.fotball_matches) )
	print("=================================================================")
	print()

	fotball_match_list = []
	for match_nordicbet in nordicbet.fotball_matches:
		for match_betway in betway.fotball_matches:
			try:
				flipped_match_nordicbet = flip_string_by_minus(match_nordicbet.name)
				flipped_match_betway = flip_string_by_minus(match_betway.name)

				if (
				similar( match_nordicbet.name, match_betway.name ) > 0.7 or
				similar( match_nordicbet.name, flipped_match_betway) > 0.7 or
				similar( flipped_match_nordicbet, flipped_match_betway) > 0.7 or
				similar( flipped_match_nordicbet, match_betway.name) > 0.7
				):
					print("Match found: ", match_betway.name, " | ", match_nordicbet.name)
					fotball_match_list.append([match_nordicbet, match_betway])

			except Exception as exception:
				print(exception)

	for match_pair in fotball_match_list:
		MatchManager.compare_fotball(match_pair[0], match_pair[1])
		print()
		print()
	############### ///////FOTBALL ############################

if __name__ == '__main__':
	main()







