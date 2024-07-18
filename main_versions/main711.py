import streamlit as st 
import os 
import pandas as pd 
import numpy as np
from langchain.llms import OpenAI 
from langchain.agents import create_pandas_dataframe_agent
#from openai import OpenAI


data = {
    'Temperature (°C)': np.random.uniform(20, 30, size=30),
    'Humidity (%)': np.random.uniform(40, 60, size=30),
    'CO2 (ppm)': np.random.uniform(300, 500, size=30),
    'PM2.5 (µg/m³)': np.random.uniform(0, 50, size=30),
    'VOC (ppm)': np.random.uniform(0, 1, size=30),
    'LED PPFD (µmol/m²/s)': np.random.uniform(100, 400, size=30),
    'Water pH': np.random.uniform(5.5, 6.5, size=30),
    'EC (dS/m)': np.random.uniform(1.0, 2.5, size=30),
    'Energy Consumption (kWh)': np.random.uniform(100, 500, size=30)
}


#llms agents

analyst_llm = OpenAI(temperature = 0,
                     api_key="sk-a36dbf13c32f4b28a7dfc3ba81275fa8",
                     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                     )



df = pd.DataFrame(data)

pandas_agent = create_pandas_dataframe_agent(analyst_llm, df, verbose=True)

if 'clicked' not in st.session_state:
    st.session_state.clicked = {1: False}



st.title('植物工厂LLM AI助手团队')
st.divider()
st.header('AI数据分析师工作区')

with st.sidebar:
    st.write('边栏')
    
#function to update the value in session state
def clicked(button):
    st.session_state.clicked[button] = True

st.buttong('开始分析', on_click=clicked, args=[1])

if st.button('开始分析'):
    st.subheader('开始分析')
    
    with st.expander('分析思考'):
        st.write(analyst_llm('what is EDA')) #测试下
        
question = 'What is the meaning of the columns'
columns_meaning = pandas_agent.run(question)
st.write()
    

