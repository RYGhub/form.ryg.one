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
        "scope": "profile email openid",
    },
    client_id=clientId,
    client_secret=clientSecret
)

reverse_proxy_app = werkzeug.middleware.proxy_fix.ProxyFix(app=app, x_for=1, x_proto=0, x_host=1, x_port=0, x_prefix=0)


@app.route("/<string:form_user>/<string:form_id>")
def page_form(form_user: str, form_id: str):
    f.session['form_user'] = form_user
    f.session['form_id'] = form_id
    return ryg_login.authorize_redirect(redirect_uri=f.url_for("page_auth", _external=True), audience="")


@app.route("/authorize")
def page_auth():
    ryg_login.authorize_access_token()
    userdata = ryg_login.get("userinfo").json()
    form_user = f.session["form_user"]
    form_id = f.session["form_id"]
    username = userdata["nickname"]
    user_id = userdata["sub"]
    return f.redirect(f"https://{form_user}.typeform.com/to/{form_id}#username={username}&id={user_id}")


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')
