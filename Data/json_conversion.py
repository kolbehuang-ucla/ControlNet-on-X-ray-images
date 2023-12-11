import os
import json
import csv
import shutil

# Set directories
directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../xray'))
print(directory)
imageDirectory = os.path.abspath(os.path.join(directory, 'x-ray-edges-json/target'))

# Convert the original csv dataset into the ControlNet's suggested json format:
# Original format: Image, disease names ..., PatientID, diseases...
# PatientID at index 12
# ControlNet format: {source: "", target: "", prompt: ""}
# csv_file: input csv_file to be read
# out_file: output json file to be written
def getCaptions(csv_file, out_file):
    fields = ['source', 'target', 'prompt']
    n = 0
    for lines in csv_file:
        if n > 0:
            dict1 = {}
            image = lines[0]
            imageAdr = os.path.abspath(os.path.join(imageDirectory, image))
            if os.path.isfile(imageAdr): 
                sourceImage = 'source/' + image
                targetImage = 'target/' + image
                i = 1
                prompt = "Chest x-ray of a patient with no diseases"
                while i < 16:
                    if i != 12 and int(lines[i]) > 0:
                        prompt = "Chest x-ray of a patient with diseases"
                        break
                    i = i + 1
                fieldValues = [sourceImage, targetImage, prompt]
                        
                j = 0
                while j < len(fields):
                    dict1[fields[j]] = fieldValues[j]
                    j = j + 1 
                json.dump(dict1, out_file)
                out_file.write('\n')
        n = n + 1


# Loop through all csv files to find all 999 image information
file1 = open(os.path.abspath(os.path.join(directory, 'train-small-new.csv')), newline = '')
file2 = open(os.path.abspath(os.path.join(directory, 'test-small-new.csv')), newline = '')
file3 = open(os.path.abspath(os.path.join(directory, 'valid-small-new.csv')), newline = '')
csv_file1 = csv.reader(file1)
csv_file2 = csv.reader(file2)
csv_file3 = csv.reader(file3)

# Initially save to one json file
out_file = open('../xray/captions.json', 'w')

getCaptions(csv_file1, out_file)
getCaptions(csv_file2, out_file)
getCaptions(csv_file3, out_file)

out_file.close()

# Loop through the full json file
json_file = open('../xray/captions.json')

out_file_train = open('../xray/Train/caption-train.json', 'w')
out_file_test = open('../xray/Test/caption-test.json', 'w')

# Split into test and train datasets
directoryTest = os.path.abspath(os.path.join(os.path.dirname(__file__), '../xray/Test'))
directoryTrain = os.path.abspath(os.path.join(os.path.dirname(__file__), '../xray/Train'))
imageEdges = os.path.abspath(os.path.join(directory, 'x-ray-edges-json/source'))

# The dataset is already random, assign first 800 as train and remaining 199 as test
n = 0
for line in json_file:
    image = line[19: 35]
    imageTarget = os.path.abspath(os.path.join(imageDirectory, image))
    imageSource = os.path.abspath(os.path.join(imageEdges, image))
    source = ""
    target = ""
    if n < 199:
        out_file_test.write(line)
        source = os.path.abspath(os.path.join(directoryTest, 'source/' + image))
        target = os.path.abspath(os.path.join(directoryTest, 'target/' + image))
    else:
        out_file_train.write(line)
        source = os.path.abspath(os.path.join(directoryTrain, 'source/' + image))
        target = os.path.abspath(os.path.join(directoryTrain, 'target/' + image))

    print(directoryTest)
    print(directoryTrain)
    shutil.copyfile(imageTarget, target)
    shutil.copyfile(imageSource, source)
    n = n + 1

out_file_train.close()
out_file_test.close()