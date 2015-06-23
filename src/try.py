import VRP
import readers
from gurobiHandler import vrpSolver
from VRP import conf

reader = readers.solomonFileReader()

fileName = "../data/solomon_25/C104.txt"
data = reader.readFile(fileName)
vrp = VRP.VRP(data["nTrucks"], data["capacity"], data["targets"])

confs = vrp.bfsConfBuilderWrapper(25000,2500, 15)

s = vrpSolver(confs, vrp)
s.buildIP()
s.solve()

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
