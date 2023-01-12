# Sauna!
## @Author : M3tr1c_r00t

![Sauna](https://user-images.githubusercontent.com/99975622/212198177-f6bb183d-b984-4b70-bc71-bf89f0b28188.png)
Sauna is an easy windows box which in which we are going to use kerberos pre authentication to be able to know the present users which we will find in the running web server. We are going to do some kerberoasting so as to get creds and get user access. For root access, after running winpeas, we can do a Domain Syncing and Extract the administrator's password hash and login as administrator using psexec.py.
### Enumeration...
**__Nmap...__**
```
# Nmap 7.93 scan initiated Wed Jan 11 12:27:51 2023 as: nmap -sC -sV -A -p 53,80,135,139,445,3268,593,636,3269,464,389,88 -oN nmapports.txt 10.10.10.175
Nmap scan report for 10.10.10.175
Host is up (0.16s latency).

PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
80/tcp   open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Egotistical Bank :: Home
| http-methods: 
|_  Potentially risky methods: TRACE
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2023-01-11 19:27:59Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: EGOTISTICAL-BANK.LOCAL0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: EGOTISTICAL-BANK.LOCAL0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
OS fingerprint not ideal because: Missing a closed TCP port so results incomplete
No OS matches for host
Network Distance: 2 hops
Service Info: Host: SAUNA; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   311: 
|_    Message signing enabled and required
|_clock-skew: 7h00m00s
| smb2-time: 
|   date: 2023-01-11T19:28:16
|_  start_date: N/A

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   164.01 ms 10.10.14.1
2   164.01 ms 10.10.10.175

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Jan 11 12:28:57 2023 -- 1 IP address (1 host up) scanned in 66.95 seconds
```
**__Gobusterscan on the web-server...__**
```
/css                 [36m (Status: 301)[0m [Size: 147][34m [--> http://10.10.10.175/css/][0m
/fonts               [36m (Status: 301)[0m [Size: 149][34m [--> http://10.10.10.175/fonts/][0m
/images              [36m (Status: 301)[0m [Size: 150][34m [--> http://10.10.10.175/images/][0m
/Images              [36m (Status: 301)[0m [Size: 150][34m [--> http://10.10.10.175/Images/][0m
/index.html          [32m (Status: 200)[0m [Size: 32797]
```
#### Domain setting...
In this case, we are going to use crackmapexec to be able to get the domain name...
![Screenshot_2023-01-11_18_03_38](https://user-images.githubusercontent.com/99975622/212198276-f0668eb1-d367-4f46-8e0c-55113dd710f2.png)

Since the website since to static, there's not much that we can get except a list of possible usernames from the site.
![image](https://user-images.githubusercontent.com/99975622/212201651-7068f411-4098-4c06-a9b3-7bf48f922d04.png)


After gathering all the usernames, we can then transform into a series of login usernames for the machine...
```
Fergus Smith 
F.Smith
FSmith
Shaun Coins
S.Coins
SCoins
Bowie Taylor
B.Taylor
BTaylor
Hugo Bear
H.Bear
HBear
Steven Kerb 
S.Kerb
SKerb
Sophie Driver
S.Driver
SDriver
```
We can then use a tool called Kerbrute which will help us find valid usernames.
![Screenshot_2023-01-11_18_04_16](https://user-images.githubusercontent.com/99975622/212200980-4786bc12-cac5-4d02-b62f-10ede82d8431.png)

So basically what Kerbrute will do is Kerbrute is that it will brute-force and enumerate valid active-directory users by abusing the Kerberos pre-authentication.
Source...
```
https://github.com/ropnop/kerbrute
```
After running the Kerbrute tool, we find one valid user;fsmith.
![Screenshot_2023-01-11_18_06_57](https://user-images.githubusercontent.com/99975622/212201001-79b3fde8-0ad3-462e-be0a-a442e778e9de.png)

#### AS-REP Roasting...
AS-REP Roasting is a technique that enables adversaries to steal the password hashes of user accounts that have Kerberos preauthentication disabled, which they can then attempt to crack offline.

When preauthentication is enabled, a user who needs access to a resource begins the Kerberos authentication process by sending an Authentication Server Request (AS-REQ) message to the domain controller (DC). The timestamp on that message is encrypted with the hash of the user’s password. If the DC can decrypt that timestamp using its own record of the user’s password hash, it will send back an Authentication Server Response (AS-REP) message that contains a Ticket Granting Ticket (TGT) issued by the Key Distribution Center (KDC), which is used for future access requests by the user.

```
https://blog.netwrix.com/2022/11/03/cracking_ad_password_with_as_rep_roasting/
https://m0chan.github.io/2019/07/31/How-To-Attack-Kerberos-101.html#as-rep-roasting
```
For this, we're gonna use a script from impacket; GetNPUsers.py and we can get the hack of fsmith. 
![Screenshot_2023-01-11_18_08_39](https://user-images.githubusercontent.com/99975622/212201705-54389a5f-b398-4014-8207-415a5689b2b2.png)

After getting the hash, we can bruteforce it using john-the-ripper...
![Screenshot_2023-01-11_18_09_19](https://user-images.githubusercontent.com/99975622/212201728-9d85958d-4b54-4275-8b50-a1f86eda0e94.png)

We can now try to see if we can login to smb using the new creds that we have...
![Screenshot_2023-01-11_18_14_04](https://user-images.githubusercontent.com/99975622/212201794-47886903-97f4-4167-afaf-a215247aa165.png)
And since we can and have read priviledges, we cant run the psexec.py script to get a shell. So we can try evilwinrm ..
And we are in!
![Screenshot_2023-01-11_18_15_58](https://user-images.githubusercontent.com/99975622/212201819-1835471e-927e-4449-b406-ccc2f32bdd63.png)

### Priviledge Escalation...
Uploading winpeas...
![Screenshot_2023-01-11_18_19_05](https://user-images.githubusercontent.com/99975622/212201880-1aa24f12-a717-44ee-b709-5b366d007a49.png)

After running winpeas, we find some autologon creds stored in the system for the user __svc_loanmgr__
![Screenshot_2023-01-11_18_38_05](https://user-images.githubusercontent.com/99975622/212201910-b5b54ed0-9a49-464c-91dc-e7eda43c811a.png)

After logging to winrm using the creds, we look around and note that the svc_loanmgr has the ChangeAll priviledges and we can use his account to do a domain controller sync and get the hash of the administrator user.
We can use impacket- secretdump script and we get the administrator's hash.
![Screenshot_2023-01-11_18_39_07](https://user-images.githubusercontent.com/99975622/212201947-eb744241-b0ed-4ef5-b09a-c1308947d9d3.png)

Now that we have the administrator's hash, we can login to the machine using psexec.py script ...
![Screenshot_2023-01-11_18_43_50](https://user-images.githubusercontent.com/99975622/212202001-067c9992-6a20-4993-be39-ef53d983b83e.png)

And Done!

### Socials
@instagram:https://instagram.com/Metric_r00t
<br> Twitter:https://twitter.com/M3tr1c_root
