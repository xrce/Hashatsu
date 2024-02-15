import requests, os, argparse
import hashlib as hs

parse = argparse.ArgumentParser()
parse.add_argument('-m', help='crack method', dest='mode')
parse.add_argument('-s', help='hash to crack', dest='hash')
parse.add_argument('-l', help='hash list', dest='list')
parse.add_argument('-c', help='character set', dest='char')
args = parse.parse_args()

mode, hash, list, charset = args.mode, args.hash, args.list, args.char

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
    print(f"\n{R}    ハ{Y}ッ{G}シ{C}ュ{OG}キ{LG}ラー{W}\n")

if not charset: chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
else:
    chars = ""
    if '0' in charset: chars += "0123456789"
    if 'a' in charset: chars += "abcdefghijklmnopqrstuvwxyz"
    if 'A' in charset: chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if '!' in charset: chars += "!\"\$%&/()=?-.:\\*'-_:.;,"

def brute():
    def ghash(type, str):
        match type:
            case "md5": return hs.md5(str.encode()).hexdigest()
            case "sha1": return hs.sha1(str.encode()).hexdigest()
            case "sha224": return hs.sha224(str.encode()).hexdigest()
            case "sha256": return hs.sha256(str.encode()).hexdigest()
            case "sha384": return hs.sha384(str.encode()).hexdigest()
            case "sha512": return hs.sha512(str.encode()).hexdigest()
            case _: pass
    def rstring(string): return string[::-1]
    def error(index_input):
        if len(chars) <= index_input: pass
        else: return chars[index_input]
    def gstring(string):
        if len(string) <= 0: string.append(chars[0])
        else:
            string[0] = error((chars.index(string[0]) + 1) % len(chars))
            if chars.index(string[0]) == 0: return [string[0]] + gstring(string[1:])
        return string
    def decrypt():
        astring = []
        while True:
            astring = gstring(astring)
            fstring = rstring("".join(astring))
            hashes = ghash(type, fstring)
            print(f"{C} {hashes}{W} [ {R}{fstring}{W} ]", end="\r", flush=True)
            if hashes == hash:
                if list: print(f"\r{C} [+] {W}{hash}{R} : {W}{fstring}")
                else: print(f"\n{C} [+] {W}Result{R} : {W}{fstring}")
                break
    decrypt()

def shot(mode):
    email = "arrow.chosen@farmoaks.com"
    code = "a9da13def71735c0"
    res = requests.get(f"https://md5decrypt.net/en/Api/api.php?hash={hash}&hash_type={type}&email={email}&code={code}").text
    if len(res) != 0:
        if list: print(f"{C} [+] {W}{hash}{R} : {W}{res}")
        else: print(f"{C} [+] {W}Result{R} : {W}{res}")
    elif mode == 'default':
        if not list: print(Y+' //'+W+' I can\'t do it, trying bruteforce\n')
        brute()

def check(hash):
    match len(hash):
        case 32: return 'md5'
        case 40: return 'sha1'
        case 64: return 'sha256'
        case 96: return 'sha384'
        case 128: return 'sha512'
        case _: return 'invalid'

banner()

if list:
    print(f"{Y} //{W} List : {list}\n")
    with open(list) as hlist:
        while (hash := hlist.readline().rstrip()):
            type = check(hash)
            if type != 'invalid':
                if type and not mode: shot('default')
                elif mode == 'brute' and type: brute()
                elif mode == 'shot' and type: shot()
            else: print(f"{R} [-] {W}{hash}{R} ({W}invalid{R})")
else:
    type = check(hash)
    if type != 'invalid':
        print(f"{Y} //{W} Hash : {hash}")
        print(f"{Y} //{W} Type : {type}\n")
        if not mode:
            print(f"{Y} //{W} Trying to get a shot\n")
            shot('default')
        elif mode == 'brute': brute()
        elif mode == 'shot':
            print(f"{Y} //{W} Trying to get a shot\n")
            shot()
    else: print(type)
