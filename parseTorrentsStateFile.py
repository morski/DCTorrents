import torrentData

def parse(inputFileName, saveUrl):
    with open(inputFileName) as stateFile:  
        line = stateFile.readline()
        torrents = []
        hash, name, path = False, False, False
        torrentDataObject = torrentData.TorrentData()
        while line:
            if hash:
                torrentDataObject.hash = line[2:-2]
                hash = False
            if name:
                torrentDataObject.name = line[2:-2]
                name = False
            if path:
                torrentDataObject.path = line[2:-2]
                path = False

            if "http" in line.strip() and saveUrl:
                torrentDataObject.url = line[2:-2]
            if line.strip() == "asg18":
                name = True
            if line.strip() == "sg25":
                hash = True
            if line.strip() == "sg21":
                path = True

            if (torrentDataObject.url != "" or not saveUrl) and torrentDataObject.name != "" and torrentDataObject.path != "" and torrentDataObject.hash != "":
                torrents.append(torrentDataObject)
                torrentDataObject = torrentData.TorrentData()
            line = stateFile.readline()
        return torrents