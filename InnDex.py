import os
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
def writeListToJSON(fname,  obj):    
    import json
    basename= os.path.basename( fname )
    # actually write to file
    with open(fname, 'w') as outfile:
        json.dump(obj, outfile, ensure_ascii=False, indent=2)

def readListFromJSON(fname):    
    import json
    # read from file
    with open(fname, 'r') as f:
        obj = json.load(f)
        
    # return data from JSON if header is ok
    return obj

def createIndexOfDirectory(rootDir,  dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + createIndexOfDirectory(rootDir,  fullPath)
        else:
            # create tuple for list
            relpath=os.path.relpath(fullPath,  rootDir)
            md5sum= md5( fullPath )
            lastModTimeStamp= os.path.getmtime(fullPath)
            st = os.stat(fullPath)
            fsize= st.st_size
            tuple= {"fname":entry, "fsize":fsize,  "lastmod":lastModTimeStamp, "md5":md5sum,  "rootname":rootDir,  "rname":relpath }
            # add to list
            allFiles.append( tuple )
            # debug
            print(tuple)
                
    return allFiles

def findSameTupleByMd5(allFiles,  tuple):
    for entry in allFiles:
        if (entry["md5"] == tuple["md5"]):
            if entry['fname'] != tuple['fname']:
                if entry["rname"] == tuple["rname"]:
                    # ignore same file
                    continue
            else:
                return entry
    
    return 0
    
def findSameTupleByNameAndDate(allFiles,  tuple):
    for entry in allFiles:
        if (entry["fname"] == tuple["fname"]):
            if entry["fsize"] == tuple["fsize"]:
                if entry["rname"] != tuple["rname"]:
                    return entry
    
    return 0

    
def execFindDuplicates( dirName,  innDex ):
    fname = 'indexDuplicates.JSON'
    fullpath=os.path.join(dirName, fname)
    
    allFiles= innDex['data']
    pairs=list()
    count=0
    for tuple in allFiles:
        ##res= findSameTupleByMd5( innDex,  tuple )
        res= findSameTupleByNameAndDate( allFiles,  tuple)
        if res==0:
            continue
        else:
            count += 1
            singlePair={"src":tuple,  "dst":res}
            pairs.append(singlePair)
            print("found:")
            print(tuple)
            print(res)
            
    writeListToJSON(fullpath,  pairs)
    print("count:")
    print(count)

def execNewIndex( dirName ):   
    fname = 'index.JSON'
    fullpath=os.path.join(dirName, fname)
    
    
    # create index of files
    allFiles= createIndexOfDirectory( dirName,  dirName )
    
    # prepare innDex object 
    import time
    ts = time.time()
    header={'fname':fname,  'type':'list',  'listlen': len( allFiles ),  'version':'0.1',  'timestamp':ts}
    innDex={'header':header,  'data':allFiles}

    # write list to file
    writeListToJSON(fullpath,  innDex)
    
    return innDex

def execLoadIndex( dirName  ):    
    fname = 'index.JSON'
    fullpath=os.path.join(dirName, fname)
    
    # read list from file
    innDex= readListFromJSON(fullpath)
    
    # set header and data
    header= innDex['header'];
    data=innDex['data'];
    
   # check header and return empty list if header is invalids
    if (header['fname'] != fname):
        print("incorrect filename")
        return set()
    if (header['listlen'] != len( data ) ):
        print("incorrect data length")
        return set()
    if (header['version'] != '0.1'):
        print("incorrect version "+ header['version'])
        return set()
    
    return innDex


print("start app")

dirName = '/home/tswaehn/Downloads'
dirName= '/run/media/tswaehn/My Passport/data/backup_data/data';

dirName= '/run/media/tswaehn/c587a5e7-5b5a-4c0c-857d-ba4cc1872b47/data/';

innDex= execNewIndex(dirName)

innDex= execLoadIndex(dirName)

print("listing done")    

##execFindDuplicates( dirName,  innDex )

    
print("app end")
