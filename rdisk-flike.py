#!/usr/bin/python3
#coding: utf-8
#
#
# "rdisk-factory-like" (rdisk ... 'r' for Rick haha)
# Version alpha ... and dev

# importing dependences
import os 
import json
import argparse

class rdisk_flike(object):
    def __init__(self):
        self.init_obj_vars()
    def get_random(self):
        with open(self.random_pool,'rb') as f:
            d = int(f.read(1))
            f.close()
        return d
    # functions to op on pos
    def nextPos(self,is_random=False):
        self.counter += 1
        if is_random:
            return self.get_random() 
        else:
            return self.counter
    #
    def one_octal_op(self,pos,mode=None):
        if mode:
            if mode == "wipe":
                with open(self.target, 'wb+') as f:
                    f.seek(pos, whence=0)
                    f.write(chr(0))
                    f.close()
            elif mode == "randomize":
                with open(self.target, 'wb+') as f:
                    f.seek(pos, whence=0)
                    f.write(chr(self.get_random()))
                    f.close()
        else:
            print("Abort operation.")
            exit(-1)

    # function to wipe anything
    def op_target(self,mode="wipe",target=None,n_passes=3,limit_size=None,randomized=False,random_pool="/dev/random"):
        self.random_pool = random_pool
        cnt_oct=0
        self.counter = 0
        self.target = target
        for it_1 in range(0, n_passes):
            pos = self.nextPos(randomized)
            cnt_oct += 1
            if ((type(limit_size) == int) & (limit_size)):
                if cnt_oct > limit_size:
                    break
            self.one_octal_op(pos,"wipe")
    #factory like code
    def flike(self):
        os.system("sudo mkfs.fat -F32 {}".format(self.target))
    def init_obj_vars(self):
        self.target = None
        self.counter = 0
        self.random_pool = None
    def run_command(self,target, operations=[["wipe",3,"/dev/urandom"],["randomize",7,"/dev/urandom"],["wipe",1,None]], factory_like_mode=True):
        for op in operations:
            mode,n_passes,random_pool = op[0], op[1], op[2]
            self.op_target(mode=mode,target=target,n_passes=n_passes,limit_size=None,randomized=(random_pool!=None && type(random_pool)==str),random_pool=random_pool)
        if factory_like_mode:
            self.flike()
        exit(0)

#
FINAL_COMMAND_NAME = "rdiskfactorylike"
#
config_file_path = "/var/{}/conf.json".format(FINAL_COMMAND_NAME)
#
INTERNALS_SETTERS_MODE = "config"

#
if INTERNALS_SETTERS_MODE == "config":
    # inits
    n_conf=0

    #read data from the config file 
    with open(config_file_path,'rb') as f:
        data_config = f.read().decode()
        f.close()
    
    #be sure the config file is under valid json format and convert to an dictionnary list
    try:
        data_config = json.loads(data_config)
    except Exception as e:
        print("ERROR ! \nException is --- > ({})\n".format(e))
        exit(-1)

    # here place arg parsing for set configuration id 

    #or just ... read the default number
    DEFAULT_CONF_NUM = data_config["DEFAULT_CONF_ID_NUMBER"]
    if ( type(DEFAULT_CONF_NUM) == int ) and (DEFAULT_CONF_NUM):
        n_conf = DEFAULT_CONF_NUM


    # read configuration
    DEFAULT_TARGET = data_config["DEFAULTS"][n_conf]["TARGET"]
    DEFAULT_OP = data_config["DEFAULTS"][n_conf]["OP"]
    DEFAULT_RANDOM_POOL = data_config["DEFAULTS"][n_conf]["RANDOM_POOL"]
#

#
TARGET_PATH=DEFAULT_TARGET[n_conf]
OPERATIONS=DEFAULT_OP[n_conf]
#
rdfl = rdisk_flike()
rdfl.run_command(TARGET_PATH)