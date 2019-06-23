import sys
## check version
if (sys.version_info < (3, 0)):
    print("err: python 3.0 needed -- exit")
    exit(1)
    
import createIndex
import procDuplicates

print("start app")


dirName = '/home/tswaehn/Downloads'

#innDex= createIndex.new(dirName)

innDex= createIndex.load(dirName)

print("index done")    

procDuplicates.run( dirName,  innDex )

    
print("app end")
