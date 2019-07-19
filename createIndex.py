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
