#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import shutil
import codecs
import re
import string
import time
import tkinter as tk
import tkinter.filedialog as fdl
import tkinter.messagebox as mbox

__version__ = "1.1.1"
__author__ = "一个憨憨毛"

class GetWorkshopLevels(tk.Tk):
    def __init__(self):
        super().__init__()
        self.FindFileCount = 0
        self.loadUi()

    def loadUi(self):
        self.title(f"ADOFAI创意工坊关卡提取器v{__version__} - {__author__}制作")
        tk.Label(self, text="ADOFAI创意工坊位置:", justify=tk.RIGHT).grid(
            row=0, column=0, sticky=tk.E)
        tk.Label(self, text="关卡导出目录:", justify=tk.RIGHT).grid(
            row=1, column=0, sticky=tk.E)
        self.workshop_entry = tk.Entry(self, width=70)
        self.workshop_entry.grid(row=0, column=1)
        self.output_entry = tk.Entry(self, width=70)
        self.output_entry.grid(row=1, column=1)
        tk.Button(self, text="手动查找", command=self.set_workshop).grid(
            row=0, column=2)
        tk.Button(self, text="手动查找", command=self.set_output).grid(
            row=1, column=2)
        self.text = tk.Text(self, width=95, state=tk.NORMAL)
        self.text.grid(row=2, column=0, columnspan=3)
        tk.Button(self, text="导出创意工坊关卡", width=95, command=self.output).grid(
            row=3, column=0, columnspan=3)

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
            mbox.showerror("错误的目录", "此目录并不是冰与火之舞的创意工坊目录")
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
                self.text.insert(tk.END, "成功完成:"+levelInfo+"\n")
                self.text.see(tk.END)
                self.update()
                kcount += 1
        mbox.showinfo("OKAY!", "所有关卡均已导出")
        self.text.tag_add('last', tk.END)
        self.text.tag_config('last', foreground="#00FF00")
        self.text.insert(tk.END, "任务完成:所有关卡均已导出",'last')
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
