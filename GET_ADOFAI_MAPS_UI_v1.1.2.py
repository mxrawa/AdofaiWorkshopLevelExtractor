#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import shutil
import codecs
import re
import string
import time
import sys
import tkinter as tk
import tkinter.filedialog as fdl
import tkinter.messagebox as mbox

__version__ = "1.1.2"
__author__ = "一个憨憨毛"

class LanguageDict():
    def __init__(self):
        self.langdict = {
            "CN":{
                "LangSettings": "语言",
                "Title": f"ADOFAI创意工坊关卡提取器v{__version__} - {__author__}制作",
                "AdofaiWorkshopPath": "ADOFAI创意工坊目录:",
                "OutputPath": "关卡导出目录:",
                "ManualSearch": "手动查找",
                "GetLevel": "导出创意工坊关卡",
                "SuccessfullyCompleted": "成功完成:",
                "TaskCompleted": "任务完成:所有关卡均已导出",
                "WrongPathMSG": ["错误的目录", "此目录并不是冰与火之舞的创意工坊目录"],
                "TaskCompletedMSG": ["成功!", "所有关卡均已导出"]
            },
            "TC":{
                "LangSettings": "語言",
                "Title": f"ADOFAI創意工坊關卡提取器v{__version__} - {__author__}製作",
                "AdofaiWorkshopPath": "ADOFAI創意工坊目錄:",
                "OutputPath": "關卡匯出目錄:",
                "ManualSearch": "手動查找",
                "GetLevel": "匯出創意工坊關卡",
                "SuccessfullyCompleted": "成功完成:",
                "TaskCompleted": "任務完成:所有關卡均已匯出",
                "WrongPathMSG": ["錯誤的目錄", "此目錄並不是冰與火之舞的創意工坊目錄"],
                "TaskCompletedMSG": ["成功!", "所有關卡均已匯出"]
            },
            "EN":{
                "LangSettings": "Language",
                "Title": f"ADOFAI Creative Workshop Level Extractor v{__version__}- Made by {__author__}",
                "AdofaiWorkshopPath": "ADOFAI Creative Workshop directory:",
                "OutputPath": "Level Export directory:",
                "ManualSearch": "Search",
                "GetLevel": "Export Creative Workshop Level",
                "SuccessfullyCompleted": "Finished:",
                "TaskCompleted": "TaskCompleted:All levels have been exported",
                "WrongPathMSG": ["Wrong Path", "This directory is not a Creative Workshop directory of ADOFAI"],
                "TaskCompletedMSG": ["Success!", "All levels have been exported"]
            },
            "JP":{
                "LangSettings": "言語",
                "Title": f"ADOFAIクリエイティブワークショップ関数抽出器 v{__version__}- {__author__} 作成",
                "AdofaiWorkshopPath": "ADOFAIクリエイティブワークショップカタログ:",
                "OutputPath": "レベルエクスポートディレクトリ:",
                "ManualSearch": "検索",
                "GetLevel": "クリエイティブワークショップレベルのエクスポート",
                "SuccessfullyCompleted": "正常に完了しました:",
                "TaskCompleted": "タスク完了:すべてのレベルがエクスポートされました",
                "WrongPathMSG": ["フォルトディレクトリ", "このディレクトリは氷と火の舞のアイデア工房ディレクトリではありません"],
                "TaskCompletedMSG": ["成功!", "すべてのレベルがエクスポートされました"]
            }
        }

