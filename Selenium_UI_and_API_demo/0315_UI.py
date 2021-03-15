# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep
import os


class Homepage:
	def __init__(self, driver):
		self.driver = driver
		
		#locator for top menu items
		self.top_menu_locs = "//ul[@id='prime_nav']/li"

		# locators for login		
		self.login_button_loc = self.top_menu_locs + "[last()-2]"
		self.user_name_loc = self.login_button_loc + "//input[@id='username-login']"
		self.password_loc = self.login_button_loc + "//input[@id='psw']"
		self.remember_loc = self.login_button_loc + "//input[@type='checkbox']"
		self.submit_button_loc = self.login_button_loc + "//button[@class='btn-sumit']"
		self.login_wait_loc = self.login_button_loc + "//div[@class='waiting-container']"
		self.login_error_loc = self.login_button_loc + "//div[@id='form_error_login']"

		# locators for signup
		self.signup_button_loc = self.top_menu_locs + "[last()-1]"
		self.signup_email_loc = self.signup_button_loc + "//input[@name='email']"
		self.signup_country_loc = self.signup_button_loc + "//select[@name='country']"
		self.su_submit_button_loc = self.signup_button_loc + "//button[@class='btn-sumit']"

		# locators for search
		self.search_button_loc = self.top_menu_locs + "[last()]"
		self.search_field_loc = self.search_button_loc+"//input"

		
	def search(self, search_text, search_for_empty_string = False, submit = False):
		print('Clicking on search button in upper right corner.')
		self.driver.find_element(By.XPATH, self.search_button_loc).click(); sleep(1)
		if search_text or search_for_empty_string == True:
			query = search_text+Keys.RETURN if submit else search_text
			print(f'Searching for "{search_text}" in upper menu search bar')
			self.driver.find_element(By.XPATH, self.search_field_loc).send_keys(query)
		else:
		 	print('Search text is empty, please enter a valid string or set the "search_for_empty_string" flag to "True"')
		 

	def login(self, usr, pwd, remember = False, submit = True):
		if self.driver.find_element(By.XPATH, self.user_name_loc).is_displayed() == False:
			print('Clicking on login button in top menu')
			self.driver.find_element(By.XPATH, self.login_button_loc).click(); sleep(1)
		print(f'Entering "{usr}" in username field')
		self.driver.find_element(By.XPATH, self.user_name_loc).clear(); sleep(1)
		self.driver.find_element(By.XPATH, self.user_name_loc).send_keys(usr); sleep(1)
		print(f'Entering "{pwd}" in password field')
		self.driver.find_element(By.XPATH, self.password_loc).clear(); sleep(1)
		self.driver.find_element(By.XPATH, self.password_loc).send_keys(pwd); sleep(1)
		rem = self.driver.find_element(By.XPATH, self.remember_loc)
		if rem.is_selected() ^ remember: rem.click(); sleep(1)# XOR
		if submit:
			print(f'Submitting login form with the following credentials: ({usr}, {pwd})')
			self.driver.find_element(By.XPATH, self.submit_button_loc).click(); sleep(1)
			washing_machine = self.driver.find_element(By.XPATH, self.login_wait_loc)
			while washing_machine.is_displayed():
				sleep(1)
			if self.is_login_error_msg_displayed(): print(self.driver.find_element(By.XPATH, self.login_error_loc).text)

	def is_login_error_msg_displayed(self):
		return self.driver.find_element(By.XPATH, self.login_error_loc).is_displayed()

	def sign_up(self, mail, country, submit = False):
		print('Clicking on sign-up button in top menu')
		self.driver.find_element(By.XPATH, self.signup_button_loc).click(); sleep(1)
		print(f'Entering "{mail}" in e-mail field')
		self.driver.find_element(By.XPATH, self.signup_email_loc).send_keys(mail); sleep(1)
		print(f'Selecting "{country}" in country selector')
		try:
			Select(self.driver.find_element(By.XPATH, self.signup_country_loc)).select_by_visible_text(country); sleep(1)
		except Exception as e:
			print(e)				
		if submit:
			print(f'Submitting sign-up form with the following credentials: ({mail}, {country})')
			self.driver.find_element(By.XPATH, self.signup_button_loc).click()


	def hover_to(self, pat):
		menu = self.driver.find_elements(By.XPATH, self.top_menu_locs)
		menu_path = pat.split('/')
		try:
			for tile in menu_path:
				print(f'Moving mouse over menu/submenu "{tile}"')
				menu_element = next(filter(lambda e: e.text.lower() == tile, menu), None)
				if tile != menu_path[0]: ActionChains(self.driver).move_to_element(menu[0]).perform() # see Note 2.
				ActionChains(self.driver).move_to_element(menu_element).perform(); sleep(1)
				menu = menu_element.find_elements(By.XPATH, "ul/li")
			return menu_element
		except Exception as e:
			print(f'Could not find menu/submenu with text: {tile}')
			print('Available options are: '+','.join([elem.text.lower() for elem in menu])) if menu else print('No options are available')

	def click_on_menu_item(self, pat):
		print(f'Clicking on element "{pat}"')
		self.hover_to(pat).click()


