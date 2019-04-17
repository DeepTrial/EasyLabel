import tkinter as tk
'''松耦合'''
# 弹窗
class MyDialog(tk.Toplevel):
  def __init__(self):
    super().__init__()
    self.title('设置用户信息')
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


    tk.Label(self.frame, text='输入类标信息：').grid(row=0,column=0,sticky=tk.NW)
    self.labelName = tk.StringVar()
    self.labelEntry=tk.Entry(self.frame, textvariable=self.labelName)
    self.labelEntry.grid(row=1,column=0,columnspan=2,sticky=tk.NSEW,padx=10)


    tk.Label(self.frame, text='已有类标：').grid(row=2,column=0,sticky=tk.NW)
    list1 = tk.StringVar(value=self.labels)
    self.listbox1 = tk.Listbox(self.frame,height=7,listvariable=list1,selectmode="browse")
    self.listbox1.grid(row=3,column=0,columnspan=2,sticky=tk.NSEW,padx=10)

    yscrollbar = tk.Scrollbar(self.frame,orient=tk.VERTICAL)
    yscrollbar.grid(row=3, column=2, sticky="nsew")
    yscrollbar.config(command=self.listbox1.yview)
    self.listbox1.config(yscrollcommand=yscrollbar.set)
    #yscrollbar.config(command)

    self.listbox1.bind("<<ListboxSelect>>",self.show_msg)

    tk.Button(self.frame, text="取消", command=self.cancel).grid(row=4,column=0,sticky=tk.NSEW,padx=10, pady=10,)
    tk.Button(self.frame, text="确定", command=self.ok,width=16).grid(row=4,column=1,sticky=tk.NSEW,padx=10, pady=10)

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


# 主窗
class MyApp(tk.Tk):
  def __init__(self):
    super().__init__()
    #self.pack() # 若继承 tk.Frame ，此句必须有！
    self.title('用户信息')
    # 程序参数/数据
    self.name = '张三'
    self.age = 30
    # 程序界面
    self.setupUI()
  def setupUI(self):
    # 第一行（两列）
    row1 = tk.Frame(self)
    row1.pack(fill="x")
    tk.Label(row1, text='姓名：', width=8).pack(side=tk.LEFT)
    self.l1 = tk.Label(row1, text=self.name, width=20)
    self.l1.pack(side=tk.LEFT)
    # 第二行
    row2 = tk.Frame(self)
    row2.pack(fill="x")
    tk.Label(row2, text='年龄：', width=8).pack(side=tk.LEFT)
    self.l2 = tk.Label(row2, text=self.age, width=20)
    self.l2.pack(side=tk.LEFT)
    # 第三行
    row3 = tk.Frame(self)
    row3.pack(fill="x")
    tk.Button(row3, text="设置", command=self.setup_config).pack(side=tk.RIGHT)
  # 设置参数
  def setup_config(self):
    # 接收弹窗的数据
    res = self.ask_userinfo()
    #print(res)
    if res is None: return
    # 更改参数
    self.name, self.age = res
    # 更新界面
    self.l1.config(text=self.name)
    self.l2.config(text=self.age)
  # 弹窗
  def ask_userinfo(self):
    inputDialog = MyDialog()
    self.wait_window(inputDialog) # 这一句很重要！！！
    return inputDialog.userinfo

if __name__ == '__main__':
  app = MyApp()
  app.mainloop()