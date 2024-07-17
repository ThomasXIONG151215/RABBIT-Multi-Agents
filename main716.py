import streamlit as st 
import os 
import pandas as pd 
import numpy as np
from langchain.llms import openai, tongyi 
from langchain_community.llms import Tongyi
from langchain_community.llms.moonshot import Moonshot
from langchain_experimental.agents import create_pandas_dataframe_agent
from openai import OpenAI
import dashscope
from dashscope import MultiModalConversation
from http import HTTPStatus
import plotly.graph_objects as go
import requests
from dataset import df
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents.agent_types import AgentType
from langchain.utilities import WikipediaAPIWrapper
import streamlit.components.v1 as components
from chat_tools import data_analysis, manual_chat
import datetime
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document


os.environ["DASHSCOPE_API_KEY"] = "sk-a36dbf13c32f4b28a7dfc3ba81275fa8"
os.environ["MOONSHOT_API_KEY"] = "sk-wQJ6rfZixFKs8eKyPmAzXBfS1qdObnPbCIEoMyr6nq3i4IMd"


st.set_page_config(
   page_title="Mars PFAL AI App",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)
st.title('星际植物工厂AI助手')
st.divider()

# Sidebar with star system information
with st.sidebar:
    st.header('星际方位')
    st.text('当前位置：银河系')
    st.text('星际坐标：X:1234 Y:5678 Z:91011')

    apod_url = "nasa_pic1.jpeg"

    st.image(apod_url, caption='今日舱外风景', use_column_width=True)

if 'clicked' not in st.session_state:
    st.session_state.clicked = {1: False}

# 初始化session state，如果它还不存在的话
if 'new_info' not in st.session_state:
    st.session_state.new_info = ""

state_new_info = st.session_state.new_info

#function to update the value in session state
def clicked(button):
    st.session_state.clicked[button] = True

def store_txt(new_info):
    # 定义星系名称和坐标
    galaxy_name = "Milky Way"
    coordinates = "X123Y456Z789"
    # 目标目录，假设是在当前工作目录下的 'knowledge' 文件夹
    target_directory = "knowledge"

    # 获取当前的日期和时间
    current_time = datetime.datetime.now()
    formatted_datetime = current_time.strftime("%Y-%m-%d %H:%M:%S")

    knowledge_with_timestamp = f"{formatted_datetime}\n{new_info}"

    # 构造文件名
    file_name = f"{galaxy_name}_{coordinates}_{current_time.strftime('%Y%m%d_%H%M')}.txt"
    file_name = 'Milky_Way_Planting_Log.txt'

    # 创建目录，如果它还不存在
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # 文件名，您可以根据需要更改
    file_path = os.path.join(target_directory, file_name)

    # 将文本数据写入文件
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(knowledge_with_timestamp)

    st.info('新知识已成功保存')

st.header('数据总览')

with st.expander('**数据表**'):
    st.write(df)

with st.expander("查看图片"):
    # 创建两列
    col1, col2 = st.columns(2)

    # 在第一列中显示第一张图片
    with col1:
        st.write('**1号种植舱**')
        st.info('滚筒式结构｜意大利生菜')
        st.image('canopy1.jpg', use_column_width=True)

    # 在第二列中显示第二张图片
    with col2:
        st.write('**2号种植舱**')
        st.info('平板式结构｜翠恬生菜')
        st.image('canopy2.jpg', use_column_width=True)


with st.expander('**环境数据**'):
#st.write('**数据图**')

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df.index, y=df['Indoor Temperature (°C)'],
                            mode='lines', name='室内温度',
                            line=dict(color='rgb(255, 99, 71)')))
    fig1.add_trace(go.Scatter(x=df.index, y=df['Outdoor Temperature (°C)'],
                            mode='lines', name='室外温度',
                            line=dict(color='rgb(135, 206, 235)')))
    fig1.update_layout(
        showlegend=True,  # 显示图例
        legend=dict(
            orientation="h",  # 图例水平排列
            x=0.05,  # 图例的x坐标
            y=-0.2,  # 图例的y坐标
            traceorder="normal",
            font=dict(size=16),  # 改变图例字体大小
        ),
        #margin=dict(l=0, r=0, t=0, b=0),  # 移除边距，使图表紧贴容器
        #autosize=True,  # 自动调整大小
        uniformtext_minsize=12,  # 统一文本的最小尺寸
        #uniformtext_mode='hide',  # 如果文本重叠则隐藏
        #title=dict(text="能耗饼图", font=dict(size=20)),  # 标题及字体大小
    )
    fig1.update_layout(width=1000, height=600) 
    st.plotly_chart(fig1)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df.index, y=df['Indoor Humidity (%)'],
                            mode='lines', name='室内湿度',
                            line=dict(color='rgb(255, 165, 0)')))
    fig2.add_trace(go.Scatter(x=df.index, y=df['Outdoor Humidity (%)'],
                            mode='lines', name='室外湿度',
                            line=dict(color='rgb(0, 191, 255)')))
    fig2.update_layout(
        showlegend=True,  # 显示图例
        legend=dict(
            orientation="h",  # 图例水平排列
            x=0.05,  # 图例的x坐标
            y=-0.2,  # 图例的y坐标
            traceorder="normal",
            font=dict(size=16),  # 改变图例字体大小
        ),
        #margin=dict(l=0, r=0, t=0, b=0),  # 移除边距，使图表紧贴容器
        autosize=True,  # 自动调整大小
        uniformtext_minsize=12,  # 统一文本的最小尺寸
        uniformtext_mode='hide',  # 如果文本重叠则隐藏
        #title=dict(text="能耗饼图", font=dict(size=20)),  # 标题及字体大小
    )
    st.plotly_chart(fig2)

