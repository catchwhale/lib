import os.path

class XPLANRequest ():

    url_ = {
            # 'home': 'https://xplan.mlc.com.au/home',
            # 'view': '',
            'dashboard': '',
            'cashflow': '',
            'dependent': '',
            'balancesheet': ''
    }

    # host = 'xplan.mlc.com.au'
    # agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    # acformat = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    # encoding = 'gzip, deflate, sdch'
    # language = 'en-US,en;q=0.8'

    def __init__ (self, ** kwargs):
        userid = kwargs.get ('userid', '')
        self.url_ ['logout'] = 'https://xplan.mlc.com.au/home/logoff?'
        self.url_ ['view'] = 'https://xplan.mlc.com.au/factfind/view/%s?role=client&refresh=1' % (userid)
        self.url_ ['dashboard'] = 'https://xplan.mlc.com.au/dashboard/mainhtml'
        self.url_ ['income'] = 'https://xplan.mlc.com.au/factfind/view/%s?role=client&page=cashflow' % (userid)
        self.url_ ['expense'] = 'https://xplan.mlc.com.au/factfind/view/%s?role=client&page=cashflow' % (userid)
        self.url_ ['dependent'] = 'https://xplan.mlc.com.au/factfind/view/%s?role=client&page=dependent' % (userid)
        self.url_ ['asset'] = 'https://xplan.mlc.com.au/factfind/view/%s?role=client&page=balancesheet' % (userid)
        # self.url_ ['liability'] = 'https://xplan.mlc.com.au/factfind/view/%s?role=client&page=balancesheet' % (userid)
        self.url_ ['liability'] = 'https://xplan.mlc.com.au/portfolio/position?entityid=%s' % (userid)
    def get_url_ (self, key):
        return self.url_ [key]

    # def get_host (self):
    #     return self.host

    # def get_agent (self):
    #     return self.agent

    # def get_acformat (self):
    #     return self.acformat

    # def get_encoding (self):
    #     return self.encoding

    # def get_language (self):
    #     return self.language
class XPLAN_init ():
    url = {
            'home': 'https://xplan.mlc.com.au/home',
            'view': ''
        }
    host = 'xplan.mlc.com.au'
    agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    acformat = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    encoding = 'gzip, deflate, sdch'
    language = 'en-US,en;q=0.8'

    def __init__(self):
        self.url ['logout'] = 'https://xplan.mlc.com.au/home/logoff?'

    def get_url (self, key):
        return self.url [key]

    def get_host (self):
        return self.host

    def get_agent (self):
        return self.agent

    def get_acformat (self):
        return self.acformat

    def get_encoding (self):
        return self.encoding

    def get_language (self):
        return self.language
class XPLANUser ():

    username = ''
    password = ''
    # searchid = ''

    def __init__ (self, ** kwargs):
        # self.searchid = kwargs.get ('searchid', '')
        self.username = kwargs.get ('username', '')
        self.password = kwargs.get ('password', '')

    def get_username (self):
        return self.username

    def get_password (self):
        return self.password

    # def get_userid (self):
    #     return self.searchid
class XPLANID ():
    searchid = ''

    def __init__ (self, ** kwargs):
        self.searchid = kwargs.get ('searchid', '')
    def get_userid (self):
        return self.searchid

class XPLANUserList ():

    userlist = {}

    def __init__ (self):
        if os.path.isfile ('cookies') == True:
            with open ('cookies') as f:
                lines = f.readlines()
                for line in lines:
                    user = line.split (',')[0]
                    cookies = line.split (',')[1]
                    self.userlist [user] = {}
                    self.userlist [user]['cookies'] = cookies

    def add (self, ** kwargs):
        user = kwargs.get ('user', '')
        cookies = kwargs.get ('cookies', '')

        self.userlist[user] = cookies
        dat = open ('cookies', 'a')
        dat.write ('%s,%s' % (user, cookies))
        dat.close ()

    def search (self, user):
        if self.userlist[user] != None:
            return self.userlist[user]['cookies']
        return None