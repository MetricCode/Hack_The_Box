# @Author : M3tr1c_r00t
## Legacy!
![Legacy](https://user-images.githubusercontent.com/99975622/207712369-1773e8bb-c99e-4e6c-85bc-61b41e135ced.png)

<br>Legacy is a Windows XP box which has a vulnerable smb service and is exploitable using metasploit to gain root priviledges to gain our flags...
### Enumeration ...
_**Nmap**_
<br>
![Screenshot_2022-11-11_16_15_22](https://user-images.githubusercontent.com/99975622/207712918-c7410f29-a937-4961-b84a-7f8d5d79cd79.png)
From our scan results, we can see that there is an smb service that is which has message_signing disabled and has been marked dangerous by nmap default scripts...
<br> With this information, we can go to google and search for any known exploits as the os enumeration brings it out to be "Windows XP" for smb .....
<br>
![Screenshot_2022-11-11_16_16_19](https://user-images.githubusercontent.com/99975622/207713692-457bb3b6-aa55-48f9-b064-a05f53efe45c.png)

And we find one using metasploit console...
![Screenshot_2022-11-11_16_16_25](https://user-images.githubusercontent.com/99975622/207713743-e426a8fa-7aaa-40f1-8c82-5beb2e899a74.png)

### Gaining Access ...
Launching metasploit and setting up the options...
![Screenshot_2022-11-11_16_17_01](https://user-images.githubusercontent.com/99975622/207713822-b95bd0a2-b132-4a9b-ad5c-2772209fce25.png)
And we have our meterpreter session...
![Screenshot_2022-11-11_16_18_07](https://user-images.githubusercontent.com/99975622/207713983-a86742e9-5018-4b8f-8095-070f6075c9c5.png)

And with that we have Administrator priviledges...
```
net user // shows you are the Authority system user 
```
![Screenshot_2022-11-11_16_18_50](https://user-images.githubusercontent.com/99975622/207714274-22f50060-3996-47ad-a447-ad2a18e83c4e.png)


#### Getting user flag....
![Screenshot_2022-11-11_16_19_09](https://user-images.githubusercontent.com/99975622/207714204-31189c82-a4d0-46ec-80b6-c49e5f7ce04d.png)
#### Getting root flag....
![Screenshot_2022-11-11_16_19_38](https://user-images.githubusercontent.com/99975622/207714638-2e518b2b-630f-4144-b8e7-24c74e15a4d9.png)
And Done!

### Socials
@Instagram : https://instagram.com/M3tr1c_r00t
<br>@Twitter : https://twitter.com/M3tr1c_root
