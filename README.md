# Hashatsu - Hash Killer
Simple hash killer with some options

## How to Use
```sh
python hash.py -m <mode> -s <hash> -c <charset>
```

**Character Set :**
| Options | Characters                 |
| :-----: | -------------------------- |
|  **a**  | abcdefghijklmnopqrstuvwxyz |
|  **A**  | ABCDEFGHIJKLMNOPQRSTUVWXYZ |
|  **0**  | 1234567890                 |
|  **!**  | !\"\$%&/()=?-.:\\*'-_:.;,  |

**Example :**

```sh
python hash.py -m brute -s ae2b1fca515949e5d54fb22b8ed95575
```

**Or :**
```sh
python hash.py -s ae2b1fca515949e5d54fb22b8ed95575
```
```sh
python hash.py -l list.txt -m brute -c a0
```
## Dependencies
+ Python

## Python Modules
+ requests
+ os
+ argparse
+ hashlib
+ time

## Similar Tools
+ [Demd5](https://github.com/N1ght420/Demd5) - Simple MD5 Decryptor
