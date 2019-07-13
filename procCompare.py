import indexReadWrite

def __compare( file0,  file1 ):
    
    if file0['rname'] != file1['rname']:
        return 0
    if file0['md5'] != file1['md5']:
        return 0
    if file0['fsize'] != file1['fsize']:
        return 0
    
    return 1


def run(innDex0,  innDex1):
    pairs = list()
    print("begin compare")
    
    list0 = innDex0['data']
    list1 = innDex1['data']
    
    count0=0
    count1=0
    for hashKey0 in list0:
        count0 += 1
        file0= list0[hashKey0]
        file1= list1.pop(hashKey0,  None)
        tuple= { "file0":file0,  "file1": None, "res":0}
        if file1 != None:
            tuple["file1"]= file1
            count1+=1
            
            if __compare(file0,  file1) == 1:
                # files are equal
                tuple["res"]=1
         
        pairs.append(  tuple )
    
    # remaining files in list1 are not existend in list0
    for hashKey1 in list1:
        count1+=1
        file1= list1[hashKey1]
        pairs.append( {"file0":None, "file1": file1,  "res":0} )
    
    same_count= 0;
    diff_count=0
    for x in pairs:
        if x['res'] == 1:
            same_count +=1
        else:
            diff_count += 1
            fname0= x['file0']
            fname1= x['file1']

            print("{a} | {b}".format(a=fname0,  b=fname1))
            
    #print(pairs)
    indexReadWrite.write( 'indexCompare.JSON',  pairs )
    print("found {x:d} same and {y:d} diffs".format(x=same_count,  y=diff_count))
    print("compare done {x:d} {y:d}".format(x=count0,  y=count1))
    return pairs

