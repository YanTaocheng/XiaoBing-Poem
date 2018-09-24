# _*_ coding:utf-8 _*_
__anthor__ = "yan"

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import messagebox
from lxml import etree
import requests, re
import time


class XiaoBing():
    def __init__(self):
        #self.LogName = LogName #log文件名
        self.login_url = 'https://bingapppoem.azurewebsites.net/User/Login?ReturnUrl=%2fPendingPoemReview%2fLineReview%3fpage%3d40522&page=40522'
        self.page_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/LineReview?page='
        self.SetLineEdited_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/SetLineEdited'  # id,page,afterModified
        self.SetLineBad_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/SetLineBad'  # id,page
        self.SetLineRisk_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/SetLineRisky'  # id,page,Reason
        self.SetLinePos_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/SetLinePos'  # id,page
        self.SetLineNeg_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/SetLineNeg'  # id,page
        self.SetLineNeu_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/SetLineNeu'  # id,page
        self.SetLineBeginning_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/SetLineBeginning'  # id,page, flag:False
        self.SetLineEnding_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/SetLineEnding'  # id,page, flag:False,True
        self.SetLineReviewed_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/SetLineReviewed/-1'  # page
        self.requests = requests.session()

    def login(self):
        # 返回值 1：登录成功， 返回值 -1：账号密码错误， 返回值 -2：其他错误
        user_info = {
            'UserName': 'linereview',
            'Password': 'aic@2017',
            'RememberMe': 'false'
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400"
        }
        try:
            html = self.requests.post(self.login_url, data=user_info, headers=headers)
            result = re.search(r'<li>Login data is incorrect!</li>', html.text, re.S)
            if result:
                #log = open(self.LogName, 'a')
                #log.write('XiaoBing.login:'+'登录失败\n')
                #log.close()
                return -1
            else:
                #log = open(self.LogName, 'a')
                #log.write('XiaoBing.login:'+'登录成功\n')
                #log.close()
                return 1
        except Exception as e:
            #log = open('XiaoBing.login:'+self.LogName+'\n', 'a')
            #log.write(e)
            #log.close()
            return -2

    def get_info(self, page):
        # 返回值 1：reviewed， 返回值 -1：unreviewed，
        url = self.page_url + str(page)
        html = self.requests.get(url)
        #print(html.text)
        content = etree.HTML(html.text)
        id = content.xpath('//tr/td/text()')
        # info = re.findall(r"<td>.*?([0-9]{6,8}).*?</td>.*?<td>\n\r.*?(\s).*?</td>", html.text, re.S)
        #print(len(id))
        #print(id)

        reason = re.findall(r'<input id="Reason" name="Reason" style="width:240px;margin:2px" type="text" value="(.*?)" /', html.text, re.S)
        afterModified = re.findall(r' <input id="afterModified" name="afterModified" style="width:240px;margin:2px" type="text" value="(.*?)" /', html.text, re.S)
        #print(reason, afterModified)

        info = []
        for i in range(5):
            info.append(id[24*i][18:-14])
            info.append(id[1+24*i][18:-14])
            info.append(id[12+24*i][18:-14])
        #print(info)
        try:
            return_value =[]
            ReviewOrNot = 1
            for i in range(5):
                j = i*3
                if info[j + 2] == "":
                    ReviewOrNot = -1
                return_value.append((info[j], info[j + 1], info[j + 2], reason[i], afterModified[i]))
            #print(return_value)
            return [ReviewOrNot, return_value]
        except Exception as e:
            #log = open(self.LogName,'a')
            #log.write('XiaoBing.get_info'+str(e)+'\n')
            #log.close()
            pass

    def SetLineEdited(self, id, page, afterModified):
        data = {
            'id': str(id),
            'page': str(page),
            'afterModified': str(afterModified)
        }

        html = self.requests.get(self.SetLineEdited_url, data=data)

    def SetLineBad(self, id, page):
        data = {
            'id': str(id),
            'page': str(page)
        }
        html = self.requests.get(self.SetLineBad_url, data=data)

    def SetLineRisk(self, id, page, Reason):
        data = {
            'id': str(id),
            'page': str(page),
            'Reason': str(Reason)
        }
        html = self.requests.get(self.SetLineRisk_url, data=data)

    def SetLinePos(self, id, page):
        data = {
            'id': str(id),
            'page': str(page)
        }
        html = self.requests.get(self.SetLinePos_url, data=data)

    def SetLineNeg(self, id, page):
        data = {
            'id': str(id),
            'page': str(page)
        }
        html = self.requests.get(self.SetLineNeg_url, data=data)

    def SetLineNeu(self, id, page):
        data = {
            'id': str(id),
            'page': str(page)
        }
        html = self.requests.get(self.SetLineNeu_url, data=data)

    def SetLineBeginning(self, id, page, flag):
        data = {
            'id': str(id),
            'page': str(page),
            'flag': str(flag)
        }
        html = self.requests.get(self.SetLineBeginning_url, data=data)

    def SetLineEnding(self, id, page, flag):
        data = {
            'id': str(id),
            'page': str(page),
            'flag': str(flag)
        }
        html = self.requests.get(self.SetLineEnding_url, data=data)

    def SetLineReviewed(self, page):
        data = {
            'page': str(page)
        }
        html = self.requests.get(self.SetLineReviewed_url, data=data)

