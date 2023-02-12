)# Previse!
## @Author : M3tr1c_r00t
![Previse](https://user-images.githubusercontent.com/99975622/218304698-2a469fe6-22c9-4f70-88da-6d6e23ab95ef.png)
Previse is an easy box where we exploit a vulnerable web server to status modification and command execution to gain our foothold, dump the database to find user creds and get user acess. For root, we do a path hijacking on a script set to run with sudo priviledges and we pwn the box :)
### Enumeration
#### Nmap...
```
# Nmap 7.92 scan initiated Tue Nov 22 15:06:45 2022 as: nmap -sC -sV -A -p 22,80 -oN nmapports.txt 10.129.250.0
Nmap scan report for 10.129.250.0
Host is up (0.22s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 53:ed:44:40:11:6e:8b:da:69:85:79:c0:81:f2:3a:12 (RSA)
|   256 bc:54:20:ac:17:23:bb:50:20:f4:e1:6e:62:0f:01:b5 (ECDSA)
|_  256 33:c1:89:ea:59:73:b1:78:84:38:a4:21:10:0c:91:d8 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-title: Previse Login
|_Requested resource was login.php
|_http-server-header: Apache/2.4.29 (Ubuntu)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 4.15 - 5.6 (95%), Linux 5.0 (95%), Linux 5.0 - 5.4 (95%), Linux 5.3 - 5.4 (95%), Linux 2.6.32 (95%), Linux 5.0 - 5.3 (94%), Linux 3.1 (94%), Linux 3.2 (94%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Linux 5.4 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   210.55 ms 10.10.14.1
2   219.35 ms 10.129.250.0

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Nov 22 15:07:08 2022 -- 1 IP address (1 host up) scanned in 23.83 seconds

```
#### Gobuster...
```
gobuster dir -w /usr/share/wordlists/dirb/common.txt -u http://10.129.250.0/ -o gobusterlight1.txt -x php,txt,html
/.php                [33m (Status: 403)[0m [Size: 277]
/.html               [33m (Status: 403)[0m [Size: 277]
/.hta.php            [33m (Status: 403)[0m [Size: 277]
/.hta                [33m (Status: 403)[0m [Size: 277]
/.hta.html           [33m (Status: 403)[0m [Size: 277]
/.hta.txt            [33m (Status: 403)[0m [Size: 277]
/.htaccess           [33m (Status: 403)[0m [Size: 277]
/.htaccess.html      [33m (Status: 403)[0m [Size: 277]
/.htaccess.php       [33m (Status: 403)[0m [Size: 277]
/.htpasswd           [33m (Status: 403)[0m [Size: 277]
/.htpasswd.php       [33m (Status: 403)[0m [Size: 277]
/.htaccess.txt       [33m (Status: 403)[0m [Size: 277]
/.htpasswd.txt       [33m (Status: 403)[0m [Size: 277]
/.htpasswd.html      [33m (Status: 403)[0m [Size: 277]
/accounts.php        [36m (Status: 302)[0m [Size: 3994][34m [--> login.php][0m
/config.php          [32m (Status: 200)[0m [Size: 0]
/css                 [36m (Status: 301)[0m [Size: 310][34m [--> http://10.129.250.0/css/][0m
/download.php        [36m (Status: 302)[0m [Size: 0][34m [--> login.php][0m
/favicon.ico         [32m (Status: 200)[0m [Size: 15406]
/files.php           [36m (Status: 302)[0m [Size: 4914][34m [--> login.php][0m
/footer.php          [32m (Status: 200)[0m [Size: 217]
/header.php          [32m (Status: 200)[0m [Size: 980]
/index.php           [36m (Status: 302)[0m [Size: 2801][34m [--> login.php][0m
/index.php           [36m (Status: 302)[0m [Size: 2801][34m [--> login.php][0m
/js                  [36m (Status: 301)[0m [Size: 309][34m [--> http://10.129.250.0/js/][0m
/login.php           [32m (Status: 200)[0m [Size: 2224]
/logout.php          [36m (Status: 302)[0m [Size: 0][34m [--> login.php][0m
/logs.php            [36m (Status: 302)[0m [Size: 0][34m [--> login.php][0m
/nav.php             [32m (Status: 200)[0m [Size: 1248]
/server-status       [33m (Status: 403)[0m [Size: 277]
/status.php          [36m (Status: 302)[0m [Size: 2966][34m [--> login.php][0m
```
Since we can see that most of the directories are redirecting us, we can try to intercept one and try to tinker with it.

