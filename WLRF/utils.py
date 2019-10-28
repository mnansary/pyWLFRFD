# -*- coding: utf-8 -*-
"""
@author: MD.Nazmuddoha Ansary
"""
from __future__ import print_function
from termcolor import colored

import os
import numpy as np 

from collections import deque
import random 

import pandas as pd 
import shapefile
from shapely.geometry import shape
from shapely.geometry.point import Point

import json
import h5py

#--------------------------------------------------------------------------------------------------------------------------------------------------
def LOG_INFO(log_text,p_color='green'):
    print(colored('#    LOG:','blue')+colored(log_text,p_color))
def readJson(file_name):
    return json.load(open(file_name))
def create_dir(base_dir,ext_name):
    new_dir=os.path.join(base_dir,ext_name)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    return new_dir
def saveh5(path,data):
    hf = h5py.File(path,'w')
    hf.create_dataset('data',data=data)
    hf.close()
def readh5(d_path):
    data=h5py.File(d_path, 'r')
    data = np.array(data['data'])
    return data
#--------------------------------------------------------------------------------------------------------------------------------------------------
class Preprocessor(object):
    def __init__(self,ARGS,FLAGS):
        # Arguments
        self.wl_csv     =   ARGS.WATER_LEVEL_CSV
        self.rf_csv     =   ARGS.RAINFALL_CSV
        self.shp_file   =   ARGS.SHP_FILE
        self.save_dir   =   ARGS.OUTPUT_DIR
        # h5 dir
        self.h5_dir=create_dir(self.save_dir,'h5s')
        self.X_Train_h5 =   os.path.join(self.h5_dir,'X_Train.h5')
        self.X_Eval_h5  =   os.path.join(self.h5_dir,'X_Eval.h5')
        self.Y_Train_h5 =   os.path.join(self.h5_dir,'Y_Train.h5')
        self.Y_Eval_h5  =   os.path.join(self.h5_dir,'Y_Eval.h5')
        # Flags
        self.eval_split_timeframe   =   FLAGS.eval_split_timeframe
        self.test_split_timeframe   =   FLAGS.test_split_timeframe
        self.pred_len               =   FLAGS.pred_len
        self.seq_len                =   FLAGS.seq_len
        self.max_water_level        =   FLAGS.max_water_level
        self.max_rainfall           =   FLAGS.max_rainfall
    
    def __processWaterLevel(self):
        #water_level_data
        water_level_df=pd.read_csv(self.wl_csv,skiprows=[0],names=['date_time','WaterLevel'])
        water_level_df['date_time']=pd.to_datetime( water_level_df['date_time'])
        water_level_df.set_index(['date_time'],inplace=True)
        water_level_df['WaterLevel']=water_level_df['WaterLevel']/self.max_water_level
        return water_level_df
    
    def __processRainfallData(self):
        #rain_fall_data
        rain_fall_df=pd.read_csv(self.rf_csv,header=None)
        
        lat=list(rain_fall_df.iloc[0])
        lon=list(rain_fall_df.iloc[1])
        lat_lon=[str(lat[i])+'_'+str(lon[i]) for i in range(1,len(lat))]
        
        coloumn_names=['date_time']+lat_lon
        
        rain_fall_df.columns=coloumn_names
        rain_fall_df=rain_fall_df[2:]
        rain_fall_df['date_time']=pd.to_datetime( rain_fall_df['date_time'])
        rain_fall_df.set_index(['date_time'],inplace=True)
        rain_fall_df=rain_fall_df/self.max_rainfall 

        lat=lat[1:]
        lon=lon[1:]
        
        #Shpfile_data
        shp = shapefile.Reader(self.shp_file) 
        # get all the polygons
        all_shapes = shp.shapes() 
        
        final_lat=[]
        final_lon=[]
        for i in range(len(all_shapes)):
            # get a boundary polygon
            boundary = all_shapes[i] 
            for j in range(len(lat)):
                point_data=Point(lon[j],lat[j])
                if shape(boundary).contains(point_data):
                    final_lat.append(lat[j])
                    final_lon.append(lon[j])

        final_lat_lon=[str(final_lat[i]) +"_"+ str(final_lon[i]) for i in range(len(final_lat))]
        print(final_lat_lon)
        rain_fall_df=rain_fall_df[final_lat_lon]
        
        return rain_fall_df  
    
    def preprocessDataFrame(self,data_frame,shuffle_flag=True):
        sequential_data=[]
        prev_days=deque(maxlen=self.seq_len)    
        for i in data_frame.values:
            prev_days.append([n for n in i[:-1]])
            if len(prev_days)== self.seq_len:       
                sequential_data.append([np.array(prev_days),i[-1]])
        if shuffle_flag:
            random.shuffle(sequential_data)
        X=[]
        y=[]
        for seq,target in sequential_data:        
            X.append(seq)
            y.append(target)
        return np.array(X),np.array(y)
    
    def processData(self):
        LOG_INFO('Getting Water Level and Rainfall Raw Data')                            
        water_level_df  =   self.__processWaterLevel()
        rain_fall_df    =   self.__processRainfallData()
        # merge dataframes
        LOG_INFO('Merging Dataframe')
        df = pd.merge(rain_fall_df,water_level_df, left_index=True, right_index=True)
        df['Target']=df['WaterLevel'].shift(-self.pred_len)
        df.dropna(inplace=True)
        # split data
        LOG_INFO('Spliting Dataframes')
        train_df    =   df.loc[df.index <  self.eval_split_timeframe].copy()
        eval_df     =   df.loc[(df.index >=  self.eval_split_timeframe) & (df.index < self.test_split_timeframe)].copy()
        # drop Nan Values
        train_df.dropna(inplace=True)
        eval_df.dropna(inplace=True)
        # array data
        LOG_INFO('Getting Array Data')
        X_Train,Y_Train  =   self.preprocessDataFrame(train_df,shuffle_flag=True)
        X_Eval,Y_Eval    =   self.preprocessDataFrame(eval_df ,shuffle_flag=True)
        # INFO
        print(' Train   => X:{} Y:{}'.format(X_Train.shape,Y_Train.shape)) 
        print(' Eval    => X:{} Y:{}'.format(X_Eval.shape,Y_Eval.shape)) 
        # Saving Data
        LOG_INFO('Saving h5 Data')
        # X data
        saveh5(self.X_Train_h5,X_Train)
        saveh5(self.X_Eval_h5 ,X_Eval)
        # Y data
        saveh5(self.Y_Train_h5,Y_Train)
        saveh5(self.Y_Eval_h5 ,Y_Eval)
        # test data
        self.test_df= df.loc[df.index >= self.test_split_timeframe].copy()
        self.test_df= eval_df.tail(self.seq_len).append(self.test_df)
        self.test_df.dropna(inplace=True)
            