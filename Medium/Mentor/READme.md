# Mentor!
## @Author : M3tr1c_r00t
![Mentor](https://user-images.githubusercontent.com/99975622/219680029-178a4abe-213d-4d6f-8b44-2a1efeb6711c.png)

### Enumeration...
#### Nmap
```
# Nmap 7.92 scan initiated Sun Dec 11 21:39:49 2022 as: nmap -sC -sV -A -p 22,80 -oN nmapports.txt 10.129.84.239
Nmap scan report for mentorquotes.htb (10.129.84.239)
Host is up (0.23s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 c7:3b:fc:3c:f9:ce:ee:8b:48:18:d5:d1:af:8e:c2:bb (ECDSA)
|_  256 44:40:08:4c:0e:cb:d4:f1:8e:7e:ed:a8:5c:68:a4:f7 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: MentorQuotes
| http-server-header: 
|   Apache/2.4.52 (Ubuntu)
|_  Werkzeug/2.0.3 Python/3.6.9
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 4.15 - 5.6 (95%), Linux 5.3 - 5.4 (95%), Linux 2.6.32 (95%), Linux 5.0 - 5.3 (95%), Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 5.0 - 5.4 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT       ADDRESS
1   326.20 ms 10.10.14.1
2   326.45 ms mentorquotes.htb (10.129.84.239)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Dec 11 21:40:13 2022 -- 1 IP address (1 host up) scanned in 24.05 seconds
```
#### Gobusterscan...
Wierdly enough, the gobuster plus other tools like dirsearch and ffuf didnt find any files/directories so next up we can do a sub-domain scan.
```
/server-status       [33m (Status: 403)[0m [Size: 281]
```

![image](https://user-images.githubusercontent.com/99975622/219688606-b97621ac-40df-41e9-bf7b-b357897120e7.png)

#### Vhost/Sub-Domain Bruteforce
![Screenshot_2022-12-12_02_03_44](https://user-images.githubusercontent.com/99975622/219690041-e7f6b81d-1bc5-4ccd-ac91-f00baaf40c18.png)

add the ```api.mentorquotes.htb``` to your /etc/hosts file then we can continue with our enumeration.

#### directory bruteforce on the discovered sub-domain
we can fuzz for the api endpoints and we found some interesting onces.
![Screenshot_2022-12-12_02_30_51](https://user-images.githubusercontent.com/99975622/219691220-fe4705f9-ed52-437d-9e4b-cbbcc839f1e1.png)

We can try and check the docs part since it may have interesting pointers.
![Screenshot_2022-12-12_02_10_56](https://user-images.githubusercontent.com/99975622/219692286-70e8f114-120e-4cc2-8ad6-a43305df1c68.png)

At least we've found a way to interact with the api application. We can try to interact with the system by creating a user.
![Screenshot_2022-12-12_02_16_24](https://user-images.githubusercontent.com/99975622/219693753-88dffaa7-7c9a-4192-946e-d6d4fd038bd6.png)

After creating a user, we need to login so that we can get our api-token to enable us to be able to interact with the api effectively.
![Screenshot_2022-12-12_02_22_26](https://user-images.githubusercontent.com/99975622/219694096-54e1c5f7-d237-4bee-991b-ec87b19d187b.png)

We can now add the api to our request headers whenever we are making a request and we can now further interact with the api.
```
Authorization: YOUR_API_TOKEN
```
On checking out the /quotes/ endpoint, we find the same quotes that were being served on the static site.
![Screenshot_2022-12-12_02_42_02](https://user-images.githubusercontent.com/99975622/219694869-71086d88-a323-4665-b115-d472d5db1800.png)
We can try to interact with the /users/ endpoint but we seem not to be authorized.
![Screenshot_2022-12-12_02_44_08](https://user-images.githubusercontent.com/99975622/219695381-a331c960-34a4-4ba5-a062-1288ef667a2d.png)

If you noticed in the docs endpoint, there was a username ...
![image](https://user-images.githubusercontent.com/99975622/219713456-d466d14e-0fdc-4781-bf51-f811ea34e0e6.png)
So james is a possible username.
We can try to bypass the authentication by creating a new user with his same name and see if this works...
![Screenshot_2022-12-12_03_21_52](https://user-images.githubusercontent.com/99975622/219715093-bb929d8e-62cc-4c3b-8afd-b1ab45243dc9.png)
lets now get our api-token... 
![Screenshot_2022-12-12_03_21_56](https://user-images.githubusercontent.com/99975622/219715334-6cffafab-fdf2-4c6a-98ce-38c3ae85aea7.png)

and try to get to the /users endpoint
![Screenshot_2022-12-12_03_21_59](https://user-images.githubusercontent.com/99975622/219715440-e6eccb81-c7dd-4407-b759-ae82ca20bcd8.png)
Nice! it worked. 

Let's try and see if we can access the /admin endpoint...
![Screenshot_2022-12-12_03_23_27](https://user-images.githubusercontent.com/99975622/219716324-07b282c4-9252-4402-bdac-c5b1eaad1386.png)
noice.
We find that there are other endpoints which didn't turn up in the bruteforce results but we can now interact with them.

On visiting the first one, it seems not to have any valuable data.
![Screenshot_2022-12-12_03_27_22](https://user-images.githubusercontent.com/99975622/219717183-ea113fab-e961-49dd-b67f-61570e20b417.png)

If we check the next...
![Screenshot_2022-12-12_03_32_29](https://user-images.githubusercontent.com/99975622/219850539-212f9283-be0c-4be8-9504-9c3f014a7fa0.png)

The api needs 2 entries, body and data... With this info, we can try to get an rce using backticks and were in!
```
https://www.wallarm.com/what/how-to-hack-api-in-60-minutes-with-open-source
```
### Lateral Movement
After getting a reverse shell, we find ourselves in a docker container.
Luckily enough, we can get the user flag.
![Screenshot_2022-12-12_03_33_41](https://user-images.githubusercontent.com/99975622/219850484-1c8904ba-e4a7-4b92-a81d-8317d02739a6.png)

After looking around in the file system of the server, I found some database credentials for the postgress server...
![Screenshot_2022-12-12_03_49_35](https://user-images.githubusercontent.com/99975622/219850995-5add89c8-f082-47ca-9ae8-06093983c3b4.png)
I decided to check the open ports on the docker container and i found only one internal service.
I assumed this to be the postgres service running since the normal port for postgres is ``` 5432```
![Screenshot_2022-12-12_10_36_18](https://user-images.githubusercontent.com/99975622/219851124-735a9d6a-87cc-4c08-95a2-b5eeea4f58f3.png)

I then used the chisel binary to do a port forwarding so that we could access the service.
After port forwarding, login to the postgres service using psql and we find some hashed creds which seem to be md5
![Screenshot_2022-12-12_11_31_34](https://user-images.githubusercontent.com/99975622/219851208-45df495d-3083-4321-9803-34f65a5b8255.png)
I then cracked the svc password as james' password wasnt crackable.
![Screenshot_2022-12-12_12_22_55](https://user-images.githubusercontent.com/99975622/219851266-820895cb-0a5d-4a62-9e0b-86994450da89.png)

and we could login as the svc user via ssh.
![Screenshot_2022-12-12_13_18_09](https://user-images.githubusercontent.com/99975622/219851865-df80a05d-d537-4aca-950d-5c46f4fd6932.png)
### Svc to James
After a bit of dead ends with further enumeration, i decided to try and look for a password in any possible file using the grep command.
And wierdly enough, I found the password in ```/etc/snmp/snmpd.conf```
![Screenshot_2022-12-12_14_24_49](https://user-images.githubusercontent.com/99975622/219851920-478e2af4-eae8-41b7-b9dd-37cbcf0f1564.png)

### James to Root
Just check the sudo permissions and turns out we can run the /bin/sh as root.
Basically giving us access to root directly.
![Screenshot_2022-12-12_14_24_49](https://user-images.githubusercontent.com/99975622/219851920-478e2af4-eae8-41b7-b9dd-37cbcf0f1564.png)

And Done!

## My socials:
<br>@ twitter: https://twitter.com/M3tr1c_root
<br>@ instagram: https://instagram.com/m3tr1c_r00t/
