# @author : M3tr1c_r00t
## RedPanda!
![RedPanda](https://user-images.githubusercontent.com/99975622/205444975-3447a92f-d56f-4465-9544-52a6585c047a.png)


### Enumeration...
nmap
![Screenshot_2022-11-20_15_38_51](https://user-images.githubusercontent.com/99975622/205445009-3f8ddebc-3c24-46b9-9fac-2c42433e57c1.png)
Looking at the nmap scan, only two ports are open...
Not having anything to useful from the nmap scan, lets visit the webpage and have a look at it.
![Screenshot_2022-11-20_15_39_16](https://user-images.githubusercontent.com/99975622/205445026-5d27a9dc-1c1a-43ae-be88-ec79661dc98a.png)
The site asks for some input for a panda name,  but it only seems to give output on some specific ones in its database.
On just sending empty data, we get a response...
![Screenshot_2022-11-20_15_39_25](https://user-images.githubusercontent.com/99975622/205445029-82573e84-7b15-4627-ae13-a4b8bca79b31.png)

After a bit of interaction with the site, i finally got a hold on how to gain access onto the system....
Plus, if you would have checked your wappalyzer extension, you would have noticed the system was running on a java kind of framework...

### SSTI
Finally got a foothold to work upon....
![image](https://user-images.githubusercontent.com/99975622/205456530-7d222419-936b-4b8c-af3b-5051c5ec7a92.png)
On trying to see id there's a SSTI vulnerability, if realized we could get a response while using the "*" special character...

![Screenshot_2022-11-20_15_40_23](https://user-images.githubusercontent.com/99975622/205445039-26d98841-5551-4ea9-9a22-6e75a0db605f.png)

Getting reverse shell,
uploading our reverse shell script.
![Screenshot_2022-11-20_15_46_11](https://user-images.githubusercontent.com/99975622/205445066-872fe492-1a70-4280-8216-943e0b4a325f.png)


Getting our reverse shell...



Getting user flag....



### Priviledge Escalation...



