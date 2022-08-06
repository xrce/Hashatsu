#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os, argparse, hashlib

parse = argparse.ArgumentParser()
parse.add_argument('-m', help='crack method', dest='mode')
parse.add_argument('-s', help='hash to crack', dest='hash')
parse.add_argument('-l', help='hash list', dest='list')
parse.add_argument('-c', help='character set', dest='char')
args = parse.parse_args()

mode = args.mode
hashtext = args.hash
hashlist = args.list
charset = args.char

B  = '\033[1;34'
C  = '\033[1;36m'
G  = '\033[1;34m'
OG = '\033[92m'
LG = '\033[1;32m'
W  = '\033[1;37m'
R  = '\033[1;31m'
Y  = '\033[1;33m'

def banner():
    os.system('clear')
    print("")
    print(R+"    ハ"+Y+"ッ"+G+"シ"+C+"ュ"+OG+"キ"+LG+"ラー"+W)
    print("")

if not charset:
    ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
else:
    ascii_letters = ""
    if 'a' in charset:
        ascii_letters += "abcdefghijklmnopqrstuvwxyz"
    if 'A' in charset:
        ascii_letters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if '0' in charset:
        ascii_letters += "0123456789"
    if '!' in charset:
        ascii_letters += "!\"\$%&/()=?-.:\\*'-_:.;,"

def hashbrute():
    string_list = ascii_letters
    
    def generateHashFromString(hashtype, cleartextString):
        if hashtype == "md5":
            return hashlib.md5(cleartextString.encode()).hexdigest()
        elif hashtype == "sha1":
            return hashlib.sha1(cleartextString.encode()).hexdigest()
        elif hashtype == "sha224":
            return hashlib.sha224(cleartextString.encode()).hexdigest()
        elif hashtype == "sha256":
            return hashlib.sha256(cleartextString.encode()).hexdigest()
        elif hashtype == "sha384":
            return hashlib.sha384(cleartextString.encode()).hexdigest()
        elif hashtype == "sha512":
            return hashlib.sha512(cleartextString.encode()).hexdigest()
        else:
            pass
    def reverseString(string):
        return string[::-1]
    def IndexErrorCheck(index_input):
        if len(string_list) <= index_input:
            pass
        else:
            return string_list[index_input]
    def StringGenerator(string):
        if len(string) <= 0:
            string.append(string_list[0])
        else:
            # error checking needs to be done, otherwise a ValueError will raise
            string[0] = IndexErrorCheck((string_list.index(string[0]) + 1) % len(string_list))
            if string_list.index(string[0]) == 0:
                return [string[0]] + StringGenerator(string[1:])
        return string
    def decrypt():
        generated_string = []
        while True:
            generated_string = StringGenerator(generated_string)
            formatted_string = reverseString("".join(generated_string))
            hashes = generateHashFromString(hashtype, formatted_string)
            print(C+" "+hashes+W+" [ "+R+formatted_string+W+" ]", end="\r", flush=True)
            if hashes == hashtext:
                if hashlist:
                    print(C+"\r [+] "+W+hashtext+R+" : "+W+formatted_string)
                else:
                    print(C+"\n [+] "+W+"Result"+R+" : "+W+formatted_string)
                break
    decrypt()

def md5decrypt(mode):
    email = "bransen.vikranth@logdots.com"
    code = "49898fab6e014903"
    result = requests.get('https://md5decrypt.net/en/Api/api.php?hash=%s&hash_type=%s&email=%s&code=%s' % (hashtext, hashtype, email, code)).text
    if len(result) != 0:
        if hashlist:
            print(C+" [+] "+W+hashtext+R+" : "+W+result)
        else:
            print(C+" [+] "+W+"Result"+R+" : "+W+result)
    else:
        if mode == 'default':
            if not hashlist:
                print(Y+' //'+W+' I can\'t do it, trying bruteforce')
                print("")
            hashbrute()

def checktype(hashtext):
    if len(hashtext) == 32:
        return 'md5'
    elif len(hashtext) == 40:
        return 'sha1'
    elif len(hashtext) == 64:
        return 'sha256'
    elif len(hashtext) == 96:
        return 'sha384'
    elif len(hashtext) == 128:
        return 'sha512'
    else:
        return 'Not a valid Hash'

banner()

if hashlist:
    print(Y+' //'+W+' List : '+hashlist)
    print("")
    with open(hashlist) as hlist:
        while (hashtext := hlist.readline().rstrip()):
            hashtype = checktype(hashtext)
            if hashtype != 'Not a valid Hash':
                if hashtype and not mode:
                    md5decrypt('default')
                elif mode == 'brute' and hashtype:
                    hashbrute()
                elif mode == 'shot' and hashtype:
                    md5decrypt()

else:
    hashtype = checktype(hashtext)
    if hashtype != 'Not a valid Hash':
        print(Y+' //'+W+' Hash : '+hashtext)
        print(Y+' //'+W+' Type : '+hashtype)
        print("")
        if not mode:
            print(Y+' //'+W+' Trying to get a shot\n')
            md5decrypt('default')
        elif mode == 'brute':
            hashbrute()
        elif mode == 'shot':
            print(Y+' //'+W+' Trying to get a shot\n')
            md5decrypt()
    else:
        print(hashtype)