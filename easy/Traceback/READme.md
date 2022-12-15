# Traceback!
## @Author : M3tr1c-r00t 
![](https://i.imgur.com/sUoGjDP.png)
Traceback is a nice easy box which has a backdoor and we can use the backdoor to gain user access.


### Enumeration...
```
# Nmap 7.92 scan initiated Thu Nov 24 22:25:58 2022 as: nmap -sC -sV -A -p 22,80 -oN nmapports.txt 10.129.45.30
Nmap scan report for 10.129.45.30
Host is up (0.32s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 96:25:51:8e:6c:83:07:48:ce:11:4b:1f:e5:6d:8a:28 (RSA)
|   256 54:bd:46:71:14:bd:b2:42:a1:b6:b0:2d:94:14:3b:0d (ECDSA)
|_  256 4d:c3:f8:52:b8:85:ec:9c:3e:4d:57:2c:4a:82:fd:86 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Help us
|_http-server-header: Apache/2.4.29 (Ubuntu)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.2 - 4.9 (95%), Linux 5.1 (95%), Linux 3.1 (94%), Linux 3.2 (94%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Linux 3.10 - 4.11 (94%), HP P2000 G3 NAS device (93%), Linux 3.16 (93%), Oracle VM Server 3.4.2 (Linux 4.1) (92%), ASUS RT-N56U WAP (Linux 3.4) (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT       ADDRESS
1   506.83 ms 10.10.14.1
2   506.92 ms 10.129.45.30

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu Nov 24 22:26:52 2022 -- 1 IP address (1 host up) scanned in 54.29 seconds

```
### 
There's nothing to interesting in the nmap scan so we can go ahead and visit the server...

![](https://i.imgur.com/qD5ch1I.png)

Checking on the source code, we get another hint....
![](https://i.imgur.com/YsJiWT5.png)


Weve got a hint that there's a backdoor on the server so we can go ahead and do a gobusterscan using a backdoor wordlist from **Seclists...**
![](https://i.imgur.com/IpDj3rG.jpg)


And we've found our php backdoor on the system....
![](https://i.imgur.com/G67E4tb.png)
We can ran system commands on this backdoor so we can ran a reverse shell one liner to get at least a stable shell
![](https://i.imgur.com/uM9OHlu.png)

When we move into the home directory of the webmin user, we find a note...
![](https://i.imgur.com/lBVS01n.jpg)
Lua is a scripting language and we can take advantage of the script which is located in the sysadmin home directory...

```
https://www.tutorialspoint.com/lua/lua_file_io.htm

```
We can use the above cheatsheet to help us to enter our generated ssh-key into the sysadmin's .ssh/authorized_keys file...
![](https://i.imgur.com/gcUUjgT.jpg)
And with that,run the script and we can now ssh as the sysadmin user and get our user flag...
![](https://i.imgur.com/zOtI4c0.jpg)

### Priv Esc...
I ran linpeas but didnt find anything interesting.
On running pspy binary, we can see that there's a process running in the background as root ....
Its the message of the day...
![](https://i.imgur.com/Yug4GUt.jpg)

We can echo  a reverse shell command into the message of the day banner script as every script in that directory is being run as root....
![](https://i.imgur.com/J97dffB.jpg)
And boom! We're root!
![](https://i.imgur.com/W3mqZ9K.jpg)
### Socials
@Instagram:https://instagram.com/M3tr1c_r00t
<br>@Twitter:https://twitter.com/M3tr1c_root
