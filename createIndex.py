import os
import hashlib
import indexReadWrite
import time
import glob

# const
__FNAME= "index.JSON"
__FVERS= "0.2"
__FINAL="final"
__PARTLY="partly"

def __md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4*1024*1024), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
def __getNameHash( relname ):
    hash_md5 = hashlib.md5()
    hash_md5.update(relname.encode('utf-8'))
    return hash_md5.hexdigest()

# global vars to generate the index -- \TODO: find a better way of doing that
__total_scan_size= 0
__total_files_list= dict()
__stat_start_time=0
__stat_scan_size=0
__backup_start_time=0

def __createIndexOfDirectory(rootDir,  dirName,  iname,  ts ):
    global __total_scan_size
    global __total_files_list
    global __stat_start_time
    global __stat_scan_size
    global __backup_start_time
    
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    
    if __stat_start_time == 0:
        __stat_start_time= time.time()
        
    if __backup_start_time == 0:
        __backup_start_time= time.time()
        
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
            # go to subfolders            
            __createIndexOfDirectory(rootDir,  fullPath, iname,  ts )
        else:
            # create tuple for list
            relpath=os.path.relpath(fullPath,  rootDir)
            lastModTimeStamp= os.path.getmtime(fullPath)
            st = os.stat(fullPath)
            fsize= st.st_size
            
            #
            dictHash= __getNameHash( relpath )
            
            # check if the same file already been indexed in the partly index
            sameEntry= __isSameFile( __total_files_list,  relpath,  fsize,  lastModTimeStamp  ) 
            if sameEntry== 0:
                # file is not yet present in index -- so add to index
                
                # creating the md5sum over the complete file is processing expensive
                md5sum= __md5( fullPath )
                # generate the tuple
                tuple= {"fname":entry, "fsize":fsize,  "lastmod":lastModTimeStamp, "md5":md5sum,  "rootname":rootDir,  "rname":relpath }
                # add to dict
                __total_files_list[dictHash]=  tuple 
                
            # store the current result as temporary result -- just in case something goes wrong, we can continue
            backupDeltaTime= time.time() - __backup_start_time
            if backupDeltaTime > 60:
                # reset timer
                __backup_start_time= time.time()
                # execute backup
                __writeIndexFile( rootDir,  iname, __total_files_list,  ts,  __PARTLY   )
                __writeIndexFile( rootDir,  iname, __total_files_list,  ts,  __PARTLY+".dual"   )
                print("automatic backup of index done")

            # stats
            __total_scan_size +=fsize
            __stat_scan_size += fsize
            
            # the write timer
            deltaTime= (time.time() - __stat_start_time)
            
            # on timer threshold
            if deltaTime > 1:
                # reset timer
                __stat_start_time= time.time()

                # debug output
                sizeInMb= __stat_scan_size/1024/1024
                throughPut= sizeInMb / deltaTime
                # reset byte counter
                __stat_scan_size= 0
                relname= os.path.relpath(dirName,  rootDir)
                debug= "[files: {f:5d},  size: {s:8.2f}MB {t:8.2f}MB/s] [{x:60}]".format(f= len(__total_files_list),  s= __total_scan_size/1024/1024,  t=throughPut,  x= relname)
                print("\r" + debug,  end="\r")


    if (dirName == rootDir):
        print("\r\n")
        
    return 

def __isSameFile( partList,  relpath,  fsize,  lastModTimeStamp  ):   
    if len(partList) == 0:
        return 0
        
    dictHash= __getNameHash( relpath )
    
    if dictHash in partList:
        sameFile= partList[dictHash]
        # check the details
        if (sameFile['fsize'] != fsize):
            return 0
        if (sameFile['lastmod']  != lastModTimeStamp):
            return 0
        
        return sameFile
    else:
        return 0

