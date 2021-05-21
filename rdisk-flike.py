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
from base64 import b64encode as benc
class rdisk_flike(object):
    def __init__(self):
        self.init_obj_vars()
    def get_random(self):
        with open(self.random_pool,'rb') as f:
            d = ord(f.read(1))
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
            if self.NOP:
                if mode == "wipe":
                    os.system('echo \"{}\" &>/dev/null'.format(benc(chr(0))))
                elif mode == "randomize":
                    os.system('echo \"{}\" &>/dev/null'.format(benc(chr(self.get_random()))))
            else:    
                if mode == "wipe":
                    with open(self.target, 'wb+') as f:
                        f.seek(pos, whence=0)
                        f.write(chr(0).encode())
                        f.close()
                elif mode == "randomize":
                    with open(self.target, 'wb+') as f:
                        f.seek(pos, whence=0)
                        f.write(chr(self.get_random()).encode())
                        f.close()
        else:
            print("Abort operation.")
            exit(-1)
    # set nop func
    def set_NOP(self,value=False):
        self.NOP = value
    # function to wipe anything
    def op_target(self,mode="wipe",target=None,n_passes=3,limit_size=None,randomized=False,random_pool="/dev/random"):
        self.random_pool = random_pool
        cnt_oct=0
        self.counter = 0
        self.target = target
        for it_1 in range(0, n_passes):
            print("\r({}/{}) passes\r".format(it_1,n_passes),end='')
            pos = self.nextPos(randomized)
            cnt_oct += 1
            if ((type(limit_size) == int) & bool(limit_size)):
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
        self.NOP = False
    def run_command(self,target, operations=[["wipe",3,"/dev/urandom"],["randomize",7,"/dev/urandom"],["wipe",1,None]], random_pool_overset=None, factory_like_mode=True):
        for op in operations:
            mode,n_passes,random_pool = op[0], op[1], op[2]
            if random_pool_overset:
                random_pool = random_pool_overset
            self.op_target(mode=mode,target=target,n_passes=n_passes,limit_size=None,randomized=(random_pool!=None and type(random_pool)==str),random_pool=random_pool)
        if factory_like_mode:
            self.flike()
        exit(0)
#
#
#
parser = argparse.ArgumentParser()
parser.add_argument("target", type=str, help="The file(virtual disk) or the symlink of the volume to be the target.")
parser.add_argument("--OP_STRING", type=str, help="OPERATION CODE STRING(JSON OR JUST AN PYTHON STACK LIST INTO AN STRING... THAT WORK...)", required=False)
parser.add_argument("--RANDOM_POOL", type=str, help="Set the symlink of the random stream if you want choice !", required=False)
parser.add_argument("-DC", "--default-config", action="store_true", help="Option to specify is the default configuration with the default index code of the configuration profiles(it's an stack into JSON).")
parser.add_argument("-DCN", "--default-config-number", type=int, help="Option to specify is the default configuration at specific index code of the configuration profiles(it's an stack into JSON).")
parser.add_argument("-FKout", "--factory-like-mode" ,action="store_true", help="Enable the feature to set an final look like the disk is from an factory to warehouse before in handles...")
parser.add_argument("-t", "--countdown", type=int, help="Shedule the begins of process after an specified seconds countdown...")
parser.add_argument("-NOP","--no-action-mode", action="store_true", help="No action on the target, but usage of the random pool and countdown operationnal[FOR AN FAKE MODE].")
parser.add_argument("-tWKD", "--wait-key-to-disengage", type=str, help="Option to enable the key-protected disengage procedure(add an ask for disengage and an countdown, if the countdown is not set by the specific flag, the default countdown setted is 30(seconds).)")
# v1.0 goals -------- ^ ^ ^ ^ ^
# Yeah it's Rickiest  | | | | |
#  Things... Crazy ?! | | | | |
#=-=-=-=-=-=-=-=-=-=-=+-+-+-+-+
#
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
args             = parser.parse_args()
TARGET           = args.target
OPERATION_STRING = args.OP_STRING
RANDOM_POOL      = args.RANDOM_POOL
NOP              = args.no_action_mode
DC               = args.default_config
DNC              = args.default_config_number
FKout            = args.factory_like_mode
tWKD             = args.wait_key_to_disengage
tdwn             = args.countdown
#====================================================================
FINAL_COMMAND_NAME = "rdiskfactorylike"
#this parts... pfff need to be more smart .... so easy haha, later...
#====                                                            ====
config_file_path = "/var/{}/conf.json".format(FINAL_COMMAND_NAME)
#====================================================================
if DC:
    INTERNALS_SETTERS_MODE = "config"
else:
    INTERNALS_SETTERS_MODE = "args"
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
    if DNC:
        n_conf = DNC
    elif bool(DC) and not DNC: 
        #or just ... read the default number
        DEFAULT_CONF_NUM = data_config["DEFAULT_CONF_ID_NUMBER"]
        if ( type(DEFAULT_CONF_NUM) == int ) and bool(DEFAULT_CONF_NUM):
            n_conf = DEFAULT_CONF_NUM


    # read configuration
    DEFAULT_TARGET = data_config["DEFAULTS"][n_conf]["TARGET"]
    DEFAULT_OP = data_config["DEFAULTS"][n_conf]["OP"]
    DEFAULT_RANDOM_POOL = data_config["DEFAULTS"][n_conf]["RANDOM_POOL"]
#
TARGET_PATH=TARGET
#
if (DNC) or bool(DC):
    if not TARGET:
        TARGET_PATH=DEFAULT_TARGET
    OPERATIONS=DEFAULT_OP
    RANDOM_POOL=DEFAULT_RANDOM_POOL
elif (not (DNC)) and (not bool(DC)):
    if not TARGET:
        TARGET_PATH=TARGET
    if OPERATION_STRING:
        OPERATIONS=OPERATION_STRING
    else:
        OPERATIONS=[["wipe",3,"/dev/urandom"],["randomize",7,"/dev/urandom"],["wipe",1,None]]
#
#
if not RANDOM_POOL:
    RANDOM_POOL="/dev/random"
if FKout==None:
    FKout = False


#
rdfl = rdisk_flike()
if NOP:
    rdfl.set_NOP(value=True)
else:
    rdfl.set_NOP(value=False)
rdfl.run_command(TARGET_PATH,OPERATIONS,random_pool_overset=RANDOM_POOL,factory_like_mode=FKout)