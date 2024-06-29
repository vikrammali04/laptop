import streamlit as st
import pickle
import numpy as np
import os

# import the model
file_path = os.path.join(os.path.dirname(__file__), 'pipe.pkl')
file_path1 = os.path.join(os.path.dirname(__file__), 'df.pkl')

pipe = pickle.load(open(file_path,'rb'))
df = pickle.load(open(file_path1,'rb'))

st.title("Laptop Price Predictor")
brands=df['Company'].unique()
brands=brands[brands!='Apple']
# brand
company = st.selectbox('Brand',brands)

# type of laptop
type = st.selectbox('Type',df['TypeName'].unique())

# Ram
ram = st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])

# weight
weight = st.number_input('Weight of the Laptop (In Kg)')

# Touchscreen
touchscreen = st.selectbox('Touchscreen',['No','Yes'])

# IPS
ips = st.selectbox('IPS',['No','Yes'])

# screen size
screen_size = st.number_input('Screen Size (In Inches)')

# resolution
resolution = st.selectbox('Screen Resolution',sorted(['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440']))


#cpu
cpu = st.selectbox('CPU',sorted(df['Cpu brand'].unique()))

hdd = st.selectbox('HDD(In GB)',[0,128,256,512,1024,2048])

ssd = st.selectbox('SSD(In GB)',[0,128,256,512,1024])

gpu = st.selectbox('GPU',sorted(df['Gpu brand'].unique()))
os_type=df['os'].unique()
os_type=os_type[os_type!='Mac']
os = st.selectbox('OS',os_type)

f   = st.selectbox('Frequency( In GHz )',sorted([2.3 , 1.8 , 2.5 , 2.7 , 3.1 , 3.  , 2.2 , 1.6 , 2.  , 2.8 , 1.2 ,
       2.9 , 2.4 , 1.44, 1.5 , 1.9 , 1.1 , 1.3 , 2.6 , 3.6 , 3.2 , 1.  ,
       2.1 , 0.9 , 1.92]))

if st.button('Predict Price'):
    # query
    if weight > 6 or weight <1:
        st.error('Please enter a valid Weight. Weight must be between 1 and 6 kg.')
        st.stop() 
    if screen_size<10 or screen_size>18:
        st.error('Please enter a valid screen size. Screen size must be between 10 and 18 and inches.')
        st.stop() 
    
    if ssd==0 and hdd==0:
       st.error('SSD and HDD both can not be zero.')
       st.stop() 
           

        
    ppi = None
    if touchscreen == 'Yes':
        touchscreen = 1
    else:
        touchscreen = 0

    if ips == 'Yes':
        ips = 1
    else:
        ips = 0


    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size
    query = np.array([company,type,ram,weight,touchscreen,ips,ppi,cpu,f,hdd,ssd,gpu,os])

    query = query.reshape(1,13)
    st.header("The predicted price of this configuration is :  " + str(int(np.exp(pipe.predict(query)[0]))))