def __getAllIndexFiles( dirName,  fname):    
    fullpath=os.path.join(dirName, fname)
    listOfFiles = glob.glob(fullpath + '.*')
    if len(listOfFiles) == 0:
        return ""

    # convert file list to tuple list for post processing
    indexFileList= list()
    for fullFileName in listOfFiles:
        timestamp= os.path.getmtime(fullFileName)
        basename= os.path.basename(fullFileName)
        
        if fullFileName.find( __PARTLY ) >= 0:
            status= __PARTLY
        else:
            status= __FINAL
            
        tuple= {'fname':basename,  'rname':dirName,  'status':status,  'timestamp':timestamp}
        indexFileList.append( tuple )
        
    # sort by timestamp
    indexFileList.sort( key=lambda x:x['timestamp'])
    return indexFileList
    
def __getLatestIndexFile( dirName,  fname ):
    
    indexFileList= __getAllIndexFiles( dirName,  fname )
    if len(indexFileList) == 0:
        return ""
    
    # pick the last item
    last= indexFileList[-1]
    
    fname= last['fname']
    print("picking latest file [{s}]".format( s=fname) )
    
    return fname
    

def __writeIndexFile(rootDir,  iname, allFiles,  ts,  status):      
    
    timstampStr= str( int( ts ) )

    if status == __FINAL:
        indexFile= os.path.join( rootDir,  iname+"."+timstampStr)
    else:
        indexFile= os.path.join( rootDir,  iname+"."+timstampStr+"."+status)
   
    basename= os.path.basename(indexFile)
    header={'fname':basename,  'type':'list',  'listlen': len( allFiles ),  'version':__FVERS,  'timestamp':ts,  'status':status}
    
    # prepare innDex object 
    innDex={'header':header,  'data':allFiles}

    print("indexing done -- writing final file")
    # write list to file
    indexReadWrite.write(indexFile,  innDex)
    
    print("done - thanks ")
    return innDex
    
def __readIndexFile( dirName,  fname ):
    fullpath=os.path.join(dirName, fname)
    
    print("reading index file {s}".format(s=fullpath) )
    # read list from file
    innDex= indexReadWrite.read(fullpath)
    
    # set header and data
    header= innDex['header'];
    data=innDex['data'];
    
   # check header and return empty list if header is invalids
    if (header['fname'] != fname):
        print("incorrect filename")
        return dict()
    if (header['listlen'] != len( data ) ):
        print("incorrect data length")
        return dict()
    if (header['version'] != __FVERS):
        print("incorrect version "+ header['version'])
        return dict()    
        
    return innDex



def new( dirName ):   
    global __total_files_list   # \TODO: try to avoid the global variable - replace by call-by-reference
    
    if os.path.exists( dirName ) == False:
        print("err: path not existing {x}".format(x=dirName))
        return
    
    # get timestamp
    ts= time.time()
    
    # load most recent index and check if this is incomplete
    partDex= load( dirName )
    partList= dict()

    if len( partDex ) > 0:
        header= partDex['header']
        if  (header['status']  == __PARTLY):
            print("using partly index file " )            
        else:
            print("using last full index file ")
        
        # 
        partList= partDex['data']
    
    if len(partList) == 0:
        print("no partly index file found")

            
    
    # set list to loaded list
    __total_files_list= partList
    
    # start to loop through the folders
    __createIndexOfDirectory( dirName,  dirName, __FNAME,  ts )
    
    innDex= __writeIndexFile( dirName,  __FNAME,  __total_files_list,  ts,  __FINAL)
    
    return innDex
    
    

def load( dirName  ):    
    print("loading dir {s}".format(s=dirName))
    fname= __getLatestIndexFile( dirName,  __FNAME )
    if  fname == "":
        return dict()
        
    innDex= __readIndexFile( dirName,  fname )
    
    return innDex    
    
    
def getFullIndexFileList( dirName ):
    tempList= __getAllIndexFiles( dirName,  __FNAME )

    if len(tempList) == 0:
        return list()
        
    # remove all partly
    indexFileList= list()
    for entry in tempList:
        if (entry['status']  == __FINAL ):
            indexFileList.append(entry)
    
    return indexFileList
