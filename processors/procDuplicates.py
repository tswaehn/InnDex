import os
from tools import my_json


def __findSameTupleByMd5(allFiles,  tuple):
    for hashKey in allFiles:
        entry= allFiles[hashKey]
        if (entry["md5"] == tuple["md5"]):
            if entry['rname'] != tuple['rname']:
                return entry
    
    return 0
    
def __findSameTupleByNameAndDate(allFiles,  tuple):
    for hashKey in allFiles:
        entry= allFiles[hashKey]
        if (entry["fname"] == tuple["fname"]):
            if entry["fsize"] == tuple["fsize"]:
                if entry["rname"] != tuple["rname"]:
                    return entry
    
    return 0



#
#   map file content md5sum (key) to filename hash (value)
#
def __createMd5KeyTable( allFiles ):    
    
    md5KeyTable= dict()
    
    for hashKey in allFiles:
        entry= allFiles[hashKey]
        md5Key= entry['md5']
        if md5Key in md5KeyTable:
            md5KeyTable[md5Key].append(  hashKey )
        else:
            md5KeyTable[md5Key]= list()
            md5KeyTable[md5Key].append( hashKey )
    
    return md5KeyTable
    
def run( dirName,  innDex ):
    fname = 'indexDuplicates.JSON'
    fullpath=os.path.join(dirName, fname)
    
    allFiles= innDex['data']
    
    md5KeyTable= __createMd5KeyTable( allFiles)
    print(md5KeyTable)
    
    count= 0
    size= 0
    duplicates= dict()
    for md5Key in md5KeyTable:
        if len(md5KeyTable[md5Key]) > 1:
            count += 1
            duplicates[md5Key]= list()
            for hashKey in md5KeyTable[md5Key]:
                entry= allFiles[hashKey]
                duplicates[md5Key].append( entry )
                fsize= entry['fsize']
                size += fsize
            
            size -= fsize
                
            print ("found duplicate")
            print (md5KeyTable[md5Key])
    
            
    my_json.write(fullpath, duplicates)
    print("count:")
    print(count)
    print("lost size:")
    print(size/1024/1024)
