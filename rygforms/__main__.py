import flask as f
import authlib.integrations.flask_client
import werkzeug.middleware.proxy_fix
import os

app = f.Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']
clientId = os.environ['CLIENT_ID']
clientSecret = os.environ['CLIENT_SECRET']

oauth = authlib.integrations.flask_client.OAuth(app=app)
ryg_login = oauth.register(
    name="ryg_login",
    api_base_url="https://ryg.eu.auth0.com",
    authorize_url='https://ryg.eu.auth0.com/authorize',
    access_token_url="https://ryg.eu.auth0.com/oauth/token",
    server_metadata_url="https://ryg.eu.auth0.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "profile email",
    },
    client_id=clientId,
    client_secret=clientSecret
)

reverse_proxy_app = werkzeug.middleware.proxy_fix.ProxyFix(app=app, x_for=1, x_proto=0, x_host=1, x_port=0, x_prefix=0)


@app.route("/<string:fid>")
def page_form(fid):
    f.session['fid'] = fid
    return ryg_login.authorize_redirect(redirect_uri=f.url_for("page_auth", _external=True), audience="")


@app.route("/authorize")
def page_auth():
    ryg_login.authorize_access_token()
    userdata = ryg_login.get("userinfo").json()
    email = userdata['nickname']
    return "ok then"


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')
