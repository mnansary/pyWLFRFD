# pyWLFRFD
Water Level prediction from RainFall Data

    Version: 0.0.2    
    Author : Md. Nazmuddoha Ansary    
                  
![](/info/src_img/python.ico?raw=true )
![](/info/src_img/keras.ico?raw=true)
![](/info/src_img/pandas.ico?raw=true)
![](/info/src_img/tensorflow.ico?raw=true)

# Version and Requirements
* Python == 3.6.8
* Keras==2.3.1
* numpy==1.17.3
* pandas==0.25.2

1.Create a Virtualenv   
2.*pip3 install -r requirements.txt*  
**NOTE:** tensorflow is used as backend

#  DataSet  
> Add description in verson 0.0.3

#  Execution
* Change The following Values in ***config.json*** 

        "ARGS":  
        {  
            "SHP_FILE"                : "/home/ansary/RESEARCH/RainFall/Data/Borak/Borak.shp",  
            "WATER_LEVEL_CSV"         : "/home/ansary/RESEARCH/RainFall/Data/Raw/waterlevel.csv",  
            "RAINFALL_CSV"            : "/home/ansary/RESEARCH/RainFall/Data/Raw/rainfall.csv",  
            "OUTPUT_DIR"              : "/home/ansary/RESEARCH/RainFall/Data/"  
        }  


* Run **main.py**  
> version: 0.0.2

        usage: main.py [-h] model_type
        WaterLevel Data Prediction From RainFall Data
        positional arguments:
        model_type  name of the LSTM model to be USED. Available: StackedLSTM 
        optional arguments:
        -h, --help  show this help message and exit


# Results
* If execution is successful a folder called **h5s** should be created with the following folder tree:

            h5s              
            ├── X_Eval.h5
            ├── X_Train.h5
            ├── Y_Eval.h5
            └── Y_Train.h5

* After Complete Training and Testing a folder named **{MODELNAME}_MAX_FEATs:{maximum_features_to_be_extracted}_EPOCHS:{num_of_training_epochs}** (which is considered as **identifier** for a certain setting)  will be created in the **OUTPUT_DIR** which will contain the following folder tree:

            identifier
            ├── {identifier}_arch.png
            ├── {identifier}_loss.png
            ├── {identifier}_model.h5
            └── {identifier}_test.png

**NOTE**
* An Example idenditier looks like: **StackedLSTM_MAX_FEATs:64_EPOCHS:500**
> Model Name= StackedLSTM, Max Feats = 64, Epochs = 500 
* **{identifier}_arch.png** plots the model structre
* **{identifier}_loss.png** plots training history (overfit/ underfit identification)
* **{identifier}_test.png** plots the test data and prediction
* **{identifier}_model.h5** is the *model_weight* file for deployment

# RNN Models 
* Stacked LSTM
* Bidirectional LSTM
> To Be Added in version 0.0.6
* CNN LSTM
> To Be Added in version 0.0.7
* ConvLSTM
> To Be Added in version 0.0.8

### Stacked LSTM
The implemented Model Structre is as follows:

![](/info/stacked_arch.png?raw=true )


*   NUMBER OF TRAINING EPOCHS: **500**
*   BATCH SIZE: **128**
*   MAXIMUM FEATURE TAKEN AT ANY LAYER: **64**
*   R2 SCORE: **0.9601588319668203**
*   Mean Absolute Error : **0.14679548759599492**

The training **loss history** and **prediction with target** plot is as follows:

![](/info/stacked_loss.png?raw=true )
![](/info/stacked_test.png?raw=true )





**ENVIRONMENT**  

    OS          : Ubuntu 18.04.3 LTS (64-bit) Bionic Beaver        
    Memory      : 7.7 GiB  
    Processor   : Intel® Core™ i5-8250U CPU @ 1.60GHz × 8    
    Graphics    : Intel® UHD Graphics 620 (Kabylake GT2)  
    Gnome       : 3.28.2  


