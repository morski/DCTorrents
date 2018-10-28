def getUniqueUrls(torrentData):
    urls = set(list(map(lambda x: x.url, torrentData)))
    with open("announce.txt", 'w') as outfile:
        outfile.write(";".join(urls))