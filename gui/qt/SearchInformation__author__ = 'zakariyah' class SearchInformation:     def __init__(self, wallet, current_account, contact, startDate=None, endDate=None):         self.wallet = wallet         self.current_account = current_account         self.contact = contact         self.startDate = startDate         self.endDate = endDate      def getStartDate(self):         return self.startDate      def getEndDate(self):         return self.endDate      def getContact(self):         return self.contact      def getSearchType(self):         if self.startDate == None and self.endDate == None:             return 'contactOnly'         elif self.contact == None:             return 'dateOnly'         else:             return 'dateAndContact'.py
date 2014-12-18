__author__ = 'zakariyah'
class SearchInformation:
    def __init__(self, wallet, current_account, contact, startDate=None, endDate=None):
        self.wallet = wallet
        self.current_account = current_account
        self.contact = contact
        self.startDate = startDate
        self.endDate = endDate

    def getStartDate(self):
        return self.startDate

    def getEndDate(self):
        return self.endDate

    def getContact(self):
        return self.contact

    def getSearchType(self):
        if self.startDate == None and self.endDate == None:
            return 'contactOnly'
        elif self.contact == None:
            return 'dateOnly'
        else:
            return 'dateAndContact'
