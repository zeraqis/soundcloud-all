#!/usr/bin/env python
string = "python get-favorites-1.py"
shell = string
for i in range(2,33):
    newstring = string.replace("favorites-1", "favorites-" + str(i))
    shell = shell + ' & ' + newstring
print shell