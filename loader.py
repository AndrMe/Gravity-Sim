import json as js
import os

def load_data(name):
    '''loads all the configs and other data from json file'''
    dir_path=os.getcwd()
    if name not in os.listdir():
        f=open(dir_path+'/'+name,'w')
        empt_data=dict()
        js.dump(empt_data,f)
        f.close()
        print(f'file not found, created new at {dir_path}/{name}') 
    try:
        data=js.load(open(dir_path+'/'+name))
    except:
        f=open(dir_path+'/'+name,'w')
        data=dict()
        js.dump(data,f)
        f.close()
        data=js.load(open(dir_path+'/'+name))
        f.close()
        print(f'error while loading file, created new at {dir_path}/{name}')   
    return data    

def update_data_in_file(data,name):
    'compares previouse save file(or if it exists) and append/replaced whith any new data provided'
    dir_path=os.getcwd()
    if name not in os.listdir():
        f=open(dir_path+'/'+name,'w')
        js.dump(data,f)
        f.close()  
    else:
        try:
            file_data=js.load(open(dir_path+'/'+name))
            new_data=combine_dicts(file_data,data)
            f=open(dir_path+'/'+name,'w')
            js.dump(new_data,f)
            f.close()  
        except:
            f=open(dir_path+'/'+name,'w')
            js.dump(data,f)
            f.close()  
            print(f'error reading previous save, created new at {dir_path}/{name}')

def combine_dicts(oldData:dict,newData:dict):
    resData=dict(oldData)
    od_keys=oldData.keys()
    for key in newData:
        if (key in od_keys):
            if type(oldData[key])==dict:
                combine_dicts(oldData[key],newData[key])
            else:
                resData[key]=newData[key]
        else:
            resData[key]=newData[key]

    return resData

def load_init_data(name):
    '''extracts confs, trace and planets from file'''
    init_data=load_data(name)
    try:
        configs=init_data['configs']
    except:
        print('confs not saved')
        configs=None
    try:
        planets=init_data['planets']
    except:
        print('no planet data')
        planets=[]
    try:
        trace=init_data['trace']
    except:
        trace=[]
    return [configs,planets,trace]
