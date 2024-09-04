# apache_tls_fingerprint
Expose TLS fingerprint metadata in apache mod_ssl. Try to cover all attributes necessary for ja3 and ja4

## Notes

Metadata Required:

  - SSLVersion
    - Version already exposed in mod_ssl is version negotiated which may be different from client proposed?
  - Ciphers
  - SSLExtension
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

### References

#### ja3 and ja4 attributes:

https://github.com/salesforce/ja3?tab=readme-ov-file#how-it-works
https://github.com/FoxIO-LLC/ja4/blob/main/technical_details/JA4.md

#### OpenSSL code:

https://github.com/apache/trafficserver/blob/36da45475db02790b95d615a690b91170aa2f06c/plugins/ja3_fingerprint/ja3_fingerprint.cc
https://docs.openssl.org/1.1.1/man3/SSL_CTX_set_client_hello_cb/#name

#### Apache code:

bin2hex function: https://nightlies.apache.org/httpd/trunk/doxygen/group__ProxyReq.html#gafb84a149e70d4197fc79306cff502dc6

#### Debian Packaging:
https://www.linuxjournal.com/content/rebuilding-and-modifying-debian-packages
https://wiki.debian.org/UsingQuilt

