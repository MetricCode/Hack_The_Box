# Academy!
## @Author : M3tr1c_r00t
![Academy](https://user-images.githubusercontent.com/99975622/209184686-64969825-87ac-43c2-a1b5-38ac5587f509.png)

### Enumeration ...
_**Nmap...**_
```
# Nmap 7.92 scan initiated Fri Nov 25 19:10:27 2022 as: nmap -sC -sV -A -p 22,80,33060 -oN nmapports.txt 10.129.250.108
Nmap scan report for academy.htb (10.129.250.108)
Host is up (0.22s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 c0:90:a3:d8:35:25:6f:fa:33:06:cf:80:13:a0:a5:53 (RSA)
|   256 2a:d5:4b:d0:46:f0:ed:c9:3c:8d:f6:5d:ab:ae:77:96 (ECDSA)
|_  256 e1:64:14:c3:cc:51:b2:3b:a6:28:a7:b1:ae:5f:45:35 (ED25519)
80/tcp    open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Hack The Box Academy
|_http-server-header: Apache/2.4.41 (Ubuntu)
33060/tcp open  mysqlx?
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port33060-TCP:V=7.92%I=7%D=11/25%Time=63811331%P=x86_64-pc-linux-gnu%r(
SF:GenericLines,9,"\x05\0\0\0\x0b\x08\x05\x1a\0");
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 4.15 - 5.6 (95%), Linux 5.0 - 5.4 (95%), Linux 5.3 - 5.4 (95%), Linux 2.6.32 (95%), Linux 5.0 (94%), Linux 5.0 - 5.3 (94%), Linux 5.4 (94%), Linux 3.1 (94%), Linux 3.2 (94%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   230.96 ms 10.10.14.1
2   230.91 ms academy.htb (10.129.250.108)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Nov 25 19:13:42 2022 -- 1 IP address (1 host up) scanned in 195.67 seconds

```
Visiting the site, we add, academy.htb to our /etc/hosts file and then check out the site....
<br>We and we find a static site...

![Screenshot_2022-11-25_22_17_23](https://user-images.githubusercontent.com/99975622/209185311-d06be7be-ede6-4cbb-b121-f9b8c1485f1b.png)
After registering, we are redicrected to the home page but its a static site...
<br>_**Next , directory bruteforcing...**_
<br>In this instance, i used the raft-small-files-lowercase.txt wordlist from seclists...
```
/index.php           [32m (Status: 200)[0m [Size: 2117]
/login.php           [32m (Status: 200)[0m [Size: 2627]
/register.php        [32m (Status: 200)[0m [Size: 3003]
/admin.php           [32m (Status: 200)[0m [Size: 2633]
/config.php          [32m (Status: 200)[0m [Size: 0]
/home.php            [36m (Status: 302)[0m [Size: 55034][34m [--> login.php][0m
/.htaccess.php       [33m (Status: 403)[0m [Size: 276]
/.htaccess           [33m (Status: 403)[0m [Size: 276]
/.                   [32m (Status: 200)[0m [Size: 2117]
/.html               [33m (Status: 403)[0m [Size: 276]
/.html.php           [33m (Status: 403)[0m [Size: 276]
/.php                [33m (Status: 403)[0m [Size: 276]
/.htpasswd           [33m (Status: 403)[0m [Size: 276]
/.htpasswd.php       [33m (Status: 403)[0m [Size: 276]
/.htm.php            [33m (Status: 403)[0m [Size: 276]
/.htm                [33m (Status: 403)[0m [Size: 276]
/.htpasswds.php      [33m (Status: 403)[0m [Size: 276]
/.htpasswds          [33m (Status: 403)[0m [Size: 276]
/.htgroup            [33m (Status: 403)[0m [Size: 276]
/.htgroup.php        [33m (Status: 403)[0m [Size: 276]
/wp-forum.phps       [33m (Status: 403)[0m [Size: 276]
/.htaccess.bak       [33m (Status: 403)[0m [Size: 276]
/.htaccess.bak.php   [33m (Status: 403)[0m [Size: 276]
/.htuser.php         [33m (Status: 403)[0m [Size: 276]
/.htuser             [33m (Status: 403)[0m [Size: 276]
```
And something interesting is that there is an admin page...
<br>we can forge the admin status by trying to create a username similar to admin or even add some characters such as the space character which registering....
<br>This is because the request is being url encoded when sent....
<br>Another key thing to note while sending the request, there's a hidden parameter,roleid which is set to 0, if we change it to 1, we get user priviledges regardless of the username used.....

![Screenshot_2022-11-25_22_22_15](https://user-images.githubusercontent.com/99975622/209187450-7b332330-ff45-43b6-bace-04567d7783a1.png)

After that we can log in with new creds....
![Screenshot_2022-11-25_22_23_44](https://user-images.githubusercontent.com/99975622/209187847-d46a0e85-b6c0-4ab1-badf-168719c89503.png)

And we have found a new sub-domain; add it to your /etc/hosts file and taking a look at ....

![Screenshot_2022-11-25_22_24_32](https://user-images.githubusercontent.com/99975622/209188089-6833714c-cd4c-4a00-b43f-4a91d85b351b.png)
By just having a look at the sub-domain, we can see there's a token and also discover that the running  framework is laravel for php.....

![Screenshot_2022-11-25_22_27_40](https://user-images.githubusercontent.com/99975622/209188291-da4f1918-5197-40bd-b250-6b0d682657c2.png)

After doing a searchsploit, we recognize there's an exploit we can use ....
<br>Fire up msfconsole and set up the settings...
![Screenshot_2022-11-25_22_32_19](https://user-images.githubusercontent.com/99975622/209188679-32ac5438-dc34-4252-96bf-eceefe114544.png)

After setting up the options and running the exploit, we finally get access

![Screenshot_2022-11-25_22_34_20](https://user-images.githubusercontent.com/99975622/209188765-aae1a6a1-cb53-4c92-9077-6e2e30d41c3b.png)
We have the www-data shell...

![Screenshot_2022-11-25_22_34_42](https://user-images.githubusercontent.com/99975622/209188921-6861dcca-8fe1-41d0-8397-be789d224143.png)

After a bit of poking around in the system, i found a .env file which had some creds....

![Screenshot_2022-11-25_22_40_20](https://user-images.githubusercontent.com/99975622/209189338-27e56685-9a39-48bd-9452-858a6aedeecd.png)
We can go and check out which users are present in the system by grepping for bash in /etc/passwd 
![Screenshot_2022-11-25_22_43_59](https://user-images.githubusercontent.com/99975622/209189447-4a51493b-2d81-4d8f-911a-1e8dac499e35.png)

As there are quite a number of users, we can try password spraying the users to see if we can gain access...
<br>So after saving the usernames in a file, and the found password in a file, we can use hydra to password spray...
![Screenshot_2022-11-25_22_49_09](https://user-images.githubusercontent.com/99975622/209189692-9ee1ec3e-d7a9-4595-aa62-917cd1ddbd81.png)
And with that, we can get our user flag...
![Screenshot_2022-11-25_22_52_04](https://user-images.githubusercontent.com/99975622/209189758-70787c40-d977-4e54-86df-70e0148ed9ac.png)

After running linpeas in the remote machine, i note something wierd, there we audit logs present .....
![Screenshot_2022-11-25_23_06_26](https://user-images.githubusercontent.com/99975622/209190054-bc0ed5b5-505e-4638-af20-52cc48a0b38a.png)

After seeing that i wanted to confirm some of my suspicions and wanted to see my user's id ....

![Screenshot_2022-11-25_23_06_36](https://user-images.githubusercontent.com/99975622/209190212-5c6d2649-befa-4a08-b0a8-aefdebda2e84.png)
And they are true....
<br>We are (adm) group ...
<br>The adm group is usually used to monitor system tasks and can read system log files...
![image](https://user-images.githubusercontent.com/99975622/209190578-1d2eca42-d804-49bd-871f-ca1dabc118f6.png)
And with that piece of information at hand, we can now check the reports on the user....
```
aureport --tty
```
![Screenshot_2022-11-25_23_07_10](https://user-images.githubusercontent.com/99975622/209190725-31c16190-c21b-4ee8-80de-575a78bba52f.png)

And we can see the creds of the mrb3n user....
<br>Using them and we log in....

![Screenshot_2022-11-25_23_07_33](https://user-images.githubusercontent.com/99975622/209191096-c07cd3b9-26eb-4ddd-89b3-79695edbb81f.png)
We can check the user permissions and we find the user can run the composer binary as root....
![Screenshot_2022-11-25_23_07_52](https://user-images.githubusercontent.com/99975622/209191257-87483a4e-740e-4f81-95cb-5d36ad14db4d.png)

After heading on to gtfobins, we find there is an exploit for the binary....
![Screenshot_2022-11-25_23_09_23](https://user-images.githubusercontent.com/99975622/209191519-e140b8c7-5d39-4883-8ce1-0c9440b8be09.png)
And with that, we are root, you can head to the root directory and get the root flag....
![Screenshot_2022-11-25_23_10_06](https://user-images.githubusercontent.com/99975622/209191647-a53224b0-066e-47f6-883f-f2030ede8218.png)

Done!
### Socials
@Instagram:https://instagram.com/M3tr1c_r00t
<br>@Twitter:https://twitter.com/M3tr1c_root
