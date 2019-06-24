
import indexReadWrite
# const
__CONFIG="innDex.conf.JSON"
__CONFIG_VER="1.0"

def load():
    global __CONFIG
    
    try:
        config= indexReadWrite.read( __CONFIG )
    except FileNotFoundError:
        print("config not found")
        config= __createNewConfig()
        
        
    return config
            
def get( config,  key):            
    
    if key in config:
        return config[key]
    else:
        set( config,  key,  None )
        return config[key]


def set( config,  key,  value):    
    config[key]= value
    indexReadWrite.write( __CONFIG,  config )

    
def __createNewConfig():
    global __CONFIG
    global __CONFIG_VER
    
    print("creating default config")
    config= dict()
    
    set( config,  'version', __CONFIG_VER )
    set( config,  'update_index', list({"folder1",  "folder2"}) )    

    # write
    indexReadWrite.write( __CONFIG,  config )
    # load
    config= indexReadWrite.read( __CONFIG )
    
    return config
    
