# @author : M3tr1c_r00t
Lame is a Retired Hack the box Easy Machine

![Lame](https://user-images.githubusercontent.com/99975622/201052773-ca562c51-cb0c-4d9c-8183-0dd4b6734077.png)

Well, we start by enumarating the Machine:
![Screenshot_2022-11-09_20_58_23](https://user-images.githubusercontent.com/99975622/201049482-4b978a46-1d70-4868-97c6-ebfed2d03e5c.png)

We see that there is anonymous login but there is nothing important there.
 There is openssh though we need creds to login.
 
 Well, look at the smb Samba 3.0.20 - Debian in the host script discovery.
So lets visit our good old friend google and see what goodies are there...

![Screenshot_2022-11-09_20_59_08](https://user-images.githubusercontent.com/99975622/201050322-66f533c1-d1bd-47f7-9f3f-bb96e772ef9f.png)
 On clicking the samba vulnerabilities page, we can see on the public exploits page of the infosec website that we can use metasploit and try to see if we can gain access to the system 
 
 ![Screenshot_2022-11-09_20_59_30](https://user-images.githubusercontent.com/99975622/201050672-4bde789b-20fe-461b-b41e-4e16a324ab31.png)

So lets try this...

Run metasploit.
on metasploit: use exploit/multi/samba/usermap_script
then: show options
Set the LHOST to the hackthebox machine's IP
set RHOSTS to your IP
NB :If you dont know your IP, type ifconfig on the terminal then check the inet of tun0 or tun1.
Then set the RPORT to the port in which the smb server is open on the htb machine; which in our case according to the nmap scan is 445
![Screenshot_2022-11-09_21_04_35](https://user-images.githubusercontent.com/99975622/201051343-077b5a5d-e208-4e8f-9b30-087275736f75.png)


After setting all that, type: 'run' or 'exploit'
![Screenshot_2022-11-09_21_05_19](https://user-images.githubusercontent.com/99975622/201051744-08840251-68a4-45ca-8465-5fc25d014676.png)


after a while, type id to confirm the exploit works and you can see that you are root.
 
NB: You can upgrade the shell to a bash shell by typing shell.
lets find the user.txt flag
cd into /home/makis and you find the user flag.
![Screenshot_2022-11-09_21_06_04](https://user-images.githubusercontent.com/99975622/201052188-c46eb092-2602-4371-91c9-4069bbd62603.png)
cd into /root and cat root.txt to get the root flag.
![Screenshot_2022-11-09_21_06_24](https://user-images.githubusercontent.com/99975622/201052338-e6b2a061-23b0-467d-816b-29361b7ad6f9.png)

And done!
My socials:
          @ twitter: twitter.com/M3tr1c_root
          @ instagram: instagram.com/m3tr1c_r00t/


