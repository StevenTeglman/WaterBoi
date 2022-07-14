a = 5
b = 6
c = 1

l = {a:1, b:2, c:3}

def foofun(l):
    for k,v in l.items():
        l[k] = 1


foofun(l)

for i in l.values():
    print(i)
