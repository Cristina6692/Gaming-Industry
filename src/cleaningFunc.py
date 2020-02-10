import math


#Pasa latitud y longitud de un DF a formato geojson:

def asGeoJSON(lat,lng):
    try:
        lat = float(lat)
        lng = float(lng)
        if not math.isnan(lat) and not math.isnan(lng):
            return {
                "type":"Point",
                "coordinates":[lng,lat]
            }
    except Exception:
        print("Invalid data")
        return None