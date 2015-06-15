class VRP:
    
    def __init__(self,nTrucks,capacity,targetsData, speed = 1):
        self.nTrucks         = nTrucks
        self.capacity        = capacity
        self.speed           = speed
        self.targetLocations = [(target['x'],target['y'])       for target in targetsData]
        self.targetsWindows  = [(target['start'],target['end']) for target in targetsData]
        self.targetDurations = [target['duration']              for target in targetsData]
        self.targetDemand    = [target['demand']                for target in targetsData]
        self.nTargets        = len(self.targetDemand)

    def bfsConfBuilderWrapper(self, buildParam, runParam):
        pass
        
    def checkFeasible(self,conf,targetId):
        pass
        
    def getDistance(self,t1,t2):
        pass
    
    def trimConfs(self,newConfs,buildParam):
        pass
    
    def bfsConfBuilder(self, buildParam, runParam, lastLevelConfs):
        newConfs = []
        for conf in lastLevelConfs:
            lastDistanceTravelled = self.getDistance(conf.targets[-1],0)
            for targetId in range(self.nTargets):
                if targetId in conf.targets:
                    continue
                (success, newFinishTime,newCapacity) = self.checkFeasible(conf,targetId)
                if not success:
                    continue
                newConfTargets = conf.targets + [targetId]
                newConfVal     = conf.val - lastDistanceTravelled + self.getDistance(targetId,0) 
                
                newConf = conf(newConfTargets, newConfVal, newFinishTime, newCapacity)
                newConfs.append(newConf)
        newConfs = self.trimConfs(newConfs,buildParam)
        return newConfs
                    
class conf:
    
    def __init__(self, targets, val = -1, finishTime = -1, currentCapacity = -1):
        self.targets = targets
        if (val == -1):
            (self.val,self.finishTime,self.currentCapacity) = self.calcParams(targets)
        else: 
            self.val = val
            self.finishTime
            self.currentCapacity
    
    # calc val as the sum of distances between the confs
    # calc finish time as val
    def calcParams(self, target):
        pass
        
    