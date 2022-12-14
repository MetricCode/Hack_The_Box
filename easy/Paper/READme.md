# @Author : M3tr1c_r00t
## Paper!
![Paper](https://user-images.githubusercontent.com/99975622/207163312-7f2ee8ee-ae72-40b6-aac2-d67468a1c143.png)
Paper is an easy box where we can exploit an Arbitrary File Read Vulnerability off Drafted posts from wordpress version 5.2.3 to get creds of the site and ssh as the given user and using linpeas to get root user....

### Enumeration
_**Nmap...**_
<br> There were 3 ports open on the box i.e 22, 80 and 443

```
# Nmap 7.92 scan initiated Tue Nov 22 19:22:44 2022 as: nmap -sC -sV -A -p 22,80,443 -oN nmapports.txt 10.129.136.31
Nmap scan report for 10.129.136.31
Host is up (0.77s latency).

PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.0 (protocol 2.0)
| ssh-hostkey: 
|   2048 10:05:ea:50:56:a6:00:cb:1c:9c:93:df:5f:83:e0:64 (RSA)
|   256 58:8c:82:1c:c6:63:2a:83:87:5c:2f:2b:4f:4d:c3:79 (ECDSA)
|_  256 31:78:af:d1:3b:c4:2e:9d:60:4e:eb:5d:03:ec:a0:22 (ED25519)
80/tcp  open  http     Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1k mod_fcgid/2.3.9)
|_http-server-header: Apache/2.4.37 (centos) OpenSSL/1.1.1k mod_fcgid/2.3.9
|_http-generator: HTML Tidy for HTML5 for Linux version 5.7.28
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: HTTP Server Test Page powered by CentOS
443/tcp open  ssl/http Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1k mod_fcgid/2.3.9)
|_http-server-header: Apache/2.4.37 (centos) OpenSSL/1.1.1k mod_fcgid/2.3.9
| tls-alpn: 
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=Unspecified/countryName=US
| Subject Alternative Name: DNS:localhost.localdomain
| Not valid before: 2021-07-03T08:52:34
|_Not valid after:  2022-07-08T10:32:34
|_http-title: HTTP Server Test Page powered by CentOS
| http-methods: 
|_  Potentially risky methods: TRACE
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.2 - 4.9 (95%), Linux 3.1 (94%), Linux 3.2 (94%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Linux 3.10 - 4.11 (94%), Linux 5.1 (94%), HP P2000 G3 NAS device (93%), Linux 3.18 (93%), Linux 3.16 (93%), ASUS RT-N56U WAP (Linux 3.4) (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   538.70 ms 10.10.14.1
2   538.53 ms 10.129.136.31

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Nov 22 19:23:54 2022 -- 1 IP address (1 host up) scanned in 70.12 seconds

```
On visiting the ip on port 80, we are redirected to host;
<br> **_office.paper_**
![Screenshot_2022-11-22_23_41_07](https://user-images.githubusercontent.com/99975622/207164883-bedc026b-765a-4d1f-b921-c8a807aff166.png)

<br>So , lets add that to our /etc/hosts file ...
![Screenshot_2022-11-22_23_44_09](https://user-images.githubusercontent.com/99975622/207164972-df0f6c1a-d85d-4ebe-9fc2-c71e25192e1d.png)

**_Gobuster/Directory Brute...._**
<br>Next up, i ran a gobusterscan using common.txt wordlists and found a directory "/manual" which reveals to us this is a wordpress site...
```
/.hta                [33m (Status: 403) [0m [Size: 199]
/.htaccess           [33m (Status: 403) [0m [Size: 199]
/.htpasswd           [33m (Status: 403) [0m [Size: 199]
/cgi-bin/            [33m (Status: 403) [0m [Size: 199]
/manual              [36m (Status: 301) [0m [Size: 236] [34m [--> http://10.129.136.31/manual/] [0m
```
On that note, I did a wordpress scan using wpscan and we find the version...
![Screenshot_2022-11-22_23_47_42](https://user-images.githubusercontent.com/99975622/207165581-762e5db0-8e57-4113-90a2-53f6447f51f4.png)

Since it's an older version of wordpress, we can search for vulnerabilities....
![Screenshot_2022-11-22_23_53_30](https://user-images.githubusercontent.com/99975622/207165703-56f6de83-0da4-4ba2-88a6-90303eb1e827.png)
And we can see that we can we can get this by adding _**"/?static=1&order=asc"**_ in the url to view the saved drafts...

![Screenshot_2022-11-22_23_53_54](https://user-images.githubusercontent.com/99975622/207166148-24b400c6-f540-4fce-8b9e-d0f8b6ebf829.png)

On doing so, we get an error. But if we get rid of the _**order=asc**_, it works!

![Screenshot_2022-11-22_23_54_04](https://user-images.githubusercontent.com/99975622/207166297-79ebc158-fb92-4105-8a31-367676f6d678.png)

Looking at the dumped drafts, we can see there's an Employee chat system...
![Screenshot_2022-11-22_23_54_18](https://user-images.githubusercontent.com/99975622/207166937-d747360d-338b-4833-8c59-acadcb0f460b.png)
We can visit the url and register...

![Screenshot_2022-11-22_23_55_46](https://user-images.githubusercontent.com/99975622/207166624-34188a3b-e19f-4d5b-aef0-5b31152fa758.png)
We're in....
![Screenshot_2022-11-22_23_57_30](https://user-images.githubusercontent.com/99975622/207167348-32c66759-2566-4f1d-9d29-cc675a13ca7f.png)

After going through the employee's chats, we note that there's a bot in the system set by the admin to run bash commands on the server to get and read files...
![Screenshot_2022-11-22_23_57_49](https://user-images.githubusercontent.com/99975622/207167510-3bb38186-365d-4c9c-a59b-40ccc4a0a5c6.png)
 

```
recyclops file ../../../../../etc/passwd
```
we can run the code below to check on the system's environment...
```
recyclops file ../../../../../proc/self/environ
```
And we get some creds...
![Screenshot_2022-11-23_00_07_14](https://user-images.githubusercontent.com/99975622/207168981-d6d69328-30d2-43e9-9877-df6c3faaa4d1.png)

<br> We can try to ssh as dwight and it works...
<br> You can get the user flag...
![Screenshot_2022-11-23_00_08_53](https://user-images.githubusercontent.com/99975622/207169064-b3e3d656-85be-4238-9a95-a67c76d92d60.png)

We can also run the script as below adding the environment in the environ directory...
```
recyclops file ../../../../../proc/self/environ.env
```
![Screenshot_2022-11-23_00_07_35](https://user-images.githubusercontent.com/99975622/207169293-cb02a5c6-5861-41ea-9996-d1f60dd6e64e.png)

### Priv Esc...
![Screenshot_2022-11-23_00_11_16](https://user-images.githubusercontent.com/99975622/207170451-8e1ae662-4977-45cc-8cdf-05837c45c07f.png)

On running Linpeas, we realise that the system is vulnerable to _**"CVE-2021-3560"**_ (Polkit-Privilege-Esclation PoC)
```
https://github.com/secnigma/CVE-2021-3560-Polkit-Privilege-Esclation
```
Clone the script then upload it to the box...
<br>On running the script, it creates a new user secnigma:secnigmaftw (Check source code for the creds...) that can run any command as root...
![Screenshot_2022-11-23_00_27_05](https://user-images.githubusercontent.com/99975622/207170797-b1e22b18-0527-467c-93cc-a589cb5f2663.png)
Move to the user using su.
<br> Next you can run sudo bash and we're root!
![Screenshot_2022-11-23_00_27_27](https://user-images.githubusercontent.com/99975622/207170964-8a37950f-533c-4866-9c03-b160167d72c8.png)
Get your root flag and boom!
<br>Done!

### Socials
@Instagram : https://instagram.com/M3tr1c_r00t
<br>@Twitter : https://twitter.com/M3tr1c_root
