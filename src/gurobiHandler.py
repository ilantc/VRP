import gurobipy

class vrpSolver():
    
    def __init__(self, confs, VRPobject,timeout):
        indices = {}
        for i in range(1,VRPobject.nTargets):
            indices[i] = []
        cId = 0
#         f = lambda t: indices[t].append[cId]
        for c in confs:
            map(lambda t: indices[t].append(cId), c.targets)
            cId += 1 
        
        self.confs = confs
        self.indices = indices
        self.VRPobj = VRPobject
        self.M      = 1000 
        self.timeout = timeout
            
    def buildIP(self, setNumTrucks = None):
        model = gurobipy.Model('VRPModel')
        
        # variables
        x = {}
        for i in range(len(self.confs)):
            x[i] = model.addVar(vtype=gurobipy.GRB.BINARY, name=str(i))
        model.update()

        # constraints
        for targetId in self.indices:
            model.addConstr(gurobipy.quicksum(x[i] for i in self.indices[targetId]) >= 1,'target_%s' % (i))
        
        if setNumTrucks:    
            model.addConstr(gurobipy.quicksum(x[i] for i in range(len(self.confs))) <= setNumTrucks,'at_most_%i_confs' % (setNumTrucks))
        
        # objective
        if setNumTrucks:
            model.setObjective(gurobipy.quicksum(x[i]*(self.confs[i].val) for i in range(len(self.confs))))
        else:
            model.setObjective(gurobipy.quicksum(x[i]*(self.confs[i].val + self.M) for i in range(len(self.confs))))
        model.setAttr("modelSense", gurobipy.GRB.MINIMIZE)
        model.setParam('TimeLimit', self.timeout)
        model.update()
        
        self.x = x
        self.model = model
    
    def solve(self):
        # Compute optimal solution
        self.model.setParam('OutputFlag', False )
        self.model.optimize()
        chosenConfs = []
        exitOnTimeOut = False
        print "status =",self.model.status,"(",gurobipy.GRB.status.OPTIMAL,"=opt,",gurobipy.GRB.status.INFEASIBLE,"=inf,",gurobipy.GRB.status.TIME_LIMIT,"=timout)"
        if self.model.status == gurobipy.GRB.status.INFEASIBLE:
            return [-1,-1,-1]
        if self.model.status in [gurobipy.GRB.status.OPTIMAL,gurobipy.GRB.status.TIME_LIMIT]:
            if self.model.status == gurobipy.GRB.status.TIME_LIMIT:
                exitOnTimeOut = True
            for i in range(len(self.confs)):
                if self.x[i].x > 0:
                    print "conf", i, "was chosen"
                    chosenConfs.append(i)
            print "\nopt val is", self.model.getAttr("ObjVal")
        confsWithShortcuts = self.VRPobj.performShortcuts(map(lambda c: self.confs[c],chosenConfs))
        totalDist = 0.0
        for con in confsWithShortcuts:
            totalDist += con.val
            print con.targets
        print "\nnVehicels =",len(confsWithShortcuts), "total distance =",totalDist
        return [len(confsWithShortcuts),totalDist,exitOnTimeOut]
