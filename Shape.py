from lib.SHAPE_LIB import *
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
        self.skip_label = []

    def addShape(self,image_name,height,width,coordlist,is_reference):
        self.data_dict["reference"]=is_reference
        self.data_dict["filename"]=image_name
        self.data_dict["height"]=height
        self.data_dict["width"]=width
        self.shape_dict.append(coordlist)
        self.skip_label.append(0)

    def undo(self):
        self.shape_dict.remove(self.shape_dict[-1])

    def get_shape_dict(self):
        return self.shape_dict

    def debug(self):
        print("*"*10)
        print(self.shape_dict)
        print("*" * 10)



    def unite_overlap_part(self):
        self.data_dict["labels"]=[]
        for i in range(len(self.shape_dict)):
            temp_pack=[]
            # temp_pack内容顺序 bbox_coordlist, polygon_coordlist, polygon_area, category_id
            if self.skip_label[i]==1:
                continue
            for j in range(i+1,len(self.shape_dict)):
                if self.shape_dict[i][-1]==self.shape_dict[j][-1] and self.shape_dict[i][0]!=self.shape_dict[j][0] and self.skip_label[j]==0:
                    minxi,minyi,maxxi,maxyi=map_min_max(self.data_dict,self.shape_dict[i])
                    minxj, minyj, maxxj, maxyj = map_min_max(self.data_dict,self.shape_dict[j])
                    print("overlap:",overlap_area([minxi, minyi, maxxi, maxyi], [minxj, minyj, maxxj, maxyj]))
                    if overlap_area([minxi,minyi,maxxi,maxyi],[minxj, minyj, maxxj, maxyj])>=0.8:
                        if self.shape_dict[i][0]==1:
                            temp_pack.append(self.shape_dict[i][1:-1])
                            temp_pack.append(self.shape_dict[j][1:-1])
                            temp_pack.append(calculate_shape(self.shape_dict[j][1:-1]))
                        else:
                            temp_pack.append(self.shape_dict[j][1:-1])
                            temp_pack.append(self.shape_dict[i][1:-1])
                            temp_pack.append(calculate_shape(self.shape_dict[i][1:-1]))
                        temp_pack.append(self.shape_dict[i][-1])
                        self.skip_label[j]=1

            if len(temp_pack)==0:
                if self.shape_dict[i][0] == 1:
                    temp_pack.append(self.shape_dict[i][1:-1])
                    temp_pack.append([])
                    temp_pack.append(-1)
                else:
                    temp_pack.append([])
                    temp_pack.append(self.shape_dict[i][1:-1])
                    temp_pack.append(calculate_shape(self.shape_dict[i][1:-1]))
                temp_pack.append(self.shape_dict[i][-1])
            self.data_dict["labels"].append(temp_pack)


    def save(self,path,name):
        print(self.data_dict)
        self.unite_overlap_part()
        print(self.data_dict)
        label_name=self.saver.JSONModify(self.data_dict)
        self.saver.JSONWrite(path,name,label_name)
        return label_name

