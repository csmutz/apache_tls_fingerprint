# apache_tls_fingerprint
Expose TLS fingerprint metadata in apache mod_ssl. Try to cover all attributes necessary for ja3 and ja4

## Notes

Metadata Required:

  - ~~SSLVersion~~ (SSL_CLIENTHELLO_VERSION) (ja3)
  - ~~Ciphers~~ (SSL_CLIENTHELLO_CIPHERS) (ja3, ja4, optimal)
  - ~~SSLExtension~~ (SSL_CLIENTHELLO_EXTENSION_IDS) (ja3, ja4, optimal)
    - OpenSSL doesn't report grease here so for these values grease is always stripped. Possibly other extensions unknown to OpenSSL are stripped?
    - Test SSL_client_hello_get_extension_order to see if it return grease values too (OpenSSL >= 3.2 only)
  - ~~Signature Algorithms~~ (SSL_CLIENTHELLO_SIG_ALGOS) (ja3, ja4)
  - ~~EllipticCurve~~ (SSL_CLIENTHELLO_EC_GROUPS) (ja3, optimal))
  - ~~EllipticCurvePointFormat~~ (SSL_CLIENTHELLO_EC_FORMATS) (ja3)
  - ~~ALPN~~ (SSL_CLIENTHELLO_ALPN) (ja4)
  - ~~SNI/Server_name~~ (Already in mod_ssl) (ja4)
  - ~~Protocol~~ (tcp or quic) (presumably will be available through which quic is officially implemented on openssl/apache. For now, assume tcp) (ja4)
  - ~~Compression methods~~ (SSL_CLIENTHELLO_COMP_METHODS) (NA)
    - Remove as superfluous?, basically no clients advertise compression methods anymore, not used in ja3 or ja4 
  - ~~Supported versions~~ (SSL_CLIENTHELLO_SUPPORTED_VERSIONS) (optimal)
  - Other fields or extensions?
    - supported key exchange methods (NA) -- not used, no need
  

How will data be represented? 
  - As hex of raw values (prefered approach)
    - ~~ALPN as CSV of string since raw value is string~~ No, just do all as hex blobs. grease can make alpn non-ascii, future alpns may not be ascii
  - dash separate list, ja3 style (this is a bunch of extra work, for little benefit)
  - Remove grease or not?
    - Most fingerprinting tools ignore grease

### Access to Handshake information

Handshake information is only available during handshake callback. mod_ssl already registers handshake callback for SNI.

### Config item to enable

Should probably create a configuration directive (could work at vhost or server level) to enable clienthello collection, by default skip collection of data.

Plan is to have server or vhost level collection of client hello data. If it is collected, then add it to environment vars following same rules as STDenvvars.

SSLSrvConfigRec -- this is were config needs to go

SSLCompression, SSLSessionCacheTimeout are example directives.

Access via: mySrvConfig(s) s is server_rec/sslconn->server

See also modules/ssl/mod_ssl.c,  SSL_CMD_SRV(Compression

### Testing

 - ~~Create simple scripts to confirm generation of ja3 and ja4~~
   -  see flask scripts that print CLIENTHELLO values and derived ja3/ja4
 - statistical analysis, look for most important features/attributes
 - test directive to disable/enable clienthello collection
 - ~~Logging~~
   - The following will log values needed for fingerprinting. Replace combined log format with extended in sites-enabled/default-ssl.conf.

```
        ErrorLog ${APACHE_LOG_DIR}/error.log
        #CustomLog ${APACHE_LOG_DIR}/access.log combined
        LogFormat "%v %p %h %{remote}p %l %u %t %{sec}t.%{usec_frac}t %D \"%r\" %>s %I %O \"%{Host}i\" \"%{Referer}i\" \"%{User-Agent}i\" \"%{Connection}i\" \"%{Accept-Language}i\" \"%{Accept-Encoding}i\" \"%{Accept}i\" \"%{X-Forwarded-For}i\" \"%{Cookie}i\" \"%{Authorization}i\" %{SSL_CLIENTHELLO_VERSION}x %{SSL_CLIENTHELLO_SUPPORTED_VERSIONS}x %{SSL_CLIENTHELLO_CIPHERS}x %{SSL_CLIENTHELLO_EXTENSION_IDS}x %{SSL_CLIENTHELLO_SIG_ALGOS}x %{SSL_CLIENTHELLO_EC_GROUPS}x %{SSL_CLIENTHELLO_EC_FORMATS}x %{SSL_CLIENTHELLO_ALPN}x" extended
        CustomLog ${APACHE_LOG_DIR}/access.log extended
```

### References/Notes

#### ja3 and ja4 attributes:

https://github.com/salesforce/ja3?tab=readme-ov-file#how-it-works

https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/JA4.md

#### OpenSSL code:

https://github.com/apache/trafficserver/blob/36da45475db02790b95d615a690b91170aa2f06c/plugins/ja3_fingerprint/ja3_fingerprint.cc

https://docs.openssl.org/1.1.1/man3/SSL_CTX_set_client_hello_cb/#name

#### Apache code:

https://nightlies.apache.org/httpd/trunk/doxygen/group__APR__Util__Escaping.html#gac87b3c2f42fb60f6ea4d8321e60ce69e

#### Debian Packaging:

https://www.linuxjournal.com/content/rebuilding-and-modifying-debian-packages

https://wiki.debian.org/UsingQuilt
```
quilt top - show current patchfile
```
#### Flask demo app

https://asdkazmi.medium.com/deploying-flask-app-with-wsgi-and-apache-server-on-ubuntu-20-04-396607e0e40f

https://flask.palletsprojects.com/en/2.0.x/deploying/mod_wsgi/

