import sys
import os
import hashlib
import indexReadWrite
import time
import glob

# const
__FNAME= "index.JSON"

def __md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096000000), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    

def __createIndexOfDirectory(rootDir,  dirName,  totalSize):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # check for links
        if os.path.islink(fullPath):
            print("skipping symlink " + fullPath)
            continue
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + __createIndexOfDirectory(rootDir,  fullPath,  totalSize)
        else:
            # create tuple for list
            relpath=os.path.relpath(fullPath,  rootDir)
            #md5sum= __md5( fullPath )
            md5sum= 0
            lastModTimeStamp= os.path.getmtime(fullPath)
            st = os.stat(fullPath)
            fsize= st.st_size
            tuple= {"fname":entry, "fsize":fsize,  "lastmod":lastModTimeStamp, "md5":md5sum,  "rootname":rootDir,  "rname":relpath }
            # add to list
            allFiles.append( tuple )
            # debug
            totalSize +=fsize
            sys.stdout.write('.')
            print("\rfound "+str(len(allFiles))+ " files",  end="\r")
            ##print(tuple)

    if (dirName == rootDir):
        print("\r\n")
    return allFiles

   
def __getIndexFileList( dirName ):    
    fileList= list()
    time.time()
    return fileList


def __getLatestIndexFile( dirName,  fname ):
    fullpath=os.path.join(dirName, fname)
    listOfFiles = glob.glob(fullpath + '.*')
    x= 0
    b = 0
    for entry in listOfFiles:
        print (entry)
        if x==0:
            x= entry
            b= os.path.getmtime(entry)
            continue
        # lastModTimeStamp
        a= os.path.getmtime(entry)
        if (a > b):
            b= a
            x= entry
    
    fname= os.path.basename( x )
    print("loading file")
    print(fname)
    return fname
    
    
def new( dirName ):   
    # get timestamp
    ts= time.time()
    timstampStr= str( int( ts ) )
    
    # create filename
    fname = __FNAME + "." +timstampStr
    fullpath=os.path.join(dirName, fname)
    
    # create index of files
    allFiles= __createIndexOfDirectory( dirName,  dirName,  0 )
    
    # prepare innDex object 
    header={'fname':fname,  'type':'list',  'listlen': len( allFiles ),  'version':'0.1',  'timestamp':ts}
    innDex={'header':header,  'data':allFiles}

    # write list to file
    indexReadWrite.write(fullpath,  innDex)
    
    return innDex
    
    

def load( dirName  ):    
    fname= __getLatestIndexFile( dirName,  __FNAME )
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
