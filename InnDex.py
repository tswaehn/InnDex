import createIndex
# import procDuplicates
import procCompare
import config.config as CFG

print("start app")

job_config = CFG.Config("innDex.conf")

# ---
# update index
if job_config.get('update') == 1:
    dirList = job_config.get('update_index')
    if (dirList is not None) and (len(dirList) > 0):
        for dirName in dirList:
            print("start index - {s}".format(s=dirName))
            createIndex.new(dirName)        


# innDex= createIndex.load(dirName)

if job_config.get('compare') == 1:
    dirList = job_config.get('proc_compare')
    if (dirList is not None) and (len(dirList) == 2):
        dir0 = dirList[0]
        dir1 = dirList[1]

        innDex0 = createIndex.load(dir0)
        innDex1 = createIndex.load(dir1)

        procCompare.run(innDex0,  innDex1)


#procDuplicates.run( dirName,  innDex )

   
    
    
    
    
    
print("app end")
