from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from utils import load_config, pretty_print_json
from accesslink import AccessLink

CONFIG_FILENAME = "config.yml"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID of spreadsheet.
SPREADSHEET_ID = 'SPREADSHEET ID GOES HERE...'


class PolarAccessLink(object):
    """Polar Accesslink main class object"""

    def __init__(self):
        self.config = load_config(CONFIG_FILENAME)

        if "access_token" not in self.config:
            print("Authorization is required. Run authorization.py first.")
            return

        self.accesslink = AccessLink(client_id=self.config["client_id"],
                                     client_secret=self.config["client_secret"])

    def list_nightly_recharges(self):
        nightly_recharges = self.accesslink.nightly_recharge.list_nightly_recharges(user_id=self.config["user_id"],
                                                                                    access_token=self.config[
                                                                                        "access_token"])
        pretty_print_json(nightly_recharges)

    def get_nightly_recharge(self):
        # get latest nights recharge data
        from datetime import date
        today = date.today()
        d = today.strftime("%Y-%m-%d")
        nightly_recharge = self.accesslink.nightly_recharge.get_nightly_recharge(d, user_id=self.config["user_id"],
                                                                                 access_token=self.config[
                                                                                     "access_token"])
        # pretty_print_json(nightly_recharge)
        return nightly_recharge

    def get_sleep(self):
        # get latest nights recharge data
        from datetime import date
        today = date.today()
        d = today.strftime("%Y-%m-%d")
        sleep = self.accesslink.sleep.get_sleep(d, user_id=self.config["user_id"],
                                                access_token=self.config["access_token"])
        # pretty_print_json(sleep)
        return sleep

    def send_to_googlesheets(self):
        """Basic usage of the Sheets API to update a sheet
        OAuth client id and Service Account credential (Service Account User role) must be created first in
        Google API Console - https://console.developers.google.com/apis/dashboard.
        The generated token.pickle must be in same dir where script is run unless paths are updated.

        Review https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the_api_name
        to get started with initial Google api connection but I don't think writes will work until Service Account
        credential is created.

        ***In this example, download the api creds to "polar_metrics_api_creds.json"
        ***Oauth credentials should be saved to credentials.json
        """

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'polar_metrics_api_creds.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        # call polar accesslink objects to get values
        polar_resp = self.get_nightly_recharge()
        polar_sleep_resp = self.get_sleep()
        # pretty_print_json(polar_sleep_resp)

        # add total sleep metrics and convert all to hours
        total_sleep = round(sum([polar_sleep_resp["deep_sleep"],
                                 polar_sleep_resp["light_sleep"], polar_sleep_resp["rem_sleep"]]) / 3600, 2)

        deep_sleep = round(polar_sleep_resp["deep_sleep"] / 3600, 2)
        light_sleep = round(polar_sleep_resp["light_sleep"] / 3600, 2)
        rem_sleep = round(polar_sleep_resp["rem_sleep"] / 3600, 2)
        total_interruption_duration = round(polar_sleep_resp["total_interruption_duration"] / 3600, 2)

        values = [
            [
                polar_resp["ans_charge"],
                polar_resp["beat_to_beat_avg"],
                polar_resp["breathing_rate_avg"],
                polar_resp["date"],
                polar_resp["heart_rate_avg"],
                polar_resp["heart_rate_variability_avg"],
                polar_resp["nightly_recharge_status"],
                polar_sleep_resp["continuity"],
                polar_sleep_resp["continuity_class"],
                polar_sleep_resp["date"],
                # polar_sleep_resp["deep_sleep"],
                deep_sleep,
                polar_sleep_resp["device_id"],
                # polar_sleep_resp["light_sleep"],
                light_sleep,
                # polar_sleep_resp["rem_sleep"],
                rem_sleep,
                polar_sleep_resp["sleep_end_time"],
                polar_sleep_resp["sleep_score"],
                polar_sleep_resp["sleep_start_time"],
                # polar_sleep_resp["total_interruption_duration"],
                total_interruption_duration,
                polar_sleep_resp["unrecognized_sleep_stage"],
                total_sleep
            ],
            # Additional rows ...
        ]
        body = {
            'values': values
        }

        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="Data!A:Z",
            body={
                "majorDimension": "ROWS",
                "values": values
            },
            valueInputOption="USER_ENTERED"
        ).execute()
        # print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    # main()
    accesslink = PolarAccessLink()
    accesslink.send_to_googlesheets()
