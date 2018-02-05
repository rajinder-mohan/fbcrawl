from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from bs4 import *
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



profile_id=4
mobile_url='https://m.facebook.com/profile.php?id='+str(profile_id)+'#!/profile.php?id='+str(profile_id)
web_url='https://facebook.com/profile.php?id='+str(profile_id)+'#!/profile.php?id='+str(profile_id)
friend_listurl='/friends?lst=100005366535835%3A'+str(profile_id)+'%3A1514178298&source_ref=pb_friends_tl'

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)


def fetch():
    html = BeautifulSoup(browser.page_source,"lxml")
    all_friends_li=html.find_all('li', {'class': 'fbProfileBrowserListItem'})
    print 'in fetch'
    for friend in all_friends_li:
        href=friend.find_all('a', href=True)
        print href
        print '\n'
        print len(href)
        print '\n'
        print href[0]
        print '\n'
        print href[1]
        print '\n'
        print dir(href[1])
        break
def pagination(length):
    script=browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(10)
    html = BeautifulSoup(browser.page_source,"lxml")
    all_friends_li=html.find_all('li', {'class': 'fbProfileBrowserListItem'})
    if (len(all_friends_li)>length):
        pagination(len(all_friends_li))

    else:
        print 'in else pagination'
        fetch()



try:
    profile_obj=browser.get(mobile_url)

    if 'login.php' in browser.current_url:
        print 'in line 33'
        browser.find_element_by_name("email").clear()
        email_field=browser.find_element_by_name('email')
        email_field.send_keys('testeresfera@gmail.com/')
        browser.find_element_by_name("pass").clear()
        pass_field=browser.find_element_by_name('pass')
        pass_field.send_keys('esfera1234')
        browser.find_element_by_id("u_0_5").click()
        time.sleep(5)
        browser.get(web_url)
        current_url=browser.current_url
        change_friendlist_url=current_url+friend_listurl
        browser.get(change_friendlist_url)
        email_login_sub=browser.find_element_by_class_name("_54k8 _52jh _56bs _56b_ _56bw _56bu")
        print email_login_sub
        browser.find_element_by_id("m_login_password").clear()
        pass_field=browser.find_element_by_id('m_login_password')
        browser.findElement(By.className("_54k8 _52jh _56bs _56b_ _56bw _56bu")).click()
        print browser.current_url

            # browser.find_element_by_class_name("_54k8 _52jh _56bs _56b_ _56bw _56bu").click()

    else:
        login_but=browser.find_element_by_id("u_0_4")
        print 'in line 58'

        try:
            login_but.click()
            browser.find_element_by_name("email").clear()
            email_field=browser.find_element_by_name('email')
            email_field.send_keys('testeresfera@gmail.com/')
            browser.find_element_by_name("pass").clear()
            pass_field=browser.find_element_by_name('pass')
            pass_field.send_keys('esfera1234')
            browser.find_element_by_id("u_0_5").click()
            time.sleep(5)
            browser.get(web_url)
            current_url=browser.current_url
            change_friendlist_url=current_url+friend_listurl
            browser.get(change_friendlist_url)
            page_source=browser.page_source
            html = BeautifulSoup(page_source,"lxml")
            all_friends_li=html.find_all('li', {'class': 'fbProfileBrowserListItem'})
            print 'called pagination'
            result=pagination(len(all_friends_li))
            print 'line 110'

        except Exception as r:
            print ' in line 79',r
            browser.find_element_by_xpath("//button[@value='Log In']").click()
            time.sleep(2)

            pass_field=browser.find_element_by_id('m_login_password')
            pass_field.send_keys('esfera1234')
            browser.find_element_by_id("u_0_6").click()
            time.sleep(5)
            browser.get(web_url)
            print 'line 118'
            current_url=browser.current_url
            change_friendlist_url=current_url+friend_listurl
            browser.get(change_friendlist_url)
            page_source=browser.page_source
            html = BeautifulSoup(page_source,"lxml")
            all_friends_li=html.find_all('li', {'class': 'fbProfileBrowserListItem'})
            print 'line 129'
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            html = BeautifulSoup(browser.page_source,"lxml")
            all_friends_li=html.find_all('li', {'class': 'fbProfileBrowserListItem'})
            result=pagination(len(all_friends_li))
            print 'called pagination'

except Exception as r:
    print 'Final Except ----',r
