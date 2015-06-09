class VRP:
    
    def __init__(self,nTrucks,capacity,targetsData):
        self.nTrucks = nTrucks
        self.targetLocations = [(target['x'],target['y'])       for target in targetsData]
        self.targetsWindows  = [(target['start'],target['end']) for target in targetsData]
        self.targetDurations = [target['duration']              for target in targetsData]
        self.targetDemand    = [target['demand']                for target in targetsData]


class solomonFileReader:
    
    def __init__(self):
        pass
    
    def readFile(self,fileName):
        data = {}
        f = open(fileName)
        
        # problem name
        data['name'] = f.next().strip()
        # 3 blank lines
        for _ in range(3):
            f.next()
        # nTrucks and capacity
        line = f.next()
        lineData = line.strip().split()
        data["nTrucks"] = lineData[0]
        data["capacity"] = lineData[1]
        # skip 4
        for _ in range(4):
            f.next()
        # targets data
        data['targets'] = []
        for line in f:
            l = line.strip()
            if l == "":
                continue 
            lineData            = l.split()
            target = {}
            target["id"]          = lineData[0]
            target["x"]           = lineData[1]
            target["y"]           = lineData[2]
            target["demand"]      = lineData[3]
            target["start"]       = lineData[4]
            target["end"]         = lineData[5]
            target["duration"]    = lineData[6]
            data['targets'].append(target)
        
        return data