![Screenshot_2022-11-22_15_50_23](https://user-images.githubusercontent.com/99975622/218304789-34586948-ccb5-4b5a-a623-e304528c339b.png)

If we try to convert the status code to "200 Ok", we get into the accounts.php without being redirected.
![Screenshot_2022-11-22_15_50_35](https://user-images.githubusercontent.com/99975622/218304885-1ed131ad-1f23-4344-8cb5-5bcdc41b21ac.png)
And we're in.

So, we can just create a user to avoid the redirects tho we can fix this using burp so that we can access all the aspects of the web server.

If we visit the files page, we find a zip file. Download it and it has the site's source code.

If we check the file_logs.php file, we can see that we can specify a delimiter to either a comma or space.
```
<?php
session_start();
if (!isset($_SESSION['user'])) {
    header('Location: login.php');
}
?>

<?php include( 'header.php' ); ?>

<title>Previse File Access Logs</title>
</head>
<body>

<?php include( 'nav.php' ); ?>
<section class="uk-section uk-section-default">
    <div class="uk-container">
        <h2 class="uk-heading-divider">Request Log Data</h2>
        <p>We take security very seriously, and keep logs of file access actions. We can set delimters for your needs!</p>
        <p>Find out which users have been downloading files.</p>
        <form action="logs.php" method="post">
            <div class="uk-margin uk-width-1-4@s">
                <label class="uk-form-label" for="delim-log">File delimeter:</label>
                <select class="uk-select" name="delim" id="delim-log">
                    <option value="comma">comma</option>
                    <option value="space">space</option>
                    <option value="tab">tab</option>
                </select>
            </div>
            <button class="uk-button uk-button-default" type="submit" value="submit">Submit</button>
        </form>
    </div>
</section>
    
<?php include( 'footer.php' ); ?>

```

With that , we have our entry point.

### Foothold as www-data
we can make a request to the log.php and specify the delimeter to be a comma, then inject our code.

![Screenshot_2022-11-22_16_01_20](https://user-images.githubusercontent.com/99975622/218308947-7a289ae1-b6ee-42ef-8ae2-ba398c4316f0.png)

I tried a rev shell bash payload but it had to be url encoded for it to work.

![Screenshot_2022-11-22_16_04_32](https://user-images.githubusercontent.com/99975622/218309074-73024594-8514-4171-b46f-a2a3331ccfc4.png)

And we are in as www-data.

### Www-data to user...
Since in the backup zip file there was a config file with mysql creds, that was the next step.

![Screenshot_2022-11-22_17_41_17](https://user-images.githubusercontent.com/99975622/218309174-3ded5bf8-d39b-4616-9190-7d03305dd57a.png)

We find the creds but the password is encyrpted.
The password seems to be md5-crypt so we can crack this using hashcat.
```
 hashcat -m 500 hash /usr/share/wordlists/rockyou.txt
```
![Screenshot_2022-11-22_18_06_22](https://user-images.githubusercontent.com/99975622/218309337-4c2748b7-4365-485c-a6b8-3273a2314ccd.png)

With that, we can ssh into the m4lwhere user with the pass and we're in.
![Screenshot_2022-11-22_18_09_41](https://user-images.githubusercontent.com/99975622/218309425-44a9cc02-9145-4434-af18-caf417dd7fe8.png)


### User to Root
If we run sudo -l, we can see that we can run a /opt/scripts/access_backup.sh as sudo.
![Screenshot_2022-11-22_18_59_03](https://user-images.githubusercontent.com/99975622/218309628-a907f857-2083-4959-814c-9b4bba1c6064.png)

The Script uses the gzip command but the full path to the gzip binary is not specified.

We can now do a path hijack for this. 
So, we can create a simple bash script which will make the /bin/bash binary have suid bit set or we can also send a reverse shell on our machine.

![Screenshot_2022-11-22_19_04_49](https://user-images.githubusercontent.com/99975622/218309762-3927337a-7cf8-4025-b70d-2f5913289af2.png)

Make sure to make the file be excutable and update the path.
![Screenshot_2022-11-22_19_03_58](https://user-images.githubusercontent.com/99975622/218309804-ff16ee33-0fa9-4309-a784-dcbffcfb1d5b.png)

With that set, we can now run the sudo script.
![Screenshot_2022-11-22_19_06_54](https://user-images.githubusercontent.com/99975622/218309865-e3dd3911-8e29-4383-9ba3-7eb320e74e47.png)

And done!

## My socials:
<br>@ twitter: https://twitter.com/M3tr1c_root
<br>@ instagram: https://instagram.com/m3tr1c_r00t/