if __name__ == '__main__':
	def test_user_story_7(current_browser):
		'''
		This test automates user story no. 7:
			- user hovers over items in the top menu (covering: T[est]C[ase]_menu_id123, ...)
			- user attempts a login with invalid credentials (covering: TC_login_id456, TC_login_id789, ...)
			- user enters text in the search bar (covering TC_search_id002)
			- user navigates to a certain menu item and clicks on it (covering TC_menu_id027)
			- user initiates a sign-up event (covering TC_signup_id014)

		The test also saves screenshots in the working directory to get some visual evidence if needed in the future.
		'''
		try:
			drv = current_browser
			drv.get('https://www.marketsight.com/')
		
			hp = Homepage(drv)
		
			print('\nThe user hovers through the menu items in the top menu.')
			for menu_item in ['platform', 'pricing', 'services', 'solutions', 'resources', 'about us']:
				hp.hover_to(menu_item)
				drv.save_screenshot(os.getcwd()+'\\story7_menu_{}.png'.format(menu_item.replace(' ','_')))
		
			print('\nThe user tries to log in with invalid credentials.')
			hp.login('letmein@acme.com','1234')
			drv.save_screenshot(os.getcwd()+'\\story7_failed_login.png')
	
			assert hp.is_login_error_msg_displayed()
		
			print('\nThe user enters "SPSS" in the search bar.')
			hp.search('SPSS')
			drv.save_screenshot(os.getcwd()+'\\story7_text_ins_searchbar.png')
	
			print('\nThe user navigates to the "solutions/by data platform/spss" menu item and clicks on it.')
			hp.click_on_menu_item('solutions/by data platform/spss')
			drv.save_screenshot(os.getcwd()+'\\story7_to_SPSS.png')
	
			print('\nThe users initiates a sign-up. (without submitting the form)')
			hp.sign_up('z.sesum@sfry.yu','Yugoslavia')	# I think Yugoslavia doesn't exists as a country anymore
			drv.save_screenshot(os.getcwd()+'\\story7_signup_init.png')
			sleep(3)
		except Exception as e:
			print(e)
		finally:
			drv.quit()


	def test_tc_acclock_id001(current_browser):
		''' Covering test case tc_acclock_id001: Login error message is changed to "Warning: account lockout after 2 more unsuccessful login attempt." after a single failed login attempts with the same user.
		'''
		try:
			drv = current_browser
			drv.get('https://www.marketsight.com/')
		
			hp = Homepage(drv)
			for i in range(1,4):
				hp.login('nosuchuser123',str(i))				
				drv.save_screenshot(os.getcwd()+'\\tc_acclockid001_attempt{}.png'.format(i))
			assert drv.find_element(By.XPATH, hp.login_error_loc).text == "Warning: account lockout after 1 more unsuccessful login attempt."
		except Exception as e:
			print(e)
		finally:
			drv.quit()

	current_browser = webdriver.Firefox() # additional browsers should be used for testing, for cross browser validation
	test_user_story_7(current_browser)
	print('\n',40*'-=','\n')
	current_browser = webdriver.Firefox()
	test_tc_acclock_id001(current_browser)

#Notes:
#1. For some reason the search function is not working when the script is run from the terminal (or SublimeText3), hitting the return key redirects generates an SSL certificate error, I could not solve the problem (using profile or desired capabilities excepting insecure CERTs), however the script is working as expected when run from Python IDLE. Behaviour needs clarification and further testing
#
#2. In the hover_to method it is necesarry to move to the first element of the submenu (to the right), because moving directly to the target element (presumably) moves the mouse in a straight path, causing the menu structure to collapse if this path intersects another menu element.