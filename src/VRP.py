from math import sqrt
import math
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

    def bfsConfBuilderWrapper(self, buildParam, runParam,MaxSizeConf):
        confs=[]
        emptyconf=conf([], self, 0, 0, 0)
        confs.append(emptyconf)
        lastLevelConfs = confs
        for confSize in xrange(0,MaxSizeConf+1):
            newConfs        = self.bfsConfBuilder(lastLevelConfs)
            lastLevelConfs  = self.trimConfs(newConfs, buildParam)
            newConfsForRun  = self.trimConfs(lastLevelConfs, runParam)
            confs.extend(newConfsForRun)
            print "conf size =",confSize, "built", len(newConfs), "chosen", len(lastLevelConfs)
        return confs

        
    def checkFeasible(self,conf,targetId):
        
        finishTime  = conf.finishTime
        capacity    = conf.currentCapacity
        if len(conf.targets) == 0:
            lastTarget = 0
        else:
            lastTarget = conf.targets[-1]
        
        newFinish   = -1
        success     = False
        
        # capacity constraints
        newCapacity = capacity + self.targetDemand[targetId]
        if newCapacity > self.capacity:
            return (success,newFinish,newCapacity)
        
        # time window constraints
        arrivalTime = finishTime + self.getDistance(lastTarget, targetId)
        windowStart = self.targetsWindows[targetId][0]
        windowEnd   = self.targetsWindows[targetId][1]
        if arrivalTime > windowEnd:
            return (success,newFinish,newCapacity)
        waitingTime = max(0,windowStart - arrivalTime)
        newFinish   = arrivalTime + self.targetDurations[targetId] + waitingTime
        success     = True
        return (success,newFinish,newCapacity)
        
    def getDistance(self,t1,t2):
        (x1,y1) = self.targetLocations[t1]
        (x2,y2) = self.targetLocations[t2]
        return sqrt( math.pow(x1 - x2,2) + math.pow(y1 - y2,2) )
    
    def trimConfs(self,confs,trimParam, removeDups = False):
#         return confs
        sortedConfs=sorted(confs, key=lambda conf: conf.val)
        outputConfs = sortedConfs[0:trimParam]
        if removeDups:
            targets2ConfId = {}
            indexInSortedConfs = trimParam
            indexInOutputConfs = 0 
            nUniqueConfs = 0
            # remove dups from output confs - and add more confs if possible
#             while nUniqueConfs < trimParam:
#                 if
        return outputConfs 
    
    def bfsConfBuilder(self, lastLevelConfs):
        newConfs = []
        for currConf in lastLevelConfs: #need to check the first empty conf
            # hnadle 1st target 
            if len(currConf.targets) == 0:
                lastTarget = 0
            else:
                lastTarget = currConf.targets[-1]
            lastDistanceTravelled = self.getDistance(lastTarget,0)
            for targetId in range(1,self.nTargets):
                if targetId in currConf.targets:
                    continue
                (success, newFinishTime,newCapacity) = self.checkFeasible(currConf,targetId)
                if not success:
                    if ((currConf.targets == [5, 3, 7, 8, 10, 11, 9]) and (targetId == 6)):
                        print "here"
                    continue
                newConfTargets  = currConf.targets + [targetId]
                newConfVal      = currConf.val - lastDistanceTravelled + self.getDistance(targetId,0) + self.getDistance(lastTarget, targetId) 
                newConf         = conf(newConfTargets, self, newConfVal, newFinishTime, newCapacity)
                newConfs.append(newConf)
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
        return (val,finishTime,currentDemand)
    
    def printConfTimes(self):
        prevTarget = 0
        currTime   = 0
        for target in self.targets:
            timeToTravel     = (self.VRPobject.getDistance(prevTarget,target) / self.VRPobject.speed)
            timeToService    = self.VRPobject.targetDurations[target]
            earlyArrival     = timeToTravel + currTime 
            windowStart      = self.VRPobject.targetsWindows[target][0]
            waitingTime      = max(0,windowStart - earlyArrival)
            print target, "starting at", currTime + timeToTravel + waitingTime, "window is", self.VRPobject.targetsWindows[target]
            currTime        += timeToTravel + waitingTime + timeToService 
            prevTarget       = target
                  
        
    