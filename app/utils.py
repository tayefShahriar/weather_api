from django.conf import settings
import requests
from datetime import datetime as dt
def request_to_weatherapi(city):
    try:
        URL = f"http://api.weatherapi.com/v1/current.json?key={settings.WA_APIKEY}&q={city}"
        res = requests.get(URL)
        # print("================", res.raise_for_status())
        res_json = res.json()
        return {
            "city": res_json["location"]["name"],
            "description": res_json["current"]["condition"]["text"],
            "icon": f'http:{res_json["current"]["condition"]["icon"]}',
            "temperature": res_json["current"]["temp_c"],
            "updated_date": dt.fromtimestamp(res_json["current"]["last_updated_epoch"]).strftime('%Y-%m-%d %H:%M'),
            "api_response": res.text
        }
    except Exception as e:
        raise ValueError(f"API returned an api error: {e}")
