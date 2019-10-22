#!/usr/bin/env python3
"""
@author: MD.Nazmuddoha Ansary
"""
from __future__ import print_function
from termcolor import colored

from model.utils import Preprocessor,readh5,readJson
#-----------------------------------------------------Load Config----------------------------------------------------------
config_data=readJson('config.json')

class ARGS:
    SHP_FILE             = config_data['ARGS']['SHP_FILE']
    WATER_LEVEL_CSV      = config_data['ARGS']['WATER_LEVEL_CSV']
    RAINFALL_CSV         = config_data['ARGS']['RAINFALL_CSV']
    OUTPUT_DIR           = config_data['ARGS']['OUTPUT_DIR']

class FLAGS:
    eval_split_timeframe = config_data['FLAGS']["eval_split_timeframe"]          
    test_split_timeframe = config_data['FLAGS']["test_split_timeframe"]             
    pred_len             = config_data['FLAGS']["pred_len"]    
    seq_len              = config_data['FLAGS']["seq_len"]
    max_water_level      = config_data['FLAGS']["max_water_level"]
    max_rainfall         = config_data['FLAGS']["max_rainfall"]            
#-----------------------------------------------------------------------------------------------------------------------------------
import time
import os
import numpy as np 
#-----------------------------------------------------------------------------------------------------------------------------------
def main(argv):
    obj=Preprocessor(ARGS,FLAGS)
    obj.processData()
#-----------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main('RAINFALL')