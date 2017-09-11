#!/usr/bin/python
import requests
import appid

ENDPOINT = "developer.trimet.org/ws/V1/FeedSpecAlerts?appID={0}".format(appid.APP_ID)


def get_alerts():
    r = requests.get('https://' + ENDPOINT)
    data = r.content

    if 'error' in data:
        print(data['error'])
        exit(1)

    print(data)


get_alerts()
