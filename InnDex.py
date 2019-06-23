import os
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
def outputJSON(fname,  list):    
    import json
    header={'fname':fname,  'type':'list'}
    fileContainerData={'header':header,  'data':list}
    with open(fname, 'w') as outfile:
        json.dump(fileContainerData, outfile, ensure_ascii=False, indent=2)

def inputJSON(fname):    
    import json
    with open(fname, 'r') as f:
        fileContainerData = json.load(f)
    header= fileContainerData['header']
    list=fileContainerData['data']
    return list

def getListOfFiles(dirName):
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
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            # create tuple for list
            md5sum= md5( fullPath )
            tuple= {"fname":entry,  "dname":dirName, "md5":md5sum,  "fullpath":fullPath}
            # add to list
            allFiles.append(tuple)
            # debug
            print(tuple)
                
    return allFiles

def findTuple(allFiles,  tuple):
    for entry in allFiles:
        if (entry["md5"] == tuple["md5"]):
            if entry["fullpath"] != tuple["fullpath"]:
                return entry
    
    return 0
    
def findDuplicates(allFiles):
    
    pairs=list()
    count=0
    for tuple in allFiles:
        res= findTuple( allFiles,  tuple )
        if res==0:
            print("nothing")
        else:
            count += 1
            singlePair={"src":tuple,  "dst":res}
            pairs.append(singlePair)
            print("found:")
            print(tuple)
            print(res)
            
    outputJSON('pairs.JSON',  pairs)
    print("count:")
    print(count)
    
dirName = '/home/tswaehn/Downloads';

print("hello")

allFiles= getListOfFiles( dirName )
# write list to file
outputJSON('allFiles.JSON',  allFiles)
# read list from file
allFiles= inputJSON('allFiles.JSON')

print("listing done")    

findDuplicates( allFiles )

    
print("app end")
