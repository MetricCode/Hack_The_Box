# @author : M3tr1c_r00t
## Devel!
![Devel](https://user-images.githubusercontent.com/99975622/204380944-af3dabdc-24f2-44ec-be04-5f0b343dacd4.png)

Devel is an easy Windows machine which is vulnerable to ftp file upload to get a shell using msfvenom payload and metasploit.
### Enumeration
![Screenshot_2022-11-11_18_04_59](https://user-images.githubusercontent.com/99975622/204376005-883f40a8-d140-42b7-84ad-ac9ca95d7358.png)
We find that there are 2 ports open ftp and port 80.
After going through the FTP, we find that the files in the ftp are the same files in the website.

This then allows us to upload files and we can get a reverse shell.

So. we are going to make a payload using msfvenom and upload it to the ftp service.
![Screenshot_2022-11-11_18_11_22](https://user-images.githubusercontent.com/99975622/204377079-fb4ac6c2-bfd6-4586-b2c2-58b16a6786a7.png)
Were gonna use the aspx format coz that's the normal format for windows machine websites.

Next up, uploading the payload to the FTP service;....
![Screenshot_2022-11-11_18_12_00](https://user-images.githubusercontent.com/99975622/204377887-332db2e7-5a74-4109-996c-ab37b77e5fe6.png)

Next up, were gonna open up metasploit, move to exploits/multi/handler and set our payload to windows/meterpreter/reverse_tcp which should be simlar to our msfvenom payload.

Then update the options by setting up your LHOST and then we can run our exploit and we get a meterpreter shell after accessing our payload through the site!
![Screenshot_2022-11-11_18_22_04](https://user-images.githubusercontent.com/99975622/204378517-f409f4e6-5c93-49fa-8a29-71cf8266b0db.png)

One of the reasons why i like using metasploit is because as soon as you get your meterpreter shell, most of your seesions will already have root escalation.

And on that note, we are root. We can get our flags!
![Screenshot_2022-11-11_18_24_22](https://user-images.githubusercontent.com/99975622/204378985-d73d7c86-cd8a-4e3a-9975-e73cee2eacf9.png)

If in your session you weren't root, you can upgrade to root using the local exploit suggester module on metasploit.

First of all, background your current meterpreter session,and then use multi/recon/local_exploit_suggester.

Set your session id to your background session.

You can check your sessions by typing sessions, then run the module....
![Screenshot_2022-11-11_18_26_54](https://user-images.githubusercontent.com/99975622/204380601-8751c300-7ef8-4014-858f-b13a0b580b48.png)
After it completes checking, it will escalate your priviledges to root user by following the prompts{if any ;)}
![Screenshot_2022-11-11_18_30_36](https://user-images.githubusercontent.com/99975622/204380768-9de2019a-4646-46a5-b813-b4f7343a1a7c.png)
And Done!
### Socials
@Instagram:https://instagram.com/M3tr1c_r00t
<br>@Twitter:https://twitter.com/M3tr1c_root