class MainPage(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('XiaoBing Poem 1.1')
        ws = self.root.winfo_screenwidth() #获取桌面长度
        hs = self.root.winfo_screenheight() #获取桌面高度
        self.root.geometry('950x600+%d+%d'%(ws/2-450,hs/2-300))  # 设置窗口大小    是x 不是*
        self.xiaobing = XiaoBing()
        self.xiaobing.login()
        self.main_page()

    def main_page(self):
        self.root.resizable(0,0)

        # Tab Control introduced here --------------------------------------
        tabControl = ttk.Notebook(self.root)          # Create Tab Control

        self.tab1 = ttk.Frame(tabControl)            # Create a tab
        tabControl.add(self.tab1, text='Poem Review')      # Add the tab

        self.tab2 = ttk.Frame(tabControl)            # Add a second tab
        tabControl.add(self.tab2, text='Lyric Review')      # Make second tab visible

        tabControl.pack(expand=1, fill="both")  # Pack to make visible
        # ~ Tab Control introduced here -----------------------------------------

        #--------------------------tab1 Poem Review -------------------------------
        self.tab1_page = StringVar()
        self.page_skip(self.tab1, self.tab1_page)
        #self.content_page(self.tab1, self.tab1_page)
        #---------------------------------~tab1 Poem Review ---------------------------------------------------

        #--------------------------tab2 Poem Review -------------------------------
        #self.tab2_page = StringVar
        #self.page_skip(self.tab2, self.tab2_page)
        #self.content_page(self.tab2, self.tab2_page)
        #---------------------------------~tab2 Poem Review ---------------------------------------------------



        # Time display
        Label1 = Label(self.root, text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        Label1.pack(side=BOTTOM, fill=X)
        def trickit():
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            Label1.config(text=currentTime)
            self.root.update()
            Label1.after(1000, trickit)

        Label1.after(1000, trickit)

    def page_skip(self, tab, page):
        #We are creating a container in tab to hold Page Skip widgets
        page_skip = ttk.LabelFrame(tab)
        #page_skip.pack(side=BOTTOM, fill="y")
        page_skip.grid(column=0, row=0, padx=10, pady=1, sticky='W')

        #Page label
        ttk.Label(page_skip, text="Page:").grid(column=0, row=0, sticky='W')

        #Page enter
        try:
            file = open('page.txt','r')
            current_page = file.readline()
            page.set(current_page)
            file.close()
        except:
            pass
        self.page_enter = ttk.Entry(page_skip, width=8, textvariable=page)
        self.page_enter.grid(column=1, row=0, sticky='W')

        #Skip button
        ttk.Button(page_skip, width=8, text='Skip', command=self.skip_button).grid(column=2, row=0, padx=10, sticky='W')
        #Last Page button
        ttk.Button(page_skip, width=8, text='Last', command=self.last_button).grid(column=3, row=0, sticky='W')
        #Next Page button
        ttk.Button(page_skip, width=8, text='Next', command=self.next_button).grid(column=4, row=0, sticky='W')
        #Original Page button
        ttk.Button(page_skip, width=12, text='Original Page', command=self.web_button).grid(column=5, row=0, padx=10, sticky='W')
        #Review Button
        ttk.Button(page_skip, width=8, text='Review', command=self.review_button).grid(column=6, row=0, padx=20, sticky='W')

    def content_page(self, tab, info):
        #info的格式[reviewOrNot,[(id1,content1,status1,risky_reason1,afterModified1),(id2,content2,status2,risky_reason2,afterModified2)]]
        content_page = ttk.LabelFrame(tab)
        content_page.grid(column=0, row=1, padx=10, pady=1, sticky='W')
        style = ttk.Style()
        style.configure('BW.TLabel', foreground="blue")

        #-------------------Poem 1-----------------------------------
        #number
        number1 = ttk.Label(content_page, text=info[1][0][0], relief=SUNKEN, anchor=CENTER, width=8).grid(column=0, row=0)
        #Poem content
        self.poem_content1 = StringVar()
        self.poem_content1.set(info[1][0][1])
        poem_content1 = ttk.Entry(content_page, width=40, text=self.poem_content1)
        poem_content1.grid(column=1, row=0, padx=20, columnspan=4, sticky='W')
        poem_content1.config(state='readonly')
        #Delete,Edit,Fail buttom
        ttk.Button(content_page, width=5, text='错', command=lambda: self.copy_content('错', self.poem_content1.get(), self.poem_edit1)).grid(column=2, row=1, sticky='W')
        ttk.Button(content_page, width=5, text='改', command=lambda: self.copy_content('改', self.poem_content1.get(), self.poem_edit1)).grid(column=3, row=1, sticky='W')
        ttk.Button(content_page, width=5, text='删', command=lambda: self.copy_content('删', self.poem_content1.get(), self.poem_edit1)).grid(column=4, row=1, sticky='W')
        #Risky,Edit,Bad  button
        ttk.Button(content_page, width=5, text='Risky', command=lambda: self.risk_button(info[1][0][0], self.page_enter.get(), self.poem_risky1.get())).grid(column=5, row=0, sticky='W')
        ttk.Button(content_page, width=5, text='Edit', command=lambda: self.edited_button(info[1][0][0], self.page_enter.get(), self.poem_edit1.get())).grid(column=5, row=1, sticky='W')
        ttk.Button(content_page, width=5, text='Bad', command=lambda: self.bad_button(info[1][0][0], self.page_enter.get())).grid(column=5, row=2, sticky='W')
        #Poem risky text
        self.poem_risky1 = StringVar()
        self.poem_risky1.set(info[1][0][3])
        poem_risky1 = ttk.Entry(content_page, width=40, text=self.poem_risky1)
        poem_risky1.grid(column=6, row=0, padx=20, columnspan=4, sticky='W')
        #Poem edit text
        self.poem_edit1 = StringVar()
        self.poem_edit1.set(info[1][0][4])
        poem_edit1 = ttk.Entry(content_page, width=40, text=self.poem_edit1)
        poem_edit1.grid(column=6, row=1, padx=20, columnspan=4, sticky='W')
        #Beginning, Ending button
        ttk.Button(content_page, width=9, text='Beginning', command=lambda: self.beginning_button(info[1][0][0], self.page_enter.get(), 'False')).grid(column=10, row=0, sticky='W')
        ttk.Button(content_page, width=9, text='Ending', command=lambda: self.ending_button(info[1][0][0], self.page_enter.get(), 'False')).grid(column=10, row=1, sticky='W')
        #Pos,Neg,Neu buttom
        ttk.Button(content_page, width=8, text='Pos(1)', command=lambda: self.pos_button(info[1][0][0], self.page_enter.get())).grid(column=7, row=2, sticky='W')
        ttk.Button(content_page, width=8, text='Neg(-1)', command=lambda: self.neg_button(info[1][0][0], self.page_enter.get())).grid(column=8, row=2, sticky='W')
        ttk.Button(content_page, width=8, text='Neu(0)', command=lambda: self.neu_button(info[1][0][0], self.page_enter.get())).grid(column=9, row=2, sticky='W')
        #status display
        ttk.Label(content_page, text=info[1][0][2], relief=SUNKEN, anchor=CENTER, width=8, style='BW.TLabel').grid(column=11, row=0, padx=5)

        #-------------------Poem 2-----------------------------------
        #number
        number2 = ttk.Label(content_page, text=info[1][1][0], relief=SUNKEN, anchor=CENTER, width=8).grid(column=0, row=3, pady=10)
        #Poem content
        self.poem_content2 = StringVar()
        self.poem_content2.set(info[1][1][1])
        poem_content2 = ttk.Entry(content_page, width=40, text=self.poem_content2)
        poem_content2.grid(column=1, row=3, padx=20, columnspan=4, sticky='W')
        poem_content2.config(state='readonly')
        #Delete,Edit,Fail buttom
        ttk.Button(content_page, width=5, text='错', command=lambda: self.copy_content('错', self.poem_content2.get(), self.poem_edit2)).grid(column=2, row=4, sticky='W')
        ttk.Button(content_page, width=5, text='改', command=lambda: self.copy_content('改', self.poem_content2.get(), self.poem_edit2)).grid(column=3, row=4, sticky='W')
        ttk.Button(content_page, width=5, text='删', command=lambda: self.copy_content('删', self.poem_content2.get(), self.poem_edit2)).grid(column=4, row=4, sticky='W')
        #Risky,Edit,Bad  button
        ttk.Button(content_page, width=5, text='Risky', command=lambda: self.risk_button(info[1][1][0], self.page_enter.get(), self.poem_risky2.get())).grid(column=5, row=3, sticky='W')
        ttk.Button(content_page, width=5, text='Edit', command=lambda: self.edited_button(info[1][1][0], self.page_enter.get(), self.poem_edit2.get())).grid(column=5, row=4, sticky='W')
        ttk.Button(content_page, width=5, text='Bad', command=lambda: self.bad_button(info[1][1][0], self.page_enter.get())).grid(column=5, row=5, sticky='W')
        #Poem risky text
        self.poem_risky2 = StringVar()
        self.poem_risky2.set(info[1][1][3])
        poem_risky2 = ttk.Entry(content_page, width=40, text=self.poem_risky2)
        poem_risky2.grid(column=6, row=3, padx=20, columnspan=4, sticky='W')
        #Poem edit text
        self.poem_edit2 = StringVar()
        self.poem_edit2.set(info[1][1][4])
        poem_edit2 = ttk.Entry(content_page, width=40, text=self.poem_edit2)
        poem_edit2.grid(column=6, row=4, padx=20, columnspan=4, sticky='W')
        #Beginning, Ending button
        ttk.Button(content_page, width=9, text='Beginning', command=lambda: self.beginning_button(info[1][1][0], self.page_enter.get(), 'False')).grid(column=10, row=3, sticky='W')
        ttk.Button(content_page, width=9, text='Ending', command=lambda: self.ending_button(info[1][1][0], self.page_enter.get(), 'False')).grid(column=10, row=4, sticky='W')
        #Pos,Neg,Neu buttom
        ttk.Button(content_page, width=8, text='Pos(1)', command=lambda: self.pos_button(info[1][1][0], self.page_enter.get())).grid(column=7, row=5, sticky='W')
        ttk.Button(content_page, width=8, text='Neg(-1)', command=lambda: self.neg_button(info[1][1][0], self.page_enter.get())).grid(column=8, row=5, sticky='W')
        ttk.Button(content_page, width=8, text='Neu(0)', command=lambda: self.neu_button(info[1][1][0], self.page_enter.get())).grid(column=9, row=5, sticky='W')
        #status display
        ttk.Label(content_page, text=info[1][1][2], relief=SUNKEN, anchor=CENTER, width=8, style='BW.TLabel').grid(column=11, row=3, padx=5)

        #-------------------Poem 3-----------------------------------
        #number
        number3 = ttk.Label(content_page, text=info[1][2][0], relief=SUNKEN, anchor=CENTER, width=8).grid(column=0, row=6, pady=10)
        #Poem content
        self.poem_content3 = StringVar()
        self.poem_content3.set(info[1][2][1])
        poem_content3 = ttk.Entry(content_page, width=40, text=self.poem_content3)
        poem_content3.grid(column=1, row=6, padx=20, columnspan=4, sticky='W')
        poem_content3.config(state='readonly')
        #Delete,Edit,Fail buttom
        ttk.Button(content_page, width=5, text='错', command=lambda: self.copy_content('错', self.poem_content3.get(), self.poem_edit3)).grid(column=2, row=7, sticky='W')
        ttk.Button(content_page, width=5, text='改', command=lambda: self.copy_content('改', self.poem_content3.get(), self.poem_edit3)).grid(column=3, row=7, sticky='W')
        ttk.Button(content_page, width=5, text='删', command=lambda: self.copy_content('删', self.poem_content3.get(), self.poem_edit3)).grid(column=4, row=7, sticky='W')
        #Risky,Edit,Bad  button
        ttk.Button(content_page, width=5, text='Risky', command=lambda: self.risk_button(info[1][2][0], self.page_enter.get(), self.poem_risky3.get())).grid(column=5, row=6, sticky='W')
        ttk.Button(content_page, width=5, text='Edit', command=lambda: self.edited_button(info[1][2][0], self.page_enter.get(), self.poem_edit3.get())).grid(column=5, row=7, sticky='W')
        ttk.Button(content_page, width=5, text='Bad', command=lambda: self.bad_button(info[1][2][0], self.page_enter.get())).grid(column=5, row=8, sticky='W')
        #Poem risky text
        self.poem_risky3 = StringVar()
        self.poem_risky3.set(info[1][2][3])
        poem_risky3 = ttk.Entry(content_page, width=40, text=self.poem_risky3)
        poem_risky3.grid(column=6, row=6, padx=20, columnspan=4, sticky='W')
        #Poem edit text
        self.poem_edit3 = StringVar()
        self.poem_edit3.set(info[1][2][4])
        poem_edit3 = ttk.Entry(content_page, width=40, text=self.poem_edit3)
        poem_edit3.grid(column=6, row=7, padx=20, columnspan=4, sticky='W')
        #Beginning, Ending button
        ttk.Button(content_page, width=9, text='Beginning', command=lambda: self.beginning_button(info[1][2][0], self.page_enter.get(), 'False')).grid(column=10, row=6, sticky='W')
        ttk.Button(content_page, width=9, text='Ending', command=lambda: self.ending_button(info[1][2][0], self.page_enter.get(), 'False')).grid(column=10, row=7, sticky='W')
        #Pos,Neg,Neu buttom
        ttk.Button(content_page, width=8, text='Pos(1)', command=lambda: self.pos_button(info[1][2][0], self.page_enter.get())).grid(column=7, row=8, sticky='W')
        ttk.Button(content_page, width=8, text='Neg(-1)', command=lambda: self.neg_button(info[1][2][0], self.page_enter.get())).grid(column=8, row=8, sticky='W')
        ttk.Button(content_page, width=8, text='Neu(0)', command=lambda: self.neu_button(info[1][2][0], self.page_enter.get())).grid(column=9, row=8, sticky='W')
        #status display
        ttk.Label(content_page, text=info[1][2][2], relief=SUNKEN, anchor=CENTER, width=8, style='BW.TLabel').grid(column=11, row=6, padx=5)

        #-------------------Poem 4-----------------------------------
        #number
        number4 = ttk.Label(content_page, text=info[1][3][0], relief=SUNKEN, anchor=CENTER, width=8).grid(column=0, row=9, pady=10)
        #Poem content
        self.poem_content4 = StringVar()
        self.poem_content4.set(info[1][3][1])
        poem_content4 = ttk.Entry(content_page, width=40, text=self.poem_content4)
        poem_content4.grid(column=1, row=9, padx=20, columnspan=4, sticky='W')
        poem_content4.config(state='readonly')
        #Delete,Edit,Fail buttom
        ttk.Button(content_page, width=5, text='错', command=lambda: self.copy_content('错', self.poem_content4.get(), self.poem_edit4)).grid(column=2, row=10, sticky='W')
        ttk.Button(content_page, width=5, text='改', command=lambda: self.copy_content('改', self.poem_content4.get(), self.poem_edit4)).grid(column=3, row=10, sticky='W')
        ttk.Button(content_page, width=5, text='删', command=lambda: self.copy_content('删', self.poem_content4.get(), self.poem_edit4)).grid(column=4, row=10, sticky='W')
        #Risky,Edit,Bad  button
        ttk.Button(content_page, width=5, text='Risky', command=lambda: self.risk_button(info[1][3][0], self.page_enter.get(), self.poem_risky4.get())).grid(column=5, row=9, sticky='W')
        ttk.Button(content_page, width=5, text='Edit', command=lambda: self.edited_button(info[1][3][0], self.page_enter.get(), self.poem_edit4.get())).grid(column=5, row=10, sticky='W')
        ttk.Button(content_page, width=5, text='Bad', command=lambda: self.bad_button(info[1][3][0], self.page_enter.get())).grid(column=5, row=11, sticky='W')
        #Poem risky text
        self.poem_risky4 = StringVar()
        self.poem_risky4.set(info[1][3][3])
        poem_risky4 = ttk.Entry(content_page, width=40, text=self.poem_risky4)
        poem_risky4.grid(column=6, row=9, padx=20, columnspan=4, sticky='W')
        #Poem edit text
        self.poem_edit4 = StringVar()
        self.poem_edit4.set(info[1][3][4])
        poem_edit4 = ttk.Entry(content_page, width=40, text=self.poem_edit4)
        poem_edit4.grid(column=6, row=10, padx=20, columnspan=4, sticky='W')
        #Beginning, Ending button
        ttk.Button(content_page, width=9, text='Beginning', command=lambda: self.beginning_button(info[1][3][0], self.page_enter.get(), 'False')).grid(column=10, row=9, sticky='W')
        ttk.Button(content_page, width=9, text='Ending', command=lambda: self.ending_button(info[1][3][0], self.page_enter.get(), 'False')).grid(column=10, row=10, sticky='W')
        #Pos,Neg,Neu buttom
        ttk.Button(content_page, width=8, text='Pos(1)', command=lambda: self.pos_button(info[1][3][0], self.page_enter.get())).grid(column=7, row=11, sticky='W')
        ttk.Button(content_page, width=8, text='Neg(-1)', command=lambda: self.neg_button(info[1][3][0], self.page_enter.get())).grid(column=8, row=11, sticky='W')
        ttk.Button(content_page, width=8, text='Neu(0)', command=lambda: self.neu_button(info[1][3][0], self.page_enter.get())).grid(column=9, row=11, sticky='W')
        #status display
        ttk.Label(content_page, text=info[1][3][2], relief=SUNKEN, anchor=CENTER, width=8, style='BW.TLabel').grid(column=11, row=9, padx=5)

        #-------------------Poem 5-----------------------------------
        #number
        number5 = ttk.Label(content_page, text=info[1][4][0], relief=SUNKEN, anchor=CENTER, width=8).grid(column=0, row=12, pady=10)
        #Poem content
        self.poem_content5 = StringVar()
        self.poem_content5.set(info[1][4][1])
        poem_content5 = ttk.Entry(content_page, width=40, text=self.poem_content5)
        poem_content5.grid(column=1, row=12, padx=20, columnspan=4, sticky='W')
        poem_content5.config(state='readonly')
        #Delete,Edit,Fail buttom
        ttk.Button(content_page, width=5, text='错', command=lambda: self.copy_content('错', self.poem_content5.get(), self.poem_edit5)).grid(column=2, row=13, sticky='W')
        ttk.Button(content_page, width=5, text='改', command=lambda: self.copy_content('改', self.poem_content5.get(), self.poem_edit5)).grid(column=3, row=13, sticky='W')
        ttk.Button(content_page, width=5, text='删', command=lambda: self.copy_content('删', self.poem_content5.get(), self.poem_edit5)).grid(column=4, row=13, sticky='W')
        #Risky,Edit,Bad  button
        ttk.Button(content_page, width=5, text='Risky', command=lambda: self.risk_button(info[1][4][0], self.page_enter.get(), self.poem_risky5.get())).grid(column=5, row=12, sticky='W')
        ttk.Button(content_page, width=5, text='Edit', command=lambda: self.edited_button(info[1][4][0], self.page_enter.get(), self.poem_edit5.get())).grid(column=5, row=13, sticky='W')
        ttk.Button(content_page, width=5, text='Bad', command=lambda: self.bad_button(info[1][4][0], self.page_enter.get())).grid(column=5, row=14, sticky='W')
        #Poem risky text
        self.poem_risky5 = StringVar()
        self.poem_risky5.set(info[1][4][3])
        poem_risky5 = ttk.Entry(content_page, width=40, text=self.poem_risky5)
        poem_risky5.grid(column=6, row=12, padx=20, columnspan=4, sticky='W')
        #Poem edit text
        self.poem_edit5 = StringVar()
        self.poem_edit5.set(info[1][4][4])
        poem_edit5 = ttk.Entry(content_page, width=40, text=self.poem_edit5)
        poem_edit5.grid(column=6, row=13, padx=20, columnspan=4, sticky='W')
        #Beginning, Ending button
        ttk.Button(content_page, width=9, text='Beginning', command=lambda: self.beginning_button(info[1][4][0], self.page_enter.get(), 'False')).grid(column=10, row=12, sticky='W')
        ttk.Button(content_page, width=9, text='Ending', command=lambda: self.ending_button(info[1][4][0], self.page_enter.get(), 'False')).grid(column=10, row=13, sticky='W')
        #Pos,Neg,Neu buttom
        ttk.Button(content_page, width=8, text='Pos(1)', command=lambda: self.pos_button(info[1][4][0], self.page_enter.get())).grid(column=7, row=14, sticky='W')
        ttk.Button(content_page, width=8, text='Neg(-1)', command=lambda: self.neg_button(info[1][4][0], self.page_enter.get())).grid(column=8, row=14, sticky='W')
        ttk.Button(content_page, width=8, text='Neu(0)', command=lambda: self.neu_button(info[1][4][0], self.page_enter.get())).grid(column=9, row=14, sticky='W')
        #status display
        ttk.Label(content_page, text=info[1][4][2], relief=SUNKEN, anchor=CENTER, width=8, style='BW.TLabel').grid(column=11, row=12, padx=5)

    def status_display(self, tab, operation, judge):
        #judge = info[0]
        status_display = ttk.LabelFrame(tab)
        status_display.grid(column=0, row=0, padx=10, pady=1, sticky='E')

        Label(status_display, text=operation, relief=SUNKEN, anchor=CENTER, width=12, fg='blue').grid(column=1, row=0, padx=10)
        if judge == -1:
            judge = '未审核'
            Label(status_display, text=judge, relief=SUNKEN, anchor=CENTER, width=8, fg='white', bg='red').grid(column=0, row=0, padx=10)
        elif judge == 1:
            judge = '已审核'
            Label(status_display, text=judge, relief=SUNKEN, anchor=CENTER, width=8, fg='white', bg='green').grid(column=0, row=0, padx=10)

    def skip_button(self):
        current_page = int(self.page_enter.get())
        if current_page > 0:
            info = self.xiaobing.get_info(current_page)
            #print(info)
            self.content_page(self.tab1, info)
            self.status_display(self.tab1, 'Skip Page', info[0])
            file = open('page.txt','w')
            file.write(str(current_page))
            file.close()

    def last_button(self):
        current_page = int(self.page_enter.get())
        if current_page > 1:
            current_page = int(current_page) - 1
        self.tab1_page.set(str(current_page))
        info = self.xiaobing.get_info(current_page)
        self.content_page(self.tab1, info)
        self.status_display(self.tab1, 'Last Page', info[0])
        file = open('page.txt','w')
        file.write(str(current_page))
        file.close()

    def next_button(self):
        current_page = int(self.page_enter.get())
        current_page = int(current_page) + 1
        if current_page > 0:
            self.tab1_page.set(str(current_page))
            info = self.xiaobing.get_info(current_page)
            self.content_page(self.tab1, info)
            self.status_display(self.tab1, 'Next Page', info[0])
            file = open('page.txt','w')
            file.write(str(current_page))
            file.close()

    def web_button(self):
        import webbrowser
        page_url = 'https://bingapppoem.azurewebsites.net/PendingPoemReview/LineReview?page='
        current_page = int(self.page_enter.get())
        if current_page > 0:
            url = page_url+str(current_page)
            webbrowser.open(url,new=0,autoraise=True)
        info = self.xiaobing.get_info(current_page)
        self.status_display(self.tab1, 'Original Page', info[0])

    def review_button(self):
        current_page = self.page_enter.get()
        self.xiaobing.SetLineReviewed(current_page)
        info = self.xiaobing.get_info(current_page)
        #print(info)
        info[0] = 1
        self.status_display(self.tab1, 'Review', info[0])
        #self.content_page(info)

    def beginning_button(self, id, current_page, flag):
        self.xiaobing.SetLineBeginning(id, current_page, flag)
        self.status_display(self.tab1, id + '_Beginning', 0)

    def ending_button(self, id, current_page, flag):
        self.xiaobing.SetLineEnding(id, current_page, flag)
        self.status_display(self.tab1, id + '_Ending', 0)

    def copy_content(self, action, copy_text, paste_text):
        value1 = action + '/' + copy_text
        paste_text.set(value1)

    def edited_button(self, id, current_page, afterModified):
        self.xiaobing.SetLineEdited(id, current_page, afterModified)
        #info = self.xiaobing.get_info(current_page)
        #self.status(info)
        self.status_display(self.tab1, id + '_Edit', 0)
        #self.content_page(info)

    def risk_button(self, id, current_page, Reason):
        self.xiaobing.SetLineRisk(id, current_page, Reason)
        #info = self.xiaobing.get_info(current_page)
        #self.status(info)
        self.status_display(self.tab1, id + '_Risky', 0)
        #self.content_page(info)

    def bad_button(self, id, current_page):
        self.xiaobing.SetLineBad(id, current_page)
        #info = self.xiaobing.get_info(current_page)
        #self.status(info)
        self.status_display(self.tab1, id + '_Bad', 0)
        #self.content_page(info)

    def pos_button(self, id, current_page):
        self.xiaobing.SetLinePos(id, current_page)
        info = self.xiaobing.get_info(current_page)
        self.content_page(self.tab1, info)
        self.status_display(self.tab1, id + '_Pos', info[0])

    def neg_button(self, id, current_page):
        self.xiaobing.SetLineNeg(id, current_page)
        info = self.xiaobing.get_info(current_page)
        self.content_page(self.tab1, info)
        self.status_display(self.tab1, id + '_Neg', info[0])

    def neu_button(self, id, current_page):
        self.xiaobing.SetLineNeu(id, current_page)
        info = self.xiaobing.get_info(current_page)
        self.content_page(self.tab1, info)
        self.status_display(self.tab1, id + '_Neu', info[0])


if __name__ == '__main__':
    app = MainPage()
    mainloop()
