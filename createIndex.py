import os
import hashlib
import indexReadWrite

def __md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    

def __createIndexOfDirectory(rootDir,  dirName):
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
            allFiles = allFiles + __createIndexOfDirectory(rootDir,  fullPath)
        else:
            # create tuple for list
            relpath=os.path.relpath(fullPath,  rootDir)
            md5sum= __md5( fullPath )
            lastModTimeStamp= os.path.getmtime(fullPath)
            st = os.stat(fullPath)
            fsize= st.st_size
            tuple= {"fname":entry, "fsize":fsize,  "lastmod":lastModTimeStamp, "md5":md5sum,  "rootname":rootDir,  "rname":relpath }
            # add to list
            allFiles.append( tuple )
            # debug
            print(tuple)
                
    return allFiles
    
    

def new( dirName ):   
    fname = 'index.JSON'
    fullpath=os.path.join(dirName, fname)
    
    
    # create index of files
    allFiles= __createIndexOfDirectory( dirName,  dirName )
    
    # prepare innDex object 
    import time
    ts = time.time()
    header={'fname':fname,  'type':'list',  'listlen': len( allFiles ),  'version':'0.1',  'timestamp':ts}
    innDex={'header':header,  'data':allFiles}

    # write list to file
    indexReadWrite.write(fullpath,  innDex)
    
    return innDex
    
    

def load( dirName  ):    
    fname = 'index.JSON'
    fullpath=os.path.join(dirName, fname)
    
    # read list from file
    innDex= indexReadWrite.read(fullpath)
    
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
