import json
import sys, getopt
import difflib

class TorrentData(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    name = ""
    hash = ""
    path = ""
    url = ""

def saveJsonToFile(jsonData, outputfile):
    with open(outputfile, 'w') as outfile:
        json.dump(jsonData, outfile)

def saveListAsJson(data, outputfile):
    with open(outputfile, 'w') as outfile:
        outfile.write("[\n")
        outfile.write(",".join(data))
        outfile.write("]\n")

def saveTorrentDataToJson(torrentData, outputFile):
    jsonTorrentsList = []
    for torrent in torrentData:
        jsonTorrentsList.append(torrent.toJSON())
    saveListAsJson(jsonTorrentsList, outputFile)

def parseTorrentStateFile(inputFileName):
    with open(inputFileName) as stateFile:  
        line = stateFile.readline()
        torrents = []
        hash, name, path = False, False, False
        torrentData = TorrentData()
        while line:
            if hash:
                torrentData.hash = line[2:-2]
                hash = False
            if name:
                torrentData.name = line[2:-2]
                name = False
            if path:
                torrentData.path = line[2:-2]
                path = False


            if "http" in line.strip():
                torrentData.url = line[2:-2] + " - "
            if line.strip() == "asg18":
                name = True
            if line.strip() == "sg25":
                hash = True
            if line.strip() == "sg21":
                path = True

            if torrentData.url != "" and torrentData.name != "" and torrentData.path != "" and torrentData.hash != "":
                torrents.append(torrentData)
                torrentData = TorrentData()
            line = stateFile.readline()
        return torrents

def getSetCommon(setA, setB):
    return set(setA) & set(setB)

def getSetDifference(setA, setB):
    uniq = []
    uniq.append(set(setA) - set(setB))
    uniq.append(set(setB) - set(setA))
    return uniq

def compareStateJsonFiles(fileA, fileB, outpuname, duplicate):
    with open(fileA,'r') as fa, open(fileB,'r') as fb:
        jsonA = json.load(fa)
        jsonB = json.load(fb)
        print(len(jsonA))
        print(len(jsonB))
        jsonAhashes = list(map(lambda x: x["hash"], jsonA))
        jsonBhashes = list(map(lambda x: x["hash"], jsonB))
        unique = getSetDifference(jsonAhashes, jsonBhashes)
        uniqueAJsons = list(filter(lambda x: x["hash"] in unique[0], jsonA))
        uniqueBJsons = list(filter(lambda x: x["hash"] in unique[1], jsonB))
        print(len(uniqueAJsons))
        print(len(uniqueBJsons))
        saveJsonToFile(uniqueAJsons, fileA[:-5]+"_unique.json")
        saveJsonToFile(uniqueBJsons, fileB[:-5]+"_unique.json")
        if duplicate:
            common = getSetCommon(jsonAhashes, jsonBhashes)
            commonJsons = list(filter(lambda x: x["hash"] in common, jsonA))
            print(len(commonJsons))
            saveJsonToFile(commonJsons, fileA[:-5]+"_duplicates.json")

def main(argv):
    inputFileName = []
    inputFileName.append('torrents.state')
    outputFileName = []
    outputFileName.append('torrents.json')
    
    duplicate = False
    parseMode = True
    compareMode = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:cd",["help","ifile=","ofile=","comparemode","duplicate"])
    except getopt.GetoptError:
        print('test.py -h for more info')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print( '-i <inputfile>, --ifile <inputfile> (torrents.state file for normal use - when compare mode is active specify 2 -i <inputfile> for JSONs to compare)')
            print('-o <outputfile>, --ofile <outputfilename> (filename that JSON data i saved to)')
            print( '-c, --comparemode (Compares 2 JSONS files and difference result is saved into new file. Use -d, --duplicate if you want to also save file with duplicates)')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFileName.append(arg)
        elif opt in ("-o", "--ofile"):
            outputFileName.append(arg)
        elif opt in ("-c", "--comparemode"): 
            compareMode = True
            parseMode = False
        elif opt in ("-d", "--duplicate"):
            duplicate = True

    if parseMode:
        torrents = parseTorrentStateFile(inputFileName[1] if len(inputFileName) > 1 else inputFileName[0])
        saveTorrentDataToJson(torrents, outputFileName[1] if len(outputFileName) > 1 else outputFileName[0])
    
    if compareMode:
        if len(inputFileName) < 3:
            print("Filenames missing. Use two -i to define json files")
            sys.exit(2)
        compareStateJsonFiles(inputFileName[1], inputFileName[2], outputFileName[1] if len(outputFileName) > 1 else outputFileName[0], duplicate)

if __name__ == "__main__":
   main(sys.argv[1:])