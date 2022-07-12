import json


fp = "/home/waterboi/WaterBoi/config/plant_data.json"

with open(fp, "r") as jsonFile:
    data = json.load(jsonFile)

print(data)
