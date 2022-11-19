# @author:M3tr1c_r00t
## Curling!
![Curling](https://user-images.githubusercontent.com/99975622/202869168-893257fe-43f1-4fee-8579-112d77190d0b.png)

### Enumeration
We run an nmap scan and find we have two ports that are open...
![Screenshot_2022-11-17_01_18_38](https://user-images.githubusercontent.com/99975622/202869187-75754eee-16da-49ea-b14c-d04801212ae8.png)

Lets move to firefox and check out the site...

![Screenshot_2022-11-17_01_20_40](https://user-images.githubusercontent.com/99975622/202869329-d5e58c2b-bce2-4748-82d4-56697e332400.png)
**Note ** that after the article for 2018, there's a name :_floris_ maybe its a username?


Running a gobusterscan we find some interesting directories...
![Screenshot_2022-11-17_01_18_49](https://user-images.githubusercontent.com/99975622/202869222-c14146f7-a977-49c8-889a-9d3a28cbce80.png)

I ran the gobuterscan again using -x txt,php and found a file: **secret.txt**
![Screenshot_2022-11-17_01_19_52](https://user-images.githubusercontent.com/99975622/202869257-d30c54bd-5f3c-45cf-bb47-afee26f9d127.png)

It was hashed in base64.
![Screenshot_2022-11-17_01_20_20](https://user-images.githubusercontent.com/99975622/202869282-cfbff554-9870-44e5-bf80-f9fc57b72f48.png)
On decrypting, we find a credential which seems to be a password...
On the joomla login page, we try the username as _floris_ and the password as _Curling2018!_ and it works!

We also see something interesting at the bottom right corner of the site. Its the joomla version. _**Joomla 3.8.8**_

After a bit of googling, we find out that the joomla version has a vulnerability that allows for RCE... via the templates and can help us to get a reverse shell 
![Screenshot_2022-11-17_01_21_38](https://user-images.githubusercontent.com/99975622/202869914-2e9cfd1c-813e-4424-aa6f-deddeb1d4502.png)
I chose the B33z template and modified the index.php file 

