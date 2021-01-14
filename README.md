# Sync Polar Recharge and Sleep Data to Google Sheets
## This is forked from the official Polar Open AccessLink example application

This is a small application that uses the [Polar Open AccessLink](https://www.polar.com/accesslink-api) API.
Some information below has been edited to support this fork otherwise credit where credit is due.  
This has been based on the official [Polar repo](https://github.com/polarofficial/accesslink-example-python) and modified by me.  
It's not perfect but it works if you set the Google creds up correctly and will sync data.  
Once you have data in Google Sheets you can build dashboard visualisations with [Google Data Studio](https://datastudio.google.com)

## Prerequisites

* [Polar Flow](https://flow.polar.com) account
* Python and pip

## Getting Started

#### 1. Create new API client 
 
Navigate to https://admin.polaraccesslink.com. Log in with your Polar Flow account and create a new client.

Use `http://localhost:5000/oauth2_callback` as the authorization callback domain for this example.
  
#### 2. Configure client credentials

Fill in your client id and secret in config.yml:

```
client_id: 57a715f8-b7e8-11e7-abc4-cec278b6b50a
client_secret: 62c54f4a-b7e8-11e7-abc4-cec278b6b50a
```
  
#### 3. Install python dependencies
This includes the required Google api packages

```
pip install -r requirements.txt
```

#### 4. Link user 

User account needs to be linked to client application before client can get any user data. User is asked for authorization 
in Polar Flow, and user is redirected back to application callback url with authorization code once user has accepted the request.
 
To start example callback service, run:

```
python authorization.py
```

and navigate to 'https://flow.polar.com/oauth2/authorization?response_type=code&client_id=CLIENT_ID' to link user account.  
This step is required to obtain a valid token for making further requests to the Polar api.

#### 5. Run Sync application
    
There are a couple of scripts you can run. The first is much like the standard example but included Nightly Recharge data.
```
python accesslink_get_recharges.py
```
The other and more exciting script will pull Nightly Recharge and Sleep data from the api and send it to a Google Sheet.  
You must have created the Google Sheet first and entered the spreadsheet id in the script. 
You must also have created oauth and api credentials in the [Google API Console](https://console.developers.google.com/apis/dashboard).
```
python google_polar_metrics_update.py
```
OAuth client id and Service Account credential (Service Account User role) must be created first in
Google API Console - https://console.developers.google.com/apis/dashboard.
The generated token.pickle must be in same dir where script is run unless paths are updated.

Review https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the_api_name
to get started with initial Google api connection, but I don't think writes will work until Service Account
credential is created.  

Oauth credentials should be saved to **"credentials.json"**  
API Service Account credentials should be saved to **"polar_metrics_api_creds.json"**

The script appends data, but the headers need to be created manually.  
For your convenience, the relevant headers are:  
```
ANS Charge, Beat to Beat Avg (ms), Breathing Rate Avg (rpm), Recharge Date, Heart Rate Avg, HRV Avg (ms), Nightly Recharge Status, Continuity, Continuity Class, Sleep Date, Deep Sleep, Device Id,
Light Sleep, REM Sleep,	Sleep End Time,	Sleep Score, Sleep Start Time, Total Interruption Duration, Unrecognized Sleep Stage, Total Sleep (hr)
```
Please note that the sheet name ("Data") is coded into the script so if you want to change that, make sure the script matches.
