# @author:M3tr1c_r00t
## Curling!
![Curling](https://user-images.githubusercontent.com/99975622/202869168-893257fe-43f1-4fee-8579-112d77190d0b.png)

### Enumeration
We run an nmap scan and find we have two ports that are open...
![Screenshot_2022-11-17_01_18_38](https://user-images.githubusercontent.com/99975622/202869187-75754eee-16da-49ea-b14c-d04801212ae8.png)

Lets move to firefox and check out the site...

![Screenshot_2022-11-17_01_20_40](https://user-images.githubusercontent.com/99975622/202869329-d5e58c2b-bce2-4748-82d4-56697e332400.png)
Note that after the article for 2018, there's a name :_floris_ maybe its a username?


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
![Screenshot_2022-11-17_01_21_50](https://user-images.githubusercontent.com/99975622/202870341-75902e2d-c274-4343-9fe0-15ba63d32303.png)

You can use the phpreverseshell from pentestmonkey 
![Screenshot_2022-11-17_01_22_25](https://user-images.githubusercontent.com/99975622/202870885-93a7b439-4b38-4869-b5fa-e7ca45fac49f.png)
and make sure to change the LHOST and LPORT ....

![Screenshot_2022-11-17_01_22_42](https://user-images.githubusercontent.com/99975622/202870894-e92cbce6-dc58-4f1a-974e-966846d56b62.png)

Set up a listener and run go to the index file and boom! 
You get your reverse shell....

![Screenshot_2022-11-17_01_23_29](https://user-images.githubusercontent.com/99975622/202870922-420ab6d2-4c5e-43a8-a380-fec91d4808dd.png)
Although we have the rev shell, permissions were limited. I ran linpeas and find the pwnkit vulnerability

![Screenshot_2022-11-17_01_26_33](https://user-images.githubusercontent.com/99975622/202870945-ab915181-b120-4a61-bcc6-dfeccc3ed6e9.png)
After uploading the python script, run the file and you get root.

![Screenshot_2022-11-17_01_28_41](https://user-images.githubusercontent.com/99975622/202870972-01cb5fd8-78e3-4526-8573-c3933dc96c40.png)
Now you can get your user and root flags!
And done!
### Socials
@Instagram:https://instagram.com/M3tr1c_r00t
<br>@Twitter:https://twitter.com/M3tr1c_root