class GetWorkshopLevels(tk.Tk):
    def __init__(self):
        super().__init__()
        self.FindFileCount = 0
        global v
        v = tk.IntVar()
        self.appdata = os.path.expanduser('~')+"\\AppData"
        try:
            with open(self.appdata+"\\Lang.txt","r",encoding="utf-8") as df:
                lang=df.read()
                self.langdict = LanguageDict().langdict[lang]
                if lang == "CN":
                    v.set(1)
                elif lang == "TC":
                    v.set(2)
                elif lang == "EN":
                    v.set(3)
                elif lang == "JP":
                    v.set(4)
        except:
            with open(self.appdata+"\\Lang.txt","w",encoding="utf-8") as df:
                df.write("CN")
                self.langdict = LanguageDict().langdict["CN"]
            v.set(1)
        self.SetLang_2(v.get())
        self.loadUi()

    def loadUi(self):
        self.title(self.langdict["Title"])
        tk.Label(self, text=self.langdict["AdofaiWorkshopPath"], justify=tk.RIGHT).grid(
            row=0, column=0, sticky=tk.E)
        tk.Label(self, text=self.langdict["OutputPath"], justify=tk.RIGHT).grid(
            row=1, column=0, sticky=tk.E)
        self.workshop_entry = tk.Entry(self, width=70)
        self.workshop_entry.grid(row=0, column=1)
        self.output_entry = tk.Entry(self, width=70)
        self.output_entry.grid(row=1, column=1)
        tk.Button(self, text=self.langdict["ManualSearch"], command=self.set_workshop).grid(
            row=0, column=2)
        tk.Button(self, text=self.langdict["ManualSearch"], command=self.set_output).grid(
            row=1, column=2)
        self.text = tk.Text(self, width=97, state=tk.NORMAL)
        self.text.grid(row=2, column=0, columnspan=3)
        tk.Button(self, text=self.langdict["GetLevel"], width=95, command=self.output).grid(
            row=3, column=0, columnspan=3)
        self.menu = tk.Menu(self)
        self.submenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label=self.langdict["LangSettings"], menu=self.submenu)
        langs = [
            ("简体中文",1),
            ("繁體中文",2),
            ("English",3),
            ("日本語",4)
        ]
        for lang, num in langs:
            self.submenu.add_radiobutton(label=lang,variable=v,value=num,command=lambda: self.SetLang(v.get()))
        self.config(menu=self.menu)

    def SetLang_2(self, langId: int) -> None:
        lang = ""
        if langId == 1:
            lang = "CN"
        elif langId == 2:
            lang = "TC"
        elif langId == 3:
            lang = "EN"
        elif langId == 4:
            lang = "JP"
        self.langdict = LanguageDict().langdict[lang]

    def SetLang(self, langId: int) -> None:
        lang = ""
        if langId == 1:
            lang = "CN"
        elif langId == 2:
            lang = "TC"
        elif langId == 3:
            lang = "EN"
        elif langId == 4:
            lang = "JP"
        self.langdict = LanguageDict().langdict[lang]
        with open(self.appdata+"\\Lang.txt","w",encoding="utf-8") as df:
            df.write(lang)
            self.destroy()
            with open(self.appdata+"\\temp.bat","w",encoding="gbk") as kf:
                kf.write(f"""@echo off & cls & taskkill /f /t /im python.exe
python {__file__}
exit""")
                kf.close()
            with open(self.appdata+"\\temp.vbs","w",encoding="gbk") as dk:
                dk.write(f"""Set ws = CreateObject("Wscript.Shell")
ws.run "cmd /c {self.appdata}\\temp.bat",vbhide""")
                dk.close()
            os.system("start "+self.appdata+"\\temp.vbs")

    def output(self):
        self.workshop = self.workshop_entry.get()
        self.output = self.output_entry.get()
        self.ProcessingLevel()

    def set_workshop(self):
        folder = fdl.askdirectory()
        if folder.split("/")[-1] == "977950":
            self.workshop_entry.delete(0, "end")
            self.workshop_entry.insert("end", folder)
        else:
            mbox.showerror(self.langdict["WrongPathMSG"][0], self.langdict["WrongPathMSG"][1])
            pass

    def set_output(self):
        folder = fdl.askdirectory()
        self.output_entry.delete(0, "end")
        self.output_entry.insert("end", folder)

    def ProcessingLevel(self):
        self.IDList = self.GetLevelID()
        self.LevelFiles = {}
        for mapid in self.IDList:
            count = 0
            self.LevelFiles[mapid] = []
            self.LevelPath = self.workshop + "\\" + mapid
            for pfile in os.listdir(self.LevelPath):
                if os.path.splitext(pfile)[-1] == ".adofai":
                    if pfile.lower() != "backup.adofai":
                        count += 1
            for mfile in os.listdir(self.LevelPath):
                if os.path.splitext(mfile)[-1].lower() == ".adofai":
                    if mfile.lower() != "backup.adofai":
                        if count > 1:
                            self.LevelFiles[mapid].append(mfile)
                        else:
                            self.LevelFiles[mapid] = mfile
        tEnd = {}
        sizeSet = {}
        for ID, endFile in self.LevelFiles.items():
            if isinstance(endFile, list):
                PathSet = []
                for aloneFile in endFile:
                    filePath = self.workshop + "\\"+ID+"\\"+aloneFile
                    PathSet.append(filePath)
                tEnd[ID] = PathSet
                for k in tEnd:
                    nowList = tEnd[k]
                    tr = {}
                    tmpSize = {}
                    te = []
                    tr[k] = []
                    try:
                        for n in nowList:
                            tr[k].append(n)
                        for x1, x2 in tr.items():
                            for xi in x2:
                                tmpSize[xi] = os.path.getsize(xi)
                                nowx = 0
                                for xt in tmpSize.values():
                                    te.append(xt)
                        for nxt in tmpSize.values():
                            if nxt == max(te):
                                sizeSet[k] = list(tmpSize.keys())[
                                    list(tmpSize.values()).index(nxt)]
                            else:
                                nowx += 1
                    except Exception:
                        pass
            else:
                filePath = self.workshop + "\\"+ID+"\\"+endFile
                sizeSet[ID] = filePath
        kcount = 0
        for dKey, dVaules in sizeSet.items():
            try:
                levelInfo = self.readInfo(sizeSet[dKey]).replace(
                    "\\n", "").replace('"', "").replace("\\", "")
                levelInfo = ' '.join(levelInfo.split())
            except Exception:
                pass
            if levelInfo and (not os.path.exists(self.output+"\\"+levelInfo)):
                folderPath = self.workshop + "\\"+dKey
                shutil.copytree(os.path.abspath(folderPath),
                                os.path.abspath(self.output+"\\"+dKey))
                os.rename(self.output+"\\"+dKey, self.output+"\\"+levelInfo)
                self.text.insert(tk.END, self.langdict["SuccessfullyCompleted"]+levelInfo+"\n")
                self.text.see(tk.END)
                self.update()
                kcount += 1
        mbox.showinfo(self.langdict["TaskCompletedMSG"][0], self.langdict["TaskCompletedMSG"][1])
        self.text.tag_add('last', tk.END)
        self.text.tag_config('last', foreground="#00FF00")
        self.text.insert(tk.END, self.langdict["TaskCompleted"],'last')
        self.update()

    def readInfo(self, path):
        with open(path, "r", encoding="utf-8-sig") as f:
            f = f.read()
            searchObj = re.search(r'"song": "(.*)", ', f)
            searchObj2 = re.search(r'"artist": "(.*)", ', f)
            if searchObj and searchObj2:
                song = searchObj.group(1)
                artist = searchObj2.group(1)
                pattern = re.compile(r'<[^>]+>', re.S)
                song = pattern.sub('', song)
                artist = pattern.sub('', artist)
                return artist + " - " + song

    def GetLevelID(self):
        return os.listdir(self.workshop)


app = GetWorkshopLevels()
app.mainloop()
