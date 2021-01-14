#!/usr/bin/env python

from .resource import Resource


class Sleep(Resource):
    """This resource allows partners to access their users' sleep.

    https://www.polar.com/accesslink-api/#get-sleep
    """


    def get_sleep(self, date, user_id, access_token):
        """Get Users Sleep data for given date

        :param user_id: id of the user
        :param access_token: access token of the user
        :param date: Date of Nightly Recharge as ISO-8601 date string, example: "2020-01-01"
        """
        return self._get(endpoint="/users/sleep/" + date.format(user_id=user_id),
                         access_token=access_token)


