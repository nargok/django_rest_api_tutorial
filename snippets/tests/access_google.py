import requests

def sample():
    try:
        res = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as e:
        print(e)
        raise e
    return {
        "statusCode": res.status_code,
        "ip": res.text
    }