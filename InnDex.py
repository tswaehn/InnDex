import sys
## check version
if (sys.version_info < (3, 0)):
    print("err: python 3.0 needed -- exit")
    exit(1)
    
import createIndex
import procDuplicates

print("start app")


dirName = '/home/tswaehn/Downloads'
dirName= '/run/media/tswaehn/My Passport/data/backup_data/data';
#dirName= '/run/media/tswaehn/c587a5e7-5b5a-4c0c-857d-ba4cc1872b47/data/';
#dirName= '/home/tswaehn'

innDex= createIndex.new(dirName)

innDex= createIndex.load(dirName)

print("index done")    

#procDuplicates.run( dirName,  innDex )

    
print("app end")