with st.expander('能耗数据'):
    data = {
'Energy Type': ['LED Energy Consumption (kWh)', 'AC Energy Consumption (kWh)', 'Water Pump Energy Consumption (kWh)'],
'Energy Consumption': [100, 200, 150]
}
    df = pd.DataFrame(data)

    # 创建Plotly Pie Chart
    fig = go.Figure(data=[go.Pie(labels=df['Energy Type'], values=df['Energy Consumption'])])

    # 更新图表布局
    fig.update_layout(
        showlegend=True,  # 显示图例
        legend=dict(
            orientation="h",  # 图例水平排列
            x=0.05,  # 图例的x坐标
            y=-0.2,  # 图例的y坐标
            traceorder="normal",
            font=dict(size=16),  # 改变图例字体大小
        ),
        #margin=dict(l=0, r=0, t=0, b=0),  # 移除边距，使图表紧贴容器
        #autosize=True,  # 自动调整大小
        uniformtext_minsize=12,  # 统一文本的最小尺寸
        uniformtext_mode='hide',  # 如果文本重叠则隐藏
        #title=dict(text="能耗饼图", font=dict(size=20)),  # 标题及字体大小
    )

    # 在Streamlit中显示图表
    st.plotly_chart(fig)

        

st.header('嫦娥兔 AI Agent工作区')

ai_analyst, ai_assistant, ai_mechanist = st.tabs(['AI数据分析师','AI助理农艺师','AI机械工程师'])

with ai_analyst:
    st.subheader('交互问答')
    #new_knowledge = ""
    prompt = st.chat_input('请输入你感兴趣的问题')
    if prompt:
        message, my_data_problem = manual_chat(prompt)
        message.write(my_data_problem)
        state_new_info += my_data_problem

    st.subheader('自动分析')
    start_anal = st.button('开始回答预设问题', on_click=clicked, args=[1])

    with st.expander('自动分析'):
        if start_anal:
            combined_info = data_analysis()

            state_new_info += combined_info
            st.info('Done')
    #st.write(new_knowledge)

    st.subheader('保存新知识')
    store_info = st.button('按下保存分析结果作为新知识')
    with st.expander('保存新知识'):
        if store_info:
            store_txt(state_new_info) #只是保存，还没有清零当前状态


    def test_dify_client():
        import requests
        import json 
 
        
        url = "https://api.dify.ai/v1/chat-messages"

        headers = {
            'Authorization': 'Bearer app-hTghItxhCBRwRUwhOVu7b8s6',
            'Content-Type': 'application/json',
        }

        data = {
            "inputs": {},
            "query": "如何种植意大利生菜?",
            "response_mode": "streaming",
            "conversation_id":"",
            "user": "abc-123" 
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))

        with st.chat_message("assistant"):
            st.write(response.json())
    if st.button('test dify'):
        test_dify_client()
    

with ai_assistant: 
    st.write('人类工程师直接表明下一步想解决的问题，在进行RAG之前就缩小文档知识范围帮助准确提炼')

    label_list = st.multiselect('选择标签',['培训操作','提升生菜产能','改善番茄种植','节能增效','调整光照'])

    doc_list = []

    label_to_docs = {
        '培训操作':['基础综述','紧急情况手册'],
        '提升生菜产能':['红罗马生菜种植操作指南','意大利生菜种植操作指南'],
        '改善番茄种植':['番茄种植操作指南'],
        '节能增效':['LED灯具操作指南'],
        '调整光照':['LED灯具操作指南'],
    }

    for label in label_list:
        for doc in label_to_docs[label]:
            if doc not in doc_list:
                doc_list.append(doc)

    #st.success(f'这一环节适合的文档有{[doc for doc in doc_list]}')

    docs_md = '\n'.join([f'- {doc}' for doc in doc_list])

    avatar = ':material/cruelty_free:'
    message = st.chat_message(name="ai",
                            avatar=avatar
                            )
    
    message.markdown(f'这一环节适合的文档有:\n{docs_md}')

    to_read_content = ""
    for doc in doc_list:

        markdown_path = f"knowledge/{doc}.md"
        loader = UnstructuredMarkdownLoader(markdown_path)

        data = loader.load()
        assert len(data) == 1
        assert isinstance(data[0], Document)
        readme_content = data[0].page_content

        to_read_content += readme_content

    st.write(to_read_content)



    with st.expander('语音交互框'):
        components.iframe("https://webdemo-global.agora.io/example/basic/basicLive/index.html",
                                    height=400,
                                    scrolling=True)

                    
with ai_mechanist:
    if st.button('清零状态信息'):
        #完成一整个流程的设定后就可以把session state清零了
        state_new_info = ""  
                    
                