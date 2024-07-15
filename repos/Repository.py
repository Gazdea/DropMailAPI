from gql import Client as GQLClient, gql
from gql.transport.websockets import WebsocketsTransport

dropmail = "wss://dropmail.me/api/graphql/"
websocket = "/websocket"

class DropMail:
    def __init__(self, token):
        """
        Initializes a new instance of the DropMail class.

        Args:
            token (str): The authentication token for the DropMail API.

        Returns:
            None
        """
        self.token = token
        self.transport = WebsocketsTransport(url=dropmail + token + websocket)
        self.client = GQLClient(transport=self.transport, fetch_schema_from_transport=True)

    def get_domains(self):
        """
        Retrieves domains information from the API and returns it.
        """
        query = gql("query {domains {id, name, introducedAt, availableVia}}")
        return self.client.execute(query)

    def list_sessions(self):
        """
        Retrieves a list of sessions with their IDs and expiration dates from the API.

        Args:
            self: The instance of the DropMail class.

        Returns:
            The result of executing the query to retrieve a list of sessions.
        """
        query = gql("query {sessions {id, expiresAt}}")
        return self.client.execute(query)

    def get_sessions(self):
        """
        Retrieves a list of sessions with their IDs and expiration dates from the API.

        Args:
            self: The instance of the DropMail class.

        Returns:
            The result of executing the query to retrieve a list of sessions.
        """
        query = gql("mutation {introduceSession {id, expiresAt, addresses {address, restoreKey}}}")
        return self.client.execute(query)

    def get_address(self, session_id=None, domain_id=None):
        """
        Retrieves the address information for a particular session and domain.

        Args:
            self: The instance of the DropMail class.
            session_id (optional): The session ID. If not provided, it's fetched from the introduceSession.
            domain_id (optional): The domain ID. If not provided, it's fetched from the first domain.

        Returns:
            The result of executing the query to introduce an address.
        """
        if domain_id is None:
            domain_id = self.get_domains().get("domains")[0].get("id")
        if session_id is None:
            session_id = self.get_sessions().get("introduceSession").get("id")
        query = gql("mutation ($input: IntroduceAddressInput!) {introduceAddress(input: $input) {address, restoreKey}}")
        variable_values = {"input": {"sessionId": session_id, "domainId": domain_id}}
        return self.client.execute(query, variable_values=variable_values)

    def list_addresses(self, session_id):
        """
        Retrieves the list of addresses for a specific session.

        Args:
            self: The instance of the DropMail class.
            session_id: The ID of the session for which addresses are to be retrieved.

        Returns:
            The result of executing the query to list addresses.
        """
        query = gql("query ($id: ID!) {session(id:$id){addresses{address, restoreKey}}}")
        variable_values = {"id": session_id}
        return self.client.execute(query, variable_values=variable_values)

    async def subscribe_mail(self, session_id):
        """
        Asynchronously subscribes to a mail session.

        Args:
            self: The instance of the DropMail class.
            session_id: The ID of the session to subscribe to.

        Returns:
            The result of executing the subscription query.
        """
        query = gql("subscription ($id: ID!) {sessionMailReceived(id:$id) {rawSize, fromAddr, toAddr, downloadUrl, text, headerSubject} }")
        variable_values = {"id": session_id}
        return await self.client.execute_async(query, variable_values=variable_values)

    def list_mails(self, session_id):
        """
        Retrieves a list of emails associated with a specific session.

        Args:
            self: The instance of the DropMail class.
            session_id: The ID of the session for which emails are to be retrieved.

        Returns:
            The result of executing the query to list emails.
        """
        query = gql("query ($id: ID!) {session(id:$id){mails{rawSize, fromAddr, toAddr, downloadUrl, text, headerSubject}}}")
        variable_values = {"id": session_id}
        return self.client.execute(query, variable_values=variable_values)
