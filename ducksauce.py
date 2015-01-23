#!/usr/bin/python
# Written by Jeff Tehovnik on 10/31/2014 (Happy Halloween!)
# Last Modified 12/16/2014
import httplib, sys
import os
import time
import pexpect
import zipfile
import mechanize
import hashlib
import datetime
import pickle

# Create the Hashing Function for creating SHA256 Hash from file
# Thanks to techtonik's HashDeep.py code: https://gist.github.com/techtonik/5175896
# for the following function

def getFileHashSHA256(filehash):
    blocksize = 64*1024
    sha = hashlib.sha256()
    with open(filehash, 'rb') as fp:
        while True:
            data = fp.read(blocksize)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest() 

#The following is from StackOverflow user Ashwini Chaudhary
def check_hashstring(thehashstring):
	if thehashstring in open('currenthash.txt').read():
    		print thehashstring + " already processed, skipping..."
		return True
	else :
		return False

#Get Files from sensor and put them into a ./data folder
#Note this section can be copied and used for as many sensors as you have
#Be sure to change the IP address and password to appropriate values
child = pexpect.spawn('scp -r admin@127.0.0.1:/data/malware/done/ .', timeout=500)
child.expect (['assword:', pexpect.EOF])
child.sendline ("SecretPassword")
child.expect(pexpect.EOF)
child.close()

# Create list of SHA256's
h_sha256=[]

# Loop through files in ./done directory and delete if hash exists
for (dirname, dirs, files5) in os.walk('./done'):
        for filename5 in files5:
# Delete files with .zip extension (cleanout directory from FireEye)
		if filename5.endswith('.zip') :
			os.remove(os.path.join(dirname, filename5))
# Hash the files in the ./done directory
		if filename5.endswith('.malware') :
			zhash= getFileHashSHA256(os.path.join(dirname, filename5))
			if (check_hashstring(zhash) == False) :
				h_sha256.append(getFileHashSHA256(os.path.join(dirname,filename5)))
			elif (check_hashstring(zhash) == True) : 
				os.remove(os.path.join(dirname, filename5))
			else :
				print ('fail on check_hashstring')

#Append Hashes to running list of processed hashes
hashfile=open('currenthash.txt', 'a')
for (myitem) in h_sha256:
	hashfile.write("%s\n" % myitem)

# Create Directory for Zip
def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

# Create Zip File
if __name__ == '__main__':
    zipf = zipfile.ZipFile('ducksauce.zip', 'w')
    zipdir('./done', zipf)
    zipf.close()
