import json

def saveJsonToFile(jsonData, outputfile):
    with open(outputfile, 'w') as outfile:
        json.dump(jsonData, outfile)

def getSetCommon(setA, setB):
    return set(setA) & set(setB)

def getSetDifference(setA, setB):
    uniq = []
    uniq.append(set(setA) - set(setB))
    uniq.append(set(setB) - set(setA))
    return uniq

def compare(fileA, fileB, outpuname, duplicate):
    with open(fileA,'r') as fa, open(fileB,'r') as fb:
        jsonA = json.load(fa)
        jsonB = json.load(fb)
        jsonAhashes = list(map(lambda x: x["hash"], jsonA))
        jsonBhashes = list(map(lambda x: x["hash"], jsonB))
        unique = getSetDifference(jsonAhashes, jsonBhashes)
        uniqueAJsons = list(filter(lambda x: x["hash"] in unique[0], jsonA))
        uniqueBJsons = list(filter(lambda x: x["hash"] in unique[1], jsonB))
        saveJsonToFile(uniqueAJsons, fileA[:-5]+"_unique.json")
        saveJsonToFile(uniqueBJsons, fileB[:-5]+"_unique.json")
        if duplicate:
            common = getSetCommon(jsonAhashes, jsonBhashes)
            commonJsons = list(filter(lambda x: x["hash"] in common, jsonA))
            saveJsonToFile(commonJsons, fileA[:-5]+"_duplicates.json")