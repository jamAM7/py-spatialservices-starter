import requests

BASE = "https://portal.spatial.nsw.gov.au/server/rest/services"

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



def get_lot_info(x, y):
    url = f"{BASE}/NSW_Land_Parcel_Property_Theme_multiCRS/FeatureServer/8/query"
    
    params = {
        "geometry":       f'{{"x": {x}, "y": {y}, "spatialReference": {{"wkid": 102100}}}}',
        "geometryType":   "esriGeometryPoint",      # it says it will always be esriGeometryPoint on the website
        "spatialRel":     "esriSpatialRelIntersects",
        "inSR":           "102100",
        "outFields":      "*",
        "returnGeometry": True,
        "f":              "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    features = data.get("features", [])
    if not features:
        print("No lot found")
        return None
    
    feature = features[0]
    attrs = feature["attributes"]
    
    return {
        "lotidstring":  attrs.get("lotidstring"),
        "lotnumber":    attrs.get("lotnumber"),
        "plannumber":   attrs.get("plannumber"),
        "sectionnumber": attrs.get("sectionnumber"),
        "startdate":     attrs.get("startdate"),
        "enddate":       attrs.get("enddate"),
        "centroidid":   attrs.get("centroidid"), # i thought this might be the centre point, but seems to be something else, returns none on
        #"planlotarea":  attrs.get("planlotarea"), # dont think we'll need this
        "geometry":     feature["geometry"]  # we'll need this for the survey mark query
    }

# Example
# result = get_address_info("1 Pacific Highway North Sydney")
# print(result)


# def get_survey_mark_info(x, y):
#     url = f"{BASE}/SurveyMarkGDA2020_multiCRS/FeatureServer/query"
    
#     params = {
#         # "geometry":       f'{{"x": {x}, "y": {y}, "spatialReference": {{"wkid": 102100}}}}',
#         "geometry":       get_lot_info(address_result["x"], address_result["y"])["geometry"], # use the geometry from the lot query, which should be more accurate than the address geometry
#         "geometryType":   "esriGeometryPoint",
#         "spatialRel":     "esriSpatialRelIntersects",
#         "inSR":           "102100",
#         "outFields":      "*",
#         "returnGeometry": True,
#         "f":              "json"
#     }
    
#     response = requests.get(url, params=params)
#     data = response.json()
    
#     features = data.get("features", [])
#     if not features:
#         print("No survey mark found")
#         return None
    
#     feature = features[0]
#     attrs = feature["attributes"]
    
#     return {
#         "markid":       attrs.get("markid"),
#         "marktype":     attrs.get("marktype"),
#         "description":  attrs.get("description"),
#         #"geometry":     feature["geometry"]  # we might need this for the next query
#     }



address_result = get_address_info("1 PACIFIC HIGHWAY NORTH SYDNEY")
lot_result = get_lot_info(address_result["x"], address_result["y"])
survey_mark_result = get_survey_mark_info(address_result["x"], address_result["y"])
print("Address Results: \n" + str(address_result) + "\n" + 
      "\nLot Results: \n" + str(lot_result) + "\n" + 
      "\nSurvey Marks Results: \n" + str(survey_mark_result) + "\n")