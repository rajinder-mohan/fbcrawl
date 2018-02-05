# -*- coding: utf-8 -*-

							# ACTIVITY	VIEWS
# from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import *
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from models import *
from django.http import HttpResponse,FileResponse, Http404
from bs4 import BeautifulSoup
import json
from datetime import timedelta
import datetime
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db.models import Sum
from  more_itertools import unique_everseen
from operator import itemgetter

import os,random,string



proxy = {'address': '123.123.123.123:2345',
		 'username': 'johnsmith123',
		 'password': 'iliketurtles'}


capabilities = dict(DesiredCapabilities.CHROME)
capabilities['proxy'] = {'proxyType': 'MANUAL',
						 'httpProxy': proxy['address'],
						 'ftpProxy': proxy['address'],
						 'sslProxy': proxy['address'],
						 'noProxy': '',
						 'class': "org.openqa.selenium.Proxy",
						 'autodetect': False}

capabilities['proxy']['socksUsername'] = proxy['username']
capabilities['proxy']['socksPassword'] = proxy['password']




chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)






class Home(TemplateView):
	template_name = 'homepage.html'


	def scrap(self,url):

		mobile_url=url
		web_url=url
		friend_listurl='/friends?lst=100005366535835%3A4%3A1514178298&source_ref=pb_friends_tl'
		browser = webdriver.Chrome(chrome_options=chrome_options)
		profile_obj=browser.get(mobile_url)
		time.sleep(5)
		try:
			browser.execute_script("document.getElementById('u_0_c').style.display = 'none';")
		except Exception:
			pass
		try:
			try:
				login_form=browser.find_elements_by_id("login_form")
				# print "-------------------------login form found---------------------------"
				browser.find_element_by_name("email").clear()
				email_field=browser.find_element_by_name('email')
				email_field.send_keys('testeresfera@gmail.com')
				browser.find_element_by_name("pass").clear()
				pass_field=browser.find_element_by_name('pass')
				pass_field.send_keys('esfera1234')
				browser.find_element_by_xpath("//input[@type='submit' and @value='Log In']").click()
				time.sleep(5)
			except Exception as xe:
				print xe
				try:
					browser.find_element_by_id("loginbutton").click()
				except Exception as e:
					print e
					pass
				pass
			# print "-------------------------login complete-----------------------------"
			# print "-------------------------redirect to submit url---------------------"
			browser.get(web_url)
			browser.find_element_by_css_selector("._2x4v").click()
			time.sleep(5)
			while True:
				try:
					list_div = browser.find_element_by_class_name("uiMorePagerPrimary")
					list_div.click()
					time.sleep(5)
				except Exception as e:
					print e
					break
			time.sleep(5)
			#get hover links list
			# print "-------------------------Fetching list of people liked post---------"
			hover_anchors = browser.find_elements_by_xpath("//div[@class='_5j0e fsl fwb fcb']/a")
			count = 0
			# print "-------------------------Scraping starts---------------------------"
			data_dict={}
			data_dict['unknown']=0
			for anchor in hover_anchors:
				#on hover

				hover = ActionChains(browser).move_to_element(anchor)
				hover.perform()
				# print "-------------------------Mouse on element---------------------------"
				# fetch data
				try:

					time.sleep(10)

					data_in_the_bubble = browser.find_element_by_tag_name("body")

					data_in_the_bubble1 = data_in_the_bubble.get_attribute("innerHTML")

					soup = BeautifulSoup(data_in_the_bubble1, "html.parser")
					all_divs = soup.find_all("div", class_="_4o-e")
					name_div = soup.find("div", class_="ellipsis")
					print name_div.text
					# print "------------------------Process start------------------------------"
					try:
						for divs in all_divs:
							inside_divs = divs.find_all("div")
							for div in inside_divs:
								address_data = div.contents
								if len(address_data)==2:
										match_content = address_data[0]
										match_content = match_content.strip()
										if match_content=="From":
											address_anchor = div.find("a")
											address = address_anchor.text
											full_address = address.encode('utf-8')
											if full_address.find(",") is not -1:
												required_value = full_address.split(",")[-1]
											else:
												required_value = full_address
											required_value = required_value.title()

											if data_dic:
												if required_value in data_dict:
													data_dict[required_value] += 1
												else:
													data_dict[required_value] = 1
											else:
												data_dict[required_value] = 1

											break
										elif match_content=="Lives in":
											address_anchor = div.find("a")
											address = address_anchor.text
											full_address = address.encode('utf-8')
											if full_address.find(",") is not -1:
												required_value = full_address.split(",")[-1]
											else:
												required_value = full_address

											required_value = required_value.title()

											if data_dict:
												if required_value in data_dict:
													data_dict[required_value] += 1
												else:
													data_dict[required_value] = 1
											else:
												data_dict[required_value] = 1

											break
										else:
											data_dict['unknown'] +=1
					except Exception:
						data_dict['unknown'] +=1
				except Exception as e:
					print e
					pass
				#on hover out
				# print "-------------------------Moving mouse out---------------------------"
				hover.move_by_offset(-10000,-10000)
				hover.perform()
				time.sleep(5)
				count = count + 1
			print data_dict
			for i,j in data_dict.iteritems():
				j=float(j)
				total = len(hover_anchors)
				total = float(total)
				percent =  100.0 * (j/total)

				data_dict[i] = percent
			print data_dict
			browser.quit()
			return data_dict
		except Exception as e:
			print e
			browser.quit()
			return ""



	def post(self, request, *args, **kwargs):
		url=request.POST['id']
		check_str = "m.facebook.com"
		if url.find(check_str) is not -1:
			url.replace(check_str, "www.facebook.com")
		result=self.scrap(url)
		lis=[]
		for key, value in sorted(result.iteritems(), key=lambda (k,v): (v,k)):
			ii={key:value}
			lis.append(ii)
		return HttpResponse(json.dumps(lis),content_type="application/json")


	def get_context_data(self, *args, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)

		# segmentations
