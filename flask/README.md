## Flask Demo App

Enable mod_ssl and default ssl site

Install flask and mod_wsgi:
```sudo apt install python3-flask libapache2-mod-wsgi-py3```

Edit /etc/apache2/sites-enabled/default-ssl.conf as described on the top level readme.

```
        WSGIDaemonProcess flaskapp threads=5
        WSGIScriptAlias /fingerprint /var/www/html/fingerprint/flaskapp.wsgi

        <Directory /var/www/html/fingerprint>
                SSLOptions +StdEnvVars
                WSGIProcessGroup flaskapp
                WSGIApplicationGroup %{GLOBAL}
                Order deny,allow
                Allow from all
        </Directory>
```

Put the .py and .wsgi files in /var/www/html/fingerprint

URL is https://SERVER_IP/fingerprint
