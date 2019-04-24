import json
from datetime import datetime
from lib.YAML_LIB import *
from glob import glob
import uuid

class JSON:
    def __init__(self):
        stamp=datetime.now()
        self.stamp=str(stamp)
        self.yamlParser = LabelYAML("labelDef.yaml")

    def JSONRead(self,path):
        with open(path, 'r') as json_f:
            self.data = json.load(json_f)
        return self.data

    def JSONWrite(self,path,name,label_name):
        if self.data["image"]["is_reference"]==1:
            name=label_name+"-"+name
        with open(path+name,'w') as json_f:
            json.dump(self.data, json_f,sort_keys=False)


    def JSONModify(self,data_dict):
        self.JSONRead("./templet/Xray.json")
        self.yamlParser.read()
        self.yamlParser.generate_relation()
        self.data["info"]["data_created"]=self.stamp
        self.data["image"]["file_name"]=data_dict["filename"]
        self.data["image"]["id"]=str(uuid.uuid1())
        self.data["image"]["height"]=data_dict["height"]
        self.data["image"]["width"] = data_dict["width"]
        self.data["image"]["is_reference"] = data_dict["reference"]

        annotations=[]
        for info_pack in data_dict["labels"]:
            anno_info={}
            self.reference_id=self.yamlParser.cluster_family(info_pack[-1])
            anno_info["category_id"]=self.reference_id
            anno_info["bbox"]=info_pack[0]
            anno_info["segmentation"]=info_pack[1]
            anno_info["area"]=info_pack[2]
            annotations.append(anno_info)
        self.data["annotations"]=annotations
        return self.reference_id

    def fetchLabel(self,image_name):
        filematch=glob("./annotation_output/*"+image_name+".json")
        if len(filematch)>0:
            label_info=self.JSONRead(filematch[0])
        else:
            return None

        self.yamlParser.read()
        self.yamlParser.generate_relation()
        annotations=label_info["annotations"]
        temp_label=[]
        for anno in annotations:
            if len(anno["bbox"])>0:
                anno["bbox"].insert(0,1)
                anno["bbox"].append(self.yamlParser.id2name(anno["category_id"]))
                temp_label.append(anno["bbox"])
            if len(anno["segmentation"])>0:
                anno["segmentation"].insert(0, 2)
                anno["segmentation"].append(self.yamlParser.id2name(anno["category_id"]))
                temp_label.append(anno["segmentation"])
        return temp_label



# j = JSON()
# h = j.JSONRead('Xray.json')
# j.JSONModify("1111")