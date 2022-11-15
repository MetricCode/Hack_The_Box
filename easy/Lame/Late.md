# @author : M3t1c_r00t
Late is an easy box that requires on to get access to the id_rsa/ssh file to be able to get local access into the system and later on get root priviledges on the system. :)
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
 
![etc passwd](https://user-images.githubusercontent.com/99975622/201913678-0366373f-954a-43e7-9106-a8843a6![Screenshot_2022-11-11_10_36_57](https://user-images.githubusercontent.com/99975622/201913767-3e2e2554-4591-415b-8e7e-dcdaa01a08d4.png)
04bcc.png)

Now that we can see te users, lets try and look for the .ssh/id_rsa file for the svc_acc account. 

![idrsa](https://user-images.githubusercontent.com/99975622/201914089-23b4f39a-2966-4f22-a6b7-87c269ebe39b.png)

and here are the contents of the output...
I then renamed the file and tried to ssh directly into the svc_acc account and **voila!**
And we can view the contents of the user.txt flag.
![Screenshot_2022-11-11_10_38_21](https://user-images.githubusercontent.com/99975622/201914674-764f763f-f7e9-44ad-8e2c-b3c12da439d1.png)

