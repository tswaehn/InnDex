import createIndex
# import procDuplicates
import procCompare
import config.config as cfg
import readers.readers as readers

print("start app")

job_config = cfg.Config("innDex.conf")

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

if job_config.get('run_innDex') == 1:
    print('index enabled')
    dirname = job_config.get('innDex_dir')

    innDex0 = createIndex.load(dirname)
    readers.process_list(innDex0)
else:
    print('index disabled')
    job_config.set('run_innDex', 0)
    job_config.set('innDex_dir', 'folder_XYZ')
    
    
    
    
    
print("app end")
