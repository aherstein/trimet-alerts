#!/usr/bin/python
from google.transit import gtfs_realtime_pb2
import urllib
import unicodedata
import appid

ENDPOINT = "developer.trimet.org/ws/V1/FeedSpecAlerts?appID={0}"


def get_alerts():
    # Get feed data
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.urlopen('https://' + ENDPOINT.format(appid.APP_ID))
    feed.ParseFromString(response.read())

    # Loop through ang get all alerts
    for entity in feed.entity:
        if entity.HasField('alert'):
            alerts = entity.alert.description_text.translation  # Path to array of alerts
            for alert in alerts:  # Loop though array of alerts
                # do_something(alert.text)
                print(alert)
                print("-----------------------------------------------------------------------------------------------")


def do_something(alert):
    alert = unicodedata.normalize('NFKD', alert).encode('ascii', 'ignore')
    if 'auto blocking' in alert or 'car blocking' in alert:
        print(alert)


get_alerts()
