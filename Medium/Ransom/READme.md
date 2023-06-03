# Ransom!
## @Author : M3tr1c_r00t

![Ransom](https://github.com/MetricCode/MetricCode/assets/99975622/66099b53-dc6e-402e-a324-a253c82a5f56)


Ransom is a medium ranked box in which we get to bypass a login page via php type juggling. After getting passed the login, we get a zip file which contains the backup of the user. The file is password protected but it uses an encryption algorithm which is vulnerable to a plain text attack.

After the plain text attack, we can get the id_rsa file and then login as the user. For root, we need to look for the web-root of the web-server and then we can get the user creds.

### Enumeration...

#### Nmap scan...

```
# Nmap 7.80 scan initiated Tue May  9 07:36:36 2023 as: nmap -sC -sV -A -v -oN nmapscan.txt 10.129.227.93
Nmap scan report for 10.129.227.93
Host is up (0.17s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: D41D8CD98F00B204E9800998ECF8427E
| http-methods: 
|_  Supported Methods: GET HEAD OPTIONS
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-title:  Admin - HTML5 Admin Template
|_Requested resource was http://10.129.227.93/login
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue May  9 07:37:18 2023 -- 1 IP address (1 host up) scanned in 42.64 seconds
```

#### dsearch...

```
# Dirsearch started Tue May  9 07:38:20 2023 as: dirsearch.py -w /usr/share/wordlists/dirb/common.txt -u http://10.129.227.93 -e php,txt,html,css,js -o /home/m3tr1c/Desktop/Ransom/dsearch.txt

301   312B   http://10.129.227.93:80/css    -> REDIRECTS TO: http://10.129.227.93/css/
200     0B   http://10.129.227.93:80/favicon.ico
301   314B   http://10.129.227.93:80/fonts    -> REDIRECTS TO: http://10.129.227.93/fonts/
302   390B   http://10.129.227.93:80/index.php    -> REDIRECTS TO: http://10.129.227.93/index.php/login
301   311B   http://10.129.227.93:80/js    -> REDIRECTS TO: http://10.129.227.93/js/
200     6KB  http://10.129.227.93:80/login
200    24B   http://10.129.227.93:80/robots.txt
403   278B   http://10.129.227.93:80/server-status
500   590KB  http://10.129.227.93:80/register
```


### Foothold

![Screenshot from 2023-05-09 07-59-32](https://github.com/MetricCode/MetricCode/assets/99975622/cab2718a-66aa-42ef-9a46-74610c549f0b)

Since this is a login page, i tried some sql injection but no luck.


![Screenshot from 2023-05-09 08-00-00](https://github.com/MetricCode/MetricCode/assets/99975622/d2c2d4d8-622a-4338-9253-095a4a55c443)

If we check out the login using burp suite, we can see that the data is being directed to the /api/login endpoint.

![Screenshot from 2023-05-09 08-04-42](https://github.com/MetricCode/MetricCode/assets/99975622/53e36959-ce9f-409c-826e-f6ce183a44db)

This endpoint also seems to be vulnerable to a SSRF attack as the parameters does not have the token sent together with it.

I tried first of all to change the request method to post but it wasnt accepted.


![Screenshot from 2023-05-09 08-04-59](https://github.com/MetricCode/MetricCode/assets/99975622/6543252c-1977-4f15-943b-50ecde21da94)


I then tried sending the request as json data after changing the application content type to `json` and worked.

![Screenshot from 2023-05-09 08-07-51](https://github.com/MetricCode/MetricCode/assets/99975622/a43c0a9c-f36e-4e6b-9466-1b8ea19f7cc2)

Since we get to define the data type in json data, i set the password to be equals to true and it worked.
![Screenshot from 2023-05-09 08-09-25](https://github.com/MetricCode/MetricCode/assets/99975622/acd346af-08e0-4964-8eb7-b6f1bf4d006c)

This vuln is called php type juggling which comes up due to php being a simple language. In php, which is kind of similar to python, the user doesnt have to tell it the data type, php will just identify the data type for itself based on the circumstance that the data is being used.

In this case, we changed the data type from a string to a boolean(true).

We can also set the value of password to be equal to 0 and it will work as true is 0 and false is 1.

![Screenshot from 2023-05-09 08-09-48](https://github.com/MetricCode/MetricCode/assets/99975622/c129eafd-bd1f-41ce-8ebd-de6f75f56d82)

Since we got access, we find 2 files, the user flag and a zipped file.

![Screenshot from 2023-05-09 08-11-10](https://github.com/MetricCode/MetricCode/assets/99975622/d5a30274-56c8-4fac-9a03-31d9c4178e94)

I downloaded the zip file and we can try to unzip it but it requires a password. I tried using john but no luck.

We can just use the unzip command and list the file contents and we can see that this is the home backup file of the user on the machine.

![Screenshot from 2023-05-09 08-13-40](https://github.com/MetricCode/MetricCode/assets/99975622/2fb35820-a880-47b8-b52a-db9fefd87f49)

Since we got nowhere with trying to crack the zip file's password, we can actually take a look at the compression and encryption details of this file.

If we use 7zip, we can see a lot more info on this using the `7z l -slt file.zip`

![Screenshot from 2023-05-09 08-21-28](https://github.com/MetricCode/MetricCode/assets/99975622/134495e2-92f7-4078-a23c-7ea1f02a85fa)

If we search on the `ZipCrypto delfate encryption Deflate` method on google, we can find an interesting article on medium explaining on how a certain person cracked the encrypted files that we're once leaked during a cyber attack(CONTI Ransomware source code leak).

CONTI ransomware, also known as ContiLocker, is a type of ransomware that belongs to the ransomware-as-a-service (RaaS) model. RaaS allows cybercriminals to rent or affiliate themselves with the ransomware and receive a portion of the ransom payments made by victims. CONTI ransomware has been associated with various high-profile attacks targeting organizations worldwide.

If we follow the article, the article calls this a plain text attack where we use a file which is oddly common in the zip. If we have it, we can use its contents to create a new key and use it to create a similar zip file in which we can set our own password and get the contents of the internal files.

First of all, we need to zip the identical file(.bash_history)...

![Screenshot from 2023-05-09 08-34-26](https://github.com/MetricCode/MetricCode/assets/99975622/8bd9df13-690d-4b20-82ac-8a64949da251)

After that, we need to git clone a specific tool ( bkcrack) and build it on our machine.

![Screenshot from 2023-05-09 08-44-10](https://github.com/MetricCode/MetricCode/assets/99975622/501357ab-e7db-464a-84a8-df376c9bada2)

