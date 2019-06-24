import sys
## check version
if (sys.version_info < (3, 0)):
    print("err: python 3.0 needed -- exit")
    exit(1)
    
import createIndex
#import procDuplicates
import procCompare
import config

print("start app")

conf= config.load()

# ---
# update index
if (config.get(conf, 'update') == 1):
    dirList= config.get(conf, 'update_index')
    if (dirList != None) and  (len(dirList) > 0):
        for dirName in dirList:
            print("start index - {s}".format(s=dirName))
            createIndex.new(dirName)        



#innDex= createIndex.load(dirName)

if (config.get(conf, 'compare') == 1):
    dirList= config.get(conf, 'proc_compare')
    if (dirList != None) and  (len(dirList) ==2):
        dir0= dirList["dir0"]
        dir1= dirList["dir1"]

        innDex0= createIndex.load(dir0)
        innDex1= createIndex.load(dir1)

        procCompare.run( innDex0,  innDex1 )


#procDuplicates.run( dirName,  innDex )

   
    
    
    
    
    
print("app end")
