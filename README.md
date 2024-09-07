# apache_tls_fingerprint
Expose TLS fingerprint metadata in apache mod_ssl. Try to cover all attributes necessary for ja3 and ja4

## Notes

Metadata Required:

  - ~~SSLVersion~~ (SSL_CLIENTHELLO_VERSION) 
    - Version already exposed in mod_ssl is version negotiated is different from that offered by the client in the client hello
      - https://docs.openssl.org/1.1.1/man3/SSL_get_version/#name
  - ~~Ciphers~~ (SSL_CLIENTHELLO_CIPHERS)
  - SSLExtension (close, need to reformat: SSL_CLIENTHELLO_EXTENSION_IDS)
  - Signature Algorithms
  - EllipticCurve
  - EllipticCurvePointFormat
  - ALPN
    - Expose as CSV of strings?
  - ~~SNI/Server_name~~ (Already in mod_ssl)
  - Protocol (tcp or quic) (presumably will be available through which quic is officially implemented on openssl/apache. For now, assume tcp)

How will data be represented? 
  - As hex of raw values (prefered approach)
  - dash separate list, ja3 style (this is a bunch of extra work, for little benefit)
  - Remove grease or not? Use of grease seemes like the sort of attribute you want for fingerprinting. Expose all data, including grease, and let the user of the metadata decide how they want to use it.

### Access to Handshake information

Handshake information is only available during handshake callback. mod_ssl already registers handshake callback for SNI.

 - During callback we allocate new modssl_clienthello_vars struct (using connection mem pool) that is child of SSLConnRec and populate raw values from SSL clienthello functions
     - TODO: break this out to separate function 
 - In the environment vars get raw values from the SSLConnRec struct and format (using req pool) accordingly

### Config item to enable

Should probably create a configuration directive (could work at vhost or global level) to enable clienthello collection, by default skip collection of data.

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
