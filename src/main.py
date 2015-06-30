import utils
import os

runner          = utils.vrpRunner('solomon')
filePrinter     = utils.filePrinter()
bestsol         = utils.bestSols()
dirNames2sols   = {"solomon_25":bestsol.all25Data,"solomon_50":bestsol.all50Data,"solomon_100":bestsol.all100Data}
dirNames        = dirNames2sols.keys()
dataDir         = "../data/"
maxConfSize     = 15
parameterSetups = [{"runParam": 1000, "buildParam": 1000},\
                   {"runParam": 5000, "buildParam": 5000},\
                   {"runParam": 10000,"buildParam": 10000},\
                   {"runParam": 15000,"buildParam": 15000}]
testRun = True
if testRun:
    dirNames = ["solomon_25","solomon_50"]
    parameterSetups = [{"runParam": 100, "buildParam": 100},{"runParam": 200, "buildParam": 200}]


for dirName in dirNames:
    allFiles = []
    for f in os.listdir(dataDir + dirName):
        if f.endswith(".txt"):
            allFiles.append(f)
    outputFileName = "res_" + dirName + ".csv"
    allRes = []
    for parameterSetup in parameterSetups:
        for f in allFiles:
            solKey = f[:-4]
            res = runner.generateAndSolveInstance(dataDir + dirName + "/" + f, parameterSetup["buildParam"], parameterSetup["runParam"], maxConfSize)
            allRes.append(res)
    filePrinter.printRes(allRes, outputFileName)
         
    