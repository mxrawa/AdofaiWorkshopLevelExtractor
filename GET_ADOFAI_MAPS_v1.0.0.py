import os, shutil, codecs, re

class GetWorkshopLevels():
    def __init__(self):
        self.workshop = r"D:\nn_steam\steamapps\workshop\content\977950"
        self.output = r"D:\桌面\冰与火之舞\自定义关卡\创意工坊谱"
        self.ProcessingLevel()

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
                    filePath = self.workshop +"\\"+ID+"\\"+aloneFile
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
                                sizeSet[k] = list(tmpSize.keys())[list(tmpSize.values()).index(nxt)]
                            else:
                                nowx += 1
                    except Exception:
                        pass
            else:
                filePath = self.workshop +"\\"+ID+"\\"+endFile
                sizeSet[ID] = filePath
        for dKey, dVaules in sizeSet.items():
            try:
                levelInfo = self.readInfo(sizeSet[dKey]).replace("\\n","").replace('"',"").replace("\\", "")
            except Exception:
                pass
            if levelInfo and (not os.path.exists(self.output+"\\"+levelInfo)):
                folderPath = self.workshop +"\\"+dKey
                shutil.copytree(os.path.abspath(folderPath), os.path.abspath(self.output+"\\"+dKey))
                os.rename(self.output+"\\"+dKey,self.output+"\\"+levelInfo)
                print("Finished:",levelInfo)
        print("处理完成!")

    def readInfo(self, path):
        with open(path,"r",encoding="utf-8-sig") as f:
            f = f.read()
            searchObj = re.search(r'"song": "(.*)", ',f)
            searchObj2 = re.search(r'"artist": "(.*)", ',f)
            if searchObj and searchObj2:
                song = searchObj.group(1)
                artist = searchObj2.group(1)
                pattern = re.compile(r'<[^>]+>',re.S)
                song = pattern.sub('', song)
                artist = pattern.sub('', artist)
                return artist + " - " + song

    def GetLevelID(self):
        return os.listdir(self.workshop)

GetWorkshopLevels() 