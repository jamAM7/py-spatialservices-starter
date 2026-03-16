import requests
from config import BASE

def get_address_info(address_string):
    url = f"{BASE}/NSW_Geocoded_Addressing_Theme/FeatureServer/1/query" # this is url for address stuff
    
    params = {
        "where": f"address = '{address_string.upper()}'", # I have chosen to use = instead of LIKE "address%" because I want an exact match, so no risk of returning wrong address. This assumes the survyeor knows the exact address they are looking for.
        "outFields": "*",       # return all columns
        "returnGeometry": True, # include x, y coordinates
        "f": "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    features = data.get("features", [])
    if not features:
        print("No address found")
        return None
    
    # Take the first match
    feature = features[0]
    attrs = feature["attributes"]
    geom  = feature["geometry"]
    
    geotype = data.get("geometryType", [])
    #geott = geotype[0]


    return {
        "address":    attrs.get("address"),
        "centroidid": attrs.get("centroidid"), # i thought this might be the centre point, but seems to be something else, returns none
        #"lotidstring": attrs.get("lotidstring"),  # e.g. "1//DP123456"
        "x": geom["x"],
        "y": geom["y"],
        "geometryType": geotype
    }