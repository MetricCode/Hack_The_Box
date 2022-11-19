# @author : M3tr1c_r00t

![Armageddon](https://user-images.githubusercontent.com/99975622/202858878-ea0fc53e-b726-4ea8-acf9-bcfb43175592.png)

Enumeration
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


 



