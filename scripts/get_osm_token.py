# Most of this script is from: https://github.com/metaodi/osmapi/blob/develop/examples/oauth2_backend.py

# This script shows how to authenticate with OAuth2 with a backend application
# The token is saved to disk in $HOME/.osmapi/token.json
# It can be reused until it's revoked or expired.

# install oauthlib for requests:  pip install oauthlib requests-oauthlib
from requests_oauthlib import OAuth2Session
import webbrowser
import json
import os
import sys

# on osm.org, go My Account, OAuth 2 Applications, Register a new application. Name it, specify redirect URL to be urn:ietf:wg:oauth:2.0:oob, click Modify the map scope. Copy over strings:
client_id = "XXXXXXXXXX"
client_secret = "XXXXXXXXXX"

redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

authorization_base_url = "https://www.openstreetmap.org/oauth2/authorize"
token_url = "https://www.openstreetmap.org/oauth2/token"
scope = ["write_api"]


def get_osmapi_path():
    base_dir = ""

    if os.getenv("HOME"):
        base_dir = os.getenv("HOME")
    elif os.getenv("HOMEDRIVE") and os.getenv("HOMEPATH"):
        base_dir = os.path.join(os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"))
    elif os.getenv("USERPROFILE"):
        base_dir = os.getenv("USERPROFILE")

    if not base_dir:
        print(
            "Unable to find home directory (check env vars HOME, HOMEDRIVE, HOMEPATH and USERPROFILE)",  # noqa
            file=sys.stderr,
        )
        raise Exception("Home directory not found")

    return os.path.join(base_dir, ".osmapi")


def token_saver(token):
    osmapi_path = get_osmapi_path()
    token_path = os.path.join(osmapi_path, "token.json")

    with open(token_path, "w") as f:
        print(f"Saving token {token} to {token_path}")
        f.write(json.dumps(token))


def save_and_get_access_token(client_id, client_secret, redirect_uri, scope):
    oauth = OAuth2Session(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
    )

    login_url, _ = oauth.authorization_url(authorization_base_url)

    print(f"Authorize user using this URL: {login_url}")
    webbrowser.open(login_url)

    authorization_code = input("Paste the authorization code here: ")

    token = oauth.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code=authorization_code,
    )

    token_saver(token)
    return token


token = save_and_get_access_token(client_id, client_secret, redirect_uri, scope)
print(token)
