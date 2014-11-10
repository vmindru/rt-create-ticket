#!/bin/env python
import os,fileinput

z='/tmp/klist_var'
k=''

if os.path.isfile(z):
	print "file"
else:
	print  "nofile"


text=''
for line in fileinput.input(files = z):
    text=text+line

print text
