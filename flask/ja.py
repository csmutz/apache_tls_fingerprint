#!/usr/bin/env python3
'''
rough implementations of ja3 and ja4 for testing of apache variables
This implementation is not complete, it will fail on many edge cases--but does work for common ones
- tcp is hardcoded
- alpn does not handle grease
- if supported versions extension is not present, doesn't read version field
'''
import sys
import json
import struct
import hashlib

tls_versions = { 
    "0304": "13",
    "0303": "12",
    "0302": "11",
    "0301": "10",
    "0300": "s3",
    "0002": "s2",
    "feff": "d1",
    "fefd": "d2",
    "fefc": "d3" }


def filter_grease(orig):
    filtered = []
    for e in orig:
        if ((e[1] == "a" or e[1] == "A") and (e[3] == "a" or e[3] == "A")):
            pass
        else:
            filtered.append(e)
    return filtered

def filter_extensions_ja4(orig):
    filtered = []
    for e in orig:
        if (e == "0000" or e == "0010"):
            pass
        else:
            filtered.append(e)
    return filtered

def hex2int_dsv(orig):
    ints = []
    for i in orig:
        ints.append(str(int(i,16)))
    return "-".join(ints)

def split_hex_4(orig):
    output = [orig[i:i+4] for i in range(0, len(orig), 4)]
    return output

def unpack_ciphers(ciphers_packed):
    ciphers = split_hex_4(ciphers_packed)
    return hex2int_dsv(filter_grease(ciphers))

def unpack_formats(formats_packed):
    formats = [formats_packed[i:i+2] for i in range(0, len(formats_packed), 2)]
    return hex2int_dsv(formats)


def ja3(data):
    '''
    calc ja3 using dictionary of values provided from apache
    '''   
    version = ""
    ciphers = ""
    extensions = ""
    groups = ""
    formats = ""

    if "SSL_CLIENTHELLO_VERSION" in data:
        version = str(int(data["SSL_CLIENTHELLO_VERSION"],16))
    if "SSL_CLIENTHELLO_CIPHERS" in data:
        ciphers = unpack_ciphers(data["SSL_CLIENTHELLO_CIPHERS"])
    if "SSL_CLIENTHELLO_EXTENSION_IDS" in data:
        extensions = unpack_ciphers(data["SSL_CLIENTHELLO_EXTENSION_IDS"])
    if "SSL_CLIENTHELLO_EC_GROUPS" in data:
        groups = unpack_ciphers(data["SSL_CLIENTHELLO_EC_GROUPS"])
    if "SSL_CLIENTHELLO_EC_FORMATS" in data:
        formats = unpack_formats(data["SSL_CLIENTHELLO_EC_FORMATS"])

    
    full_ja3 = "%s,%s,%s,%s,%s" %(version,ciphers,extensions,groups,formats)
    #print(full_ja3)
    return hashlib.md5(full_ja3.encode()).hexdigest()

def ja4(data):
    version = "00"
    sni = "i"
    extensions_filtered = []
    ciphers_filtered = []
    alpn = "00"
    ciphers_hash = "000000000000"
    extensions_hash = "000000000000"
    

    if "SSL_CLIENTHELLO_SUPPORTED_VERSIONS" in data:
        versions = split_hex_4(data["SSL_CLIENTHELLO_SUPPORTED_VERSIONS"])
        v = sorted(filter_grease(versions), reverse=True)[0]
        if v in tls_versions:
            version = tls_versions[v]
    if "SSL_CLIENTHELLO_CIPHERS" in data:
        ciphers = split_hex_4(data["SSL_CLIENTHELLO_CIPHERS"])
        ciphers_filtered = filter_grease(ciphers)
        cipher_hash = hashlib.sha256((",".join(sorted(ciphers_filtered))).encode()).hexdigest()[0:12]
    if "SSL_CLIENTHELLO_EXTENSION_IDS" in data:
        extensions = split_hex_4(data["SSL_CLIENTHELLO_EXTENSION_IDS"])
        if "0000" in extensions:
            sni = "d"
        extensions_filtered = filter_grease(extensions)
        extensions_for_hash = ",".join(sorted(filter_extensions_ja4(extensions_filtered)))
        #print(extensions_for_hash)
        if "SSL_CLIENTHELLO_SIG_ALGOS" in data:
            algos = split_hex_4(data["SSL_CLIENTHELLO_SIG_ALGOS"])
            algos_for_hash = ",".join(filter_grease(algos))
            #print(algos_for_hash)
            extensions_hash = hashlib.sha256(("%s_%s" % (extensions_for_hash,algos_for_hash)).encode()).hexdigest()[0:12]

    if "SSL_CLIENTHELLO_ALPN" in data:
        alpn_raw = data["SSL_CLIENTHELLO_ALPN"]
        offset = int(alpn_raw[0:2],16)
        alpn = "%s%s" % (chr(int(alpn_raw[2:4],16)),chr(int(alpn_raw[(offset * 2):(offset * 2 + 2)],16)))

    return "t%s%s%02i%02i%s_%s_%s" % (version,sni,len(ciphers_filtered),len(extensions_filtered),alpn,cipher_hash,extensions_hash)


def main():
    with open(sys.argv[1]) as f:
        data = json.load(f)
    print("ja3: %s" % (ja3(data)))
    print("ja4: %s" % (ja4(data)))

        

if __name__ == '__main__':
    main()
