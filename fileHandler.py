import os
import json
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
        self.Episode = 0
        self.EndTime = None
        self.RewardSum = 0
        
        if os.path.isfile(fileName) :
            with open(self.fileName,'r') as r:
                data = r.read()
                data = json.loads(data)
                self.Episode = int(data['Episode'])
                self.EndTime = data['EndTime']
                self.RewardSum = data['RewardSum']
                pass
            pass
        else:
            self.Save()
    def IsEnd(self):
        judgementFile = "End"
        isEnd = os.path.exists(judgementFile)
        if isEnd :
            os.remove(judgementFile)
        return isEnd
    def Save(self):
        data = {
            'Episode' : self.Episode,
            'EndTime' : str(datetime.datetime.now()),
            'RewardSum' : self.RewardSum
        }
        with open(self.fileName,'w') as w:
            w.write(json.dumps(data))
            pass
        pass
    pass
