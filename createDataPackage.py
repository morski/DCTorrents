import json
import os
import shutil
import parseTorrentsStateFile
import saveTorrentDataToJson

def copyTorrentFilesToLocalDirectory(torrentHashes, src, dest):
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name) and full_file_name[-8:] == ".torrent" and any(full_file_name[:-8] in s for s in torrentHashes)):
            shutil.copy(full_file_name, dest)

def main():
    with open("settings.json",'r') as settingsJson:
        settings = json.load(settingsJson)

        torrents = parseTorrentsStateFile.parse(settings["torrentsStateFolderPath"] + settings["torrentsStateFileName"], settings["addAnnounceUrlToOutputFile"])
        saveTorrentDataToJson.save(torrents, settings["outputFolder"] + settings["torrentsStateParsedFileName"])

        hashList = list(map(lambda x: x.hash, torrents))
        print(hashList)
        copyTorrentFilesToLocalDirectory(hashList, settings["torrentsStateFolderPath"], settings["outputFolder"])



if __name__ == "__main__":
   main()