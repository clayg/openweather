#!/usr/bin/env python
import sys
import requests
import os


APP_ID = os.environ['APPID']
LAT_LON = 'lat-lon'
CITY = 'city'
ZIP = 'zip'


def parse(input_string):
    pass


def call_api(query):
    query['appid'] = APP_ID
    resp = requests.get('http://api.openweathermap.org/data/2.5/weather',
                        params=query)
    return resp.json()


def call_geo_cords(lat, lon):
    query = {
        'lat': lat,
        'lon': lon,
    }
    return call_api(query)


def call_city(city):
    query = {
        'q': city,
    }
    return call_api(query)


def call_zip(zip_code, country_code=None):
    qarg = str(zip_code)
    if country_code:
        qarg += ',%s' % country_code
    query = {
        'zip': qarg
    }
    return call_api(query)


def dispatch_api_call(call_type, args):
    dispatch_map = {
        LAT_LON: call_geo_cords,
        CITY: call_city,
        ZIP: call_zip,
    }
    return dispatch_map[call_type](*args)


def guess_type(line):
    try:
        a, b = line.split(',', 1)
    except ValueError:
        # probably a city
        return CITY, (line,)
    try:
        b = float(b)
    except ValueError:
        # probably a country code
        return ZIP, (int(a), b)
    # probably a lat, long
    return LAT_LON, (float(a), float(b))


def parse_args(string):
    call_args = []
    for line in string.splitlines():
        call_args.append(guess_type(line.strip()))
    return call_args


def main():
    call_args = parse_args(sys.stdin.read())
    temps = []
    for call_type, args in call_args:
        print(call_type, args)
        data = dispatch_api_call(call_type, args)
        print(data['name'], data['main']['temp'])
        # print(json.dumps(data, indent=2))
        temps.append((data['main']['temp'], args))
    max_temp, max_arg = max(temps)
    print(max_temp, max_arg)


if __name__ == "__main__":
    sys.exit(main())
