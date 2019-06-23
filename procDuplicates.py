import os
import indexReadWrite

def __findSameTupleByMd5(allFiles,  tuple):
    for entry in allFiles:
        if (entry["md5"] == tuple["md5"]):
            if entry['fname'] != tuple['fname']:
                if entry["rname"] == tuple["rname"]:
                    # ignore same file
                    continue
            else:
                return entry
    
    return 0
    
def __findSameTupleByNameAndDate(allFiles,  tuple):
    for entry in allFiles:
        if (entry["fname"] == tuple["fname"]):
            if entry["fsize"] == tuple["fsize"]:
                if entry["rname"] != tuple["rname"]:
                    return entry
    
    return 0

    
def run( dirName,  innDex ):
    fname = 'indexDuplicates.JSON'
    fullpath=os.path.join(dirName, fname)
    
    allFiles= innDex['data']
    pairs=list()
    count=0
    for tuple in allFiles:
        ##res= __findSameTupleByMd5( innDex,  tuple )
        res= __findSameTupleByNameAndDate( allFiles,  tuple)
        if res==0:
            continue
        else:
            count += 1
            singlePair={"src":tuple,  "dst":res}
            pairs.append(singlePair)
            print("found:")
            print(tuple)
            print(res)
            
    indexReadWrite.write(fullpath,  pairs)
    print("count:")
    print(count)
