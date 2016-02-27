from HTMLParser import HTMLParser

# Parser Engine
class XPLANParser (HTMLParser):

    urllist = []
    xdata = {}
    rdata = ''
    attr = ''
    valid = False
    content = False
    row = -1
    col = -1
    rowstart = False
    config = None
    misc = False

    headers = {

        # td: 1, 2, 3
        'income': [
            'Action',
            'Type',
            'Owner',
            'Amount',
            'Freq',
            'Start Date',
            'Annual'
        ],

        # td: 1, 2, 3, 6
        'expense': [
            'Action',
            'Type',
            'Owner',
            'Amount',
            'Freq',
            'Start Date',
            'Fixed/Variable',
            'Proposed Amount'
        ],

        # td: 2, 3, 5, 6, 9, 10
        'asset': [
            'Action',
            'Account/Client Number',
            'Type',
            'Asset Type',
            'Platform Selection',
            'Description',
            'Owner Type',
            'Value Last Updated',
            'Status',
            'Current Value',
            'Capital Cost'
        ],

        # td: 2, 3, 5, 6, 7, 8
        'liability': [
            'Action',
            'Account/Client Number',
            'Type',
            'Sub-Type',
            'Institution',
            'Owner Type',
            'Values Last Updated',
            'Status',
            'Outstanding Balance',
            'Interest Rate'
        ],

        'dependent': [
            'Action',
            'Entity',
            'Title',
            'First Name',
            'Surname',
            'Relation',
            'Date of Birth',
            'Age',
            'Financial Dependant',
            'Gender',
            'Dependant Until Age'
        ]
    }

    def __init__ (self, ** kwargs):
        HTMLParser.__init__(self)
        attr = kwargs.get ('attr', '')
        config = kwargs.get ('config', '')

        if attr == '' or config == '':
            return

        self.attr = attr
        self.config = config

    def get_urllist (self):
        return self.urllist

    def get_data (self):
        return self.xdata

    def worksheet_name (self):
        if self.config == 'income':
            return 'Income'
        elif self.config == 'expense':
            return 'Expenses'
        elif self.config == 'asset':
            return 'Assets'
        elif self.config == 'liability':
            return 'Liabilities'
        elif self.config == 'dependent':
            return 'Dependants'

    def handle_starttag (self, tag, attrs):
        if tag == 'iframe':
            for attr in attrs:
                if attr [0] == 'name' and attr [1] == self.attr:
                    self.valid = True;

                if attr [0] == 'src' and self.valid == True:
                    self.urllist.append (attr [1])

        if tag == 'script' and self.content == True:
            self.misc = True

        if tag == 'span' and self.content == True:
            self.misc = True

        if tag == 'input' and self.content == True:
            self.misc = True

        if tag == 'tr':
            for attr in attrs:
                if attr [0] == 'class' and attr [1] == 'item_odd':
                    self.rowstart = True
                    self.row += 1
                    self.xdata [self.row] = {
                        'worksheet': self.worksheet_name ()
                    }
                if attr [0] == 'class' and attr [1] == 'item_even':
                    self.rowstart = True
                    self.row += 1
                    self.xdata [self.row] = {
                        'worksheet': self.worksheet_name ()
                    }

        if tag == 'td':
            for attr in attrs:
                if (
                    attr [0] == 'class' and
                    attr [1] == 'list' and
                    self.rowstart == True
                    ):
                    self.content = True
                elif (
                    attr [0] == 'class' and
                    attr [1] == 'listl' and
                    self.rowstart == True
                    ):
                    self.content = True
                elif (
                    attr [0] == 'class' and
                    attr [1] == 'listr' and
                    self.rowstart == True
                    ):
                    self.content = True

    def handle_endtag (self, tag):
        if self.content == True and tag == 'td':
            self.content = False
            self.col += 1
            header = self.headers [self.config][self.col]
            self.xdata [self.row].update({header: self.rdata.strip ()})
            self.rdata = ''

        if self.rowstart == True and tag == 'tr':
            self.rowstart = False
            self.col = -1

    def handle_data (self, data):
        if (
                self.misc == False and
                self.content == True and
                self.rowstart == True
            ):
            self.rdata += (data.strip(' \n')) + ' '
        if self.misc == True:
            self.misc = False

