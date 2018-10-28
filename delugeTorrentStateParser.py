import json
import sys, getopt
import difflib
from .parseTorrentsStateFile import parse
from .compareStateJsonFiles import compare
from .getUrlsFromJson import getUniqueUrls
from .saveTorrentDataToJson import save









def main(argv):
    with open("settings.json",'r') as settingsJson:
        settings = json.load(settingsJson)



    inputFileName = []
    inputFileName.append('torrents.state')
    outputFileName = []
    outputFileName.append('torrents.json')
    
    saveUrl = False
    duplicate = False
    parseMode = True
    compareMode = False
    announceMode = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:cdua",["help","ifile=","ofile=","comparemode","duplicate","url","announce"])
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
            announceMode = False
        elif opt in ("-d", "--duplicate"):
            duplicate = True
        elif opt in ("-u","--url"):
            saveUrl = True
        elif opt in ("-a", "--announce"):
            announceMode = True
            compareMode = False
            parseMode = False

    if parseMode:
        torrents = parse(inputFileName[1] if len(inputFileName) > 1 else inputFileName[0], saveUrl)
        save(torrents, outputFileName[1] if len(outputFileName) > 1 else outputFileName[0])
    
    if compareMode:
        if len(inputFileName) < 3:
            print("Filenames missing. Use two -i to define json files")
            sys.exit(2)
        compare(inputFileName[1], inputFileName[2], outputFileName[1] if len(outputFileName) > 1 else outputFileName[0], duplicate)

    if announceMode:
        torrents = parse(inputFileName[1] if len(inputFileName) > 1 else inputFileName[0], True)
        getUniqueUrls(torrents)

if __name__ == "__main__":
   main(sys.argv[1:])