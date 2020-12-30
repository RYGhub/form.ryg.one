# RYGforms

Ask for a OAuth2 login, then redirect to a Typeform having one or more hidden fields.

## Running

### Development

1. Clone this repository:
   ```bash
   git clone git@github.com:RYGhub/rygforms.git
   ```

2. Enter the cloned directory:
   ```bash
   cd rygforms
   ```

3. Create a new `.env` file inside containing the configuration (see [the example](EXAMPLE.env)):
   ```bash
   cp EXAMPLE.env .env
   ```

4. Install the requirements using Poetry:
   ```bash
   poetry install
   ```

5. Run the debug server from inside the Poetry environment:
   ```bash
   poetry shell
   python -m rygforms
   ```

### Production

1. Create a new venv and enter it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install through PyPI:
   ```bash
   pip install rygforms gunicorn
   ```
   
3. Copy the [provided systemd unit file](web-rygforms.service) to the `/etc/systemd/system` directory:
   ```bash
   curl https://raw.githubusercontent.com/RYGhub/rygforms/master/web-rygforms.service > /etc/systemd/system/web-rygforms.service
   ```   

4. Reload the systemd unit files:
   ```bash
   systemctl daemon-reload
   ```

4. Start (and optionally enable) the service:
   ```bash
   systemctl start "web-rygforms"
   systemctl enable "web-rygforms"
   ```

6. Copy the [provided Apache site file](rp-rygforms.conf) to the `/etc/apache2/sites-available` directory:
   ```bash
   curl https://raw.githubusercontent.com/RYGhub/rygforms/master/rp-rygforms.conf > /etc/apache2/sites-available/rp-rygforms.conf
   ```

7. Enable the `rp-rygforms` site reload the Apache configuration:
   ```bash
   a2ensite rp-rygforms
   systemctl reload apache2
   ```
