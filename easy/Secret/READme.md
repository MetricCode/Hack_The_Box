# Academy!
## @Author : M3tr1c_r00t
![Secret](https://user-images.githubusercontent.com/99975622/209347889-7a75b535-d2c7-44cc-8bd3-cb8757b519d1.png)


### Enumeration...
**__Nmap..__**
```
# Nmap 7.92 scan initiated Fri Nov 11 10:53:44 2022 as: nmap -sC -sV -A -v -oN nmapscan.txt 10.129.175.31
Increasing send delay for 10.129.175.31 from 0 to 5 due to 79 out of 262 dropped probes since last increase.
Increasing send delay for 10.129.175.31 from 20 to 40 due to 11 out of 12 dropped probes since last increase.
Increasing send delay for 10.129.175.31 from 40 to 80 due to 11 out of 12 dropped probes since last increase.
Nmap scan report for 10.129.175.31
Host is up (0.47s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 97:af:61:44:10:89:b9:53:f0:80:3f:d7:19:b1:e2:9c (RSA)
|   256 95:ed:65:8d:cd:08:2b:55:dd:17:51:31:1e:3e:18:12 (ECDSA)
|_  256 33:7b:c1:71:d3:33:0f:92:4e:83:5a:1f:52:02:93:5e (ED25519)
80/tcp   open  http    nginx 1.18.0 (Ubuntu)
|_http-title: DUMB Docs
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.18.0 (Ubuntu)
3000/tcp open  http    Node.js (Express middleware)
|_http-title: DUMB Docs
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Nov 11 10:55:48 2022 -- 1 IP address (1 host up) scanned in 123.86 seconds

```
We can see there are 2 web servers up.. So let's visit the first on port 80...

![Screenshot_2022-11-11_13_29_58](https://user-images.githubusercontent.com/99975622/209348304-f54c035a-2392-436c-8fcf-b516c070e871.png)
After a bit of looking into the site, we find there's a source code file which we can download and look into

![Screenshot_2022-11-11_13_30_01](https://user-images.githubusercontent.com/99975622/209348410-0789baae-8841-4f50-994b-601a2c1055f5.png)

After unzipping the downloaded source code, we can go through it and we find that there's a git repo which mite of interest but will check on that later....

![Screenshot_2022-11-11_13_30_36](https://user-images.githubusercontent.com/99975622/209348714-9a273593-919f-4b92-807a-b6f223c9fb9e.png)

Well, after going through the git repo, i ran a directory bruteforce and we find there's an api present...

```
/api                 [32m (Status: 200)[0m [Size: 93]
/assets              [36m (Status: 301)[0m [Size: 179][34m [--> /assets/][0m
/docs                [32m (Status: 200)[0m [Size: 20720]
/download            [36m (Status: 301)[0m [Size: 183][34m [--> /download/][0m
```
And we see there's an api....
<br> So we can get a look at the documentation of the api and see how it works...
![Screenshot_2022-11-11_13_32_30](https://user-images.githubusercontent.com/99975622/209349098-dd57b65c-2f1b-4ec1-a6fb-763e2057ede7.png)
We can make a user for the api but there's an error after sending the data ...

![Screenshot_2022-11-11_13_35_31](https://user-images.githubusercontent.com/99975622/209349213-e3f81a71-adc6-4e80-8d01-34f668c50e7c.png)

There's a quick easy fix for this....The error is there because the data we are sending off is in json format but the content type header is url encoded, we can fix this by changing the content type to json and it works!

![Screenshot_2022-11-11_13_35_49](https://user-images.githubusercontent.com/99975622/209349430-5591b5b0-adc5-45cc-af73-d95d62cbe4c6.png)
Next up we can log in with our new creds to the api and we get a token which we can use ahead...

![Screenshot_2022-11-11_13_36_24](https://user-images.githubusercontent.com/99975622/209349657-158d2dde-e0e3-4bdb-99a4-ea340fa2c003.png)



