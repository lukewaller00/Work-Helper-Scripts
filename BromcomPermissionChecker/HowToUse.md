# Bromcom Permission Checker Guide

## Step 1 - Install Dependencies
Please install Python, pip, and python package etree:

    1. Install Python and pip and ensure it is added to your systems PATH:
        https://www.python.org/downloads/
    
    2. Install dependencies for the script:
        'pip install lxml'

## Step 1 - Fetching Bromcom Permission Set
Visit the Bromcom Service URL:
    1. Go to: https://cloudmis.bromcom.com/Nucleus/WebServices/ThirdParty/TPReadOnlyDataService.asmx?op=findEntitiesBySchoolID.

    2. Enter your Bromcom School ID, GroupCall Username, and Password.
## Step 2 - Saving The Permission Set
Save and overwrite the XML file with the Placeholder file:

    1. After the XML data loads in your browser, press Ctrl + S

    2. Save the file as findEntitesBySchoolID.xml in the same folder as the Python script.
        (Save and replace with Placeholder file)

## Step 3 - Running the Script 
Navigate to folder in cmd / powershell and run script:

    1.
        Option 1:
            Shift + Right Click in file explorer to open in cmd / terminal

        Option 2:
            Type CMD in address bar of file explorer
    
        Option 3: 
            Open CMD / Terminal from start menu and copy file path of script
            Use command: cd "<MY-FILE-PATH>"
    2.
            Use command to run script:
                python ./BromcomPermissionChecker.py
## Step 4 - Reading the Output
The script will print out to the terminal window any missing permissions from the list on our support site
It will also show any additional permissions added to the account that do not appear in our list.
