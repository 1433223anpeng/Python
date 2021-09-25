from Crypto.Cipher  import AES

with open("0001.js",'rb') as f:
    a = f.read()

with open("key.key",'rb') as f:
    key = f.read()

aes = AES.new(key, AES.MODE_CBC,key)
res = aes.decrypt(a)

with open("0001.ts",'wb') as f:
    f.write(res)

print("OK")