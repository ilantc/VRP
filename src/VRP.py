from math import sqrt
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
        
        finishTime      = conf.finishTime
        capacityLeft    = conf.currentCapacity
        lastTarget      = conf.targets[-1]
        
        newFinish   = -1
        success     = False
        
        # capacity constraints
        newCapacity = capacityLeft - self.capacity(targetId)
        if newCapacity < 0:
            return (success,newFinish,newCapacity)
        
        # time window constraints
        arrivalTime = finishTime + self.getDistance(lastTarget, targetId)
        windowStart = self.targetsWindows[targetId][0]
        windowEnd   = self.targetsWindows[targetId][1]
        waitingTime = max(0,windowStart - arrivalTime)
        if arrivalTime > windowEnd:
            return (success,newFinish,newCapacity)
        newFinish   = arrivalTime + self.targetDurations[targetId] + waitingTime
        success     = True
        return (success,newFinish,newCapacity)
        
    def getDistance(self,t1,t2):
        (x1,y1) = self.targetLocations(t1)
        (x2,y2) = self.targetLocations(t2)
        return sqrt( ((x1 - x2)^2) + ((y1 - y2)^2) )
    
    def trimConfs(self,confs,trimParam):
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
    
    # target do not include "0" target at start and end
    # capacity is the total amount of capacity needed for the targets
    # val is the sum of all distances including from and to "0"
    def __init__(self, targets, VRPobject, val = -1, finishTime = -1, currentCapacity = -1):
        self.targets = targets
        self.VRPobject = VRPobject
        if (val == -1):
            (self.val,self.finishTime,self.currentCapacity) = self.calcParams()
        else: 
            self.val                = val
            self.finishTime         = finishTime 
            self.currentCapacity    = currentCapacity
    
    # calc val as the sum of distances between the confs
    # calc finish time as val
    def calcParams(self):
        val             = 0
        finishTime      = 0
        currentDemand   = 0
        prevTarget      = 0
        for target in self.targets:
            val             += (self.VRPobject.getDistance(prevTarget,target) / self.VRPobject.speed)
            currentDemand   += self.VRPobject.targetDemand[target]
            timeToTravel     = (self.VRPobject.getDistance(prevTarget,target) / self.VRPobject.speed)
            timeToService    = self.VRPobject.targetDurations[target]
            earlyArrival     = timeToTravel + finishTime 
            windowStart      = self.VRPobject.targetsWindows[target][0]
            waitingTime      = max(0,windowStart - earlyArrival)
            finishTime      += timeToTravel + waitingTime + timeToService 
            prevTarget       = target
            
        val         += (self.VRPobject.getDistance(prevTarget,0) / self.VRPobject.speed)
        return (val,finishTime,self.VRPobject.capacity - currentDemand)
            
        
    