import os
import csv
import datetime


def opponentsStateDecode(opponentsStateFileName):
    if not os.path.isfile(opponentsStateFileName) :
        assert NotADirectoryError("{} is not exists".format(opponentsStateFileName))
        pass
    data = None
    with open(opponentsStateFileName,'r') as r:
        data = eval(r.read())
        pass
    return data
def opponentsStateEncode(opponentsState,fileName):
    with open(fileName,'w') as f:
        f.write(str(opponentsState))
        pass
    pass

class TrainingInfo(object):
    def __init__(self,fileName):
        self.fileName = fileName
        self.trainingInfo = {}
        self.csvTitle = []
        

        self.StatusDataTitle = ["Episode","RewardSum"]
        self.BadInfoTitle = ["isUseBadAction","isGoOutSide","isOutSideShoot","isGoOutBall"]
        for title in self.StatusDataTitle :
            self.csvTitle.append(title)
        for title in self.BadInfoTitle :
            self.csvTitle.append(title)

        for title in self.csvTitle :
            self.trainingInfo[title] = 0
        # self.InitBadInfoCount()
    
        if os.path.isfile(fileName) :
            with open(self.fileName,'r') as csvFile:
                rows = csvFile.readlines()
                row = rows[len(rows)-1]
                data = row.split(",")
                for i in range(len(self.StatusDataTitle)) :
                    self.trainingInfo[self.StatusDataTitle[i]] = float(data[i])
                pass
            pass
        else:
            with open(fileName,'a') as w:
                writer = csv.writer(w)
                writer.writerow(self.csvTitle)
                pass
            pass
        pass

    def InitBadInfoCount(self):
        for title in self.BadInfoTitle :
            self.trainingInfo[title] = 0

    def IsEnd(self):
        judgementFile = "End"
        isEnd = os.path.exists(judgementFile)
        if isEnd :
            os.remove(judgementFile)
        return isEnd
    
    
    def Save(self):
        data = []
        for title in self.csvTitle :
            data.append(round(self.trainingInfo[title],3))
        with open(self.fileName,'a') as w:
            writer = csv.writer(w)
            writer.writerow(data)
            pass
        pass
    pass
