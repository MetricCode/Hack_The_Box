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
