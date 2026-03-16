import requests
from config import BASE

def get_survey_mark_info(x, y):
    url = f"{BASE}/SurveyMarkGDA2020_multiCRS/FeatureServer/0/query"
    
    # params = {
    #     "geometry":       f'{{"x": {x}, "y": {y}, "spatialReference": {{"wkid": 102100}}}}',
    #     "geometryType":   "esriGeometryPoint",
    #     "distance":       500,
    #     "units":          "esriSRUnit_Meter",
    #     "spatialRel":     "esriSpatialRelIntersects",
    #     "inSR":           "102100",
    #     "outFields":      "*",
    #     "returnGeometry": True,
    #     "f":              "json"
    # }

    params = {
        "layerDefs":      0,
        "geometry":       f'{{"x": {x}, "y": {y}, "spatialReference": {{"wkid": 102100}}}}',
        "geometryType":   "esriGeometryPoint",
        "spatialRel":     "esriSpatialRelIntersects",
        "distance":       300,
        "units":          "esriSRUnit_Meter",    # ← missing this
        "inSR":           "102100",
        "outFields":      "*",
        "returnGeometry": "true",
        "f":              "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    # print(response.url)  # prints the exact URL requests constructed
    # print(response.json())
    
    features = data.get("features", [])
    if not features:
        print("No survey mark found")
        return None
    
    # feature = features[0]
    # attrs = feature["attributes"]



    # # Test
    # response = requests.get(url, params=params)
    # data = response.json()
    # print(f"Total features returned: {len(data.get('features', []))}")
    # print(data)

    # print(response.url)


    
    # return {
    #     "OBJECTID":     attrs.get("OBJECTID"),
    #     "marktype":     attrs.get("marktype"),
    #     "marknumber":   attrs.get("marknumber"),
    #     "markstatus":  attrs.get("markstatus"),
    #     "marksymbol":  attrs.get("marksymbol"),
    #     "longitude":  attrs.get("longitude"),
    #     "latitude":  attrs.get("latitude"),
    # }




    # for x in features:
    #     feature = x
    #     attrs = feature["attributes"]

    #     # return {
    #     #     "OBJECTID":     attrs.get("OBJECTID"),
    #     #     "marktype":     attrs.get("marktype"),
    #     #     "marknumber":   attrs.get("marknumber"),
    #     #     "markstatus":  attrs.get("markstatus"),
    #     #     "marksymbol":  attrs.get("marksymbol"),
    #     #     "longitude":  attrs.get("longitude"),
    #     #     "latitude":  attrs.get("latitude"),
    #     # }

    #     data =  {
    #         "OBJECTID":     attrs.get("OBJECTID"),
    #         "marktype":     attrs.get("marktype"),
    #         "marknumber":   attrs.get("marknumber"),
    #         "markstatus":  attrs.get("markstatus"),
    #         "marksymbol":  attrs.get("marksymbol"),
    #         "longitude":  attrs.get("longitude"),
    #         "latitude":  attrs.get("latitude"),
    #     }

    #     print(data)






    results = []
    
    for feature in features:
        attrs = feature["attributes"]
        results.append({
            "OBJECTID":   attrs.get("OBJECTID"),
            "marktype":   attrs.get("marktype"),
            "marknumber": attrs.get("marknumber"),
            "markstatus": attrs.get("markstatus"),
            "marksymbol": attrs.get("marksymbol"),
            "longitude":  attrs.get("longitude"),
            "latitude":   attrs.get("latitude"),
        })
    
    return results