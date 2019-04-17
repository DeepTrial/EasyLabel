from tkinter import simpledialog
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.messagebox as mb
import tkinter.filedialog as dir
from lib import XML_LIB
import os,filetype
from shutil import copyfile
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
        self.work_dir = ''
        self.factor = 1.0  # 图像缩放因子
        self.x = 0
        self.y = 0  # 存储坐标
        self.clicked = False
        self.draw_available = False
        self.number = 0  # 用于矩形画图时直线提醒
        self.lable_Type = 0  # 标注类型
        self.scatter_point = []
        self.lable_save_file = XML_LIB.XMLWrite('.', 'test')
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
            self.showImage(image_path)


    ##########################
    ## label tree callbacks ##
    ##########################
    #创建标签树
    def create_lable_tree(self, tree):
        self.tr_root = tree.insert("", 0, None, open=True, text='标签类别', values=('root'))  # 树视图添加根节点
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

    def insert_label_tree(self,tree,lable_list):
        tree.insert(self.tr_root, 0, None, text=lable_list, values=(lable_list))  # 添加二级节点

    ##########################
    ##    file  callbacks   ##
    ##########################
    # 选择工作路径
    def set_work_dir(self,classmethods):
        self.viewmethos=classmethods
        work_dir = dir.Directory()
        temp_dir = work_dir.show(initialdir='.', title='设置工作目录')
        if temp_dir != '':
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
            self.draw_available = True
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
        self.showImage(names)
        self.image_index = self.image_index + 1
        self.x = 0
        self.y = 0

        # 前一张图片
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
        self.showImage(names)
        self.image_index = self.image_index - 1
        self.x = 0
        self.y = 0

        # 在canvas上显示图片
    # 显示图片
    def showImage(self, image_path):
        global img
        self.canvas.configure(width=1200, height=700)
        self.current_path = image_path
        img = Image.open(image_path)
        w, h = img.size
        self.current_width = w
        self.current_height = h
        #img = self.resize(img, w, h, 800, 600)
        #w, h = img.size
        img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=img, anchor='nw', tags='show_image')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_in_image(self):
        global img
        self.remove_canvas_lable_all()
        img = Image.open(self.current_path)
        w, h = img.size
        self.factor = self.factor * 1.1
        w = int(w * self.factor)
        h = int(h * self.factor)
        self.current_width=w
        self.current_height=h
        img = img.resize((w, h), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        #self.canvas.configure(width=1200, height=800)
        self.canvas.create_image(0, 0, image=img, anchor='nw', tags='show_image')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.vbar.config(command=self.canvas.yview)
        self.hbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

    def zoom_out_image(self):
        global img
        self.remove_canvas_lable_all()
        img = Image.open(self.current_path)
        w, h = img.size
        self.factor = self.factor * 0.9
        w = int(w *self.factor)
        h = int(h *self.factor)
        self.current_width = w
        self.current_height = h
        img = img.resize((w, h), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        #self.canvas.configure(width=1000, height=600)
        self.canvas.create_image(0, 0, image=img, anchor='nw', tags='show_image')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    ##########################
    ##   canvas callbacks   ##
    ##########################

    def mouse_on_canvas(self, event):
        event_x = int(event.x + self.canvas.xview()[0] * self.current_width)
        event_y = int(event.y + self.canvas.yview()[0] * self.current_height)
        if self.lable_Type == 1 and self.work_dir != '' and self.clicked and self.draw_available:
            self.canvas.delete('mouse_move_paint_line' + str(self.number - 1))
            self.canvas.delete('mouse_move_paint_rect' + str(self.number - 1))
            self.canvas.create_line((self.x, self.y), (event_x, event_y), width=3, fill='red',
                                    tags='mouse_move_paint_line' + str(self.number))
            self.canvas.create_rectangle((self.x, self.y), (event_x, event_y), width=3, fill='#000', outline='green',
                                         stipple='gray12', tags='mouse_move_paint_rect' + str(self.number))
            self.number = self.number + 1
        elif self.lable_Type == 2 and self.work_dir != '' and len(
                self.scatter_point) > 0 and self.clicked and self.draw_available:
            last_p = self.scatter_point[-1]
            self.canvas.delete('2_mouse_move_paint_line' + str(self.number - 1))
            self.canvas.create_line((last_p[0], last_p[1]), (event_x, event_y), width=3,
                                    tags='2_mouse_move_paint_line' + str(self.number))
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
                r = lDialog.userinfo
                #r = simpledialog.askstring('标签', '请输入标签', initialvalue='浙AXXXX')
                if self.image_index >= 0 and r != None:
                    if r[0] not in self.image_label:
                        self.insert_label_tree(self.viewmethos.lable_tree, r[0])  # 添加标签数
                        self.image_label.append(r[0])

                    self.lable_save_file.create_object(self.image_paths[self.image_index], 'image', 'path')
                    self.lable_save_file.set_lable_info(r[0], lable_name='palte')
                    self.lable_save_file.set_position_rect('poiston', w=self.factor * (event_x - self.x),
                                                           h=self.factor * (event_y - self.y), x=self.factor * self.x,
                                                           y=self.factor * self.y)
            else:
                self.x = event_x;
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
                    0] > event_x - 5 and self.scatter_point[0][1] < event_y + 5 and self.scatter_point[0][
                    1] > event_y - 5:
                    self.clicked = False
                    self.viewmethos.label_scat.config(state=tk.ACTIVE)
                    self.viewmethos.label_rect.config(state=tk.ACTIVE)
                    lDialog = LabelDialog()
                    self.wait_window(lDialog)
                    r=lDialog.userinfo
                    #r = simpledialog.askstring('标签', '请输入标签', initialvalue='浙AXXXX')
                    if self.image_index >= 0 and r != None:
                        info = {'lt': self.scatter_point[0], 'rt': self.scatter_point[1], 'lb': self.scatter_point[2],
                                'rb': self.scatter_point[3]}
                        self.lable_save_file.create_object(self.image_paths[self.image_index], 'image', 'path')
                        self.lable_save_file.set_lable_info(r[0], lable_name='palte')
                        self.lable_save_file.set_position_scat('poiston', info)
                        self.scatter_point.clear()
                else:
                    self.scatter_point.append([event_x, event_y])

        #

    def save_lable_file(self):
        if not os.path.exists("./annotation_output/"):
            os.mkdir("./annotation_output/")
        copyfile(self.current_path,"./annotation_output/1.jpg")
        self.lable_save_file.save()
        self.viewmethos.label_rect.config(state=tk.ACTIVE)
        self.viewmethos.label_scat.config(state=tk.ACTIVE)

        # 重置大小

    def remove_canvas_lable_all(self):
        self.lable_Type=0
        self.canvas.delete(tk.ALL)
        if len(self.image_paths) < 1:
            return
        self.showImage(self.image_paths[self.image_index])
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
        print(self.factor)
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

        #
    # 创建散点图
    def create_label_scat(self):
        self.lable_Type = 2
        self.canvas.delete(tk.ALL)
        if len(self.image_paths) < 1:
            return
        self.showImage(self.image_paths[self.image_index])
        self.viewmethos.label_rect.config(state=tk.DISABLED)

        # 保存标签



class LabelDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('设置类别信息')
        self.geometry('300x250')
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
        self.labelEntry=tk.Entry(self.frame, textvariable=self.labelName,font='Times 9')
        self.labelEntry.grid(row=1,column=0,columnspan=2,sticky=tk.NSEW,padx=10)


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

        tk.Button(self.frame, text="取消", command=self.cancel,font='Times 9').grid(row=4,column=0,sticky=tk.NSEW,padx=10, pady=10,)
        tk.Button(self.frame, text="确定", command=self.ok,width=16,font='Times 9').grid(row=4,column=1,sticky=tk.NSEW,padx=10, pady=10)

    def show_msg(self,*args):
        indexs = self.listbox1.curselection()
        index = int(indexs[0])
        print(self.labels[index])
        self.labelName.set(self.labels[index])
        print(self.labelName.get())



    def _process_label(self,fcn_type="read"):
        if fcn_type=="read":
            self.labels=[]
            with open("temp_label.txt",'r') as reader:
                lines=reader.readlines()
            for name in lines:
                name=name.replace("\n","")
                self.labels.append(name)
            self.labels=tuple(self.labels)

        if fcn_type=="check":
            self.labels=list(self.labels)
            current_label=self.labelName.get()
            if current_label!="" and current_label not in self.labels:
                self.labels.append(current_label)
                self.labels=tuple(self.labels)

        if fcn_type=="save":
            self.labels = list(self.labels)
            with open("temp_label.txt", 'w') as writer:
                for label_name in self.labels:
                    writer.write(label_name+'\n')


    def ok(self):
        self._process_label(fcn_type="check")
        self._process_label(fcn_type="save")
        self.userinfo = [self.labelName.get(),self.labelName.get()]
        self.destroy() # 销毁窗口

    def cancel(self):
        self.userinfo = None # 空！
        self.destroy()
