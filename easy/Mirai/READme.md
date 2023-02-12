# Mirai!
## @Author : M3tr1_r00t
![Mirai](https://user-images.githubusercontent.com/99975622/218311565-d9a52fb1-542a-47d6-9959-6e9f5155993a.png)

### Enumerationn
#### Nmap
```
# Nmap 7.92 scan initiated Wed Nov 16 16:08:50 2022 as: nmap -sC -sV -A -p 22,80,53,1722,32400,32469 -oN nmapports.txt 10.129.44.131
Nmap scan report for 10.129.44.131
Host is up (0.18s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u3 (protocol 2.0)
| ssh-hostkey: 
|   1024 aa:ef:5c:e0:8e:86:97:82:47:ff:4a:e5:40:18:90:c5 (DSA)
|   2048 e8:c1:9d:c5:43:ab:fe:61:23:3b:d7:e4:af:9b:74:18 (RSA)
|   256 b6:a0:78:38:d0:c8:10:94:8b:44:b2:ea:a0:17:42:2b (ECDSA)
|_  256 4d:68:40:f7:20:c4:e5:52:80:7a:44:38:b8:a2:a7:52 (ED25519)
53/tcp    open  domain  dnsmasq 2.76
| dns-nsid: 
|_  bind.version: dnsmasq-2.76
80/tcp    open  http    lighttpd 1.4.35
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: lighttpd/1.4.35
1722/tcp  open  upnp    Platinum UPnP 1.0.5.13 (UPnP/1.0 DLNADOC/1.50)
32400/tcp open  http    Plex Media Server httpd
|_http-favicon: Plex
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Server returned status 401 but no WWW-Authenticate header.
|_http-title: Unauthorized
|_http-cors: HEAD GET POST PUT DELETE OPTIONS
32469/tcp open  upnp    Platinum UPnP 1.0.5.13 (UPnP/1.0 DLNADOC/1.50)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 4.1 (95%), Linux 3.10 - 4.11 (95%), Linux 3.13 (95%), Linux 3.2 - 4.9 (95%), Linux 4.4 (95%), Linux 4.8 (95%), Linux 4.9 (95%), Linux 3.16 (95%), Linux 3.12 (94%), Linux 3.13 or 4.2 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 53/tcp)
HOP RTT       ADDRESS
1   290.38 ms 10.10.14.1
2   290.44 ms 10.129.44.131

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Nov 16 16:09:18 2022 -- 1 IP address (1 host up) scanned in 28.12 seconds
```
#### Gobuster
```
# Nmap 7.92 scan initiated Wed Nov 16 16:08:50 2022 as: nmap -sC -sV -A -p 22,80,53,1722,32400,32469 -oN nmapports.txt 10.129.44.131
Nmap scan report for 10.129.44.131
Host is up (0.18s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u3 (protocol 2.0)
| ssh-hostkey: 
|   1024 aa:ef:5c:e0:8e:86:97:82:47:ff:4a:e5:40:18:90:c5 (DSA)
|   2048 e8:c1:9d:c5:43:ab:fe:61:23:3b:d7:e4:af:9b:74:18 (RSA)
|   256 b6:a0:78:38:d0:c8:10:94:8b:44:b2:ea:a0:17:42:2b (ECDSA)
|_  256 4d:68:40:f7:20:c4:e5:52:80:7a:44:38:b8:a2:a7:52 (ED25519)
53/tcp    open  domain  dnsmasq 2.76
| dns-nsid: 
|_  bind.version: dnsmasq-2.76
80/tcp    open  http    lighttpd 1.4.35
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: lighttpd/1.4.35
1722/tcp  open  upnp    Platinum UPnP 1.0.5.13 (UPnP/1.0 DLNADOC/1.50)
32400/tcp open  http    Plex Media Server httpd
|_http-favicon: Plex
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Server returned status 401 but no WWW-Authenticate header.
|_http-title: Unauthorized
|_http-cors: HEAD GET POST PUT DELETE OPTIONS
32469/tcp open  upnp    Platinum UPnP 1.0.5.13 (UPnP/1.0 DLNADOC/1.50)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 4.1 (95%), Linux 3.10 - 4.11 (95%), Linux 3.13 (95%), Linux 3.2 - 4.9 (95%), Linux 4.4 (95%), Linux 4.8 (95%), Linux 4.9 (95%), Linux 3.16 (95%), Linux 3.12 (94%), Linux 3.13 or 4.2 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 53/tcp)
HOP RTT       ADDRESS
1   290.38 ms 10.10.14.1
2   290.44 ms 10.129.44.131

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Nov 16 16:09:18 2022 -- 1 IP address (1 host up) scanned in 28.12 seconds
```

#### Port 80
Since we dont have any data, we can just enumerate port 32400 which seems to be another web server.
Plus the service doesnt have any default creds.
You may also need to note that the server is a raspberry pi from the web server on port 80.

![Screenshot_2022-11-16_16_39_28](https://user-images.githubusercontent.com/99975622/218311739-f02fd312-1252-4968-9c58-56d011e5a595.png)

#### Port 32400
In this port, we find a plex sign in page but since we dont have any creds, it deems to be useless.
![Screenshot_2022-11-16_16_42_43](https://user-images.githubusercontent.com/99975622/218312256-cdf3cefa-39cf-4499-ab78-92fe732a5b19.png)

#### Port 22
With no other way forward, we can try and login into ssh using a raspberry pi's default creds and it works!
```
pi:raspberry
```
![Screenshot_2022-11-16_16_46_13](https://user-images.githubusercontent.com/99975622/218312334-cf340d9f-a09e-4ff6-afad-ee6be26a36ab.png)

#### Hunting for the root flag
![Screenshot_2022-11-16_16_46_56](https://user-images.githubusercontent.com/99975622/218312400-219b6767-9c18-4939-8ead-a7a68021d6f3.png)
We can then look for the root.txt file in the system.

We find the file in a different directory but it seems to be a goose chase XD!
![Screenshot_2022-11-16_16_49_54](https://user-images.githubusercontent.com/99975622/218312870-780e85a2-dc2a-47a1-b3e1-e22fd523d7e0.png)
Usually, usb drives are mounted onto the "/media" directory.
Also, to see the mounted devices, we can run the command;
```
mount
```
For this, we are going to check the system's internal storage using the df command
```
df -lh
```
After that, we can then run a strings command on a specific mount and we can therefore see even the deleted contents.
grep -a is to view a binary file as if it were text.
```
grep -aPo '[a-fA-F0-9]{32}' /dev/sdb
strings /dev/sdb -n 32
```
![Screenshot_2022-11-16_16_52_04](https://user-images.githubusercontent.com/99975622/218313064-5a114899-b05f-4ee4-941c-39f9a2f1d13b.png)

When I file gets deleted, the structure of the filesystem removes the metadata about that file. That includes the timestamps, filename, and a pointer to where the raw file is on disk. The delete operation does not go to that point on the disk and do anything to clean up the data, like write all nulls over it.

And done!

### Socials
@instagram:https://instagram.com/Metric_r00t
<br> Twitter:https://twitter.com/M3tr1c_root
