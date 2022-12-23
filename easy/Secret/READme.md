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
### Foothold and Entry...
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

After a bit of dead ends, i decided to take a look a the source code once again and i found in the private.js file, there's an admin user validation...

![Screenshot_2022-11-11_13_37_32](https://user-images.githubusercontent.com/99975622/209350393-6fbe934f-e688-4d65-a551-120f476c5233.png)

<br> The verification is being cross referenced from the auth-token that we were given and with that, we can try to deobfuscate the auth-token and see what it entails...
<br>For this, we are going to use a site <a href="jwt.io">jwt.io</a>

![Screenshot_2022-11-11_13_45_54](https://user-images.githubusercontent.com/99975622/209350401-f22e5f4d-ce44-47ca-88c1-b5307754a6ca.png)
With this information at hand , i went back to the git repo and we find that the .env file was removed...

![Screenshot_2022-11-11_13_47_04](https://user-images.githubusercontent.com/99975622/209350860-95b54190-abba-4300-acf4-3558d3f4562a.png)
On showing this git, we find a private token...
![Screenshot_2022-11-11_13_47_27](https://user-images.githubusercontent.com/99975622/209351009-bf4fd5a5-15c8-45bb-be21-eaf58e2e7833.png)
You also need to remember that on the 
file private.js, the auth-ticket was verifying the username to being "theadmin" So we  need to change our 
email to gain access on the auth-token that we've found ...


![Screenshot_2022-11-11_13_47_57](https://user-images.githubusercontent.com/99975622/209351825-75345d22-d622-4bab-891b-a43d7c0ea5af.png)
After that, we can gain access to the priv directory using the auth-token...


On further enumeration on the private.js file, there was a log directory which might be our entry point into the machine as it may be reading the log files directly from the server....


![Screenshot_2022-11-11_14_17_20](https://user-images.githubusercontent.com/99975622/209352210-f1b32dde-27d2-488e-952b-97027250867a.png)

And we have RCE entry point!
<br> We can now get our reverse shell...
With our RCE, we can send our reverse shell script base64 encoded as there were some issues, probably filtering...
![Screenshot_2022-11-11_14_20_08](https://user-images.githubusercontent.com/99975622/209352552-03ce62ed-989d-40f0-ade8-8cdf22e3c877.png)
And now we can get our user flag...
### Priv Esc
![Screenshot_2022-11-11_14_22_23](https://user-images.githubusercontent.com/99975622/209352629-0328b116-6d44-413f-b25e-e682de97aa70.png)

Next, i fired up linpeas to find a way for priv esc and the system is vulnerable to polkit CVE-2021-4034

![Screenshot_2022-11-11_14_22_46](https://user-images.githubusercontent.com/99975622/209352817-dffc1594-6a92-445b-8b09-749dabdef51c.png)

After that, i sent the python script to the machine and we got root!

![Screenshot_2022-11-11_14_29_31](https://user-images.githubusercontent.com/99975622/209352911-2f1d3335-ae9e-4408-b665-8d4e6062ec0c.png)

Done!
### Socials
@Instagram:https://instagram.com/M3tr1c_r00t
<br>@Twitter:https://twitter.com/M3tr1c_root
