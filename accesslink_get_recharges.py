#!/usr/bin/env python

from __future__ import print_function

from utils import load_config, save_config, pretty_print_json
from accesslink import AccessLink
from datetime import date
import json

try:
    input = input
except NameError:
    pass


CONFIG_FILENAME = "config.yml"


class PolarAccessLink(object):
    """Example application for Polar Open AccessLink v3."""

    def __init__(self):
        self.config = load_config(CONFIG_FILENAME)

        if "access_token" not in self.config:
            print("Authorization is required. Run authorization.py first.")
            return

        self.accesslink = AccessLink(client_id=self.config["client_id"],
                                     client_secret=self.config["client_secret"])

    def list_nightly_recharges(self):
        nightly_recharges = self.accesslink.nightly_recharge.list_nightly_recharges(user_id=self.config["user_id"],
                                                          access_token=self.config["access_token"])
        pretty_print_json(nightly_recharges)

    def get_nightly_recharge(self):
        # get latest nights recharge data
        from datetime import date
        today = date.today()
        d = today.strftime("%Y-%m-%d")
        nightly_recharge = self.accesslink.nightly_recharge.get_nightly_recharge(d, user_id=self.config["user_id"],
                                                          access_token=self.config["access_token"])
        #pretty_print_json(nightly_recharge)

        return pretty_print_json(nightly_recharge)


if __name__ == "__main__":
    accesslink = PolarAccessLink()
    accesslink.get_nightly_recharge()
    #accesslink.list_nightly_recharges()

