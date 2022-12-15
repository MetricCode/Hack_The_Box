# Traverxec!
## @Author : M3tr1c_r00t
![](https://i.imgur.com/CY6uedw.png)
Traverxec is a box which is vulnerable to the nostromo directory traversal to RCE vulnerability which gives paves the way for us to gain user priveldges and exploiting the journalctl binary via gtfobins to gain root priviledges!

### Enumeration...
***Nmap***
```
# Nmap 7.92 scan initiated Wed Nov 23 22:26:22 2022 as: nmap -sC -sV -A -p 22,80 -oN nmapports.txt 10.129.50.19
Nmap scan report for 10.129.50.19
Host is up (0.19s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
| ssh-hostkey: 
|   256 93:dd:1a:23:ee:d7:1f:08:6b:58:47:09:73:a3:88:cc (ECDSA)
|_  256 9d:d6:62:1e:7a:fb:8f:56:92:e6:37:f1:10:db:9b:ce (ED25519)
80/tcp open  http    nostromo 1.9.6
|_http-title: TRAVERXEC
|_http-server-header: nostromo 1.9.6
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 4.11 (91%), Linux 3.2 - 4.9 (91%), Linux 3.18 (90%), Linux 5.1 (90%), Crestron XPanel control system (89%), Linux 3.16 (88%), Linux 4.1 (87%), HP P2000 G3 NAS device (86%), ASUS RT-N56U WAP (Linux 3.4) (86%), Linux 3.1 (86%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT       ADDRESS
1   206.56 ms 10.10.14.1
2   208.12 ms 10.129.50.19

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Nov 23 22:26:41 2022 -- 1 IP address (1 host up) scanned in 19.60 seconds

```
Based on our nmap scan, we can see that the web server is nostrom which is kinda odd...

We can use searchsploit to search for a publicly available exploit for **nostrom 1.9.6**

![](https://i.imgur.com/jPkOtx6.jpg)
Checking on the source code, we can see how its ran...

![](https://i.imgur.com/OwIgiFK.jpg)

This exploit is an rce on the web server and on checking it using the id command, it works...
![](https://i.imgur.com/Xc9yrTB.jpg)

We can get a reverse shell on server....
![](https://i.imgur.com/QPL5n8Y.jpg)
Navigating to the home directory, there's a user, david, who has an encrypted ssh_key
![](https://i.imgur.com/PqDxrLV.jpg)

We can bruteforce it using John_The_Ripper and get the passphrase of the file...

```
ssh2john id_rsa > hash
john -w=/usr/share/wordlists/rockyou.txt hash
```
![](https://i.imgur.com/2gkG7uv.jpg)
And now with our passphrase, set the permissions on the id_rsa file and ssh into the system as david and get the user flag...
![](https://i.imgur.com/TnmHomc.jpg)

### Priv Esc ...
While in the home directory, there's a directory bin which contains a script that has a command being run as root using sudo...
![](https://i.imgur.com/ONvneEs.jpg)

There's a journalctl binary and moving to gtfobins,we find a way to gain root access...
![](https://i.imgur.com/FO7Vm5t.png)
We can run the sudo binary directly and boom! We are root!
![](https://i.imgur.com/BruFKHD.jpg)
### Socials
@Instagram:https://instagram.com/M3tr1c_r00t
<br>@Twitter:https://twitter.com/M3tr1c_root
