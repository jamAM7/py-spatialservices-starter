import requests
from config import BASE
from api.address import get_address_coordinates
from utils import expand_address

def survey_mark_search():
    address = expand_address(input('Enter an address: '))
    distance = input('Enter a radius distance (metres): ')

    result = get_address_coordinates(address)
    if not result:
        print('Address not found')
        return
    
    x, y = result["x"], result["y"]
    marks = get_survey_mark_info(x, y, distance)

    if marks is None:
        print('No marks found, try a further radius and check address')
    else:
        for mark in marks:
            print(str(mark) + "\n")


def get_survey_mark_by_number():
    url = f"{BASE}/SurveyMarkGDA2020_multiCRS/FeatureServer/0/query"

    marknumber = input('Enter a mark number: ')

    params = {
        "where":          f"marknumber = {marknumber}",
        "outFields":      "*",
        "returnGeometry": "true",
        "outSR":          "7856",
        "f":              "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    features = data.get("features", [])
    if not features:
        print('No mark found')
        return

    attrs = features[0]["attributes"]
    feature = features[0]

    result = {
        "marknumber":      attrs.get("marknumber"),
        "marktype":        attrs.get("marktype"),
        "markstatus":      attrs.get("markstatus"),
        "marksymbol":      attrs.get("marksymbol"),
        "easting":         feature["geometry"]["x"],
        "northing":        feature["geometry"]["y"],
        "zone":            attrs.get("mgazone"),
        "gda_class":       attrs.get("gdaclass"),
        "pos_uncertainty": attrs.get("gdaposuncertainty_label"),
        "loc_uncertainty": attrs.get("gdalocuncertainty_label"),
        "source":          attrs.get("gdasource"),
        "csf":             attrs.get("mgacsf2020"),
        "convergence":     attrs.get("mgacon"),
        "ahd_height":      attrs.get("ahdheight_label"),
        "ahd_class":       attrs.get("ahdclass"),
        "ausgeoid2020":    attrs.get("ausgeoid2020"),
    }

    for key, value in result.items():
        print(f"{key}: {value}")


def get_survey_mark_info(x, y, distance):
    url = f"{BASE}/SurveyMarkGDA2020_multiCRS/FeatureServer/0/query"

    params = {
        "geometry":     f'{{"x": {x}, "y": {y}, "spatialReference": {{"wkid": 7856}}}}',
        "geometryType": "esriGeometryPoint",
        "spatialRel":   "esriSpatialRelIntersects",
        "distance":     distance,
        "units":        "esriSRUnit_Meter",
        "inSR":         "7856",
        "outSR":        "7856",
        "outFields":    "*",
        "returnGeometry": "true",
        "f":            "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    features = data.get("features", [])
    if not features:
        return None

    results = []

    for feature in features:
        attrs = feature["attributes"]
        results.append({
            "marknumber":      attrs.get("marknumber"),
            "marktype":        attrs.get("marktype"),
            "markstatus":      attrs.get("markstatus"),
            "marksymbol":      attrs.get("marksymbol"),
            "easting":         feature["geometry"]["x"],
            "northing":        feature["geometry"]["y"],
            "zone":            attrs.get("mgazone"),
            "gda_class":       attrs.get("gdaclass"),
            "pos_uncertainty": attrs.get("gdaposuncertainty_label"),
            "loc_uncertainty": attrs.get("gdalocuncertainty_label"),
            "source":          attrs.get("gdasource"),
            "csf":             attrs.get("mgacsf2020"),
            "convergence":     attrs.get("mgacon"),
            "ahd_height":      attrs.get("ahdheight_label"),
            "ahd_class":       attrs.get("ahdclass"),
            "ausgeoid2020":    attrs.get("ausgeoid2020"),
        })

    return results
