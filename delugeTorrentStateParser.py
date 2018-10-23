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


def saveTorrentDataToJson(torrentData, outputFile):
    outputFile = sys.argv
    with open('torrents.json', 'w') as outfile:
        outfile.write("[\n")
        jsonTorrentsList = []
        for torrent in torrentData:
            jsonTorrentsList.append(torrent.toJSON())
            outfile.write(torrent.toJSON() + ",\n")
    	outfile.write(",".join(jsonTorrentsList))
        outfile.write("]\n")

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

def compareStateJsonFiles(fileA, fileB):
    with open(fileA,'r') as f1, open(fileB,'r') as f2:
        diff = difflib.ndiff(f1.readlines(), f2.readlines())    
        for line in diff:
            if line.startswith('-') or line.startswith('+'):
                if "hash" in line:
                    pos = line.find(":")
                    hash = line[pos+3:-4]
                    print(hash)

def main(argv):
    inputFileName = []
    inputFileName.append('torrents.state')
    outputFileName = []
    outputFileName.append('torrents.json')
    
    parseMode = True
    compareMode = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:c",["ifile=","ofile=","comparemode"])
        print(args)
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile> -c (comparemode)'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFileName.append(arg)
        elif opt in ("-o", "--ofile"):
            outputFileName.append(arg)
        elif opt in ("-c", "--comparemode"):
            compareMode = True
            parseMode = False

    if parseMode:
        torrents = parseTorrentStateFile(inputFileName[1] if len(inputFileName) > 1 else inputFileName[0])
        saveTorrentDataToJson(torrents, outputFileName[1] if len(outputFileName) > 1 else outputFileName[0])
    
    if compareMode:
        print(len(inputFileName))
        if len(inputFileName) < 3:
            print("Filenames missing. Use two -i to define json files")
            sys.exit(2)
        compareStateJsonFiles(inputFileName[1], inputFileName[2])

if __name__ == "__main__":
   main(sys.argv[1:])