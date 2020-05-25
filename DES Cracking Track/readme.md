# DES Cracking challenge from Northsec 2020

This challenge started with a webpage hosting a table with a list of student marks on it, and a form to submit "student, grade, password" in order to change them.  The challenge was to change the grade of one student to 100 so that he could get to college. There was also a note about the math teacher "never researching anything past cgi-bin". 

In the server's cgi-bin folder, there were two c code files - showmarks.c and changemarks.c. They're in the "challengecode" folder if you're interested in them. The showmarks file just appears to grab student marks from a database, and display them in the table. The change marks file is much more interesting - it contains a DES based hash used to confirm the password, and the two possible correct hashes ```da99d1ea64144f3e``` and ```59a3442d8babcf84```. 

## Some DES background
DES isn't a vulnerable block cipher, however there are no controls on it to ensure it's used appropriately in a hash scheme. DES uses 8 input bytes to get 56 input bits by discarding the last bit of each input byte. This is 2^56 combinations, and is virtually uncrackable. Even limiting to ascii character inputs leaves about 2^52 possible inputs. 

Fortunately, this hash algorithm deals with large inputs by repeatedly encrypting  in a chain:

```weakhash := DESEncrypt(DESEncrypt("weakhash", key[0:8]), key[8:16])``` 

It will do this repeatedly until reaching the end of the input password, but it's the two step version that's of interest to us because it enables a MITM attack - searching for a pair key1 key2, where encrypting "weakhash" by key1 is the same as decrypting one of the hashes by key2.

```DESEncrypt("weakhash", key1) == DESDecrypt(da99d1ea64144f3e, key2)```

## Solution

Once we find those two keys, they can be combined, percent encoded, and submitted to the form to change the grade. To work this solution takes about 2^(n) space and log(n)/(n) time, where n is the number of hashes you generate to match.  

My code to do this is in MITM.go. It fills your ram with hash/key pairs, then goes into the decryption stage and keeps going until it finds a match. With 8 threads and 32gb of ram it takes about 25 minutes. Unfortunately, I hadn't worked out the counter increments during Northsec, so the code was massively less efficient and couldn't finish in time.
