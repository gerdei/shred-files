# -*- coding: UTF-8 -*-
 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from time import sleep # having problems with Selenium waits, using time.sleep as a workaround
import multiprocessing, os

cookie_message_en = 'This website uses cookies for analytics, personalization and advertising'
cookie_message_ru = 'Этот сайт использует куки для аналитики, персонализации и рекламы.'

def init_browser():
        drv = webdriver.Firefox()
        drv.get('http://community-z.com/communities')
        sleep(3)
        return drv

def TC_cookies_01(quit_on_exit=True):
        drv = init_browser()
        try:
                # check alert message
                alert = drv.find_element_by_class_name('cookie-alert')
                assert cookie_message_en in alert.text
                drv.save_screenshot(os.getcwd()+'\\TC_cookies_01_alert_message.png')

                #check "Accept" button, and by clicking it, the message disappears
                accept_button = alert.find_element_by_class_name('evnt-button')
                assert 'Accept' == accept_button.text
                accept_button.click()
                sleep(3)
                assert not drv.find_elements_by_class_name('cookie-alert')
                drv.save_screenshot(os.getcwd()+'\\TC_cookies_01_after_accepting.png')
                print('TC_cookies_01_Status: PASSED')
        except Exception as e:
                print(e)
                print('TC_cookies_01_Status: FAILED')        
        finally:
                if quit_on_exit:
                        drv.quit()

def TC_cookies_02(quit_on_exit=True):
        drv = init_browser()
        try:
                alert = drv.find_element_by_class_name('cookie-alert')
                alert.find_element_by_class_name('evnt-button').click()
                drv.get('http://www.google.com')
                drv.get('http://community-z.com/communities')
                assert not drv.find_elements_by_class_name('cookie-alert')
                drv.save_screenshot(os.getcwd()+'\\TC_cookies_02_after_revisting.png')
                print('TC_cookies_02_Status: PASSED')
        except Exception as e:
                print(e)
                print('TC_cookies_02_Status: FAILED')        
        finally:
                if quit_on_exit:
                        drv.quit()

def TC_cookies_03(quit_on_exit=True,td='Русский'):
        drv = init_browser()
        try:
                # check alert message 
                alert = drv.find_element_by_class_name('cookie-alert')
                assert cookie_message_en in alert.text
                #change language
                lang_menu = drv.find_element_by_id('languageDropdown')
                lang_menu.click()
                sleep(3)
                ru = drv.find_element_by_xpath("//*[text()={}]".format(td))
                ru.click()
                sleep(3)
                rualert = drv.find_element_by_class_name('cookie-alert')
                assert cookie_message_ru in rualert.text
                drv.save_screenshot(os.getcwd()+'\\TC_cookies_03_ru_alert_message.png')
                print('TC_cookies_03_Status: PASSED')
        except Exception as e:
                print(e)
                print('TC_cookies_03_Status: FAILED')        
        finally:
                if quit_on_exit:
                        drv.quit()

def TC_search_01(quit_on_exit=True, td='Budapest'):
        drv = init_browser()
        try:                
                # find search field and enter test data
                search_field = drv.find_element_by_xpath("//input[@placeholder='Search by Title or Tags']")
                drv.save_screenshot(os.getcwd()+'\\TC_search_01_before_search.png')
                search_field.send_keys(td)
                sleep(4)
                drv.save_screenshot(os.getcwd()+'\\TC_search_01_after_search.png')
                # get communities, check that their text contain the test data
                comms = drv.find_elements_by_class_name('evnt-card-body')
                td_comms = len(list(filter(lambda t: td.lower() in t.lower(),[e.text for e in comms])))
                visible_comms = len((comms))
                assert td_comms == visible_comms
                # check url in adress bar
                assert drv.current_url == 'https://community-z.com/communities?f%5B0%5D%5Bsearch%5D=Budapest'
                print('TC_search_01_Status: PASSED')
        except Exception as e:
                print(e)
                print('TC_search_01_Status: FAILED')        
        finally:
                if quit_on_exit:
                        drv.quit()

def TC_search_02(quit_on_exit=True, td='Budapest'):
        drv = init_browser()
        try:                
                # find search field, click it, hit return
                search_field = drv.find_element_by_xpath("//input[@placeholder='Search by Title or Tags']")
                old_comms = drv.find_elements_by_class_name('evnt-card-body')
                search_field.click()
                sleep(2)
                search_field.send_keys(Keys.RETURN)
                sleep(4)
                new_comms = drv.find_elements_by_class_name('evnt-card-body')
                assert old_comms == new_comms
                print('TC_search_02_Status: PASSED')
        except Exception as e:
                print(e)
                print('TC_search_02_Status: FAILED')        
        finally:
                if quit_on_exit:
                        drv.quit()

def TC_search_03(quit_on_exit=True, td={'':'564', 'h': '349', 'u': '5', 'm': '1', 'a': '1', 'n': '1', 's': '0'}):
        drv = init_browser()
        try:
                # switch on "Online" to see number of results
                drv.find_element_by_class_name('evnt-toggle-filters-button').click()
                sleep(1)
                drv.find_element_by_class_name('evnt-filter-switch').click()
                sleep(1)
                numresults_label = drv.find_element_by_class_name('evnt-results-cell')
                print(numresults_label.text)
                search_field = drv.find_element_by_xpath("//input[@placeholder='Search by Title or Tags']")
                for c in td.keys():
                        search_field.send_keys(c)
                        sleep(2)
                        drv.save_screenshot(os.getcwd()+f'\\TC_search_03_{c}.png')
                        assert numresults_label.text.split()[0] == td[c]
                print('TC_search_03_Status: PASSED')
        except Exception as e:
                print(e)
                print('TC_search_03_Status: FAILED')        
        finally:
                if quit_on_exit:
                        drv.quit()

# under construction
def TC_loc_01(quit_on_exit=True):
        drv = init_browser()
        try:                
                # find location filter, expand China, select Shenzen
                loc_filter = drv.find_element_by_id('filter_location')
                china_filter = drv.find_element_by_xpath("div[@href='#collapse_filter_location_4']")
                shenzen_filter = drv.find_element_by_id('China_0')
                ActionChains(drv).click(loc_filter).click(china_filter).click(shenzen_filter).perform()
##                loc_filter.click()
##                sleep(1)
##                drv.find_element_by_id('filter_location_4').click()
##                sleep(1)
##                drv.find_element_by_id('China_0')
                sleep(1)
                print('TC_loc_01_Status: PASSED')
        except Exception as e:
                print(e)
                print('TC_loc_01_Status: FAILED')        
        finally:
                if quit_on_exit:
                        drv.quit()

if __name__ == '__main__':
        [f() for f in [TC_cookies_01, TC_cookies_02, TC_cookies_03, TC_search_01, TC_search_02, TC_search_03]]

