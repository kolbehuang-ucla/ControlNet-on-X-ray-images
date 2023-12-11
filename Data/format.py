import os
import json


data = []
with open("Train/caption-train.json", "r") as inputData:
    for line in inputData:
        try:
            curr = json.loads(line.rstrip('\n'))
            curr["source"] = curr["source"].split('/')[-1]
            curr["target"] = curr["target"].split('/')[-1]
            data.append(curr)
        except ValueError:
            print ("Skipping invalid line {0}".format(repr(line)))

with open("Train/prompt.json", "w") as f:
    for line in data:
        f.write(json.dumps(line, ensure_ascii=False))
        f.write('\n')
