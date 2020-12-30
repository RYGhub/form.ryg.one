from flask import Flask, session, url_for, redirect, request, render_template, abort, flash
from authlib.integrations.flask_client import OAuth
import authlib.integrations.base_client.errors
import werkzeug.middleware.proxy_fix
import os

# Based and redpilled on Gestione
app = Flask(__name__)
app.secret_key = "anus"
app.config['SESSION_COOKIE_NAME'] = "sosdoasdas"
# os.getenv('FORM_SECRET')
clientId = os.getenv('FORM_CLIENT_ID')
clientSecret = os.getenv('FORM_CLIENT_SECRET')  # Alright then
oauth = OAuth(app=app)
oauth.register(
    name="royalnet",
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
base_url = os.getenv('FORM_URL')


@app.errorhandler(401)
def page_401(e):
    return render_template('error.htm', e=e)


@app.route("/<string:fid>")
def page_form(fid):
    session['fid'] = fid
    return oauth.royalnet.authorize_redirect(redirect_uri="http://127.0.0.1:5000/authorize", audience="")


@app.route("/authorize")
def page_auth():
    token = oauth.royalnet.authorize_access_token()
    userdata = oauth.royalnet.parse_id_token(token=token)
    email = userdata['name']
    token = token
    return redirect(url_for('page_success', email=email, token=token))


@app.route("/success/<string:email>/<string:token>")
def page_success(email, token):
    return "{} {} {}".format(session['fid'], email, token)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')