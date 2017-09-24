#!/usr/bin/python
from google.transit import gtfs_realtime_pb2
import urllib
import unicodedata
import oauth2
import json
import secrets

TRIMET_ALERTS_ENDPOINT = "developer.trimet.org/ws/V1/FeedSpecAlerts?appID={0}"
TWITTER_POST_ENDPOINT = "https://api.twitter.com/1.1/statuses/update.json?status={0}"


def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=secrets.CONSUMER_KEY, secret=secrets.CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers )
    return content


def get_alerts():
    # Get feed data
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.urlopen('https://' + TRIMET_ALERTS_ENDPOINT.format(secrets.APP_ID))
    feed.ParseFromString(response.read())

    # Loop through ang get all alerts
    for entity in feed.entity:
        if entity.HasField('alert'):
            alerts = entity.alert.description_text.translation  # Path to array of alerts
            for alert in alerts:  # Loop though array of alerts
                tweet(alert.text)


def tweet(alert):
    alert = unicodedata.normalize('NFKD', alert).encode('ascii', 'ignore')
    if 'auto' in alert or 'car' in alert:
        print(alert)
        r = oauth_req(TWITTER_POST_ENDPOINT.format(urllib.quote_plus(alert)),
                      secrets.ACCESS_TOKEN,
                      secrets.ACCESS_SECRET,
                      "POST")
        data = json.loads(r)

        if 'errors' in data:
            print(data['errors'][0]['message'])
            exit(1)
        exit(0)  # We only want to tweet out once per run to avoid Twitter flood controls


get_alerts()
