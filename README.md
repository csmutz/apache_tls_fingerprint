# apache_tls_fingerprint
Expose TLS fingerprint metadata in apache mod_ssl. Try to cover all attributes necessary for ja3 and ja4 and any others we deep important

## Notes

Metadata Required:

  - SSLVersion
    - Version already exposed in mod_ssl is version negotiated which may be different from client proposed?
  - Signature Algorithms
  - Cipher
  - SSLExtension
  - EllipticCurve
  - EllipticCurvePointFormat
  - ALPN
    - Expose as CSV of strings?
  - ~~SNI/Server_name~~ (Already in mod_ssl)
  - Protocol (tcp or quic) (presumably this already available through an existing variable, for moment unnecessary as tcp can be assumed?)

How will data be represented? 
  - As hex of raw values (prefered approach)
  - dash separate list, ja3 style (this is a bunch of extra work, for little benefit)
  - 

### References

https://github.com/apache/trafficserver/blob/36da45475db02790b95d615a690b91170aa2f06c/plugins/ja3_fingerprint/ja3_fingerprint.cc
https://docs.openssl.org/1.1.1/man3/SSL_CTX_set_client_hello_cb/#name
bin2hex function: https://nightlies.apache.org/httpd/trunk/doxygen/group__ProxyReq.html#gafb84a149e70d4197fc79306cff502dc6
