# @author : M3tr1c_r00t
## Knife!
![Knife](https://user-images.githubusercontent.com/99975622/205171408-986819ef-de19-4cd3-a2c3-bd2a526d5009.png)
Knife is a easy linux box which on upon careful enumeration, there's an ucommon header in the site response which we use to get our reverse shell and gain user priviledges; and use gtfobins to get root user.

### Enumeration

_**nmap scan**_
![Screenshot_2022-11-20_22_21_28](https://user-images.githubusercontent.com/99975622/205172448-a4941442-42be-4047-a750-e635d0b2e81e.png)
There's not much really in the nmap scan.
<br> There are 2 ports open: ssh and port 80 http.

### Priv Escalation

After forwading the sites, response into burpsuite repeater tab, i noticed there was an odd header in the response.
<br> **X-Powered-By: PHP/8.1.0-dev**

After a bit of recon, i found some pieces of information which helped me to be able to get a vulnerability and exploit it.
![image](https://user-images.githubusercontent.com/99975622/205173766-ffba65a2-3295-40c4-88f2-210e8e74c52d.png)
The X-Powered-By header provides information on the technologies being used by the webserver.

After a bit more of recon ...
![image](https://user-images.githubusercontent.com/99975622/205174156-e7237beb-241c-4f59-a035-625f1274b283.png)
After inspecting the code on exploit db, we find out that the script sends a request after adding a new heading, "User-Agentt":zerodiumsystem('" + cmd + "')
![image](https://user-images.githubusercontent.com/99975622/205174749-00e151ab-93a0-4310-b3ab-c3d450e7757b.png)
Instead of using the script, i opted to do this manually so that i could get a bigger picture on what was happening.
![Screenshot_2022-11-20_22_02_13](https://user-images.githubusercontent.com/99975622/205175036-9f3be441-3bd6-4ad6-a1a1-96b2305ca7a1.png)
I tried working with the curl command to see if i get a connection and boom! 
<br>Next up, lets get our reverse shell....
![Screenshot_2022-11-20_22_09_33](https://user-images.githubusercontent.com/99975622/205175183-0a473c14-2ee2-4549-8e9a-1de3592e08b5.png)
After we get our reverseshell, we are logged in as James.
<br> Navigate to his home directory and you can get the user flag.
![Screenshot_2022-11-20_22_10_50](https://user-images.githubusercontent.com/99975622/205175376-bfcbd247-f22a-4c38-a95f-b729a2272d18.png)

On running sudo -l to see what commands we can run as root, we note that we can run the knife binary as root.
<br> Heading over to gtfobins, we find the suid of the knife binary....
![Screenshot_2022-11-20_22_12_03](https://user-images.githubusercontent.com/99975622/205175616-5be526f6-8106-474d-91bc-03a5c5ec4caa.png)
And we are root!
Get your root flag and done!
![Screenshot_2022-11-20_22_12_17](https://user-images.githubusercontent.com/99975622/205175694-aabcdefc-cba0-4396-902d-1bfd1dbe7863.png)

### Socials
@Instagram:https://instagram.com/M3tr1c_r00t
<br>@Twitter:https://twitter.com/M3tr1c_root
