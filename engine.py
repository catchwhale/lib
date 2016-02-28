import mechanize
import re
import subprocess
import os
import sys

import settings
import xparser

import random
import string

from sheet import *
from multiprocessing import Pool
import multiprocessing
# import multiprocessing
# import pathos.multiprocessing as mp
## git clone https://github.com/uqfoundation/pathos # Install as prerequisite

class XPLANEngine ():

    br = None
    request = None
    user = None
    userlist = None
    parser = None
    cookies = None
    xpland = {
        'income': {'attr': 'cashflow', 'link': 'Cashflow', 'field':'5'},
        'expense': {'attr': 'cashflow', 'link': 'Cashflow', 'field':'6'},
        'asset': {'attr': 'asset', 'link': 'Balance Sheet', 'field':'8'},
        'liability': {'attr': 'liability', 'link': 'Balance Sheet', 'field':'12'},
        'dependent': {'attr': 'dependent', 'link': 'Dependant', 'field':'0'}
    }
    config = None

    def __init__ (self, ** kwargs):
        # Parser settings

        username = kwargs.get ('username', '')
        password = kwargs.get ('password', '')

        # userid = kwargs.get ('userid', '')
        # config = kwargs.get ('config', '')        

        # self.br = mechanize.Browser ()
        # self.request = settings.XPLANRequest (userid=userid)

        # self.user = settings.XPLANUser (username=username,
        #                                 password=password)
        # self.id = settings.XPLANID (searchid=userid)
        # self.userlist = settings.XPLANUserList ()

        # attr = self.xpland[config]['attr']
        # self.parser = xparser.XPLANParser (attr=attr,
        #                                    config=config)
        self.username = username
        self.password = password
        # self.userid = userid
        # self.config = config


    def run (self):
        #user, pswd = parameters
        self.br = mechanize.Browser ()
        user = self.username
        pswd = self.password
        # userid = self.userid
        # config = self.config
        # Auto-login
        # self.request = settings.XPLANRequest (userid=userid)
        # print self.request
        # print self.br
        self.request = settings.XPLAN_init ()
        self.userlist = settings.XPLANUserList ()
        self.br.set_handle_robots (False)
        self.br.set_handle_refresh (False)

        agent = self.request.get_agent ()
        # print agent
        self.br.addheaders = [('User-agent', agent)]

        # New session
        url = self.request.get_url ('home')
        # print url
        self.br.open (url)

        self.br.select_form (nr=0)
        self.br['userid'] = user
        self.br['passwd'] = pswd

        self.br.submit ()

        # Save Cookies
        cookiejar = self.br._ua_handlers['_cookies'].cookiejar
        self.cookies = str(cookiejar).split(" ")[1]
        self.userlist.add (user=user,
                           cookies=self.cookies)
        # print self.cookies
        # return self.br
        # return self.fetch ()

    def fetch (self, key, userid):
        attr = self.xpland[key]['attr']
        self.parser = xparser.XPLANParser (attr=attr,
                                           config=key)
        # View factfind URL
        self.request_ = settings.XPLANRequest (userid=userid)
        try:
            url = self.request_.get_url_ ('view')
            r = self.br.open (url)

            # Click link
            link = self.xpland [key]['link']
            # try:
            response = self.br.follow_link (text_regex=re.compile (link))

            url = response.geturl ()

            # Get Contents
            contents = self.br.open (url)
            self.parser.feed (contents.read ())

            # Get urllist
            urllist = self.parser.get_urllist ()
            self.request = settings.XPLAN_init ()
            # print urllist
            for url in urllist:

                elem = url.split ('&')

                idx = len (elem)
                field = elem [idx - 1].split ('=') [1]

                char_set = string.ascii_uppercase + string.digits
                filename = ''.join(random.sample(char_set*20, 20))

                if field == self.xpland [key]['field']:
                    p = subprocess.Popen (['curl', 'https://xplan.mlc.com.au' + url,
                                               '-H', 'Accept-Encoding: ' + self.request.get_encoding (),
                                               '-H', 'Accept-Language: ' + self.request.get_language (),
                                               '-H', 'Upgrade-Insecure-Requests: 1',
                                               '-H', 'User-Agent: ' + self.request.get_agent (),
                                               '-H', 'Accept: ' + self.request.get_acformat (),
                                               '-H', 'Referer: ' + self.request_.get_url_ (key),
                    #                            '-H', 'Referer: ' + self.request.get_url (key),
                                               '-H', 'Cookie: ' + self.cookies,
                                               '-H', 'Connection: keep-alive',
                                               '-H', 'Cache-Control: max-age=0',
                                               '-H', 'Host: ' + self.request.get_host (),
                                               '--compressed',
                                               '-o', filename],
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                    out, err = p.communicate ()
                    try:
                        p.kill ()
                    except OSError:
                        pass
                    contents = open (filename)
                    self.parser.feed (contents.read ())
                    contents.close ()
                    if os.path.isfile (filename):
                        os.remove (filename)
            # # return self.parser.get_data ()
            data = self.parser.get_data ()
            if data:
                data = data.values()
                # print data
                # jobs = [('test2.json', attr) for attr in data]
                # print jobs
                # count = multiprocessing.cpu_count()
                # P = Pool(processes=count)
                # # parameter = filename, attribute
                # P.map(update_json2, job)
                # # print data.values
                for i in data:
                    update_json('test2.json', i)
                print data
        except:
            pass
    def go(self, list_):

        # count = multiprocessing.cpu_count()
        P = Pool(processes=8)
        # P.map(self.fetch, jobs)
        print pool.map(self.fetch, list_)
        
  #       print self.parser.get_data ()

    def write (self, entries):
        key = "1M3qsO6IkPoVFBHYkqVgDlC18KQmeP9RaU3TbGuFEqk0"
        sheet = access_sheet(key)

        for i in range(0, len(entries)):
            update_sheet ([sheet, entries[i]])

    # def logout(self, parameters):
    #     len_, end = parameters
    #     if len_ == end:
    #     # print 'hello', len_
    #         url = self.request.get_url ('logout')
    #         self.br.open (url)
    def logout(self):
        # len_, end = parameters
        # if len_ == end:
        # print 'hello', len_
        url = self.request.get_url ('logout')
        # print url
        self.br.open (url)


# XPLAN Parser Engine
# 1/17/2016 PST

# XPLAN Engine Config:

# expense
# asset
# liability
# dependent
# income

# [Test]
# Result - config - user ids
# Passed -   ALL  - 3417039
# Passed -   ALL  - 6287813
# Passed -   ALL  - 6432137
# Passed -   ALL  - 6702033
# Passed -   ALL  - 6689208

