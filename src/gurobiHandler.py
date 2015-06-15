import gurobipy
import gurobipy.GRB as GRB

class vrpSolver():
    
    def __init__(self, confs, VRPobject):
        indices = {}
        for i in range(1,VRPobject.nTargets):
            indices[i] = []
        cId = 0
        f = lambda t: indices[t].append[cId]
        for c in confs:
            map(f, c.targets)
            cId += 1 
        
        self.confs = confs
        self.indices = indices
        self.VRPobj = VRPobject
        self.M      = 10000 
            
    def buildIP(self):
        model = gurobipy.Model('VRPModel')
        
        # variables
        x = {}
        for i in range(len(self.confs)):
            x[i] = model.addVar(vtype=GRB.BINARY, name=str(i))
        model.update()

        # constraints
        for targetId in self.indices:
            model.addConstr(gurobipy.quicksum(x[i] for i in self.indices[targetId]) == 1,'target_%s' % (i))
        
        # objective
        model.setObjective(gurobipy.quicksum(x[i]*(self.confs[i].val + self.M) for i in range(len(self.confs))))
        model.setAttr("modelSense", GRB.MINIMIZE)
        model.update()
        
        model.get
        self.x = x
        self.model = model
    
    def solve(self):
        # Compute optimal solution
        self.model.optimize()
        if self.model.status == GRB.status.OPTIMAL:
            for i in range(len(self.confs)):
                if self.x[i].x > 0:
                    print "conf", i, "was chosen"
            print "\nopt val is", self.model.getAttr("ObjVal")