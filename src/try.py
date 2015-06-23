import VRP
import readers
from gurobiHandler import vrpSolver
from VRP import conf
import itertools

reader = readers.solomonFileReader()

fileName = "../data/solomon_25/C101.txt"
data = reader.readFile(fileName)
vrp = VRP.VRP(data["nTrucks"], data["capacity"], data["targets"])

confs = vrp.bfsConfBuilderWrapper(80000,80000, 15)
# 
s = vrpSolver(confs, vrp)
s.buildIP()
s.solve()
# targets = [5, 3, 7, 8, 10, 11, 9, 6, 4, 2, 1]
# for i in range(len(targets) + 1):
#     c = conf(targets[:i],vrp)
    # c.printConfTimes()
#     print "generated conf",c.targets,"=",len(filter(lambda con: con.targets == c.targets,confs))

# g = itertools.permutations([3,4,5,6,7,8,9,10,11])
# bestVal = 10000
# bestC = None
# for p in g:
#     c = conf(list(p) + [2,1], vrp)
#     print c.val,";",c.finishTime,";",c.targets
#     if c.val < bestVal:
#         bestVal = c.val
#         bestC = c
# print "best val is", bestVal,"best finish time",bestC.finishTime ,"best C is",bestC.targets
        

# targets = [[13,17,18,19,15,16,14,12],\
#            [43,42,41,40,44,46,45,48,51,50,52,49,47],\
#            [90,87,86,83,82,84,85,88,89,91],\
#            [67,65,63,62,74,72,61,64,68,66,69],\
#            [98,96,95,94,92,93,97,100,99],\
#            [5,3,7,8,10,11,9,6,4,2,1,75],\
#            [20,24,25,27,29,30,28,26,23,22,21],\
#            [81,78,76,71,70,73,77,79,80],\
#            [57,55,54,53,56,58,60,59],\
#            [32,33,31,35,37,38,39,36,34,0]]
# confs = []
# for t in targets:
#     con = conf(t, vrp)
#     confs.append(con)
#     
# print 1
