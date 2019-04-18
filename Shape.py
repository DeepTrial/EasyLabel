import math
from lib.JSON_LIB import *

class ShapeLabel():
    def __init__(self):
        self.shape_dict=[]
        self.shape_name=["keep_in_save","rectangle","polygon"]
        self.skip_label=[]
        self.data_dict={}
        self.saver=JSON()

    def clear(self):
        self.shape_dict=[]
        self.data_dict ={}

    def addShape(self,image_name,height,width,coordlist):
        self.data_dict["filename"]=image_name
        self.data_dict["height"]=height
        self.data_dict["width"]=width
        self.shape_dict.append(coordlist)
        self.skip_label.append(0)
    def undo(self):
        self.shape_dict.remove(self.shape_dict[-1])
        return self.shape_dict

    def debug(self):
        print("*"*10)
        print(self.shape_dict)
        print("*" * 10)

    def _map_min_max(self,coords):
        minx=20000000000
        miny=20000000000
        maxx=-1
        maxy=-1

        if coords[0]==1:
            minx=max(coords[1]-coords[3]/2.0,0)
            miny =max(coords[2] - coords[4] / 2.0, 0)
            maxx = min(coords[1] + coords[3] / 2.0, self.data_dict["width"])
            maxy = min(coords[2] + coords[4] / 2.0, self.data_dict["height"])
            return minx,miny,maxx,maxy
        else:
            for i in range(1,len(coords)-1):
                if minx>coords[i][0]:
                    minx=coords[i][0]
                if miny>coords[i][1]:
                    miny=coords[i][1]
                if maxx<coords[i][0]:
                    maxx=coords[i][0]
                if maxy<coords[i][1]:
                    maxy=coords[i][1]
            return minx,miny,maxx,maxy

    def _overlap(self,shape_i,shape_j):
        area_j = (shape_j[2] - shape_j[0]) * (shape_j[3] - shape_j[1])
        minx=max(shape_i[0],shape_j[0])
        miny = max(shape_i[1], shape_j[1])
        maxx = min(shape_i[2], shape_j[2])
        maxy = min(shape_i[3], shape_j[3])
        overlap_area=(maxx - minx) * (maxy - miny)
        if overlap_area/area_j>=0.8:
            return True
        else:
            return False

    def _process(self):
        self.data_dict["labels"]=[]
        for i in range(len(self.shape_dict)):
            temp_pack=[]
            if self.skip_label[i]==1:
                continue
            for j in range(i+1,len(self.shape_dict)):
                if self.shape_dict[i][-1]==self.shape_dict[j][-1] and self.shape_dict[i][0]!=self.shape_dict[j][0] and self.skip_label[j]==0:
                    minxi,minyi,maxxi,maxyi=self._map_min_max(self.shape_dict[i])
                    minxj, minyj, maxxj, maxyj = self._map_min_max(self.shape_dict[j])
                    if self._overlap([minxi,minyi,maxxi,maxyi],[minxj, minyj, maxxj, maxyj]):
                    #if math.fabs(minxi-minxj)<=15 and math.fabs(minyi-minyj)<=15 and math.fabs(maxxi-maxxj)<=15 and math.fabs(maxyi-maxyj)<=15:
                        if self.shape_dict[i][0]==1:
                            temp_pack.append(self.shape_dict[i][1:-1])
                            temp_pack.append(self.shape_dict[j][1:-1])
                        else:
                            temp_pack.append(self.shape_dict[j][1:-1])
                            temp_pack.append(self.shape_dict[i][1:-1])
                        temp_pack.append(-1)
                        temp_pack.append(self.shape_dict[i][-1])
                        self.skip_label[j]=1
            if len(temp_pack)==0:
                if self.shape_dict[i][0] == 1:
                    temp_pack.append(self.shape_dict[i][1:-1])
                    temp_pack.append([])
                else:
                    temp_pack.append([])
                    temp_pack.append(self.shape_dict[i][1:-1])
                temp_pack.append(0)
                temp_pack.append(self.shape_dict[i][-1])
            self.data_dict["labels"].append(temp_pack)


    def save(self,path,name):
        self._process()
        self.saver.JSONModify(self.data_dict)
        self.saver.JSONWrite(path,name)


def fetchLabel(image_name):
    j=JSON()
    label_info=j.JSONRead("./annotation_output/"+image_name+".json")
    annotations=label_info["annotations"]
    temp_label=[]
    for anno in annotations:
        if len(anno["bbox"])>0:
            anno["bbox"].insert(0,1)
            anno["bbox"].append(anno["category_id"])
            temp_label.append(anno["bbox"])
        if len(anno["segmentation"])>0:
            anno["segmentation"].insert(0, 2)
            anno["segmentation"].append(anno["category_id"])
            temp_label.append(anno["segmentation"])
    return temp_label