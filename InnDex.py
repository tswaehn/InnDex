import createIndex
# import procDuplicates
import procCompare
import config.config as cfg
import readers.main as readers
import readers.folderCrawler as FC

print("start app")

job_config = cfg.Config("innDex.conf")

# ---
# update index
if job_config.get('update') == 1:
    dirList = job_config.get('update_index')
    if (dirList is not None) and (len(dirList) > 0):
        for dir_name in dirList:
            print("start index - {s}".format(s=dir_name))
            # createIndex.new(dirName)
            crawler = FC.FolderCrawler(dir_name)
            crawler.run()

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

    innDex = createIndex.load(dirname)
    readers.exec_all(innDex)
else:
    print('index disabled')
    job_config.set('run_innDex', 0)
    job_config.set('innDex_dir', 'folder_XYZ')
    
    
    
    
    
print("app end")
