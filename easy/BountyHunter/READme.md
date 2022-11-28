# @author : M3tr1c_r00t
## BountyHunter!
![BountyHunter](https://user-images.githubusercontent.com/99975622/204362290-57dd3f77-0c4a-4761-bcd4-76c1fa21dbdd.png)

### Enumeration...
So as always we start with an nmap scan.....
![Screenshot_2022-11-22_00_19_21](https://user-images.githubusercontent.com/99975622/204362544-3d1f83c2-e0c7-44fb-84d3-8e55aa21a597.png)
We can that there are 2 ports open.... ssh and port 80.

Gobusterscan
After running a gobuster scan,we find a couple of directories which we could check out...
![Screenshot_2022-11-22_00_19_11](https://user-images.githubusercontent.com/99975622/204362796-ae3b0889-5ed1-4685-a4be-0da476983f91.png)

### XXE Vulnerability
![image](https://user-images.githubusercontent.com/99975622/204363407-cb28d4a3-abf8-4cb9-be8f-9c392b877e56.png)
After checking out the site, we find there's a submit page which sent data in form of a base64 encoded xml format.
After finding out about thid while using burpsuite, we can try using the basic xxe and we achieved Arbibrary file read....
On this same account, i made a python script which allows for file read and only outputs the file read contents....
''
test
''
