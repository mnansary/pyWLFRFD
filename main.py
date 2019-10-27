#!/usr/bin/env python3
"""
@author: MD.Nazmuddoha Ansary
"""
from __future__ import print_function
from termcolor import colored

from WLRF.utils import Preprocessor,readh5,readJson
from WLRF.models import train_model,test_model

import argparse
parser = argparse.ArgumentParser(description='WaterLevel Data Prediction From RainFall Data ')
parser.add_argument("model_type", help="name of the LSTM model to be USED. Available: StackedLSTM")
p_args = parser.parse_args()
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

class PARAMS:
    MAX_FEATS   = 64
    INPUT_SHAPE = None
    EPOCHS      = 500
    BATCH_SIZE  = 128
    
#-----------------------------------------------------------------------------------------------------------------------------------
import time
import os
import numpy as np 
#-----------------------------------------------------------------------------------------------------------------------------------
def main(p_args):
    # Preprocess
    PREP_OBJ=Preprocessor(ARGS,FLAGS)
    PREP_OBJ.processData()
    
    # DataSet
    X_Train =   readh5(PREP_OBJ.X_Train_h5)
    Y_Train =   readh5(PREP_OBJ.Y_Train_h5)
    X_Eval  =   readh5(PREP_OBJ.X_Eval_h5 )
    Y_Eval  =   readh5(PREP_OBJ.Y_Eval_h5 )
    DataSet =   (X_Train,Y_Train,X_Eval,Y_Eval)
    # Set Param
    PARAMS.INPUT_SHAPE=X_Train.shape[1:]
    # Train
    model,model_name=train_model(p_args.model_type,DataSet,ARGS,PARAMS)
    # Test
    test_model(ARGS,model,model_name,PREP_OBJ)
#-----------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main(p_args)