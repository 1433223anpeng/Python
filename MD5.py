from hashlib import md5

x = "autozh-CHStran\n109984457"

a = md5()
a.update(x.encode())

print(a.hexdigest())
