import json

with open('parsed_schedule.json') as f:
    data = json.load(f)

d = data['lscd']
for month in d:
    for game in month["mscd"]["g"]:
        # del game["bd"]
        # del game["gid"]
        # del game["gcode"]
        # del game["seri"]
        # del game["is"]
        # del game["htm"]
        # del game["vtm"]
        # del game["etm"]
        # del game["an"]
        # del game["as"]
        # del game["st"]
        # del game["stt"]
        # del game["gdtutc"]
        # del game["utctm"]
        # del game["ppdst"]
        if "ptsls" in game:
            del game["ptsls"]
        # del game["seq"]

with open('schedule.json', 'w') as w:
    json.dump(data, w, indent=2)
