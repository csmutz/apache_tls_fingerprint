# TLS Fingerprinting in Apache (and TLS RTT)
Expose TLS fingerprint metadata in apache mod_ssl. Cover all attributes necessary for ja3, ja4, and minimal fingerprints.

Minimal is a fingerprint created for testing here that uses the length of the 4 fields included (versions_count, ciphers_count, groups_count, extensions_count) and is an alternative to ja3 or ja4 that is very compact, is transparent, and works with many data analysis methods (ex. determine similar fingerprints).

The TLS fingerprint was accepted into apache upstream project: https://github.com/apache/httpd/commit/e9915b2bdb47a0dca4daa144a41a3c23edc3a59a

This repo now also integrates the handshake RTT code so both can be evaluated together. Accepted into apache here (included in 2.5.1 relase): https://github.com/apache/httpd/commit/79990b070f2e5374e1add982342b1fa71f5d189e

## Notes

Adds the following ENV variables
  - SSL_CLIENTHELLO_VERSION (ja3)
  - SSL_CLIENTHELLO_CIPHERS (ja3, ja4, minimal)
  - SSL_CLIENTHELLO_EXTENSIONS (ja3, ja4, minimal)
  - SSL_CLIENTHELLO_SIG_ALGOS (ja3, ja4)
  - SSL_CLIENTHELLO_GROUPS (ja3, minimal)
  - SSL_CLIENTHELLO_EC_FORMATS (ja3)
  - SSL_CLIENTHELLO_ALPN (ja4)
  - SSL_CLIENTHELLO_VERSIONS (ja4, minimal)

The ClientHello data is exposed as raw hex values (including grease) as would be seen in protocol/straight from Openssl.

The handshake RTT is also integrated here
  - SSL_HANDSHAKE_RTT

The TLS RTT is reported in microseconds.

## Demonstration
A patch that can be applied to existing distribution packages is provided. Note that OpenSSL > 3.2 is needed for RTT calculation.

#### Instructions for Ubuntu 24.10 or higher
Follow instructions here for rebuilding apache2 debian package: https://www.linuxjournal.com/content/rebuilding-and-modifying-debian-packages

  - Get the source packages for apache2
  - At the editing files step, copy the patch file to debian/patches/ and append the filename to serial
  - Put in anything you want in changelog message
  - If you have problems with build, simply delete test/clients/Makefile

#### Prebuilt packages for ubuntu 24.10

It's a really bad idea to install unsigned, binary packages from unofficial sources. See debs directory.

#### Example Flask App

See flask directory for simple app that exposes these variables.

### Configuration

Added a new directive: SSLClientHelloVars (on, off) available in Server or Virtualhost context. This turns on collection and retension of ClientHello data for the whole connection.

On a per-request basis, the StdEnvVars options dictate whether the ENV variables are exposed or not. If the ClientHello data wasn't collected, then these values will be null.

Add the following lines to /etc/apache2/sites-enabled/default-ssl.conf (inside the virtualhost section)

```
    LogFormat "%v %p %h %{remote}p %l %u %t %{sec}t.%{usec_frac}t %D \"%r\" %>s %I %O \"%{Host}i\" \"%{Referer}i\" \"%{User-Agent}i\" \"%{Connection}i\" \"%{Accept-Language}i\" \"%{Accept-Encoding}i\" \"%{Accept}i\" \"%{X-Forwarded-For}i\" \"%{Cookie}i\" \"%{Authorization}i\" %{SSL_CLIENTHELLO_VERSION}x %{SSL_CLIENTHELLO_VERSIONS}x %{SSL_CLIENTHELLO_CIPHERS}x %{SSL_CLIENTHELLO_EXTENSIONS}x %{SSL_CLIENTHELLO_SIG_ALGOS}x %{SSL_CLIENTHELLO_GROUPS}x %{SSL_CLIENTHELLO_EC_FORMATS}x %{SSL_CLIENTHELLO_ALPN}x %{SSL_HANDSHAKE_RTT}x" extended
    CustomLog ${APACHE_LOG_DIR}/access.log extended


    SSLClientHelloVars on

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

### References/Notes

#### Debian Packaging:

https://www.linuxjournal.com/content/rebuilding-and-modifying-debian-packages

https://wiki.debian.org/UsingQuilt

