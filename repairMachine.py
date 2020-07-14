import json
import re
import sys
from os import listdir
import os 

def convert_distance_from_feet_to_meters(value):
    if value is not None and isinstance(value, int):
        value = value/5
        return value + value/2
    return None

def convert_distance_from_miles_to_kilometers(value):
    if value is not None and isinstance(value, int):
        return value * 1.6
    return None

def convert_distance_from_feet_to_meters_text(value):
    replaceText = ""
    corectedUnit = " meters"
    corectedNumber = convert_distance_from_feet_to_meters(int(value[0]))
    replaceText += str(corectedNumber)
    replaceText += corectedUnit
    return replaceText

def corect_retarded_text(text):
    text = corect_text(r"([0-9]+) (feet)", text)
    text = corect_text(r"([0-9]{1,3}(,[0-9]{3})+) (feet)", text)
    text = corect_text(r"([0-9]+)-(foot)", text)
    text = corect_text(r"([0-9]+) (ft.)", text)

    text = misc_corections(text)

    return text

def misc_corections(text):
    text = re.sub("number of feet", "number of meters", text)
    return text

def corect_text(regex, text):
    feetInTextRegex = re.compile(regex) 
    extractedValues = re.findall (feetInTextRegex, text)
    for element in extractedValues:
        textInMeters = convert_distance_from_feet_to_meters_text (element)
        text = re.sub(feetInTextRegex, textInMeters, text)
    return text

def update_range(json_range):
    if json_range["units"] == "ft":    
        json_range["units"] = "m"
        json_range["value"] = convert_distance_from_feet_to_meters(json_range["value"])
    if json_range["units"] == "mi":
        json_range["units"] = "km"
        json_range["value"] = convert_distance_from_miles_to_kilometers(json_range["value"])

    return json_range

def update_data (json_data):
    if "range" in json_data:
        json_data["range"] = update_range(json_data["range"])
    if "target" in  json_data and json_data["target"]["type"] is not "creature":
        json_data["target"] = update_range(json_data["target"])
    return json_data

def update_json (json):
    if "data" in json:
        json["data"] = update_data(json["data"])
    if "items" in json:
        for i in range(len(json["items"])):
            json["items"][i]["data"] = update_data(json["items"][i]["data"])
    return json

def update_json_value_text(json_value):
    json_value = corect_retarded_text(json_value)
    return json_value

def update_json_data_text(json_data):
    if "description" in json_data:
        json_data["description"]["value"] = update_json_value_text(json_data["description"]["value"])
    if "details" in json_data and "biography" in json_data["details"]:
        json_data["details"]["biography"]["value"] = update_json_value_text(json_data["details"]["biography"]["value"])
    if "attributes" in json_data and "speed" in json_data["attributes"]:
        json_data["attributes"]["speed"]["value"] = update_json_value_text(json_data["attributes"]["speed"]["value"])
    return json_data

def update_json_text(json):
    if "items" in json:
        for i in range(len(json["items"])):
            json["items"][i]["data"] = update_json_data_text(json["items"][i]["data"])
    if "data" in json:
        json["data"] = update_json_data_text(json["data"])
    return json

def main ():
    toBeConvertedJsonList = []
    files_to_convert = listdir()
    for files in files_to_convert:
        toBeConvertedJsonList = []
        if (files != 'outFolder' and files != 'repairMachine.py'):
            with open(files, encoding="utf8") as f:
                for jsonObj in f:
                    toBeConvertedJson = json.loads(jsonObj)
                    toBeConvertedJsonList.append(toBeConvertedJson)
            out = open(os.path.join("./outFolder", files), "w")
            for jsonObj in toBeConvertedJsonList:

                jsonObj = update_json(jsonObj)

                jsonObj = update_json_text(jsonObj)

                json.dump(jsonObj, out)
                out.write("\n")
   

main()

