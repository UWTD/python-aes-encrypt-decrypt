from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import sys
import os

f = sys.argv[1]
e = False

if f.endswith('.uwcrypted'):
    e = True

if e:
    with open(f, 'rb') as infile:
        KEY = infile.read(32)
        IV = infile.read(16)
        size = infile.read(16)
        chunksize = 64 * 1024
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        with open(f'{f.replace(".uwcrypted", "")}', 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(cipher.decrypt(chunk))
            outfile.truncate(int(size))
else:
    i = Random.get_random_bytes(128)
    KEY = SHA256.new(i)
    IV = Random.get_random_bytes(16)
    cipher = AES.new(KEY.digest(), AES.MODE_CBC, IV)
    chunksize = 64 * 1024
    size = str(os.path.getsize(f)).zfill(16)
    with open(f'{f}.uwcrypted', 'wb') as outfile:
        with open(f, 'rb') as infile:
            outfile.write(KEY.digest())
            outfile.write(IV)
            outfile.write(size.encode())
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))
                outfile.write(cipher.encrypt(chunk))
