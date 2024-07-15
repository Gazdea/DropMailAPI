import random
import string
from model.Entity import Connection, Domain, Session, Address, Mail
from repos.Repository import DropMail

class ServiceDropMail:
    
    def __init__(self, token):
        """
        Initializes a new instance of the ServiceDropMail class.

        Args:
            token (str): The authentication token for the DropMail API.

        Returns:
            None
        """
        client = DropMail(token)
        self.connect = Connection()
        self.connect.client = client
        self.connect.token = token
    
    def domains(self):
        """
        Retrieves domain information from the API and constructs Domain objects with id, name, introducedAt, and availableVia attributes.
        Returns a list of Domain objects.
        """
        domains_list = []
        getDomains = self.connect.client.get_domains()
        if getDomains is None:
            return None
        for domain in getDomains.get("domains"):
            domain_obj = Domain()
            domain_obj.id = domain.get("id")
            domain_obj.name = domain.get("name")
            domain_obj.introducedAt = domain.get("introducedAt")
            domain_obj.availableVia = domain.get("availableVia")
            domains_list.append(domain_obj)
        return domains_list
    
    def list_sessions(self):
        """
        Retrieves a list of sessions with their IDs and expiration dates from the API.
        """
        sessions_list = []
        getSessions = self.connect.client.list_sessions()
        if getSessions is None:
            return None
        for session in getSessions.get("sessions"):
            session_obj = Session()
            session_obj.id = session.get("id")
            session_obj.expiresAt = session.get("expiresAt")
            sessions_list.append(session_obj)
        return sessions_list
    
    def create_session(self):
        """
        Creates a new session and returns a tuple containing the session object and the first address object associated with the session.

        :return: A tuple (session, addresses) where session is an instance of the Session class and addresses is an instance of the Address class.
                 If the API call to get sessions fails, returns None.
        """
        session = Session()
        addresses = Address()
        getSession = self.connect.client.get_sessions()
        if getSession is None:
            return None
        session.id = getSession.get("introduceSession").get("id")
        session.expiresAt = getSession.get("introduceSession").get("expiresAt")
        addresses.address = getSession.get("introduceSession").get("addresses")[0].get("address")
        addresses.restoreKey = getSession.get("introduceSession").get("addresses")[0].get("restoreKey")
        return session, addresses
    
    def add_address(self, sessionID = None, domainId = None):
        """
        Adds an address to the session based on the provided session ID and domain ID.

        Args:
            self: The instance of the class.
            sessionID (optional): The session ID to add the address to.
            domainId (optional): The domain ID associated with the address.

        Returns:
            The address object if successful, None otherwise.
        """
        address = Address()
        getAddress = self.connect.client.get_address(sessionID, domainId)
        if getAddress is None:
            return None
        address.address = getAddress.get("introduceAddress").get("address")
        address.restoreKey = getAddress.get("introduceAddress").get("restoreKey")
        return address
    
    async def subscribe_mail(self, sessionID):
        """
        A function that subscribes to a mail session asynchronously.

        Args:
            self: The instance of the class.
            sessionID: The ID of the session to subscribe to.

        Returns:
            A list of Mail objects if successful, None otherwise.
        """
        mails = []
        subscribeMail = await self.connect.client.subscribe_mail(sessionID)
        if subscribeMail is None:
            return None
        for mail in subscribeMail.get("sessionMailReceived"):
            mail_obj = Mail()
            mail_obj.rawSize = mail.get("rawSize")
            mail_obj.fromAddr = mail.get("fromAddr")
            mail_obj.toAddr = mail.get("toAddr")
            mail_obj.downloadUrl = mail.get("downloadUrl")
            mail_obj.text = mail.get("text")
            mail_obj.headerSubject = mail.get("headerSubject")
            mails.append(mail_obj)
        return mails
    
    def list_mails(self, sessionID):
        """
        Retrieves a list of emails associated with a specific session.

        Args:
            self: The instance of the DropMail class.
            sessionID: The ID of the session for which emails are to be retrieved.

        Returns:
            A list of Mail objects if successful, None otherwise.
        """
        mails = []
        listMails = self.connect.client.list_mails(sessionID)
        if listMails is None:
            return None
        for mail in listMails.get("session").get("mails"):
            mail_obj = Mail()
            mail_obj.rawSize = mail.get("rawSize")
            mail_obj.fromAddr = mail.get("fromAddr")
            mail_obj.toAddr = mail.get("toAddr")
            mail_obj.downloadUrl = mail.get("downloadUrl")
            mail_obj.text = mail.get("text")
            mail_obj.headerSubject = mail.get("headerSubject")
            mails.append(mail_obj)
        return mails
    
    def list_addresses(self, sessionID):
        """
        Retrieves a list of addresses associated with a specific session.

        Args:
            self: The instance of the DropMail class.
            sessionID: The ID of the session for which addresses are to be retrieved.

        Returns:
            A list of Address objects if successful, None otherwise.
        """
        addresses = []
        listAddresses = self.connect.client.list_addresses(sessionID)
        if listAddresses is None:
            return None
        for address in listAddresses.get("session").get("addresses"):
            address_obj = Address()
            address_obj.address = address.get("address")
            address_obj.restoreKey = address.get("restoreKey")
            addresses.append(address_obj)
        return addresses
    
    @staticmethod
    def generate_mail(baseAddress):
        """
        Generates a random email address based on the provided base address.

        Args:
            baseAddress (str): The base address from which to generate the random email address.

        Returns:
            str: The generated random email address.

        Example:
            >>> generate_mail("example@example.com")
            "example.dqj@oqb.example.com"
        """
        def generat_random_string():
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for _ in range(random.randint(4, 6)))
        
        userName, domain = baseAddress.split("@")
        extendedAddress = f"{userName}.{generat_random_string()}@{generat_random_string()}.{domain}"
        return extendedAddress