from tkinter import simpledialog
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.messagebox as mb
import tkinter.filedialog as dir
from Shape import ShapeLabel
from lib.JSON_LIB import *
import os,filetype
from shutil import copyfile
from lib.YAML_LIB import *
IMAGE_FILE_TYPE = ['jpg','JPG','PNG','png','bmp','BMP']

class CallBackFcn():
    def __init__(self):
        self.image_index = 0  # 当前处理的图像索引
        self.current_path= None
        self.current_width=0
        self.current_height=0
        self.image_paths = []  # 工作目录下的所有文件路径
        self.image_names = []
        self.image_label = []
        self.is_reference=0
        self.shapeLabel=ShapeLabel()
        self.jsonParser=JSON()
        self.work_dir = ''
        self.factor = 1.0  # 图像缩放因子
        self.x = 0
        self.y = 0  # 存储坐标
        self.clicked = False
        self.draw_available = False
        self.number = 0  # 用于矩形画图时直线提醒
        self.lable_Type = 0  # 标注类型
        self.scatter_point = []
        self.canvas=None
        self.hbar=None
        self.vbar=None
        self.image_name_tree=None
        self.viewmethos=None

    def menu_click_event(self):
        '''菜单事件'''
        pass

    ##########################
    ## image tree callbacks ##
    ##########################
    # 创建图像树
    def create_image_tree(self,tree,work_path):
        tr_root = tree.insert("", 0, None, open=True, text='工作目录',values=('root'))  # 树视图添加根节点
        node = tree.insert(tr_root, 0, None, open=True, text=work_path,values=('path'))  # 根节点下添加一级节点
        self.image_names.reverse()
        for i in range(len(self.image_names)):
            tree.insert(node, 0, None, text=self.image_names[i],values=(self.image_names[i],i))  # 添加二级节点
        self.image_names.reverse()
        tree.bind('<ButtonRelease-1>', self.image_tree_click)  # 绑定单击离开事件

    def clean_image_tree(self, tree):
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    # 单击图像树回调函数
    def image_tree_click(self, event):  # 单击
        for item in self.viewmethos.image_name_tree.selection():
            item_text = self.viewmethos.image_name_tree.item(item, "values")
            #点击根节点时不显示
            if item_text[0] in ['root', 'path']:
                continue
            self.image_index = len(self.image_names) - int(item_text[1]) - 1
            if self.image_index > 0:
                self.viewmethos.pre_image.config(state=tk.ACTIVE)
            if self.image_index == len(self.image_names) - 1:
                self.viewmethos.pre_image.config(state=tk.DISABLED)
            #print(self.image_index, item_text)
            image_path = self.work_dir + '/' + item_text[0]
            self._reset()
            self.remove_canvas_lable_all()
            self.showImage(image_path)


    ##########################
    ## label tree callbacks ##
    ##########################
    #创建标签树
    def create_lable_tree(self, tree):
        self.tr_root = tree.insert("", 0, None, open=True, text='图像信息', values=('root'))  # 树视图添加根节点
        tree.bind('<Button-1>', self.lable_tree_click)  # 绑定单击离开事件
        tree.bind('<Button-3>', self.lable_tree_Rclick)
    # lable 树左键点击事件
    def lable_tree_click(self, event):  # 单击
        for item in self.viewmethos.lable_tree.selection():
            item_text = self.viewmethos.lable_tree.item(item, "values")
            if item_text[0] == 'root':
                continue
            print(item_text[0])
    #lable 树右键点击事件
    def lable_tree_Rclick(self,event):
        for item in self.viewmethos.lable_tree.selection():
            item_text = self.viewmethos.lable_tree.item(item, "values")
            if item_text[0] == 'root':
                print('已经点击了右键' + 'root')
            else:
                print('已经点击了右键')
    # lable 树插入标签
    def insert_label_tree(self,tree,content):
        tree.insert(self.tr_root, 0, None, text=content, values=(content))  # 添加二级节点
    # 清空label 树

    def insert_info(self,**kwargs):
        var_dict=kwargs
        image_name=var_dict["image_name"]
        image_size=var_dict["image_size"]
        self.viewmethos.lable_tree.insert(self.tr_root, 'end', None, text=image_name, values=(image_name))
        self.viewmethos.lable_tree.insert(self.tr_root, 'end', None, text=image_size, values=(image_size))
        self.viewmethos.lable_tree.insert(self.tr_root, 'end', None, text="标注信息:", values=("label_info"))
        #print(self.image_label)
        for idx in range(len(self.image_label)):
            self.viewmethos.lable_tree.insert(self.tr_root, 'end', None, text=self.image_label[idx],values=(self.image_label[idx]))





    def clean_label_tree(self,tree):
        x=tree.get_children()
        for item in x:
            tree.delete(item)
        self.tr_root = tree.insert("", 0, None, open=True, text='图像信息', values=('root'))

    ##########################
    ##    file  callbacks   ##
    ##########################
    def renew(self):
        self.image_index = 0  # 当前处理的图像索引
        self.current_path = None
        self.current_width = 0
        self.current_height = 0
        self.image_paths = []  # 工作目录下的所有文件路径
        self.image_names = []
        self.image_label = []
        self.is_reference = 0
        self.work_dir = ''
        self.factor = 1.0  # 图像缩放因子
        self.x = 0
        self.y = 0  # 存储坐标
        self.clicked = False
        self.draw_available = False
        self.number = 0  # 用于矩形画图时直线提醒
        self.lable_Type = 0  # 标注类型
        self.scatter_point = []
        self.clean_image_tree(self.viewmethos.image_name_tree)


    # 选择工作路径
    def set_work_dir(self,classmethods):
        self.viewmethos=classmethods
        work_dir = dir.Directory()
        temp_dir = work_dir.show(initialdir='.', title='设置工作目录')
        if temp_dir != '':
            self.renew()
            self.remove_canvas_lable_all()
            self.work_dir = temp_dir
            self.get_all_img()
            if len(self.image_paths) < 1:
                mb.showinfo("提醒", "当前目录没有图片！")
                return
            self.showImage(self.image_paths[self.image_index])
            # self.image_index = self.image_index + 1
            classmethods.next_image.config(state=tk.ACTIVE)
            self.create_image_tree(self.viewmethos.image_name_tree, self.work_dir)
            self.viewmethos.zoomIn_image.config(state=tk.ACTIVE)
            self.viewmethos.zoomOut_image.config(state=tk.ACTIVE)
            self.viewmethos.revoke.config(state=tk.ACTIVE)
            self.viewmethos.label_rect.config(state=tk.ACTIVE)
            self.viewmethos.label_scat.config(state=tk.ACTIVE)
            self.viewmethos.save_lable.config(state=tk.ACTIVE)
            self.viewmethos.show_lable.config(state=tk.ACTIVE)
            #self.draw_available = True
        else:
            mb.showinfo("提醒", "目录选择失败！")

        # 下一张图片
    # 遍历路径下所有图片
    def get_all_img(self):
        """
        遍历文件夹下所有图像文件
        :param classmethods:
        :return: None
        """
        path = self.work_dir
        file_list = os.listdir(path)
        for i in range(len(file_list)):
            name = path + '/' + file_list[i]
            kind = filetype.guess(name)
            if kind and kind.extension in IMAGE_FILE_TYPE:
                self.image_paths.append(name)
                self.image_names.append(file_list[i])
    # 下一张图片
    def get_next_image(self):
        #self.save_lable_file()
        if len(self.image_paths) < 1:
            mb.showerror("错误", "当前目录中没有图片，请重新设置目录！")
            return
        if len(self.image_paths) - 1 < self.image_index + 1:
            mb.showinfo('提醒', '已经到最后一张！')
            self.viewmethos.next_image.config(state=tk.DISABLED)
            return
        self.remove_canvas_lable_all()
        if self.image_index == 0:
            self.viewmethos.pre_image.config(state=tk.ACTIVE)
        self.canvas.delete(tk.ALL)
        names = self.image_paths[self.image_index + 1]
        self._reset()
        self.showImage(names)
        self.image_index = self.image_index + 1




    # 上一张图片
    def get_pre_image(self):
        if self.image_index < 1:
            mb.showinfo("提醒", "已经是第一张照片了！")
            self.viewmethos.pre_image.config(state=tk.DISABLED)
            return
        self.remove_canvas_lable_all()
        if self.image_index == len(self.image_paths) - 1:
            self.viewmethos.next_image.config(state=tk.ACTIVE)
        names = self.image_paths[self.image_index - 1]
        self._reset()
        self.showImage(names)
        self.image_index = self.image_index - 1
        # 在canvas上显示图片

    # 显示图片
    def showImage(self, image_path):
        global img
        self.canvas.configure(width=1200, height=700)
        self.current_path = image_path
        img = Image.open(image_path)
        w, h = img.size
        w_factor = int(w * self.factor)
        h_factor = int(h * self.factor)
        self.current_width = int(w * self.factor)
        self.current_height = int(h * self.factor)
        img = img.resize((w_factor, h_factor), Image.ANTIALIAS)
        #img = self.resize(img, w, h, 800, 600)
        #w, h = img.size
        img = ImageTk.PhotoImage(img)

        try:
            self.clean_label_tree(self.viewmethos.lable_tree)
            self.insert_info(image_name=self.image_names[self.image_index],image_size=str(w)+"x"+str(h))
        except:
            print("load image info failed!")

        self.canvas.create_image(0, 0, image=img, anchor='nw', tags='show_image')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def zoom_in_image(self):
        global img_in
        self.remove_canvas_lable_all()
        img_in = Image.open(self.current_path)
        w, h = img_in.size
        self.factor = self.factor * 1.1
        w = int(w * self.factor)
        h = int(h * self.factor)
        self.current_width=w
        self.current_height=h
        img_in = img_in.resize((w, h), Image.ANTIALIAS)
        img_in = ImageTk.PhotoImage(img_in)
        #self.canvas.configure(width=1200, height=800)
        self.canvas.create_image(0, 0, image=img_in, anchor='nw', tags='show_image')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.vbar.config(command=self.canvas.yview)
        self.hbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)


    def zoom_out_image(self):
        global img_out
        self.remove_canvas_lable_all()
        img_out = Image.open(self.current_path)
        w, h = img_out.size
        self.factor = self.factor * 0.9
        w = int(w *self.factor)
        h = int(h *self.factor)
        self.current_width = w
        self.current_height = h
        img_out = img_out.resize((w, h), Image.ANTIALIAS)
        img_out = ImageTk.PhotoImage(img_out)

        self.canvas.create_image(0, 0, image=img_out, anchor='nw', tags='show_image')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.vbar.config(command=self.canvas.yview)
        self.hbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

    def show_label(self,model="manual"):
        self.remove_canvas_lable_all()
        self.showImage(self.image_paths[self.image_index])
        throw=True
        try:
            name = self.image_names[self.image_index].split(".")[0]
            labels=self.jsonParser.fetchLabel(name)
            self.draw_previous(labels)
            throw=False
        except:
            pass
        try:
            labels = self.shapeLabel.get_shape_dict()
            if len(labels)<=0:
                raise RuntimeError('testError')
            self.draw_previous(labels)
            #print(labels)
            throw=False
        except:
            if model=="manual" and throw:
                tk.messagebox.showinfo('提示', '未标注或标注未保存')

    def revoke_label(self):
        try:
            self.shapeLabel.undo()
            self.show_label(model="view")
        except:
            pass
    ##########################
    ##   canvas callbacks   ##
    ##########################


    def draw_previous(self,labels):
        for label in labels:
            if label[0]==1:
                self.draw_rectangle_previous(label[1:])
                if label[-1] not in self.image_label:
                    self.viewmethos.lable_tree.insert(self.tr_root, 'end', None, text=label[-1], values=(label[-1]))  # 添加标签数
                    self.image_label.append(label[-1])
            else:
                self.draw_polygon_previous(label[1:])
                if label[-1] not in self.image_label:
                    self.viewmethos.lable_tree.insert(self.tr_root, 'end', None, text=label[-1], values=(label[-1]))  # 添加标签数
                    self.image_label.append(label[-1])

    def draw_rectangle_previous(self,coords):
        self.canvas.create_line((int(self.factor*(coords[0]-coords[2]/2)), int(self.factor*(coords[1]-coords[3]/2))), (int(self.factor*(coords[0]-coords[2]/2)), int(self.factor*(coords[1]+coords[3]/2))), width=3, fill='red')
        self.canvas.create_line((int(self.factor*(coords[0] - coords[2] / 2)), int(self.factor*(coords[1] - coords[3] / 2))),(int(self.factor*(coords[0] + coords[2] / 2)), int(self.factor*(coords[1] - coords[3] / 2))), width=3, fill='red')
        self.canvas.create_line((int(self.factor*(coords[0] + coords[2] / 2)), int(self.factor*(coords[1] + coords[3] / 2))),(int(self.factor*(coords[0] + coords[2] / 2)), int(self.factor*(coords[1] - coords[3] / 2))), width=3, fill='red')
        self.canvas.create_line((int(self.factor*(coords[0] + coords[2] / 2)), int(self.factor*(coords[1] + coords[3] / 2))),(int(self.factor*(coords[0] - coords[2] / 2)), int(self.factor*(coords[1] + coords[3] / 2))), width=3, fill='red')

    def draw_polygon_previous(self,coords):
        for i in range(len(coords)-2):
            self.canvas.create_line((int(self.factor*(coords[i][0])), int(self.factor*(coords[i][1]))),(int(self.factor*(coords[i+1][0])), int(self.factor*(coords[i+1][1]))), width=3,fill='green')
        self.canvas.create_line((int(self.factor*(coords[0][0])), int(self.factor*(coords[0][1]))), (int(self.factor*(coords[-2][0])), int(self.factor*(coords[-2][1]))), width=3,fill='green')

    def mouse_on_canvas(self, event):
        event_x = int(event.x + self.canvas.xview()[0] * self.current_width)
        event_y = int(event.y + self.canvas.yview()[0] * self.current_height)

        self.canvas.delete("xline")
        self.canvas.delete("ylines")
        self.canvas.create_line((event_x, 0), (event_x,int(800*self.factor)), width=2, fill='blue',tags="xline")
        self.canvas.create_line((0, event_y), (int(1200*self.factor), event_y), width=2, fill='blue',tags="ylines")


        if self.lable_Type == 1 and self.work_dir != '' and self.clicked and self.draw_available:
            self.canvas.delete('mouse_move_paint_line' + str(self.number - 1))
            self.canvas.delete('mouse_move_paint_rect' + str(self.number - 1))
            self.canvas.create_line((self.x, self.y), (event_x, event_y), width=3, fill='red',tags='mouse_move_paint_line' + str(self.number))
            self.canvas.create_rectangle((self.x, self.y), (event_x, event_y), width=3, outline='green',stipple='gray12', tags='mouse_move_paint_rect' + str(self.number))
            self.number = self.number + 1
        elif self.lable_Type == 2 and self.work_dir != '' and len(self.scatter_point) > 0 and self.clicked and self.draw_available:
            self.canvas.delete("xline")
            self.canvas.delete("ylines")
            last_p = self.scatter_point[-1]
            self.canvas.delete('2_mouse_move_paint_line' + str(self.number - 1))
            self.canvas.create_line((last_p[0], last_p[1]), (event_x, event_y), width=3,tags='2_mouse_move_paint_line' + str(self.number))
            self.number += 1

            if len(self.scatter_point) > 1 and self.scatter_point[0][0] < event_x + 5 and self.scatter_point[0][
                0] > event_x - 5 and self.scatter_point[0][1] < event_y + 5 and self.scatter_point[0][1] > event_y - 5:
                first_p = self.scatter_point[0]
                self.canvas.create_oval((first_p[0] - 10, first_p[1] - 10, first_p[0] + 10, first_p[1] + 10),
                                        fill='green', tags='oval_exp')
            else:
                self.canvas.delete('oval_exp')

        # 点击鼠标左键监听事件，用于获取点击鼠标的位置（x,y）,没有使用

    def left_mouse_click(self, event):
        event_x=int(event.x+self.canvas.xview()[0]*self.current_width)
        event_y=int(event.y+self.canvas.yview()[0]*self.current_height)
        #print(event.x,event.y,self.canvas.xview()[0],self.canvas.xview()[1],self.canvas.yview()[0])

        if self.draw_available:
            self.canvas.create_oval((event_x - 5, event_y - 5, event_x + 5, event_y + 5), fill='red', tags='oval')

        if self.lable_Type == 1:
            if self.clicked:
                self.clicked = False
                self.viewmethos.label_scat.config(state=tk.ACTIVE)
                self.viewmethos.label_rect.config(state=tk.ACTIVE)
                lDialog = LabelDialog()
                self.viewmethos.wait_window(lDialog)
                try:
                    r = lDialog.userinfo

                    if self.image_index >= 0 and r != None:
                        if r[0] not in self.image_label:
                            self.image_label.append(r[0])
                            self.viewmethos.lable_tree.insert(self.tr_root, 'end', None, text=r[0], values=(r[0]))
                        self.is_reference = r[1]
                        coord=[self.lable_Type,(self.x+event_x)/2/self.factor ,(self.y+event_y)/2/self.factor,(event_x - self.x)/self.factor,(event_y - self.y)/self.factor ,r[0]]
                        self.shapeLabel.addShape(self.image_names[self.image_index],int(self.current_height/self.factor),int(self.current_width/self.factor),coord,r[1])
                        self.shapeLabel.debug()
                    else:
                        raise RuntimeError("return None")
                except:
                    self.remove_canvas_lable_all()
                    self.showImage(self.image_paths[self.image_index])
                self.draw_available = False
            else:
                self.x = event_x
                self.y = event_y
                self.clicked = True

        elif self.lable_Type == 2:
            if not self.clicked:
                self.scatter_point.clear()
                self.clicked = True
                self.scatter_point.append([event_x, event_y])
            else:
                last_p = self.scatter_point[-1]
                self.canvas.create_line((last_p[0], last_p[1]), (event_x, event_y), fill='green', width=3, tags='line')

                if len(self.scatter_point) > 0 and self.scatter_point[0][0] < event_x + 5 and self.scatter_point[0][
                    0] > event_x - 5 and self.scatter_point[0][1] < event_y + 5 and self.scatter_point[0][1] > event_y - 5:
                    self.clicked = False
                    self.viewmethos.label_scat.config(state=tk.ACTIVE)
                    self.viewmethos.label_rect.config(state=tk.ACTIVE)
                    lDialog = LabelDialog()
                    self.viewmethos.wait_window(lDialog)
                    try:
                        r=lDialog.userinfo

                        if self.image_index >= 0 and r != None:
                            if r[0] not in self.image_label:
                                self.image_label.append(r[0])
                                self.viewmethos.lable_tree.insert(self.tr_root, 'end', None, text=r[0],values=(r[0]))
                            self.is_reference = r[1]
                            coord = [[int(coordtuple[0]/self.factor),int(coordtuple[1]/self.factor)] for coordtuple in self.scatter_point]
                            coord.append(r[0])
                            coord.insert(0,self.lable_Type)
                            self.shapeLabel.addShape(self.image_names[self.image_index],int(self.current_height/self.factor),int(self.current_width/self.factor),coord,r[1])
                            self.shapeLabel.debug()
                            self.scatter_point.clear()
                        else:
                            raise RuntimeError("return None")
                    except:
                        self.remove_canvas_lable_all()
                        self.showImage(self.image_paths[self.image_index])
                    self.draw_available = False
                else:
                    self.scatter_point.append([event_x, event_y])


        #

    def save_lable_file(self):
        if not os.path.exists("./annotation_output/"):
            os.mkdir("./annotation_output/")
        name=(self.image_names[self.image_index]).split(".")[0]
        label_name=self.shapeLabel.save("./annotation_output/",name+".json")
        if self.is_reference:
            copyfile(self.current_path, "./annotation_output/" +label_name+"-"+name + ".jpg")
        else:
            copyfile(self.current_path, "./annotation_output/"  + name + ".jpg")
        self.viewmethos.label_rect.config(state=tk.ACTIVE)
        self.viewmethos.label_scat.config(state=tk.ACTIVE)

        # 重置大小

    def remove_canvas_lable_all(self):
        self.lable_Type=0
        self.canvas.delete(tk.ALL)
        if len(self.image_paths) < 1:
            return
        #self.showImage(self.image_paths[self.image_index])
        self.scatter_point.clear()
        self.number = 0
        # self.image_index = self.image_index + 1
        # self.next_image.config(state=tk.ACTIVE)

        # 设置工作目录

    def resize(self, pil_image, w, h, w_box=0, h_box=0):
        if w_box == 0 or h_box == 0:
            w_box = w
            h_box = h
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h
        self.factor = min([f1, f2])
        width = int(w * self.factor)
        height = int(h * self.factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    # Radiobutton选择时回调
    def radiobutton_change(self):
        #print(self.lable_Type.get())
        self.number = 0


    ##########################
    ## annotation callbacks ##
    ##########################
    # 创建矩形框
    def create_label_rect(self):
        self.lable_Type = 1
        self.canvas.delete(tk.ALL)
        if len(self.image_paths) < 1:
            return
        self.showImage(self.image_paths[self.image_index])
        self.viewmethos.label_scat.config(state=tk.DISABLED)
        self.draw_available = True

        #
    # 创建散点图
    def create_label_scat(self):
        self.lable_Type = 2
        self.canvas.delete(tk.ALL)
        if len(self.image_paths) < 1:
            return
        self.showImage(self.image_paths[self.image_index])
        self.viewmethos.label_rect.config(state=tk.DISABLED)
        self.draw_available = True

        # 保存标签

    def _reset(self):
        self.x = 0
        self.y = 0
        self.is_reference = 0
        self.factor=1.0
        self.shapeLabel.clear()
        self.clean_label_tree(self.viewmethos.lable_tree)
        self.image_label = []



class LabelDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('设置类别信息')
        self.geometry('300x300')
        self.yamlParser=LabelYAML("labelDef.yaml")
        # 弹窗界面
        self._process_label()

        self.setup_UI()


    def setup_UI(self):

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.frame = tk.Frame(self, relief=tk.FLAT)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame.columnconfigure(0, weight=1)


        tk.Label(self.frame, text='输入类标信息：',font='Times 9').grid(row=0,column=0,sticky=tk.NW)
        self.labelName = tk.StringVar()
        self.labelEntry=tk.Entry(self.frame,textvariable=self.labelName,font='Times 9')
        self.labelEntry.grid(row=1,column=0,sticky=tk.EW,padx=10)
        tk.Button(self.frame, text="新建类别", command=self.insert_label, font='Times 9').grid(row=1, column=1,sticky=tk.EW, padx=10,pady=10)

        tk.Label(self.frame, text='已有类标：',font='Times 9').grid(row=2,column=0,sticky=tk.NW)
        list1 = tk.StringVar(value=self.labels)
        self.listbox1 = tk.Listbox(self.frame,height=7,listvariable=list1,selectmode="browse",font='Times 9')
        self.listbox1.grid(row=3,column=0,columnspan=2,sticky=tk.NSEW,padx=10)

        yscrollbar = tk.Scrollbar(self.frame,orient=tk.VERTICAL)
        yscrollbar.grid(row=3, column=2, sticky="nsew")
        yscrollbar.config(command=self.listbox1.yview)
        self.listbox1.config(yscrollcommand=yscrollbar.set)
        #yscrollbar.config(command)

        self.listbox1.bind("<<ListboxSelect>>",self.show_msg)
        self.var_isRef = tk.IntVar()
        tk.Checkbutton(self.frame, text="Refernece图片", variable=self.var_isRef,font='Times 10 ').grid(row=4, column=0,sticky=tk.SW,padx=10, pady=10)
        tk.Button(self.frame, text="取消", command=self.cancel,font='Times 9').grid(row=5,column=0,sticky=tk.NSEW,padx=10, pady=10,)
        tk.Button(self.frame, text="确定", command=self.ok,width=16,font='Times 9').grid(row=5,column=1,sticky=tk.NSEW,padx=10, pady=10)

    def show_msg(self,*args):
        indexs = self.listbox1.curselection()
        index = int(indexs[0])
        print(self.labels[index])
        self.labelName.set(self.labels[index])


    def _process_label(self,fcn_type="read"):
        if fcn_type=="read":
            self.labelPAML = self.yamlParser.read()
            self.yamlParser.generate_relation()
            _,self.labels=self.yamlParser.get_label()
            self.labels=tuple(self.labels)

        if fcn_type=="check":
            self.labels=list(self.labels)
            current_label=self.labelName.get()
            if current_label!="" and current_label not in self.labels:
                self.labels=[]
                self.yamlParser.add_content(current_label,self.new_father,self.new_id)
                self.yamlParser.generate_relation()
                _, self.labels = self.yamlParser.get_label()
                self.labels = tuple(self.labels)

        if fcn_type=="save":
            self.yamlParser.save()

    def insert_label(self):
        if self.labelName.get()!="" and self.labelName.get() not in list(self.labels):
            temp=self.labelName.get()
            temp=temp.split(":")
            try:
                self.labels=list(self.labels)
                self.labels.append(temp[1])
                self.labels=tuple(self.labels)
                self.after(10,self.setup_UI())
                self.new_father=temp[0]
                self.new_id=temp[2]

            except:
                tk.messagebox.showinfo('错误', '输入格式或内容错误')
            self.yamlParser.add_content(temp[1], self.new_father, self.new_id)
        else:
            tk.messagebox.showinfo('错误', '输入为空或已存在同名类别')

    def ok(self):
        self._process_label(fcn_type="check")
        self._process_label(fcn_type="save")
        self.userinfo = [self.labelName.get(),self.var_isRef.get()]
        self.destroy() # 销毁窗口

    def cancel(self):
        self.userinfo = None # 空！
        self.destroy()
