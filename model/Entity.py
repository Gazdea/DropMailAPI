class Connection:
    token = None
    client = None
    
    def __repr__(self) -> str:
        return f"token: {self.token}, client: {self.client}"
    
class Domain:
    id = None
    name = None
    introducedAt = None
    availableVia = None
    
    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, introducedAt: {self.introducedAt}, availableVia: {self.availableVia}"
    
class Session:
    id = None
    expiresAt = None
    
    def __repr__(self) -> str:
        return f"id: {self.id}, expiresAt: {self.expiresAt}"
        
class Address:
    address = None
    restoreKey = None
    
    def __repr__(self) -> str:
        return f"address: {self.address}, restoreKey: {self.restoreKey}"
        
class Mail:
    rawSize = None
    fromAddr = None
    toAddr = None
    downloadUrl = None
    text = None
    headerSubject = None

    def __repr__(self) -> str:
        return f"rawSize: {self.rawSize}, fromAddr: {self.fromAddr}, toAddr: {self.toAddr}, downloadUrl: {self.downloadUrl}, text: {self.text}, headerSubject: {self.headerSubject}"