import json
from datetime import datetime

class JSON:
    def __init__(self):
        stamp=datetime.now()
        self.stamp=str(stamp)

    def JSONRead(self,path):
        with open(path, 'r') as json_f:
            self.data = json.load(json_f)
        return self.data

    def JSONWrite(self,path,name):
        with open(path+name,'w') as json_f:
            json.dump(self.data, json_f)

    def JSONModify(self,data_dict):
        self.JSONRead("./templet/Xray.json")
        #print(self.data["info"])
        self.data["info"]["data_created"]=self.stamp
        self.data["image"]["filename"]=data_dict["filename"]
        self.data["image"]["height"]=data_dict["height"]
        self.data["image"]["width"] = data_dict["width"]

        annotations=[]
        for info_pack in data_dict["labels"]:
            anno_info={}
            anno_info["category_id"]=info_pack[-1]
            anno_info["bbox"]=info_pack[0]
            anno_info["segmentation"]=info_pack[1]
            anno_info["area"]=info_pack[2]
            annotations.append(anno_info)
        self.data["annotations"]=annotations







# j = JSON()
# h = j.JSONRead('Xray.json')
# j.JSONModify("1111")