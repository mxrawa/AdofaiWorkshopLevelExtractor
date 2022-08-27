#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import shutil
import codecs
import re
import time
import datetime
import sys
import tkinter as tk
import tkinter.filedialog as fdl
import ttkbootstrap as ttk
import ttkbootstrap.constants as cst
import ttkbootstrap.dialogs as dlog
from ttkbootstrap.scrolled import ScrolledText

__version__ = "1.2.0"
__author__ = "一个憨憨毛"


class LanguageDict():
    def __init__(self):
        self.langdict = {
            "CN": {
                "LangSettings": "语言",
                "Title": f"ADOFAI创意工坊关卡提取器v{__version__} - {__author__}制作",
                "AdofaiWorkshopPath": "ADOFAI创意工坊目录:",
                "OutputPath": "关卡导出目录:",
                "ManualSearch": "手动查找",
                "GetLevel": "导出创意工坊关卡",
                "SuccessfullyCompleted": "成功完成:",
                "TaskCompleted": "任务完成:所有关卡均已导出",
                "WrongPathMSG": ["错误的目录", "此目录并不是冰与火之舞的创意工坊目录"],
                "TaskCompletedMSG": ["成功!", "所有关卡均已导出"],
                "EditBlockedCharacters": "编辑违规字符",
                "IllegalCharacter": "违规字符",
                "HtmlTag": "HTML标签",
                "DeleteSelectedData": "删除选中数据",
                "AddThisData": "添加此数据",
                "CannotDeleteMSG": ["不可删除",["违规词[","]带有特殊配置,不可删除"]]
            },
            "TC": {
                "LangSettings": "語言",
                "Title": f"ADOFAI創意工坊關卡提取器v{__version__} - {__author__}製作",
                "AdofaiWorkshopPath": "ADOFAI創意工坊目錄:",
                "OutputPath": "關卡匯出目錄:",
                "ManualSearch": "手動查找",
                "GetLevel": "匯出創意工坊關卡",
                "SuccessfullyCompleted": "成功完成:",
                "TaskCompleted": "任務完成:所有關卡均已匯出",
                "WrongPathMSG": ["錯誤的目錄", "此目錄並不是冰與火之舞的創意工坊目錄"],
                "TaskCompletedMSG": ["成功!", "所有關卡均已匯出"],
                "EditBlockedCharacters": "編輯違規字元",
                "IllegalCharacter": "違規字元",
                "HtmlTag": "HTML標籤",
                "DeleteSelectedData": "删除選中數據",
                "AddThisData": "添加此數據",
                "CannotDeleteMSG": ["不可删除",["違規詞[","帶有特殊配寘，不可删除"]]
            },
            "EN": {
                "LangSettings": "Language",
                "Title": f"ADOFAI Creative Workshop Level Extractor v{__version__}- Made by {__author__}",
                "AdofaiWorkshopPath": "ADOFAI Creative Workshop directory:",
                "OutputPath": "Level Export directory:",
                "ManualSearch": "Search",
                "GetLevel": "Export Creative Workshop Level",
                "SuccessfullyCompleted": "Finished:",
                "TaskCompleted": "TaskCompleted:All levels have been exported",
                "WrongPathMSG": ["Wrong Path", "This directory is not a Creative Workshop directory of ADOFAI"],
                "TaskCompletedMSG": ["Success!", "All levels have been exported"],
                "EditBlockedCharacters": "Edit Blocked Characters",
                "IllegalCharacter": "Illegal Character",
                "HtmlTag": "HtmlTag",
                "DeleteSelectedData": "Delete Selected Data",
                "AddThisData": "Add This Data",
                "CannotDeleteMSG": ["Cannot be deleted",["The violation word [","] has special configuration and cannot be deleted"]]
            },
            "JP": {
                "LangSettings": "言語",
                "Title": f"ADOFAIクリエイティブワークショップ関数抽出器 v{__version__}- {__author__} 作成",
                "AdofaiWorkshopPath": "ADOFAIクリエイティブワークショップカタログ:",
                "OutputPath": "レベルエクスポートディレクトリ:",
                "ManualSearch": "検索",
                "GetLevel": "クリエイティブワークショップレベルのエクスポート",
                "SuccessfullyCompleted": "正常に完了しました:",
                "TaskCompleted": "タスク完了:すべてのレベルがエクスポートされました",
                "WrongPathMSG": ["フォルトディレクトリ", "このディレクトリは氷と火の舞のアイデア工房ディレクトリではありません"],
                "TaskCompletedMSG": ["成功!", "すべてのレベルがエクスポートされました"],
                "EditBlockedCharacters": "違反文字の編集",
                "IllegalCharacter": "違反文字",
                "HtmlTag": "HTMLラベル",
                "DeleteSelectedData": "選択したデータを削除",
                "AddThisData": "このデータを追加",
                "CannotDeleteMSG": ["削除不可",["違反語「","」には特別な構成があり、削除できません"]]
            }
        }


