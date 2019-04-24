from yaml import load,dump



class LabelYAML():
    def __init__(self,filepath):
        self.filepath=filepath
        self.label_dict={}
        self.label_list=[]

    def read(self):
        with open(self.filepath, 'rb') as f:
            cont = f.read()
        self.labelPAML = load(cont)
        return self.labelPAML

    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            dump(self.labelPAML, f)

    def get_label(self):
        return self.label_dict,self.label_list

    def add_content(self,labelname,father,ids):
        self.label_dict[labelname]={"father":father,"id":int(ids)}
        print(self.label_dict)
        if father==None:
            self.labelPAML[labelname]=int(ids)
        else:
            category_id=[]
            chilename=labelname
            while self.label_dict[chilename]["father"] != None:
                category_id.append(self.label_dict[chilename]["father"])
                chilename = self.label_dict[chilename]["father"]
            category_id.reverse()
            change_str="self.labelPAML"
            for i in category_id:
                change_str=change_str+"[\""+i+"\"]"

            if type(eval(change_str))==dict:
                exec(change_str + "[labelname]=int(ids)")
            else:
                current_id=eval(change_str)
                exec(change_str+"={category_id[-1]:current_id,labelname:int(ids)}")
                exec("print(change_str)")







    def generate_relation(self,dict_cotent=None,father=None):
        if dict_cotent==None:
            dict_cotent=self.labelPAML
        for k,v in dict_cotent.items():
            if type(v)!=dict:
                if father==None or father==k:
                    self.label_dict[k]={"father":None,"id":v}
                    self.label_list.append(k)
                else:
                    father_list=father.split("-")
                    if len(father_list)<=1:
                        self.label_dict[k]={"father":father,"id":v}
                    else:
                        if father_list[-1]==k:
                            self.label_dict[k] = {"father": father_list[-2], "id": v}
                        else:
                            self.label_dict[k] = {"father": father_list[-1], "id": v}
                    self.label_list.append(k)
            else:
                if father!=None:
                    father=father+"-"+k
                else:
                    father=k
                self.generate_relation(v,father=father)
                father=None


    def id2name(self,id_str):
        id_list=id_str.split('-')
        label_name=None
        for i in range(len(id_list)):
            for k,v in self.label_dict.items():
                if v["father"]==label_name and v["id"]==int(id_list[i]):
                    label_name=k
                    continue
        return label_name


    def cluster_family(self,childname):
        # find father
        category_id=[]
        self.generate_relation()
        while self.label_dict[childname]["father"]!=None:
            category_id.append(self.label_dict[childname]["id"])
            childname=self.label_dict[childname]["father"]
        category_id.append(self.label_dict[childname]["id"])
        category_id.reverse()
        # generate family-str
        result_id=""
        if len(category_id)==1:
            result_id=str(category_id[0])
            return result_id

        for i in range(len(category_id)-1):
            result_id=result_id+str(category_id[i])+"-"
        result_id=result_id+str(category_id[-1])
        return result_id