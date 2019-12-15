import os

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