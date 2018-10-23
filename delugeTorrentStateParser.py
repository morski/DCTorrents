import json

class TorrentData(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    name = ""
    hash = ""
    path = ""
    url = ""


filepath = 'torrents.state.backup.22'  
with open(filepath) as fp:  
    line = fp.readline()
    cnt = 0
    torrents = []
    hash, name, path = False, False, False
    urlString, nameString, pathString, hashString = "", "", "", ""
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
        line = fp.readline()

    with open('torrents.json', 'w') as outfile:
        outfile.write("[\n")
        jsonTorrentsList = []
        for torrent in torrents:
            jsonTorrentsList.append(torrent.toJSON())
            outfile.write(torrent.toJSON() + ",\n")

        outfile.write("]\n")