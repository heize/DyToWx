import tkinter as tk
from tkinter import ttk
import requests
from io import BytesIO
from PIL import Image, ImageTk
from DownDouyin_Request import *
from DownDouyin_UploadMpClient import *
import tkinter.messagebox
import threading
from moviepy.editor import *
from datetime import datetime
import random

class DownDouyin_GUI:
    def __init__(self):
        self.shotcount = 1
        self.covery1 = 0
        self.covery2 = 0

        self.root = tk.Tk()
        self.root.title("抖音上传公众号")
        self.root.resizable(0,0)
        self.request = DownDouyin_Request()
        self.chrome = DownDouyin_UploadMpClient()
        if self.request.load_config():
            self.request.load_gh()
            self.show_main()
        else:
            self.show_login()
        self.root.mainloop()
    
    def write(self, text):
        self.txtLog.insert(tk.END, text)
        self.txtLog.see(tk.END)  # 滚动到文本末尾

    def show_login(self):
        self.frame1 = tk.Frame(self.root)
        L1 = tk.Label(self.frame1, text="用户名：")
        L1.grid(row=0,column=0,sticky=tk.W,padx=5)
        self.txtUn = tk.Entry(self.frame1, bd =1)
        self.txtUn.grid(row=0,column=1,sticky=tk.E,padx=5,pady=5)
        L2 = tk.Label(self.frame1, text="密码：")
        L2.grid(row=1,column=0,sticky=tk.W,padx=5)
        self.txtPw = tk.Entry(self.frame1, bd =1, show="*")
        self.txtPw.grid(row=1,column=1,sticky=tk.E,padx=5,pady=5)
        b = tk.Button(self.frame1, text="登录",command=self.show_login_submit,width=20,border=1)
        b.grid(row=3,column=0,columnspan=3,pady=15)
        self.frame1.pack()

    def show_login_submit(self):
        if self.txtUn.get().strip() == "":
            tkinter.messagebox.showwarning ("提示","请输入用户名")
            return
        if self.txtPw.get().strip() == "":
            tkinter.messagebox.showwarning ("提示","请输入密码")
            return
        
        loginResult = self.request.login(self.txtUn.get().strip(), self.txtPw.get().strip())
        if not loginResult:
            tkinter.messagebox.showwarning ("提示","用户名或者密码不正确")
            return
        self.request.load_gh()

        self.frame1.pack_forget()
        self.show_main()

    def show_main(self):
        frame_left = tk.Frame(self.root)

        # 0
        self.lLogo = tk.Label(frame_left)
        self.lLogo.grid(row=0, column=0,sticky=tk.W , padx=5)
        self.lName = tk.Label(frame_left, text="点击右边登录按钮,获取公众号登录二维码")
        self.lName.grid(row=0, column=1,sticky=tk.W , padx=5, pady=5)
        self.btnLoginGh = tk.Button(frame_left, text="登录公众号",command=self.show_main_logingh,border=1)
        self.btnLoginGh.grid(row=0,column=1,sticky=tk.E)

        # 1
        tk.Label(frame_left, text="抖音分享文字").grid(row=1, column=0, sticky=tk.W ,padx=5)
        self.txtShareText=tk.Text(frame_left, height=5, width=60)
        self.txtShareText.grid(row=1, column=1, sticky=tk.W ,padx=5, pady=5)

        # 2
        tk.Button(frame_left, text="抓取",command=self.show_main_dyurl,width=60).grid(row=2,column=1)

        # 3
        tk.Label(frame_left, text="抓取标题").grid(row=3, column=0, sticky=tk.W ,padx=5)
        self.txtDytitle = tk.Text(frame_left, height=5, width=60)
        self.txtDytitle.grid(row=3, column=1, sticky=tk.W ,padx=5, pady=5)

        # 4
        tk.Label(frame_left, text="水印").grid(row=4, column=0, sticky=tk.W ,padx=5)
        self.txtWater = tk.Entry(frame_left, width=60)
        self.txtWater.grid(row=4, column=1, sticky=tk.W ,padx=5, pady=5)
        # 5
        tk.Label(frame_left, text="快捷选择水印").grid(row=5, column=0, sticky=tk.W,padx=5)
        
        self.selected_value = tk.StringVar(value="f")
        # 创建一个frame作为容器
        radio_frame = tk.Frame(frame_left)
        radio_frame.grid(row=5, column=1,sticky="w")

        for radioitem in self.request.ghlist:
            radio_button = tk.Radiobutton(radio_frame,text = radioitem["name"], variable = self.selected_value,value = radioitem["name"],command=self.show_main_select)
            radio_button.pack(side=tk.LEFT, padx=2)

        # 6
        tk.Label(frame_left, text="提交标题").grid(row=6, column=0, sticky=tk.W ,padx=5)
        self.txtTitle = tk.Entry(frame_left, width=60)
        self.txtTitle.grid(row=6, column=1, sticky=tk.W ,padx=5, pady=5)

        # 7
        self.btnSubmit = tk.Button(frame_left, text="提交", width=30, border=1)
        self.btnSubmit.grid(row=7,column=1,pady=20)
        self.btnSubmit.bind('<ButtonPress-1>', self.show_main_uploadtogh)

        # 8
        self.btnScreenShot = tk.Button(frame_left, text="测试", width=30, border=1, command=self.test)
        self.btnScreenShot.grid(row=8,column=1,pady=20)

        frame_left.pack(side=tk.LEFT)

        self.rightFrame = tk.LabelFrame(self.root, text="操作区")
        self.canvas = tk.Canvas(self.rightFrame,bg='#CDC9A5',height=200,width=400)
        self.canvas.pack()

        #print to text
        # self.txtLog = tk.Text(self.rightFrame, wrap="word", height=2, background="black", fg="green", border=1)
        # self.txtLog.pack()
        # sys.stdout = self
        self.rightFrame.pack(side=tk.RIGHT, padx=10)

    def need_relogin(self):
        needRelogin = not self.chrome.IsChromeOnline()
        print(needRelogin)
        if needRelogin:
            self.chrome = DownDouyin_UploadMpClient()
            self.btnLoginGh.config(text = "退出登录这个账号")
            self.btnSubmit.config(text = "提交")
            self.show_main_logingh()
            tkinter.messagebox.showwarning("提示","须重新登陆")

        return needRelogin

    def show_main_select(self):
        self.txtWater.delete(0, tk.END)
        self.txtWater.insert(0, "公众号:" + self.selected_value.get())

    def show_main_logingh(self):
        if self.btnSubmit.cget("text") != "提交":
            return
        if self.btnLoginGh.cget("text") != "请扫面右边" and self.need_relogin():
            return

        if self.btnLoginGh.cget("text") == "登录公众号":
            image = self.chrome.Login()
            if image != None:
                image = image.resize((200, 200), Image.LANCZOS)

                tk_image = ImageTk.PhotoImage(image)
                self.canvas.create_image(0,0,image = tk_image, anchor=tk.NW, tags="logincode")
                self.canvas.image = tk_image
                self.btnLoginGh.config(text = "请扫面右边")
                self.rightFrame.config(text="请扫描下方二维码")
                thread = threading.Thread(target=self.show_main_logingh_wait_login)
                thread.start()
        elif self.btnLoginGh.cget("text") == "退出登录这个账号":
            self.chrome.Logout()
            self.btnLoginGh.config(text="登录公众号")
            self.lLogo.image = None
            self.lLogo.config(image=None)
            self.lName.config(text="点击右边登录按钮,获取公众号登录二维码")
            self.show_main_dyurl_initui()
    
    def show_main_logingh_wait_login(self):
        i = 40
        while i>0:
            logoandname = self.chrome.GetLogoAndName()

            if logoandname == None:
                print('没有扫描')
            else:
                self.root.after(0, self.show_main_logingh_wait_login_done, logoandname)
                return
            self.chrome.QgSleep(3,'等待扫描')
            i=i-1
        
        #没扫描
        self.btnLoginGh.config(text="退出登录这个账号")
        self.show_main_logingh()
        tkinter.messagebox.showwarning ("提示","未扫描登陆，请重新点击登录")
        

    def show_main_logingh_wait_login_done(self, logoandname):
        try:
            response = requests.get(logoandname[0])
            image_data = BytesIO(response.content)
            image = Image.open(image_data)
            target_width = 30
            h_size = int(float(image.height) * float(target_width / float(image.width)))

            image = image.resize((target_width, h_size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            self.lLogo.config(image=photo)
            self.lLogo.image = photo
            self.lName.config(text=logoandname[1])
            self.canvas.delete("logincode")

            self.btnLoginGh.config(text="退出登录这个账号")
        except Exception as e:
            print(f"发生错误：{e}")

    def show_main_dyurl(self):
        self.dysharetext = self.txtShareText.get("1.0", "end-1c").strip()
        if not self.dysharetext or self.btnSubmit.cget("text") != "提交":
            return
        
        if self.lName.cget("text").startswith("点击右边"):
            tkinter.messagebox.showwarning ("提示","请先登录公众号")
            return
        
        if self.need_relogin():
            return
        
        result = self.request.ana_dy(self.dysharetext)
        print(result)
        if result == None or result == "a" or result =="":
            tkinter.messagebox.showwarning ("提示","输入不正确或者获取失败")
            return
        if result["code"]!=200:
            tkinter.messagebox.showwarning ("提示","输入不正确或者获取失败")
            return
        self.txtDytitle.delete("1.0", "end")  # 清空现有内容
        self.txtDytitle.insert("1.0", result["data"]["title"].replace(" ","\n").replace("#","\n").replace("\n\n","\n"))

        self.videourl = result["data"]["url"]

        response = requests.get(result["data"]["cover"])
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        self.width = 400
        self.height = 400
        if self.width > self.height:
            self.height = int(image.height * (self.width / image.width))
        else:
            self.width = int(image.width * (self.height / image.height))

        image = image.resize((self.width, self.height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo, tags="logincode")
        self.canvas.image = photo
        self.canvas.bind('<ButtonPress-1>',self.show_main_dyurl_line)
        self.canvas.config(width=self.width, height=self.height)
        self.rightFrame.config(text="分别点击2次，设置上下边界，来裁剪视频")

    def show_main_dyurl_initui(self):
        #init ui
        self.txtDytitle.delete("1.0", "end")
        self.txtShareText.delete("1.0", "end")
        self.txtTitle.delete(0,"end")
        self.canvas.delete("logincode")
        self.canvas.delete("coverline")
        self.canvas.image = None


    def show_main_dyurl_line(self, event):
        if self.canvas.image == None:
            return
        
        if self.covery1 != 0 and self.covery2 != 0:
            self.canvas.delete("coverline")
            self.covery1 = 0
            self.covery2 = 0

        self.canvas.create_line(0,event.y,self.width,event.y,fill="red",width=2,tags="coverline")
        if self.covery1==0:
            self.covery1 = event.y / self.height
        else:
            self.covery2 = event.y / self.height

    def show_main_uploadtogh(self,event):
        thread = threading.Thread(target=self.show_main_uploadtogh_editvideo)
        thread.start()

    def show_main_uploadtogh_editvideo(self):
        self.btnSubmit.unbind("<ButtonPress-1>")
        if self.lName.cget("text").startswith("点击右边"):
            self.btnSubmit.bind('<ButtonPress-1>', self.show_main_uploadtogh)
            tkinter.messagebox.showwarning ("提示","请先登录公众号")
            return
        if not self.videourl:
            self.btnSubmit.bind('<ButtonPress-1>', self.show_main_uploadtogh)
            tkinter.messagebox.showwarning ("提示","请输入抖音分享文字，然后点击抓取按钮")
            return
        if not self.txtTitle.get().strip():
            self.btnSubmit.bind('<ButtonPress-1>', self.show_main_uploadtogh)
            tkinter.messagebox.showwarning ("提示","请填写提交标题")
            return
        if self.need_relogin():
            self.btnSubmit.bind('<ButtonPress-1>', self.show_main_uploadtogh)
            return

        #下载文件.................
        #组成时间字符串，用于创建目录和文件
        todayDir = datetime.now().strftime('%Y%m%d')
        filedatestr = f"{todayDir}_{datetime.now().strftime('%H%M%S')}_{random.randint(100,999)}"
        douyinfilename = rf"{todayDir}\{filedatestr}.mp4"
        finalFileName = rf"{todayDir}\{filedatestr}_2.mp4"
    
        #创建目录,下载视频文件
        if not os.path.exists(rf"{todayDir}"):
            os.mkdir(rf"{todayDir}")

        self.root.after(0,self.show_main_uploadtogh_editvideo_updatestatus,"正在下载...")
        down_res = requests.get(url=self.videourl)
        with open(douyinfilename,"wb") as code:
            code.write(down_res.content)

        self.root.after(0,self.show_main_uploadtogh_editvideo_updatestatus,"正在裁剪...")
        #moviepy加载视频
        clip = VideoFileClip(douyinfilename)
        #是否裁剪
        if self.covery1 != 0 and self.covery2 != 0:
            if self.covery1 > self.covery2:
                _y = self.covery1
                self.covery1 = self.covery2
                self.covery2 = _y

            print('裁剪中',self.covery1, self.covery2)
            clip = clip.crop(x1=0, y1=int(clip.size[1]*self.covery1), x2=clip.size[0], y2=int(clip.size[1]*self.covery2))#.resize(width=100).subclip(10,30)
        #加入水印
        #C:\Users\HeizePC\AppData\Local\Programs\Python\Python311\Lib\site-packages\moviepy\config_defaults.py
        #最下面加一句，不是修改
        #还需要拷贝字体
        self.root.after(0,self.show_main_uploadtogh_editvideo_updatestatus,"正在处理视频...")
        if self.txtWater.get().strip() != "":
            print('添加水印')
            font_width=(clip.w*0.3)
            font_height = 100
            caption = TextClip(self.txtWater.get(),color='#EFAF33',font='msyh.ttc', size=(font_width,font_height)).set_position((0.2, 0.2)).set_duration(clip.duration)
            video = CompositeVideoClip([clip, caption.set_start(2)])
            video.write_videofile(finalFileName)
        else:
            clip.write_videofile(finalFileName)

        self.root.after(0,self.show_main_uploadtogh_editvideo_updatestatus,"正在上传...")
        
        fullFilePathName = os.getcwd()+"\\"+finalFileName
        self.chrome.UploadToMp(fullFilePathName,f"{filedatestr}_2",self.txtTitle.get().strip(),self.request)

        self.root.after(0,self.show_main_uploadtogh_editvideo_updatestatus,"提交")
        tkinter.messagebox.showinfo("提示","本任务完成")

        self.show_main_dyurl_initui()
        self.btnSubmit.bind('<ButtonPress-1>', self.show_main_uploadtogh)

    def show_main_uploadtogh_editvideo_updatestatus(self, btnText):
        self.btnSubmit.config(text=btnText)

    def test(self):
        self.chrome.driver.save_screenshot(rf"d:\error{self.shotcount}.png")
        self.shotcount = self.shotcount + 1

app = DownDouyin_GUI()