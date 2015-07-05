import utils
import os
import sys

dbg = True
if not dbg:
    optiosHnadler   = utils.optionsHandler(sys.argv)
    (runParam,buildParam,solomonLib,timeout) = optiosHnadler.parseOptions()
    dirName = "solomon_" + str(solomonLib)
else:
    dirName = "solomon_" + str(25)
    f = "RC202.txt"
    runParam,buildParam,timeout = 1000,1000,50000
runner          = utils.vrpRunner('solomon')
filePrinter     = utils.filePrinter()
bestsol         = utils.bestSols()
headers         = ["fileName","buildParam","runParam","maxConfSize","confBuildTime","solverTime","opt_n_trucks","opt_distance","nTrucks","totalDistance","isOpt"]
dirNames2sols   = {"solomon_25":bestsol.all25Data,"solomon_50":bestsol.all50Data,"solomon_100":bestsol.all100Data}
dirNames        = dirNames2sols.keys()
dataDir         = "../data/"
maxConfSize     = 50

if dbg:
    res = runner.generateAndSolveInstance(dataDir + dirName + "/" + f, buildParam, runParam, maxConfSize,timeout)
    sys.exit()
allFiles = []
for f in os.listdir(dataDir + dirName):
    if f.endswith(".txt"):
        allFiles.append(f)
outputFileName = "res_" + dirName + ".csv"
allRes = []
for f in allFiles:
    res = runner.generateAndSolveInstance(dataDir + dirName + "/" + f, buildParam, runParam, maxConfSize,timeout)
    solKey = f[:-4]
    if solKey in dirNames2sols[dirName]:
        res["opt_n_trucks"] = dirNames2sols[dirName][solKey][0]
        res["opt_distance"] = dirNames2sols[dirName][solKey][1]
    else:
        res["opt_n_trucks"] = "n/a"
        res["opt_distance"] = "n/a"
    allRes.append(res)
filePrinter.printRes(allRes, outputFileName,headers)
