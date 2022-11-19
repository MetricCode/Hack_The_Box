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

![Screenshot_2022-11-19_18_49_42](https://user-images.githubusercontent.chttps://github.com/MetricCode/Hack_The_Box/tree/main/easy/Armageddonom/99975622/202859434-c027d979-74ff-445d-bf5c-ca1e95ba01fa.png)
