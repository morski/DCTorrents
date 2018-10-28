import json

class TorrentData(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    name = ""
    hash = ""
    path = ""
    url = ""