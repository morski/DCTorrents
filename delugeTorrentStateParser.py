import json
import sys, getopt

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

def main(argv):
    inputFileName = 'torrents.state'
    outputFileName = 'torrents.json'

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFileName = arg
        elif opt in ("-o", "--ofile"):
            outputFileName = arg

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

    saveTorrentDataToJson(torrents, outputFileName)

if __name__ == "__main__":
   main(sys.argv[1:])