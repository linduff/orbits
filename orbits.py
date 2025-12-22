import requests
from datetime import datetime, timedelta

today_date = datetime.today().strftime("%Y-%b-%d").upper()
tomorrow_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%b-%d").upper()
objects = {
    "Mercury": {
        "id": 199,
        "color": "#B1B1B1" # medium gray
    },
    "Venus": {
        "id": 299,
        "color": "#C9B37E" # pale yellow/tan (cloud tops)
    },
    # "Moon": {
    #     "id": 301,
    #     "color": "#CFCFCF" # light gray
    # },
    "Earth": {
        "id": 399,
        "color": "#1EB88E5" # ocean blue
    },
    "Mars": {
        "id": 499,
        "color": "#C1440E" # rusty red
    },
    "Jupiter": {
        "id": 599,
        "color": "#C9A66B" # warm tan (banded)
    },
    "Saturn": {
        "id": 699,
        "color": "#F5DEB3" # wheat/khaki (planet body)
    },
    "Uranus": {
        "id": 799,
        "color": "#7FC7C9" # pale cyan
    },
    "Neptune": {
        "id": 899,
        "color": "#4169E1" # deep royal blue
    },
    # "Pluto": {
    #     "id": 999,
    #     "color": "#C2B280" # beige/putty
    # },
}

current_positions = []

def getCoords(text):
    x_start = ' X ='
    y_start = ' Y ='
    z_start = ' Z ='
    z_end = '\n'

    try:
        x_start_index = text.index(x_start) + len(x_start)
        x_end_index = text.index(y_start, x_start_index)
        x = float(text[x_start_index:x_end_index])

        y_start_index = text.index(y_start) + len(y_start)
        y_end_index = text.index(z_start, y_start_index)
        y = float(text[y_start_index:y_end_index])

        z_start_index = text.index(z_start) + len(z_start)
        z_end_index = text.index(z_end, z_start_index)
        z = float(text[z_start_index:z_end_index])

        return (x,y,z)
    except ValueError:
        return None

def getPlanetsCoords():
    for planet, data in objects.items():
        response = requests.get(
            'https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND=' + str(data['id']) + '&OBJ_DATA=NO&EPHEM_TYPE=VECTORS&CENTER=@SUN&STEP_SIZE=2d&START_TIME=' + today_date + '&STOP_TIME=' + tomorrow_date
        )
        if response.status_code == 200:
            print('Retrieved ' + planet + ' information')
            x,y,z = getCoords(response.json()['result'])
        else:
            print('FAILURE')
            print(response.status_code)
            exit()
        current_positions.append({'object': planet, 'color': data['color'], 'x': x, 'y': y, 'z': z})
    return current_positions

print(getPlanetsCoords())

