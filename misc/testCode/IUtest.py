'''
Created on Sep 8, 2014

@author: George
'''
import urllib, urllib2, cookielib

username = 'gfang'
password = 'george.fang.mimi.fang.are.cool'
url = 'https://cas.iu.edu/cas/login?cassvc=ANY&casurl=https://onestart.iu.edu/my2-prd/Login.do?__p_dispatch__=login'
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'userName' : username, 'password' : password, 'uniqueID' : 'abc' })

opener.open(url, login_data)

resp = opener.open('https://onestart.iu.edu/my2-prd/portal/178--115225?__p_dispatch__=mostPopular&__cntnt_id__=107021&__p_rPortletId__=115225')
print resp.read()
