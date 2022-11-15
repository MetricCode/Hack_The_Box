# @author : M3t1c_r00t
Late is an easy box that requires on to get access to the id_rsa/ssh file to be able to get local access into the system and later on get root priviledges on the system. :)
Includes: SSTI (Server Side Template Injection) Of Python Flask 
![Late](https://user-images.githubusercontent.com/99975622/201908828-99106ceb-fb72-4673-8980-e6777168f405.png)


**Enumaration**
So we start with an Nmap Scan first to see the ports and we can see that there are only two ports open. 22 and 80.
![Screenshot_2022-11-11_10_31_36](https://user-images.githubusercontent.com/99975622/201910327-52e5f159-f162-4a35-a933-f765f36637a4.png)

Next we visit the webpage and we see a domain so we are going to add that into our /etc/hosts folder:

![Screenshot_2022-11-11_10_32_24](https://user-images.githubusercontent.com/99975622/201910489-08cac7d7-19c4-4b20-ac2c-efe3688c7836.png)

**sudo nano /etc/hosts**

![Screenshot_2022-11-11_10_32_45](https://user-images.githubusercontent.com/99975622/201911533-d3175fb6-be01-4652-9b52-0d171e6a1202.png)
I did a gobusterscan but i didnt get anything interesting but the basic files.
**gobuster dir -w /usr/share/wordlists/dirb/common.txt -u http://IP/ -o nmapscan.txt**
![Screenshot_2022-11-11_10_33_35](https://user-images.githubusercontent.com/99975622/201911658-3674bcaa-a5e3-44d7-8244-68c1c981593d.png)

So after that, i did a sub-domain enumeration using ffuf:
I used the subdomains-top1million-5000.txt file from Seclists...

![Screenshot_2022-11-11_10_33_55](https://user-images.githubusercontent.com/99975622/201911919-2e3a85b5-138c-47ec-800a-2e4412f83c64.png)
 and we found a subdomain, **images**.
 so next were gonna add the subdomain to our hosts file;
 ![Screenshot_2022-11-11_10_34_16](https://user-images.githubusercontent.com/99975622/201912409-8fcf9d7e-e7c9-41eb-8a81-25a5fede959e.png)

And on visiting the site, it seems to ben image to text converter.
So on viewing the site using the wappalyzer extension, we realise that the site is using a python based frame work, django.
On some googling, we find that we can use rce to reads the contents of the server...
![Screenshot_2022-11-11_10_35_11](https://user-images.githubusercontent.com/99975622/201913065-b0e0b7d8-c2ec-44fc-a6c1-f1f212f9b918.png)
 and the output is :**49** meaning that its vulnerable...
 
 ![Screenshot_2022-11-11_10_36_09](https://user-images.githubusercontent.com/99975622/201913205-16555632-b60e-4a70-9c7b-ad412f7c56c2.png)
 
 so i typed this command and took a screenshot, cropped the image and uploaded it to the site to be analyzed and in the output file, we can see the users via the **/etc/passwd** file contents.
 
 ![Screenshot_2022-11-11_10_37_24](https://user-images.githubusercontent.com/99975622/201915427-bd8688ad-4de2-4cfb-b00d-4927b0f7e4a0.png)

Now that we can see te users, lets try and look for the .ssh/id_rsa file for the svc_acc account. 

![idrsa](https://user-images.githubusercontent.com/99975622/201914089-23b4f39a-2966-4f22-a6b7-87c269ebe39b.png)

and here are the contents of the output...
I then renamed the file and tried to ssh directly into the svc_acc account and **voila!**
And we can view the contents of the user.txt flag.
![Screenshot_2022-11-11_10_38_21](https://user-images.githubusercontent.com/99975622/201914674-764f763f-f7e9-44ad-8e2c-b3c12da439d1.png)

So i tried poking around looking for other files, crontab and sudo -l priviledges but no luck.
So i went into my arsenal and pulled out the linpeas script and ran it against the system using a python http server and curl command and ...
![Screenshot_2022-11-11_10_39_24](https://user-images.githubusercontent.com/99975622/201916018-3242903b-d540-4072-a699-24dad02f7b61.png)
i found the that there was a file in the system that...
![Screenshot_2022-11-11_10_40_25](https://user-images.githubusercontent.com/99975622/201916217-3cfdb1a9-76d3-49f2-9f0c-8651fb5e15b7.png)
upon login of any ssh, executes as root and notices the root/admin user.
![Screenshot_2022-11-11_10_41_35](https://user-images.githubusercontent.com/99975622/201916253-00aac5f8-da1d-453e-90ea-780a4626092d.png)

Well, we can echo a reverse shell line to this file, log out then try ssh again using the svc_acc account and using a netcat listener gain root access...

![Screenshot_2022-11-11_10_46_48](https://user-images.githubusercontent.com/99975622/201916876-4814df8f-fd52-4a65-85d5-2181d1353584.png)

And we got root. 
:)
My socials: 
           @twitter: https://twitter.com/M3tr1c_root 
           @instagram: https://instagram.com/m3tr1c_r00t/

