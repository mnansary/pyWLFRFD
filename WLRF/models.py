# -*- coding: utf-8 -*-
"""
@author: MD.Nazmuddoha Ansary
"""
from __future__ import print_function
from termcolor import colored

import os
import numpy as np 
import math
import matplotlib.pyplot as plt 

from keras.models import Sequential
from keras.layers import LSTM,Dense
from keras.losses import mean_squared_error
from keras.optimizers import Adam
from keras.utils import plot_model

from WLRF.utils import create_dir,LOG_INFO

from sklearn.metrics import r2_score, mean_absolute_error
#--------------------------------------------------------------------------------------------------------------------------------------------------
def StackedLSTM(PARAMS):
    # layer features
    nb_layers=int(math.log2(PARAMS.MAX_FEATS))
    layer_specs=[(2**i) for i in range(2,nb_layers)][::-1]
    # model
    model=Sequential()
    # first LSTM Layer
    model.add(LSTM(PARAMS.MAX_FEATS,input_shape=PARAMS.INPUT_SHAPE,return_sequences=True,activation='tanh'))
    # LSTM layers
    for i in range(len(layer_specs)):
        model.add(LSTM(layer_specs[i],return_sequences=True,activation='tanh'))
    # last layers
    model.add(LSTM(2,return_sequences=False,activation='tanh'))
    model.add(Dense(1))
    model.compile(loss=mean_squared_error,optimizer=Adam())
    model_name='StackedLSTM_MAX_FEATs:{}_EPOCHS:{}'.format(PARAMS.MAX_FEATS,PARAMS.EPOCHS)
    return model,model_name
#--------------------------------------------------------------------------------------------------------------------------------------------------
def train_model(model_type,DataSet,ARGS,PARAMS):
    # define Model
    if model_type=='StackedLSTM':
       model,model_name=StackedLSTM(PARAMS)
    else:
        raise ValueError('Not Implemented Yet')
    # Model Dir
    save_dir=create_dir(ARGS.OUTPUT_DIR,model_name)
    # Load DataSet
    X_Train,Y_Train,X_Eval,Y_Eval=DataSet
    # Model Info
    print(model.summary())
    # Save Model Arch
    plot_model(model,to_file=os.path.join(save_dir,'arch.png'),show_shapes=True)
    # training
    history=model.fit(X_Train,
                      Y_Train,
                      batch_size=PARAMS.BATCH_SIZE,
                      epochs=PARAMS.EPOCHS,
                      validation_data=(X_Eval,Y_Eval))
    # plot history
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title(' train loss vs validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.savefig(os.path.join(save_dir,'loss.png'))
    plt.clf()
    plt.close()    
    # save model weigths
    model.save(os.path.join(save_dir,'model.h5'))
    
    return model,model_name
#--------------------------------------------------------------------------------------------------------------------------------------------------
def test_model(ARGS,model,model_name,PREP_OBJ): 
    # Model Dir
    save_dir=create_dir(ARGS.OUTPUT_DIR,model_name)
    # test df
    df=PREP_OBJ.test_df
    # prediction dataframe
    pred_df= df.loc[df.index >= PREP_OBJ.test_split_timeframe].copy()
    pred_df=pred_df[['Target']]
    # getting predictions
    rows= df.shape[0]
    for i in range(rows-PREP_OBJ.seq_len):
        datadf=df.iloc[i:PREP_OBJ.seq_len+i, :]
        X,_=PREP_OBJ.preprocessDataFrame(datadf,shuffle_flag=False)
        prediction=model.predict([X])
        pred_df.ix[i,'Prediction']=prediction[0][0]
    # save predictions
    pred_df.plot()
    plt.savefig(os.path.join(save_dir,'test.png'))
    # results
    r2 = r2_score( pred_df['Target'], pred_df['Prediction'] )
    mae = np.sqrt( mean_absolute_error( pred_df['Target'], pred_df['Prediction']) )
    # print
    LOG_INFO('R2 SCORE: {}'.format(r2))
    LOG_INFO('Mean Absolute Error : {}'.format(mae))
    