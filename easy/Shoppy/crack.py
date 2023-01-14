#!/usr/bin/python2
# @Author : M3tr1c_r00t

import subprocess
file = open("rockyou.txt","r")


for x in file:
    proc = subprocess.Popen('./password-manager', stdin=subprocess.PIPE)
    proc.communicate(str(x))
    if proc.returncode:
        continue

    print "Found the password: " + str(x)
    break
