def saveListAsJson(data, outputfile):
    with open(outputfile, 'w') as outfile:
        outfile.write("[\n")
        outfile.write(",".join(data))
        outfile.write("]\n")

def save(torrentData, outputFile):
    jsonTorrentsList = []
    for torrent in torrentData:
        jsonTorrentsList.append(torrent.toJSON())
    saveListAsJson(jsonTorrentsList, outputFile)