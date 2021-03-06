import json


def write(fname,  obj):    
    # actually write to file
    with open(fname, 'w', encoding='utf8') as outfile:
        json.dump(obj, outfile, ensure_ascii=False, indent=2)


def read(fname):    
    # read from file
    with open(fname, 'r', encoding='utf8') as f:
        obj = json.load(f)
        
    # return data from JSON if header is ok
    return obj
