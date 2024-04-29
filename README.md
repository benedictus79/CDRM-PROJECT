## CDRM-Project
 ![forthebadge](https://forthebadge.com/images/badges/uses-html.svg) ![forthebadge](https://forthebadge.com/images/badges/uses-css.svg) ![forthebadge](https://forthebadge.com/images/badges/uses-javascript.svg) ![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
 ## What is this?
 
 An open source web application written in python to decrypt Widevine protected content.

## Prerequisites

 - [Python](https://www.python.org/downloads/) with PIP installed

   > Python 3.12 was used at the time of writing
 - L1/L3 Content Decryption Module provisioned in .WVD format using [pyWidevine](https://github.com/devine-dl/pywidevine)
 
 ## Installation
 
 - Open your terminal and navigate to where you'd like to store the application
 - Create a new python virtual environment using `python -m venv CDRM-Project`
 - Change directory into the new `CDRM-Project` folder
 - Activate the virtual environment

    > Windows - change directory into the `Scripts` directory then `activate.bat`
    > 
    > Linux - `source/activate`

 - Install python dependencies `pip install -r requirements.txt`
 - Place your .WVD file into the root of the directory
 - Run the application `python main.py`

