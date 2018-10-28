import json
import os
import shutil
import parseTorrentsStateFile
import saveTorrentDataToJson

def copyTorrentFilesToLocalDirectory(torrentHashes, src, dest):
    src_files = os.listdir(src)
    print("Filed found in " + src +": " + len(src_files))
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        print(full_file_name)
        print(os.path.isfile(full_file_name))
        print(full_file_name[-8:] == ".torrent")
        print(any(full_file_name[:-8] in s for s in torrentHashes))
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