CodeIgniterXor
==============

PoC script to decode CodeIgniter &lt;= 2.1.4 session cookies that use _xor_encode() method.

Full details availalbe on on the following blog post: https://www.dionach.com/blog/codeigniter-session-decoding-vulnerability


Usage
=====
break.py
This is the main script, and given a target URI will attempt to obtain a cookie and brute force the session key. If this script finds a cookie but fails to decrypt it then the server has Mcrypt installed, and is not vulnerable to the attack.
testkey.py
This script will instantly decode a session cookie using the provided (hashed) key (which needs to be added to the script once it has been obtained using break.py.
encrypt.php
This script is based on the encryption functions used by CodeIgniter, and will take an unencrypted cookie (a serialized PHP array) and encrypt it using the provided key (which needs to be added to the script).

The steps to attack an application are as follows:

1. Use break.py to crack the encryption key used by the application
2. Add this key to testkey.py and encrypt.php
3. Browse to the website to create a valid cookie for your IP/UserAgent
3. Decrypt this cookie with testkey.py
5. Make any desired modifications to the cookie manually, or by patching encrypt.php to add/modify array elements before re-encrypting.
6. Re-encrypt the session cookie and paste it back into your browser.
