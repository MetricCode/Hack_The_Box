# @author : M3tr1c_r00t
## Jerry!
![Jerry](https://user-images.githubusercontent.com/99975622/205442474-25afc218-0207-44c6-bf8b-d990b913c08f.png)
JErry is said to be one of the easiest boxes on hack the box.
<br>Its a windows box that uses metasploit to gain access and gain root priviledges!

### Enumeration...
As always we start with an nmap scan followed by a gobuster....
![Screenshot_2022-11-10_13_34_20](https://user-images.githubusercontent.com/99975622/205442549-eff03c8e-86d3-4ab5-89bc-6e276c712b15.png)
After the nmap, we can see that we have only one port open, port 8080.

![Screenshot_2022-11-10_13_55_32](https://user-images.githubusercontent.com/99975622/205442568-1ff4dd9c-1e9e-413d-88ad-f0892c9a465f.png)
on looking at the gobuster scan results, we can see there is a manager director which turns out to be a login page. 
![Screenshot_2022-11-10_13_56_15](https://user-images.githubusercontent.com/99975622/205442660-e0501098-d7c2-4c77-9fd1-fc165f4f1222.png)
After looking at the error page handling, we can see that the creds are being revealed to us!
![Screenshot_2022-11-10_13_57_09](https://user-images.githubusercontent.com/99975622/205442749-5733ba88-b633-41bb-907c-6389e55005cb.png)

<br> We can the visit th page directory once again and enter the creds and boom! we're in!
![Screenshot_2022-11-10_13_57_16](https://user-images.githubusercontent.com/99975622/205442753-d21aabbd-9bf3-40e9-984a-b1209c716f31.png)
After googling, we can see that we can create a payload using msfvenom which will help us to get a reverse shell.
![Screenshot_2022-11-10_14_22_44](https://user-images.githubusercontent.com/99975622/205442866-0c1a7d72-36f3-484b-a788-39a587e20d44.png)
After making our paload, we can now upload it via the manager site.
![Screenshot_2022-11-10_14_10_37](https://user-images.githubusercontent.com/99975622/205442918-9bc50632-b8dc-42d5-972c-208023d39876.png)
Next up, lets set up our listener and we can visit our payload via the upload directory and boom!, we got our reverse shell.
![Screenshot_2022-11-10_14_12_50](https://user-images.githubusercontent.com/99975622/205442965-3526e9cd-0ddd-4e3f-b29b-edc28145ae7f.png)
![Screenshot_2022-11-10_14_16_00](https://user-images.githubusercontent.com/99975622/205443036-51584892-f780-4434-8180-a88743760032.png)

