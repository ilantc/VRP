import VRP

reader = VRP.solomonFileReader()

fileName = "../data/solomon_25/C101.txt"

data = reader.readFile(fileName)

print data