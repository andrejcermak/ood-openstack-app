from keystoneauth1.identity.v3 import Token, OidcAccessToken
from keystoneauth1 import session
from openstack import connection
from requests import get

AUTH_URL = "https://identity.ostrava.openstack.cloud.e-infra.cz/v3"
IDENTITY_PROVIDER = "login.e-infra.cz"
PROTOCOL = "openid"
PROJECT_DOMAIN_ID = "f4614917d043479b8c22017c89d96880"
def get_unscoped_token(token):
        admin = OidcAccessToken(auth_url=AUTH_URL,
                                identity_provider=IDENTITY_PROVIDER,
                                protocol=PROTOCOL,
                                access_token=token)

        sess = session.Session(auth=admin)
        return connection.Connection(session=sess).authorize()

def get_scoped_token(unscoped_token, project_id):
        user = Token(auth_url=AUTH_URL,
                token=unscoped_token,
                project_domain_id=PROJECT_DOMAIN_ID,
                project_id=project_id)

        sess = session.Session(auth=user)
        conn = connection.Connection(session=sess)
        return conn.authorize()

def get_user_id(token):
        admin = OidcAccessToken(auth_url=AUTH_URL,
                                identity_provider=IDENTITY_PROVIDER,
                                protocol=PROTOCOL,
                                access_token=token)
        sess = session.Session(auth=admin)
        return admin.get_user_id(sess)

def list_projects(token, user_id):
        projects = get("%s/users/%s/projects" % (AUTH_URL, user_id),
                       headers={"Accept": "application/json",
                                "User-Agent": "Mozilla/5.0 (X11;\
                                                    Ubuntu; Linux x86_64; rv:68.0)\
                                                    Gecko/20100101 Firefox/68.0",
                                "X-Auth-Token": token})
        return projects.json().get("projects")
