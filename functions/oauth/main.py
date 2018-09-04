import os
import json

from botocore.vendored import requests


def auth_discord(event):
    """
    Query Parameters =>
      - code : the code from authorization url.
      - redirect_uri : the redirect_uri.
    """
    data = {
        'client_id': os.environ['DISCORD_CLIENT_ID'],
        'client_secret': os.environ['DISCORD_CLIENT_SECRET'],
        'grant_type': 'authorization_code',
        'code': event['queryStringParameters']['code'],
        'redirect_uri': event['queryStringParameters']['redirect_uri'],
        'scope': 'guilds rpc.api',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    r = requests.post('https://discordapp.com/api/v6/oauth2/token', data=data, headers=headers)
    r.raise_for_status()
    return r.json()


def handle(event, context):
    """
    Query Parameters =>
      - service : name of service.
    """
    status = 200
    res = {}

    service = event['queryStringParameters']['service']
    try:
        if service == 'discord':
            res = auth_discord(event)
        else:
            status = 400
    except Exception as e:
        print(e)
        status = 500

    return {
        'statusCode': status,
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
