import streamlit as st 
import os 
import pandas as pd 
import numpy as np
from langchain.llms import openai, tongyi 
from langchain_community.llms import Tongyi
from langchain_experimental.agents import create_pandas_dataframe_agent
from openai import OpenAI
import dashscope
from dashscope import MultiModalConversation
from http import HTTPStatus

os.environ["DASHSCOPE_API_KEY"] = "sk-a36dbf13c32f4b28a7dfc3ba81275fa8"

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


st.title('植物工厂LLM AI助手团队')
st.divider()
st.header('AI数据分析师工作区')

with st.sidebar:
    st.write('边栏')
    

#llms agents
#如果依照langchain的做法引入通义千问；但这样好像不好选模型
#好处是可能会比较兼容langchain的各种已有插件
langchain_llm = Tongyi(temperature = 0,
                     #api_key="sk-a36dbf13c32f4b28a7dfc3ba81275fa8",
                     #base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                     )

#还有一个办法是通过openai或者dashscope的sdk来引入
#

sdk_llm = OpenAI(#temperature = 0,
                    api_key="sk-a36dbf13c32f4b28a7dfc3ba81275fa8",
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                    
                    )
# 
@st.cache_data
def sdk_single_message_call(role_prompt, question):
    
  messages = [{'role': 'system', 'content': role_prompt},
              {'role': 'user', 'content': question}]

  response = dashscope.Generation.call(
      dashscope.Generation.Models.qwen_turbo,
      messages=messages,
      result_format='message',  # 将返回结果格式设置为 message
  )
  if response.status_code == HTTPStatus.OK:
      print(response)
  else:
      print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
          response.request_id, response.status_code,
          response.code, response.message
      ))

  return response['output']['choices'][0].message['content']

@st.cache_data
def sdk_single_picture_modal_call_locally(local_file_path1, local_file_path2, role_prompt, question):
    """Sample of use local file.
       linux&mac file schema: file:///home/images/test.png
       windows file schema: file://D:/images/abc.png
    """
    
    messages = [{
        'role': 'system',
        'content': [{
            'text': role_prompt
        }]
    }, {
        'role':
        'user',
        'content': [
            {
                'image': local_file_path1
            },
            {
                'image': local_file_path2
            },
            {
                'text': question
            },
        ]
    }]
    response = MultiModalConversation.call(model='qwen-vl-plus', messages=messages)
    print(response)

df = pd.DataFrame(data)

agent_data_analysit = create_pandas_dataframe_agent(langchain_llm, df, verbose=True,allow_dangerous_code=True)





if 'clicked' not in st.session_state:
    st.session_state.clicked = {1: False}

#function to update the value in session state
def clicked(button):
    st.session_state.clicked[button] = True

st.button('开始分析', on_click=clicked, args=[1])

if st.session_state.clicked[1]:
    st.subheader('开始分析')
    
    @st.cache_data
    def answer_one_question():
        steps_eda = langchain_llm('What are the steps of EDA?')
        return steps_eda
    
    @st.cache_data
    def data_analysis():
        st.write("**数据总览**")
        st.write(agent_data_analysit.run("这个df有什么信息"))
        st.write("**数据清洗**")
        missing_values = agent_data_analysit.run('这里面都有多少缺失数据')
        st.write(missing_values)
        st.write("**数据分析**")
        st.write(df.describe())
        corr_anals = agent_data_analysit.run('统计一下这个df各参数间的相关性')
        st.write(corr_anals)
    
    @st.cache_data
    def function_question_variable():
        st.line_chart(df, y=[user_chosen_variable])
        summary_statistics = agent_data_analysit.run(f'帮我总结下{user_chosen_variable}的数据')
        st.write(summary_statistics)
        normality = agent_data_analysit.run(f'帮我看看{user_chosen_variable}是否符合正态分布')
        st.write(normality)
        
        distribution = agent_data_analysit.run(f'帮我看看{user_chosen_variable}是否符合正态分布')
        st.write(distribution)
        
        trends = agent_data_analysit.run(f'帮我分析下{user_chosen_variable}的趋势')
        st.write(trends)
        
        
        return
    
    with st.expander('数据分析'):
        question = '请解释下每列数据含义'
        columns_meaning = agent_data_analysit.run(question)
        st.write(columns_meaning)
        data_analysis()
    
    with st.expander('回答问题'):
        st.write(answer_one_question())

        user_chosen_variable = st.selectbox("选择你所感兴趣的参数",options=df.columns, index = 0)
        function_question_variable()
