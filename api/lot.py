import requests
from config import BASE
from api.address import get_address_coordinates
from utils import expand_address


def get_lps():
    address = expand_address(input('Enter an address: '))
    distance = input('Enter a radius distance (metres): ')

    result = get_address_coordinates(address)
    if not result:
        print('Address not found')
        return
    
    x, y = result["x"], result["y"]

    lots = get_lot_info(x, y, distance)

    if lots is None:
        print('No lots found, try a further radius and check address')
    else:
        for lot in lots:
            print(str(lot) + "\n")


def get_lot_info(x, y, distance):
    url = f"{BASE}/NSW_Land_Parcel_Property_Theme_multiCRS/FeatureServer/8/query"
    
    params = {
        "geometry":       f'{{"x": {x}, "y": {y}, "spatialReference": {{"wkid": 7856}}}}',
        "geometryType":   "esriGeometryPoint",      # it says it will always be esriGeometryPoint on the website
        "spatialRel":     "esriSpatialRelIntersects",
        "inSR":           "7856",    
        "outSR":          "7856",
        "distance":       distance,
        "units":          "esriSRUnit_Meter",
        "outFields":      "*",
        "returnGeometry": True,
        "f":              "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()


    # # Test
    # response = requests.get(url, params=params)
    # print(response.url)
    # print(response.json())
    



    features = data.get("features", [])
    if not features:
        print("No lot found")
        return None
    
    print(f"Total lots returned: {len(data.get('features', []))}")

    results = []

    for feature in features:
        attrs = feature["attributes"]
        results.append({
            "lotidstring":  attrs.get("lotidstring"),
            "lotnumber":    attrs.get("lotnumber"),
            "plannumber":   attrs.get("plannumber"),
            "sectionnumber": attrs.get("sectionnumber"),
            "startdate":     attrs.get("startdate"),
            "enddate":       attrs.get("enddate"),
            "centroidid":   attrs.get("centroidid"), # i thought this might be the centre point, but seems to be something else, returns none on
            #"planlotarea":  attrs.get("planlotarea"), # dont think we'll need this
            "geometry":     feature["geometry"]  # we'll need this for the survey mark query
        })

    return results
