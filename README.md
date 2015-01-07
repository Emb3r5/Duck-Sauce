Duck-Sauce
==========
Version 1.0

Python Script to Import Malware from Fire Eye Sensor and create a zip file of new malware for processing

Purpose:  I created this script to generate a list of known malware hashes, as well as a zip file I can submit to A/V 
vendors.  The hashes could also be sent to Virus Total or used for other Intel purposes.

This script will need the following modifications to work:
  
  - The Username, Password, and IP Address will need to be set to the correct values.  The Username/Password is used to 
  login to the Fire Eye Sensor via SSH, and that user needs to have Admin Rights on the Sensor.  The IP address is that 
  of the Fire Eye sensor.
  
  - The script was written to accomodate multiple Fire Eye Sensors.  To do this, copy lines 38 to 42 and modify the 
  username/password and IP address as needed.  You can do this as many times as needed.
  
The script works by collecting the malware samples into a "done" directory, and then hashing them for comparison of a 
running list of known hashes.  The first time running this script will load all malware samples, while subsequent runs 
will create a zip of files not included in the last run.  

