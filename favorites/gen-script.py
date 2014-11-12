#!/usr/bin/env python

tempchar = '`'
for i in range(27,33):
    with open("get-favorites-1.py", 'r') as scriptfile:
        script = scriptfile.read()
    script = script.replace("erroneous-1", "erroneous-" + str(i))
    script = script.replace("favorite-1","favorite-" + str(i))
    script = script.replace("xaa", "xb" + chr(ord(tempchar) + 1))
    tempchar = chr(ord(tempchar) + 1)
    with open("get-favorites-" + str(i) + ".py", 'w') as newscriptfile:
        newscriptfile.write(script)