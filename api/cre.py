import requests
from utils import expand_address
from api.address import get_address_coordinates

CRE_BASE = "https://maps.six.nsw.gov.au/arcgis/rest/services/sixmaps/CRE/MapServer"
CRE_LOT_LAYER = 17


def cre_search():
    address = expand_address(input('Enter an address: '))
    #distance = input('Enter a radius distance (metres): ')

    result = get_address_coordinates(address)
    if not result:
        print('Address not found')
        return
    
    x, y = result["x"], result["y"]
    cre_info = get_cre_lot_info(x, y)

    if cre_info is None:
        print('No marks found, try a further radius and check address')
    else:
        for info in cre_info:
            print(str(info) + "\n")


def get_cre_lot_info(x, y):
    url = f"{CRE_BASE}/{CRE_LOT_LAYER}/query"

    params = {
        "geometry":       f'{{"x": {x}, "y": {y}, "spatialReference": {{"wkid": 7856}}}}',
        "geometryType":   "esriGeometryPoint",
        "spatialRel":     "esriSpatialRelIntersects",
        "inSR":           "7856",
        "outSR":          "7856",
        "outFields":      "*",
        "returnGeometry": "false",
        "f":              "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    features = data.get("features", [])
    if not features:
        print("No CRE lot found")
        return

    attrs = features[0]["attributes"]

    # decode itstitlestatus coded value
    title_status_codes = {
        0: "Undefined",
        1: "ITS Title",
        2: "Manual Volume/Folio",
    }

    result = {
        "plan_label":     attrs.get("planlabel"),
        "lot_number":     attrs.get("lotnumber"),
        "title_status":   title_status_codes.get(attrs.get("itstitlestatus"), attrs.get("itstitlestatus")),
        "has_stratum":    attrs.get("hasstratum"),
        "lot_area":       attrs.get("planlotarea"),
        "lot_area_units": attrs.get("planlotareaunits"),
        "area_calc":      attrs.get("SE_Area(shape)"),
        "perimeter":      attrs.get("SE_Length(shape)"),
    }

    for key, value in result.items():
        print(f"{key}: {value}")


## One thing to flag

# The `itstitlestatus` field shows `...8 more...` coded values on the layer page — meaning there are more than the 3 visible ones. Before finishing I'd recommend visiting:
# ```
# https://maps.six.nsw.gov.au/arcgis/rest/services/sixmaps/CRE/MapServer/17?f=json