import xmlrpc.client
import os
import sys

class OdooClient:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common', allow_none=True)
        self.uid = None
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object', allow_none=True)

    def authenticate(self):
        try:
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            if self.uid:
                return True
            else:
                return False
        except Exception as e:
            raise ConnectionError(f"Odoo connection failed: {e}")

    def execute_kw(self, model, method, *args, **kwargs):
        if not self.uid:
            self.authenticate()
        
        # Read-Only Safety Lock: Only allow read-based methods
        allowed_methods = ['search', 'read', 'search_read', 'fields_get', 'get_version']
        if method not in allowed_methods:
            raise PermissionError(f"Write access denied: Method '{method}' is restricted in Read-Only mode.")
            
        try:
            return self.models.execute_kw(self.db, self.uid, self.password, model, method, args, kwargs)
        except Exception as e:
            print(f"❌ Odoo execute_kw error: {e}")
            raise

    def execute(self, model, method, *args, **kwargs):
        """Generic execution method."""
        return self.execute_kw(model, method, *args, **kwargs)

    def search_read(self, model, domain=None, fields=None, limit=None, offset=0, order=None):
        domain = domain or []
        kwargs = {'offset': offset}
        if fields:
            kwargs['fields'] = fields
        if limit:
            kwargs['limit'] = limit
        if order:
            kwargs['order'] = order
        return self.execute_kw(model, 'search_read', domain, **kwargs)

    def create(self, model, values):
        raise PermissionError("Create access denied (Read-Only Mode)")

    def write(self, model, ids, values):
        raise PermissionError("Write access denied (Read-Only Mode)")

    def unlink(self, model, ids):
        raise PermissionError("Delete access denied (Read-Only Mode)")

    def get_fields(self, model, attributes=None):
        attributes = attributes or ['string', 'help', 'type', 'relation']
        return self.execute_kw(model, 'fields_get', attributes=attributes)

    def get_version(self):
        try:
            return self.common.version()
        except Exception as e:
            return str(e)

if __name__ == "__main__":
    from dotenv import load_dotenv
    # Look for .env in the current directory or workspace root
    load_dotenv()
    
    url = os.getenv("ODOO_URL")
    db = os.getenv("ODOO_DB")
    user = os.getenv("ODOO_USER")
    pwd = os.getenv("ODOO_PASSWORD")
    
    if not all([url, db, user, pwd]):
        print("Missing environment variables. Check .env")
        sys.exit(1)

    client = OdooClient(url, db, user, pwd)
    if client.authenticate():
        print(f"✅ Authenticated successfully! UID: {client.uid}")
        print("Server Version:", client.get_version())
        
        # Test search_read on res.partner
        partners = client.search_read('res.partner', limit=5, fields=['name', 'email'])
        print(f"Fetched {len(partners)} partners.")
        for p in partners:
            print(f"- {p['name']} ({p.get('email') or 'No email'})")
    else:
        print("❌ Authentication failed.")
