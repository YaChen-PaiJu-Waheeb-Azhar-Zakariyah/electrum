__author__ = 'zshoroye'
import math
class Search:
    def __init__(self, searchInformation):
        self.searchInformation = searchInformation

    def getInformation(self):
        searchType = self.searchInformation.getSearchType()
        if searchType == 'dateOnly':
            return self.getInformationByDateOnly()
        elif searchType == 'contactOnly':
            return self.getInformationByContactNameOnly()
        elif searchType == 'dateAndContact':
            return self.getInformationByDateAndContact()
        else:
            return None

    def addressIsKnownValue(self, itemB, item):
        itemA = math.fabs(item[3] - item[4])
        if itemA == itemB:
            return True
        return False

    def getInformationByDateAndContact(self):
        startDate = self.searchInformation.getStartDate()
        endDate = self.searchInformation.getEndDate()
        contact = self.searchInformation.getContact()
        contactId = self.getContactIdFromContact(contact)
        allInformation = self.getAllInformationFromTheData(contactId, startDate, endDate)
        # informationContatiningContacts = self.getInformationContainingContact(allInformation, contactId)
        return allInformation

    def getInformationByContactNameOnly(self):
        contact = self.searchInformation.getContact()
        contactId = self.getContactIdFromContact(contact)
        allInformation = self.getAllInformationFromTheData(contactId)
        return allInformation

    def getInformationByDateOnly(self):
        startDate = self.searchInformation.getStartDate()
        endDate = self.searchInformation.getEndDate()
        # allInformation = self.getAllInformationFromTheData(startDate, endDate)
        # return allInformation

    def getContactIdFromContact(self, contact):
        contactId = None
        addr = contact
        if addr in self.searchInformation.wallet.addressbook:
            contactId = addr

        return contactId

    def getAllInformationFromTheData(self,contactId, startDate=None, endDate=None):
        tx_hashes = []
        for item in self.searchInformation.wallet.get_tx_history(self.searchInformation.current_account):
            tx_hash, conf, is_mine, value, fee, balance, timestamp = item
            transactions = self.searchInformation.wallet.transactions.get(tx_hash).outputs
            for strAddress, address, itemB in transactions:
                if address == contactId and self.addressIsKnownValue(itemB, item):
                    tx_hashes.append(item)
                    break
        return tx_hashes
