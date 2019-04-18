from lib import XML_LIB
import tkinter.ttk as ttk
from CallBackFcn import CallBackFcn
import tkinter as tk
from tkinter import Scrollbar


IMAGE_FILE_TYPE = ['jpg','JPG','PNG','png','bmp','BMP']
cbs = CallBackFcn()

class MainGUI(tk.Frame):
    '''继承tkinker中的frame类，实现可以自动化调整串口的大小'''
    img = None
    def __init__(self,root):
        super().__init__(root)
        self.root = root
        self.initComponent(root)
        #self.initMenu(root)

    # 初始化界面布局
    def initComponent(self,root):
        '''初始化界面上的控件'''
        root.rowconfigure(0,weight=1)
        root.columnconfigure(0,weight=1)
        #self.initMenu(root)  # 为顶级窗体添加菜单项

        # 设置grid布局位置
        self.grid(row=0, column=0, sticky=tk.NSEW)
        # 设置行列权重，保证内建子组件会拉伸填充
        self.rowconfigure(0, weight=1);
        self.columnconfigure(0, weight=1)

        #水平方向推拉组件   #左右布局
        #左边布局
        self.panedwin = ttk.PanedWindow(self,orient=tk.HORIZONTAL)
        self.panedwin.grid(row=0, column=0, sticky=tk.NSEW)


        #左边布局
        self.frame_left = ttk.Frame(self.panedwin,relief=tk.FLAT)
        self.frame_left.grid(row=0,column=0,sticky=tk.NSEW)
        self.frame_left.columnconfigure(0,weight=1)
        self.panedwin.add(self.frame_left,weight=50)

        #右侧布局
        self.frame_right = ttk.Frame(self.panedwin, relief=tk.FLAT)
        self.frame_right.grid(row=0, column=0, sticky=tk.NS)
        self.panedwin.add(self.frame_right, weight=1)
        self.initPlayList()

        #左下显示图片
        lable = tk.Label(self.frame_left,font='Times 16 bold',text="标注区",fg='#4876FF',anchor='nw')
        lable.grid(row=1, column=0,padx=6,pady=6,sticky=tk.NSEW)

        canvas_frame = ttk.Frame(self.frame_left)
        canvas_frame.grid(row=2, column=0)
        canvas_frame.config(width=1000,height=1000)
        cbs.canvas = tk.Canvas(canvas_frame,background='black')
        cbs.canvas.grid(row=0, column=0,sticky=tk.NSEW)

        # SCROLLING BARS
        cbs.vbar = Scrollbar(canvas_frame, orient=tk.VERTICAL)
        cbs.vbar.grid(row=0, column=1, sticky="ns")
        cbs.vbar.config(command=cbs.canvas.yview)
        cbs.hbar = Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        cbs.hbar.grid(row=2, column=0, sticky="ew")
        cbs.hbar.config(command=cbs.canvas.xview)
        cbs.canvas.config(xscrollcommand=cbs.hbar.set, yscrollcommand=cbs.vbar.set)

        cbs.canvas.bind("<Motion>", cbs.mouse_on_canvas)#self.canvas.bind("<B1-Motion>", self.mouse_move)
        cbs.canvas.bind('<Button-1>',cbs.left_mouse_click)
        #self.canvas.bind('<Button-1>',self.left_mouse_click_press)
        #self.canvas.bind('<ButtonRelease-1>', self.left_mouse_click_release)
        cbs.showImage('./icon/welcome.png')

        #左上布局
        # 左侧Frame帧第二行添加控制按钮
        self.frm_control = ttk.Frame(self.frame_left, relief=tk.FLAT)  # 四个方向拉伸
        self.frm_control.grid(row=0, column=0, sticky=tk.NSEW)
        self.initCtrl()  # 添加滑块及按钮
    # 初始化工具栏菜单
    def initMenu(self, master):
        '''初始化菜单'''
        mbar = tk.Menu(master)  # 定义顶级菜单实例
        fmenu = tk.Menu(mbar, tearoff=False)  # 在顶级菜单下创建菜单项
        mbar.add_cascade(label=' 文件 ', menu=fmenu, font=('Times', 14, 'bold'))  # 添加子菜单
        fmenu.add_command(label="打开", command=cbs.menu_click_event)
        fmenu.add_command(label="保存", command=cbs.menu_click_event)
        fmenu.add_separator()  # 添加分割线
        fmenu.add_command(label="退出", command=master.quit())

        etmenu = tk.Menu(mbar, tearoff=False)
        mbar.add_cascade(label=' 编辑 ', menu=etmenu)
        for each in ['复制', '剪切', '合并']:
            etmenu.add_command(label=each, command=cbs.menu_click_event)
        master.config(menu=mbar)  # 将顶级菜单注册到窗体
    # 初始化区域分隔栏
    def initCtrl(self):
        '''初始化控制滑块及按钮'''
        frm_but = ttk.Frame(self.frm_control, padding=2)  # 控制区第二行放置按钮及标签
        frm_but.grid(row=0, column=0, sticky=tk.EW)
        self.initButton()
    # 初始化树状图列表
    def initPlayList(self):
        '''初始化树状视图'''
        self.frame_right.rowconfigure(0, weight=1)  # 左侧Frame帧行列权重配置以便子元素填充布局
        self.frame_right.columnconfigure(0, weight=1)  # 左侧Frame帧中添加树状视图

        self.frame_right.rowconfigure(1, weight=1)  # 左侧Frame帧行列权重配置以便子元素填充布局
        self.frame_right.columnconfigure(1, weight=1)  # 左侧Frame帧中添加树状视图

        #文件名称列表
        self.image_name_tree = ttk.Treeview(self.frame_right, selectmode='browse', show='tree', padding=[0, 0, 0, 0])
        self.image_name_tree.grid(row=0, column=0, sticky=tk.NSEW)  # 树状视图填充左侧Frame帧
        self.image_name_tree.column('#0',width=300)  # 设置图标列的宽度，视图的宽度由所有列的宽决定
        # 一级节点parent='',index=第几个节点,iid=None则自动生成并返回，text为图标右侧显示文字
        # values值与columns给定的值对应
        cbs.create_image_tree(self.image_name_tree,'')

        #标签名称列表
        self.lable_tree = ttk.Treeview(self.frame_right, selectmode='browse', show='tree', padding=[0, 0, 0, 0])
        self.lable_tree.grid(row=1, column=0, sticky=tk.NSEW)  # 树状视图填充左侧Frame帧
        self.lable_tree.column('#0',width=300)  # 设置图标列的宽度，视图的宽度由所有列的宽决定
        # 一级节点parent='',index=第几个节点,iid=None则自动生成并返回，text为图标右侧显示文字
        # values值与columns给定的值对应
        cbs.create_lable_tree(self.lable_tree)
    # 初始化工具箱按钮栏
    def initButton(self):
        lable = tk.Label(self.frm_control, font='Times 16 bold', text="工具箱", fg='#4876FF', anchor='nw')
        lable.grid(row=0, column=0, sticky=tk.NSEW,padx=6,pady=6)

        self.dirImg=tk.PhotoImage(file="./icon/open.png")
        self.dirLabel=tk.Label(self.frm_control,text='设置目录',font=('Times',9))
        self.set_work_dir = tk.Button(self.frm_control,command=lambda:cbs.set_work_dir(self),image=self.dirImg,relief=tk.FLAT)
        self.set_work_dir.grid(row=1, column=0, padx=7,sticky=tk.NSEW)
        self.dirLabel.grid(row=2, column=0, padx=7,sticky=tk.NSEW)

        self.prevImg = tk.PhotoImage(file="./icon/prev.png")
        self.prevLabel=tk.Label(self.frm_control, text='上一张',font=('Times',9))
        self.pre_image = tk.Button(self.frm_control, state=tk.DISABLED, command=cbs.get_pre_image,image=self.prevImg, relief=tk.FLAT)
        self.pre_image.grid(row=1, column=1, padx=7, sticky=tk.NSEW)
        self.prevLabel.grid(row=2, column=1, padx=7, sticky=tk.NSEW)

        self.nextImg = tk.PhotoImage(file="./icon/next.png")
        self.nextLabel = tk.Label(self.frm_control, text='下一张',font=('Times',9))
        self.next_image = tk.Button(self.frm_control,state=tk.DISABLED,command=cbs.get_next_image,image=self.nextImg,relief=tk.FLAT)
        self.next_image.grid(row=1, column=2, padx=7,sticky=tk.NSEW)
        self.nextLabel.grid(row=2, column=2, padx=7, sticky=tk.NSEW)

        self.zoomInImg = tk.PhotoImage(file="./icon/zoom-in.png")
        self.zoomInLabel = tk.Label(self.frm_control, text='放大图片', font=('Times', 9))
        self.zoomIn_image = tk.Button(self.frm_control, state=tk.DISABLED, command=cbs.zoom_in_image, image=self.zoomInImg,relief=tk.FLAT)
        self.zoomIn_image.grid(row=1, column=3, padx=7, sticky=tk.NSEW)
        self.zoomInLabel.grid(row=2, column=3, padx=7, sticky=tk.NSEW)

        self.zoomOutImg = tk.PhotoImage(file="./icon/zoom-out.png")
        self.zoomOutLabel = tk.Label(self.frm_control, text='缩小图片', font=('Times', 9))
        self.zoomOut_image = tk.Button(self.frm_control, state=tk.DISABLED, command=cbs.zoom_out_image, image=self.zoomOutImg,relief=tk.FLAT)
        self.zoomOut_image.grid(row=1, column=4, padx=7, sticky=tk.NSEW)
        self.zoomOutLabel.grid(row=2, column=4, padx=7, sticky=tk.NSEW)

        self.revokeImg = tk.PhotoImage(file="./icon/undo.png")
        self.revokeLabel = tk.Label(self.frm_control, text='撤销标注',font=('Times',9))
        self.revoke = tk.Button(self.frm_control,state=tk.DISABLED,command=cbs.remove_canvas_lable_all,image=self.revokeImg,relief=tk.FLAT)
        self.revoke.grid(row=1, column=5, padx=7,sticky=tk.NSEW)
        self.revokeLabel.grid(row=2, column=5, padx=7, sticky=tk.NSEW)

        self.rectImg = tk.PhotoImage(file="./icon/objects.png")
        self.rectLabel = tk.Label(self.frm_control, text='创建矩形',font=('Times',9))
        self.label_rect = tk.Button(self.frm_control,state=tk.DISABLED,command=cbs.create_label_rect,image=self.rectImg,relief=tk.FLAT)
        self.label_rect.grid(row=1, column=6, padx=7,sticky=tk.NSEW)
        self.rectLabel.grid(row=2, column=6, padx=7, sticky=tk.NSEW)

        self.scatImg = tk.PhotoImage(file="./icon/labels.png")
        self.scatLabel = tk.Label(self.frm_control, text='创建散点',font=('Times',9))
        self.label_scat = tk.Button(self.frm_control,state=tk.DISABLED,command=cbs.create_label_scat,image=self.scatImg,relief=tk.FLAT)
        self.label_scat.grid(row=1, column=7, padx=7,sticky=tk.NSEW)
        self.scatLabel.grid(row=2, column=7, padx=7, sticky=tk.NSEW)

        self.saveImg = tk.PhotoImage(file="./icon/save.png")
        self.saveLabel = tk.Label(self.frm_control, text='保存标注',font=('Times',9))
        self.save_lable = tk.Button(self.frm_control, state=tk.DISABLED,command=cbs.save_lable_file,image=self.saveImg,relief=tk.FLAT)
        self.save_lable.grid(row=1, column=8, padx=7,sticky=tk.NSEW)
        self.saveLabel.grid(row=2, column=8, padx=7, sticky=tk.NSEW)

        self.showlabelImg = tk.PhotoImage(file="./icon/eye.png")
        self.showLabel = tk.Label(self.frm_control, text='查看标注', font=('Times', 9))
        self.show_lable = tk.Button(self.frm_control, state=tk.DISABLED, command=cbs.show_label,image=self.showlabelImg, relief=tk.FLAT)
        self.show_lable.grid(row=1, column=9, padx=7, sticky=tk.NSEW)
        self.showLabel.grid(row=2, column=9, padx=7, sticky=tk.NSEW)
    # 创建图像树


class LabelGUI(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('选择标注类别')
        self.setup_UI(self)

    def setup_UI(self):

       row1=tk.Frame(self)
       row1


