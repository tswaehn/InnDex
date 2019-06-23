import os
import createIndex
import indexReadWrite

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
            
    indexReadWrite.write(fullpath,  pairs)
    print("count:")
    print(count)



print("start app")

dirName = '/home/tswaehn/Downloads'
##dirName= '/run/media/tswaehn/My Passport/data/backup_data/data';
##dirName= '/run/media/tswaehn/c587a5e7-5b5a-4c0c-857d-ba4cc1872b47/data/';

##innDex= createIndex.new(dirName)

innDex= createIndex.load(dirName)

print("listing done")    

execFindDuplicates( dirName,  innDex )

    
print("app end")
