# Forge!
## @Author : M3tr1c_r00t

![Forge](https://user-images.githubusercontent.com/99975622/233685329-da538636-25c3-4dce-af76-c8106ab4ab09.png)

Forge is a medium ranked box which is fully centered on Server Side Request **Forge**ry.  For the foothold, we need to gain access to another sub-domain running on the server, get ftp creds and use them to be able to access the ssh-key to a user. For root, we need to use the python debugger to be able to execute commands.

### Enumeration
#### nmap...

```
# Nmap 7.80 scan initiated Fri Apr 21 17:28:56 2023 as: nmap -sC -sV -A -v -oN nmapscan.txt 10.129.195.213
Increasing send delay for 10.129.195.213 from 0 to 5 due to 55 out of 181 dropped probes since last increase.
Nmap scan report for 10.129.195.213
Host is up (0.16s latency).
Not shown: 997 closed ports
PORT   STATE    SERVICE VERSION
21/tcp filtered ftp
22/tcp open     ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open     http    Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Did not follow redirect to http://forge.htb
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Apr 21 17:29:57 2023 -- 1 IP address (1 host up) scanned in 61.49 seconds

```

#### dirsearch...

```
# Dirsearch started Fri Apr 21 17:31:35 2023 as: dirsearch.py -w /usr/share/wordlists/dirb/common.txt -u http://forge.htb -e php,txt,html,css,js -o /home/m3tr1c/Desktop/Forge/dsearch.txt

403   274B   http://forge.htb:80/server-status
301   307B   http://forge.htb:80/static    -> REDIRECTS TO: http://forge.htb/static/
200   929B   http://forge.htb:80/upload
301   224B   http://forge.htb:80/uploads    -> REDIRECTS TO: http://forge.htb/uploads/

```

#### sub-domain enumeration...

![Screenshot from 2023-04-21 17-39-37](https://user-images.githubusercontent.com/99975622/233686389-5649a98a-a219-4edb-9432-2603fb560868.png)

### Foothold
Since there is a web-server, we can check it out. You need to add the ip to route to `forge.htb` in the /etc/hosts file.

![Screenshot from 2023-04-21 18-10-33](https://user-images.githubusercontent.com/99975622/233686575-9f6adee2-2e38-4ed3-84d0-a5e1bb9ea195.png)

It seems to be an static image profiling page.  We can click on the `upload an image` section and we get redirected to a section which we can use to to upload images.

![Screenshot from 2023-04-21 18-10-58](https://user-images.githubusercontent.com/99975622/233686994-77bf0ada-2d29-41f1-a181-873b48b42726.png)

Since my sub-domain scan was done and found a sub-domain, i tried to access it but no luck. It seemed only to be accessible to localhost.


![Screenshot from 2023-04-21 18-24-01](https://user-images.githubusercontent.com/99975622/233690037-19a57975-9871-4e6e-a7bb-6f5c083655a6.png)

If we upload an image, we can see that it gets renamed probably with a random function and we can view the image. 

![Screenshot from 2023-04-21 18-13-08](https://user-images.githubusercontent.com/99975622/233687274-900c8113-7e70-4f7c-8ae0-2479ae3fe26b.png)


The upload functionality doesnt seem to mind the file type. this is probably because the web-server may be running a python based application for the site(as we cannot fully determine the technology in the backend).

![Screenshot from 2023-04-21 18-14-06](https://user-images.githubusercontent.com/99975622/233687350-8ec56043-c44a-41fa-a2b4-e7fcbfc9f9e6.png)

I tried to see if the randomly generated bits were some type of encoding or hash but it turned out to be some random stuff generated.

![Screenshot from 2023-04-21 18-15-26](https://user-images.githubusercontent.com/99975622/233687802-830858d5-f679-403b-8a66-2bdd343278f8.png)


Since there was an upload using an url option available, we can try and use it. I set up a listener using nc so that i could see the headers. And we already confirmed it is using python-requests.
![Screenshot from 2023-04-21 18-15-26](https://user-images.githubusercontent.com/99975622/233689299-c4a7ac6b-7d9f-4b36-8be7-ac6737b25fb2.png)

I tried to access 127.0.0.1, localhost and forge.htb but we got a response saying the url's are black listed.
![Screenshot from 2023-04-21 18-21-30](https://user-images.githubusercontent.com/99975622/233689239-e6216031-a7e0-4cb2-94b6-3e29a1fc5db4.png)


We can try a couple of things to bypass this one being using wierd casing and this works.
![Screenshot from 2023-04-21 18-22-04](https://user-images.githubusercontent.com/99975622/233689496-274425bf-1664-4021-b199-4fce7ae18f95.png)

Since this works, we can try to access the admin sub-domain which seems to be accessible only to the localhost. 

![Screenshot from 2023-04-21 18-23-12](https://user-images.githubusercontent.com/99975622/233690197-c1322340-58bf-4577-a0f3-16ee9091c01a.png)

Since this wasn't accessible through the browser, we can use curl and see its contents. We can see there is an announcements directory and we can access it.

![Screenshot from 2023-04-21 18-34-31](https://user-images.githubusercontent.com/99975622/233720798-b49f4afb-aa01-453d-9a7f-59d7eb30b5f4.png)


On taking a look at the announcements, we can see that we can actually access ftp using some credentials which we are given.
We can actually use the ftp creds and see the files that are in the ftp root. For this we are going to have to  hex encode the localhost ip.
So, the payload will be like;
```
http://Admin.ForgE.Htb/upload?u=ftp://user:creds@0x7f.0.0.1
```
So we can send the request and we can see the possible home directory to the `user`s home directory.
![Screenshot from 2023-04-21 18-51-39](https://user-images.githubusercontent.com/99975622/233723008-c6e90454-5326-4671-b54e-6f6bb1bfd934.png)

Since we already got this, we can actually check to see if we have the .ssh directory.

Note that if we dont give the url a trailing `/` , we are going to get an error as ftp isn't `smart enough` to do the redirection like http.

```
http://Admin.ForgE.Htb/upload?u=ftp://user:creds@0x7f.0.0.1/.ssh/
```
![Screenshot from 2023-04-21 18-52-57](https://user-images.githubusercontent.com/99975622/233723385-a041ccc1-1416-4455-97da-e2d0b8c5f55a.png)


Since it exists, we can get the `id_rsa` file.

![Screenshot from 2023-04-21 18-54-04](https://user-images.githubusercontent.com/99975622/233723503-22586217-9730-440b-a301-1fccc6898d50.png)

And log into ssh as user, we get the user flag.

![Screenshot from 2023-04-21 18-54-50](https://user-images.githubusercontent.com/99975622/233723928-b928a4f1-2a10-4ed6-8344-290b5cbb9d1d.png)

### user to root
So if we run `sudo -l`, we can see that we can run a script as root.
![Screenshot from 2023-04-21 18-55-08](https://user-images.githubusercontent.com/99975622/233724729-9e66cf97-8305-4aef-b558-1535c7721365.png)

We can take a look at the contents of the script and see what is does.

![Screenshot from 2023-04-21 18-55-29](https://user-images.githubusercontent.com/99975622/233725262-01c88795-317b-489a-9257-e7204a824842.png)

#### Explanation of What the code is doing...
The script creates a server application that listens for incoming connections on a randomly selected port between 1025 and 65535 on the loopback IP address (127.0.0.1). 

When a client connects to the server, the client is prompted to enter the secret password. If the password is correct, we are given a couple of commands options and they are then executed and the output displayed to us on our end.

If an exception(error) is raised, the script enters debug mode to help diagnose and fix the issue. This is because the pdb debugger is being summoned at that point.

Finally, the `quit()` function is called to terminate the script.

We need to note that anytime we are dropped into the pdb debugger, we are being dropped directly into a python shell and so we can execute any python commands in it.


So, in this case, we need to cause the script to error out and drop us into the debugger.

To do this, we need to login to the machine with another tty session so that we may be able to access the opened port.

After that, we can cause the system to error out by providing a string in the int part of the script then we will be dropped into the debugger.

![Screenshot from 2023-04-21 18-58-39](https://user-images.githubusercontent.com/99975622/233726856-abda88a1-333c-4ee0-8985-58eaccb3c2a7.png)

We can then spawn a shell.

![Screenshot from 2023-04-21 18-59-19](https://user-images.githubusercontent.com/99975622/233727613-8419f423-1e84-4f8a-8de4-229f7c569bbd.png)
And done!

### Extra ...
There was a clean-up script running in the root's cron tab to remove all files in the /uploads directory.

![Screenshot from 2023-04-21 19-02-49](https://user-images.githubusercontent.com/99975622/233727626-e76b0ecd-7049-419b-841d-085a8b4d74ed.png)


## My socials:
<br>@ twitter: https://twitter.com/M3tr1c_r00t
<br>@ instagram: https://instagram.com/m3tr1c_r00t/
