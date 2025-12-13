import csv
bounding_box = {"minlatitude": 35.0 , "maxlatitude": 47.5 , "minlongitude": 5.0 , "maxlongitude": 20.0,}



with open('bounding_box.csv' , mode='w' , newline="") as file:
    writer = csv.DictWriter(file , fieldnames = ["key" , "value"])
    writer.writeheader() 
    for key,value in bounding_box.items():
        writer.writerow({"key": key,"value": value})
print("bounding_box.csv has created")