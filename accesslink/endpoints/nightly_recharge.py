#!/usr/bin/env python

from .resource import Resource


class NightlyRecharge(Resource):
    """This resource allows partners to access their users' nightly recharge data.

    https://www.polar.com/accesslink-api/#nightly-recharge
    """

    def list_nightly_recharges(self, user_id, access_token):
        """List Nightly Recharge data of user for the last 28 days.

        :param user_id: id of the user
        :param access_token: access token of the user
        """
        return self._get(endpoint="/users/nightly-recharge".format(user_id=user_id),
                         access_token=access_token)

    def get_nightly_recharge(self, date, user_id, access_token):
        """Get Users Nightly Recharge data for given date

        :param user_id: id of the user
        :param access_token: access token of the user
        :param date: Date of Nightly Recharge as ISO-8601 date string, example: "2020-01-01"
        """
        return self._get(endpoint="/users/nightly-recharge/" + date.format(user_id=user_id),
                         access_token=access_token)


