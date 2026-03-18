import requests
from config import BASE

def get_lot_info(x, y):
    url = f"{BASE}/NSW_Land_Parcel_Property_Theme_multiCRS/FeatureServer/8/query"
    
    params = {
        "geometry":       f'{{"x": {x}, "y": {y}, "spatialReference": {{"wkid": 7856}}}}',
        "geometryType":   "esriGeometryPoint",      # it says it will always be esriGeometryPoint on the website
        "spatialRel":     "esriSpatialRelIntersects",
        "inSR":           "7856",    
        "outSR":          "7856",
        "distance":       50,
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




    # feature = features[0]
    # attrs = feature["attributes"]
    


   


    # return {
    #     "lotidstring":  attrs.get("lotidstring"),
    #     "lotnumber":    attrs.get("lotnumber"),
    #     "plannumber":   attrs.get("plannumber"),
    #     "sectionnumber": attrs.get("sectionnumber"),
    #     "startdate":     attrs.get("startdate"),
    #     "enddate":       attrs.get("enddate"),
    #     "centroidid":   attrs.get("centroidid"), # i thought this might be the centre point, but seems to be something else, returns none on
    #     #"planlotarea":  attrs.get("planlotarea"), # dont think we'll need this
    #     "geometry":     feature["geometry"]  # we'll need this for the survey mark query
    # }