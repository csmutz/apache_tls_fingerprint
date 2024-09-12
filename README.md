# apache_tls_fingerprint
Expose TLS fingerprint metadata in apache mod_ssl. Try to cover all attributes necessary for ja3 and ja4

## Notes

Metadata Required:

  - ~~SSLVersion~~ (SSL_CLIENTHELLO_VERSION) 
  - ~~Ciphers~~ (SSL_CLIENTHELLO_CIPHERS)
  - ~~SSLExtension~~ (SSL_CLIENTHELLO_EXTENSION_IDS)
  - ~~Signature Algorithms~~ (SSL_CLIENTHELLO_SIG_ALGOS)
  - ~~EllipticCurve~~ (SSL_CLIENTHELLO_EC_GROUPS)
  - ~~EllipticCurvePointFormat~~ (SSL_CLIENTHELLO_EC_FORMATS)
  - ~~ALPN~~ (SSL_CLIENTHELLO_ALPN)
  - ~~SNI/Server_name~~ (Already in mod_ssl)
  - ~~Protocol~~ (tcp or quic) (presumably will be available through which quic is officially implemented on openssl/apache. For now, assume tcp)
  - ~~Compression methods~~ (SSL_CLIENTHELLO_COMP_METHODS)
  - ~~Supported versions~~ (SSL_CLIENTHELLO_SUPPORTED_VERSIONS)
  - Other fields or extensions?
  

How will data be represented? 
  - As hex of raw values (prefered approach)
    - ALPN as CSV of string since raw value is string
  - dash separate list, ja3 style (this is a bunch of extra work, for little benefit)
  - Remove grease or not?
    - Use of grease seemes like the sort of attribute you want for fingerprinting. Expose all data, including grease, and let the user of the metadata decide how they want to use it.

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

 - Create simple scripts to confirm generation of ja3 and ja4
 - statistical analysis, look for most important features/attributes
 - test directive to disable/enable clienthello collection

### References

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