class GetWorkshopLevels(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(width=False, height=False)
        self.FindFileCount = 0
        style = ttk.Style()
        self.geometry("+200+200")
        style.theme_use("morph")
        global v
        v = tk.IntVar()
        self.appdata = os.path.expanduser('~')+"\\AppData"
        try:
            with open(self.appdata+"\\Lang.txt", "r", encoding="utf-8") as df:
                self.lang = df.read()
                self.langdict = LanguageDict().langdict[self.lang]
                if self.lang == "CN":
                    v.set(1)
                elif self.lang == "TC":
                    v.set(2)
                elif self.lang == "EN":
                    v.set(3)
                elif self.lang == "JP":
                    v.set(4)
        except:
            with open(self.appdata+"\\Lang.txt", "w", encoding="utf-8") as df:
                df.write("CN")
                self.langdict = LanguageDict().langdict["CN"]
            v.set(1)
        self.SetLang_2(v.get())
        self.loadUi()

    def loadUi(self):
        self.title(self.langdict["Title"])
        ttk.Label(self, text=self.langdict["AdofaiWorkshopPath"], justify=tk.RIGHT).grid(
            row=0, column=0, sticky=tk.E)
        ttk.Label(self, text=self.langdict["OutputPath"], justify=tk.RIGHT).grid(
            row=1, column=0, sticky=tk.E)
        self.workshop_entry = ttk.Entry(self, width=70)
        self.workshop_entry.grid(row=0, column=1)
        self.output_entry = ttk.Entry(self, width=70)
        self.output_entry.grid(row=1, column=1)
        ttk.Button(self, text=self.langdict["ManualSearch"], command=self.set_workshop, bootstyle=(cst.SUCCESS, cst.OUTLINE)).grid(
            row=0, column=2)
        ttk.Button(self, text=self.langdict["ManualSearch"], command=self.set_output, bootstyle=(cst.SUCCESS, cst.OUTLINE)).grid(
            row=1, column=2)
        self.AFRAME = ttk.Frame(self)
        self.AFRAME.grid(row=2, column=0, columnspan=3)
        if (self.lang != "EN") and (self.lang != "JP"):
            self.text = ScrolledText(
                self.AFRAME, padding=5, height=20, autohide=True, width=97)
            self.text.pack(fill=cst.BOTH, expand=cst.YES)
            ttk.Button(self.AFRAME, text=self.langdict["GetLevel"], width=95, command=self.output, bootstyle=(cst.SUCCESS, cst.OUTLINE)).pack()
        elif self.lang == "EN":
            self.text = ScrolledText(
                self.AFRAME, padding=5, height=20, autohide=True, width=112)
            self.text.pack(fill=cst.BOTH, expand=cst.YES)
            ttk.Button(self.AFRAME, text=self.langdict["GetLevel"], width=110, command=self.output, bootstyle=(cst.SUCCESS, cst.OUTLINE)).pack()
        elif self.lang == "JP":
            self.text = ScrolledText(
                self.AFRAME, padding=5, height=20, autohide=True, width=115)
            self.text.pack(fill=cst.BOTH, expand=cst.YES)
            ttk.Button(self.AFRAME, text=self.langdict["GetLevel"], width=114, command=self.output, bootstyle=(cst.SUCCESS, cst.OUTLINE)).pack()
        self.menu = ttk.Menu(self)
        self.submenu = ttk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(
            label=self.langdict["LangSettings"], menu=self.submenu)
        langs = [
            ("简体中文", 1),
            ("繁體中文", 2),
            ("English", 3),
            ("日本語", 4)
        ]
        for lang, num in langs:
            self.submenu.add_radiobutton(
                label=lang, variable=v, value=num, command=lambda: self.SetLang(v.get()))
        self.config(menu=self.menu)
        self.banWordsFrame = ttk.Labelframe(
            self, text=self.langdict["EditBlockedCharacters"], bootstyle=cst.PRIMARY)
        self.banWordsFrame.grid(row=0, rowspan=3, column=3)
        self.bannedWordsTree = ttk.Treeview(self.banWordsFrame,
                                       columns=[0],
                                       show=cst.HEADINGS,
                                       height=18
                                       )
        banWords = [
            (self.langdict['HtmlTag']),
            ('+')
        ]
        for row in banWords:
            self.bannedWordsTree.insert('', tk.END, values=row)
        self.bannedWordsTree.selection_set('I001')
        self.bannedWordsTree.heading(0, text=self.langdict["IllegalCharacter"])
        self.bannedWordsTree.column(0, width=31)
        self.bannedWordsTree.pack(side=cst.TOP, anchor=cst.NE, fill=cst.X)
        def tmpFunc():
            if AddItem.get():
                self.bannedWordsTree.insert('', 'end', values=(AddItem.get()))
                banWords.append((AddItem.get()))
        def tmpFunc2():
            try:
                if self.bannedWordsTree.item(self.bannedWordsTree.selection())["values"][0] != self.langdict["HtmlTag"]:
                    self.bannedWordsTree.delete(self.bannedWordsTree.selection())
                else:
                    htmltag = self.langdict["HtmlTag"]
                    dlog.Messagebox.show_warning(title=self.langdict["CannotDeleteMSG"][0],message=self.langdict["CannotDeleteMSG"][1][0]+htmltag+self.langdict["CannotDeleteMSG"][1][1])
            except Exception:
                self.bannedWordsTree.delete(self.bannedWordsTree.selection())
        ttk.Button(self.banWordsFrame, text=self.langdict["AddThisData"], width=30, bootstyle=("OUTLINE", "SUCCESS"),
                    command=lambda: tmpFunc()).pack(side=cst.BOTTOM)
        AddItem = ttk.Entry(self.banWordsFrame, width=32)
        AddItem.pack(side=cst.BOTTOM)
        ttk.Button(self.banWordsFrame, text=self.langdict["DeleteSelectedData"], width=30, bootstyle=("OUTLINE", "SUCCESS"),
                    command=lambda: tmpFunc2()).pack(side=cst.BOTTOM)

    def SetLang_2(self, langId: int) -> None:
        self.lang = ""
        if langId == 1:
            self.lang = "CN"
        elif langId == 2:
            self.lang = "TC"
        elif langId == 3:
            self.lang = "EN"
        elif langId == 4:
            self.lang = "JP"
        self.langdict = LanguageDict().langdict[self.lang]

    def SetLang(self, langId: int) -> None:
        self.lang = ""
        if langId == 1:
            self.lang = "CN"
        elif langId == 2:
            self.lang = "TC"
        elif langId == 3:
            self.lang = "EN"
        elif langId == 4:
            self.lang = "JP"
        self.langdict = LanguageDict().langdict[self.lang]
        with open(self.appdata+"\\Lang.txt", "w", encoding="utf-8") as df:
            df.write(self.lang)
            self.destroy()
            with open(self.appdata+"\\temp.bat", "w", encoding="gbk") as kf:
                kf.write(f"""@echo off & cls & taskkill /f /t /im python.exe
python {__file__}
exit""")
                kf.close()
            with open(self.appdata+"\\temp.vbs", "w", encoding="gbk") as dk:
                dk.write(f"""Set ws = CreateObject("Wscript.Shell")
ws.run "cmd /c {self.appdata}\\temp.bat",vbhide""")
                dk.close()
            os.system("start "+self.appdata+"\\temp.vbs")

    def output(self):
        self.workshop = self.workshop_entry.get()
        self.output = self.output_entry.get()
        self.Banned = []
        for b in self.bannedWordsTree.get_children():
            try:
                if self.bannedWordsTree.item(b)["values"][0] != self.langdict['HtmlTag']:
                    self.Banned.append(self.bannedWordsTree.item(b)["values"][0])
            except Exception:
                self.Banned.append(" ")
        self.ProcessingLevel()

    def set_workshop(self):
        folder = fdl.askdirectory()
        if folder.split("/")[-1] == "977950":
            self.workshop_entry.delete(0, "end")
            self.workshop_entry.insert("end", folder)
        else:
            dlog.Messagebox.show_error(
                title=self.langdict["WrongPathMSG"][0], message=self.langdict["WrongPathMSG"][1])

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
                for banWord in self.Banned:
                    levelInfo = levelInfo.replace(banWord, "")
                levelInfo = ' '.join(levelInfo.split())
            except Exception:
                pass
            if levelInfo and (not os.path.exists(self.output+"\\"+levelInfo)):
                folderPath = self.workshop + "\\"+dKey
                shutil.copytree(os.path.abspath(folderPath),
                                os.path.abspath(self.output+"\\"+dKey))
                os.rename(self.output+"\\"+dKey, self.output+"\\"+levelInfo)
                self.text.insert(
                    tk.END, self.langdict["SuccessfullyCompleted"]+levelInfo+"\n")
                self.text.see(tk.END)
                self.update()
                kcount += 1
        dlog.Messagebox.show_info(
            title=self.langdict["TaskCompletedMSG"][0], message=self.langdict["TaskCompletedMSG"][1])
        self.text.tag_add('last', tk.END)
        self.text.tag_config('last', foreground="#00FF00")
        self.text.insert(tk.END, self.langdict["TaskCompleted"], 'last')
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
