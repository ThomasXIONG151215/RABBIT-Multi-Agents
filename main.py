import streamlit as st 
import os 
import pandas as pd 
from openai import OpenAI
import plotly.graph_objects as go
from dataset import df
from chat_tools import data_analysis, manual_chat
import datetime
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
from chat_tools import moonshot_llm

os.environ["DASHSCOPE_API_KEY"] = "sk-a36dbf13c32f4b28a7dfc3ba81275fa8"
os.environ["MOONSHOT_API_KEY"] = "sk-wQJ6rfZixFKs8eKyPmAzXBfS1qdObnPbCIEoMyr6nq3i4IMd"


st.set_page_config(
   page_title="Mars PFAL AI App",
   page_icon="🥬",
   layout="wide",
   initial_sidebar_state="expanded",
)
st.title('🥬🤖星际植物工厂AI助手')

st.write("**未来火星城植物工厂**")
st.image("./images/mars_pfal.png", 
         #caption="未来火星城植物工厂"
         )

st.divider()

col1, col2 = st.columns(2)

# 在第一列中显示第一张图片
with col1:
    st.write('**1号种植舱**')
    st.info('滚筒式结构｜意大利生菜')
    st.image('./images/canopy1.jpg', use_column_width=True)

# 在第二列中显示第二张图片
with col2:
    st.write('**2号种植舱**')
    st.info('平板式结构｜翠恬生菜')
    st.image('./images/canopy2.jpg', use_column_width=True)

st.divider()

# Sidebar with star system information 
with st.sidebar:
    st.header('星际方位')
    st.text('当前位置：银河系')
    st.text('星际坐标：X:1234 Y:5678 Z:91011')

    st.image("./images/mars_city.jpeg", caption="今日未来火星城")

    st.image("./images/nasa_pic1.jpeg", caption='今日卫星捕捉风景', use_column_width=True)


if 'clicked' not in st.session_state:
    st.session_state.clicked = {1: False}

# 初始化session state，如果它还不存在的话
if 'new_info' not in st.session_state:
    st.session_state.new_info = ""

state_new_info = st.session_state.new_info

if 'ai_assistant_suggestion' not in st.session_state:
    st.session_state.ai_assistant_suggestion = ""

ai_assistant_suggestion = st.session_state.ai_assistant_suggestion

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


with st.expander('**数据可视化数据**'):

    canopy_fig = go.Figure()
    canopy_fig.add_trace(go.Scatter(x=df.index, y=df['Growth Rate (mm/day)'],
                            mode='lines', name='1号种植舱植物长势',
                            line=dict(color='rgb(255, 99, 71)')))
    canopy_fig.add_trace(go.Scatter(x=df.index, y=df['Growth Rate2 (mm/day)'],
                            mode='lines', name='2号种植舱植物长势',
                            line=dict(color='rgb(255, 99, 71)')))
    canopy_fig.update_layout(
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
    canopy_fig.update_layout(width=500, height=300) 
    #Growth Rate (mm/day)


    index_fig = go.Figure()
    index_fig.add_trace(go.Scatter(x=df.index, y=df['Harvest Index'],
                            mode='lines', name='1号种植舱收成指数',
                            line=dict(color='rgb(255, 99, 71)')))
    index_fig.add_trace(go.Scatter(x=df.index, y=df['Harvest Index2'],
                            mode='lines', name='2号种植舱收成指数',
                            line=dict(color='rgb(255, 99, 71)')))
    index_fig.update_layout(
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
    index_fig.update_layout(width=500, height=300) 
    #Growth Rate (mm/day)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df.index, y=df['Indoor Temperature (°C)'],
                            mode='lines', name='室内温度',
                            line=dict(color='rgb(255, 99, 71)')))
    fig1.add_trace(go.Scatter(x=df.index, y=df['Outdoor Temperature (°C)'],
                            mode='lines', name='火星温度',
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
    fig1.update_layout(width=500, height=300) 
    

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df.index, y=df['Indoor Humidity (%)'],
                            mode='lines', name='室内湿度',
                            line=dict(color='rgb(255, 165, 0)')))
    fig2.add_trace(go.Scatter(x=df.index, y=df['Outdoor Humidity (%)'],
                            mode='lines', name='火星湿度',
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
    fig2.update_layout(width=500, height=300) 
    

    data = {
'Energy Type': ['LED能耗 (kWh)', '空调能耗 (kWh)', '水泵能耗 (kWh)'],
'Energy Consumption': [100, 200, 150]
}
    df = pd.DataFrame(data)

    # 创建Plotly Pie Chart
    fig_pie = go.Figure(data=[go.Pie(labels=df['Energy Type'], values=df['Energy Consumption'])])

    # 更新图表布局
    fig_pie.update_layout(
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
    fig_pie.update_layout(width=500, height=600) 

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(canopy_fig)
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
    with col2:
        st.plotly_chart(index_fig)
        st.plotly_chart(fig_pie)
        

st.header('AI Agent工作区')

ai_analyst, ai_assistant, ai_mechanist = st.tabs(['AI数据分析师','AI助理农艺师','AI执行工程师'])

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
    if store_info:
        store_txt(state_new_info) #只是保存，还没有清零当前状态

def moonshot_super_user_prompt(): #ai助理农艺师根据上一个步骤的ai数据分析师的分析结果生成的下一步提示词。
    super_prompt = "你是一个认真，专注，积极向上的助理农艺师，\
    最近的种植情况是这样子的{state_new_info},\
    目前我们想解决的问题在这个字符串数组当中{label_list},\
    具体的问题则是{further_prompt},\
    希望你从这些上下文的问题中中提炼出可能有帮助的信息\
    "
    #answer = moonshot_llm(super_prompt)

    return super_prompt 

import httpx 
from typing import *
from pathlib import Path


#直接一个prompt解决问题形式的rag
@st.cache_resource
def direct_caching(doc_list):
    to_read_content = ""
    for doc in doc_list:

        markdown_path = f"knowledge/{doc}"
        loader = UnstructuredMarkdownLoader(markdown_path)

        data = loader.load()
        assert len(data) == 1
        assert isinstance(data[0], Document)
        readme_content = data[0].page_content

        to_read_content += readme_content
    
    return to_read_content


#上下文缓存应用形式的rag
@st.cache_resource
def moonshot_caching(doc_list, cache_tag):
    """
    :param files: 一个包含要上传文件的路径的列表，路径可以是绝对路径也可以是相对路径，请使用字符串
        的形式传递文件路径。
    :param cache_tag: 设置 Context Caching 的 tag 值，你可以将 tag 理解为自定义的 Cache 名称，
        当你设置了 cache_tag 的值，就意味着启用 Context Caching 功能，默认缓存时间是 300 秒，每次
        携带缓存进行 `/v1/chat/completions` 请求都将刷新缓存存活时间（300 秒）。
    :return: 一个包含了文件内容或文件缓存的 messages 列表，请将这些 messages 加入到 Context 中，
        即请求 `/v1/chat/completions` 接口时的 messages 参数中。
    """
    
    messages = []

    # 对每个文件路径，我们都会上传文件并抽取文件内容，最后生成一个 role 为 system 的 message，并加入
    # 到最终返回的 messages 列表中。
    for doc in doc_list:
        file_path = f"knowledge/{doc}"
        file_object = client.files.create(file=Path(file_path),purpose="file-extract")
        file_content = client.files.content(file_id=file_object.id).text
        messages.append({
            "role":"system",
            "content": file_content,
        })

    if cache_tag:
        r = httpx.post(f"{client.base_url}caching",
                       headers={
                           "Authorization":f"Bearer {client.api_key}",
                       },
                       json={
                           "model": "moonshot-v1",
                           "messages": messages,
                           "ttl": 300, #缓存时间（秒），可以延长
                           "tags": [cache_tag],
                       })
        if r.status_code != 200:
            raise Exception(r.text)
    else:
        return messages

with ai_assistant: 
    st.write('人类工程师直接表明下一步想解决的问题，在进行RAG之前就缩小文档知识范围帮助准确提炼')
    client = OpenAI(
        base_url="https://api.moonshot.cn/v1",
        api_key=os.environ["MOONSHOT_API_KEY"]
    )
    label_list = st.multiselect('选择标签',['培训操作','提升生菜产能','改善番茄种植','节能增效','调整光照'])

    doc_list = []

    label_to_docs = {
        '培训操作':['基础综述.md','紧急情况手册.md'],
        '提升生菜产能':['红罗马生菜种植操作指南.md','意大利生菜种植操作指南.md'],
        '改善番茄种植':['番茄种植操作指南.md'],
        '节能增效':['LED灯具操作指南.md'],
        '调整光照':['LED灯具操作指南.md'],
    }

    for label in label_list:
        for doc in label_to_docs[label]:
            if doc not in doc_list:
                doc_list.append(doc)

    docs_md = '\n'.join([f'- {doc}' for doc in doc_list])

    avatar = ':material/cruelty_free:'

    further_prompt = st.chat_input('请进一步标明想要解决的问题')
    if further_prompt:

        message_bar = st.chat_message(name="ai",
                                avatar=avatar
                                )
        
        message_bar.markdown(f'这一环节适合的文档有:\n{docs_md}')
        message_bar.success('启动moonshot上下文缓存功能吸取选定文档内容')

        moonshot_caching_rag_content = moonshot_caching(doc_list=doc_list,
                                                 cache_tag='test'
                                                 )
        direct_caching_rag_content = direct_caching(doc_list)
        input_messages = [
            #*moonshot_caching_rag_content,
            {
            "role":"system",
            "content": direct_caching_rag_content,
            },   
            {
                "role": "system",
            "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，"
                       "准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不"
                       "可翻译成其他语言。",
            },
            {
                "role": "user",
                "content": f"你是一个认真，专注，积极向上的助理农艺师，\
                            最近的种植情况是这样子的{state_new_info},\
                            目前我们想解决的问题在这个字符串数组当中{label_list},\
                            具体的问题则是{further_prompt},\
                            希望你从这些上下文的问题中中提炼出可能有帮助的信息\
                            你提供的信息最多两百个字。\
                            "
            }]

        completion = client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=input_messages,
        )
        ai_assistant_suggestion = completion.choices[0].message.content
        message_bar.write(ai_assistant_suggestion)


def optimal_conditions_plot(name,values_right,values_left, show_legend):
# 创建条形图
    fig = go.Figure()

    # 添加向右展开的条形图
    fig.add_trace(go.Bar(
        x=values_right,
        y=labels,
        name=f'理想水平',
        orientation='h',
        marker_color='rgba(50, 171, 96, 0.6)',  # 右侧条形图颜色
        width=0.2,
    ))

    # 添加向左展开的条形图
    fig.add_trace(go.Bar(
        x=values_left,
        y=labels,
        name=f'实际水平',
        orientation='h',
        marker_color='rgba(245, 130, 48, 0.6)',  # 左侧条形图颜色
        width=0.2,
    ))

    # 更新布局以适应左右展开的条形图
    fig.update_layout(
        barmode='relative',  # 设置为相对模式，以便条形图可以向两边展开
        xaxis=dict(showticklabels=False),  # 设置x轴为线性模式
        title_text=f'{name}理想条件与当前条件对比',  # 图表标题
        showlegend=show_legend,  # 显示图例
        width=400,
        height=600
    )
    return fig


def moonshot_short_summarize(info_to_sum):
    input_messages = [
            {
                "role": "system",
            "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。"
            },
            {
                "role": "user",
                "content": f"\
                            总结下这段话{info_to_sum}\
                            你提供的信息最多两百个字。\
                            "
            }]

    completion = client.chat.completions.create(
        model="moonshot-v1-128k",
        messages=input_messages,
    )
    summarized_text = completion.choices[0].message.content

    return summarized_text


with ai_mechanist:
    st.subheader('当前已知的品种特性')
    st.write('这里呈现通过长短期累积下来的种植经验判断的果蔬品种最喜欢的环境条件，人类工程师可以在这里和AI执行工程师继续调整环境控制系统')

    # 示例数据
    labels = ['湿度(%)', '温度(C)', 'CO2浓度(ppm)', '光强(mm/m2.s)']
    oak_optimal = [3, 4, 4, 2]  # 向右展开的条形图数据
    oak_current = [-1, -3, -3, -1.8]  # 向左展开的条形图数据

    romaine_optimal = [5, 2, 5, 1]  # 向右展开的条形图数据
    romaine_current = [-4, -3, -4.5, -0.8]  # 向左展开的条形图数据

    oak_fig = optimal_conditions_plot("意大利生菜",oak_optimal,oak_current, False)
    romaine_fig = optimal_conditions_plot("红罗马生菜", romaine_optimal, romaine_current, True)

    col1, col2 = st.columns(2)
    with col1:
    # 在Streamlit中显示图
        st.plotly_chart(oak_fig)
    with col2:
        st.plotly_chart(romaine_fig)

    with st.expander('AI数据分析师与AI助理农艺师的分析建议'):
        if state_new_info!="":
            #完成一整个流程的设定后就可以把session state清零了
            st.write("AI数据分析师的建议")
            analyst_message_bar = st.chat_message(name="AI数据分析师",
                                    avatar=avatar)
            
            analyst_summarize = moonshot_short_summarize(state_new_info)

            analyst_message_bar.write(analyst_summarize)

        if ai_assistant_suggestion!="":
            st.write("AI助理农艺师的建议")
            assistant_message_bar = st.chat_message(name="AI助理农艺师",
                                    avatar=avatar)
            assistant_summarize = moonshot_short_summarize(ai_assistant_suggestion)
            assistant_message_bar.write(assistant_summarize)

    st.subheader('控制面板')
    st.write('根据前面的长期经验和最新知识，AI执行工程师可以自行调控设备参数，持续优化植物生长条件')
    def controller(type_of, name, value, max_value):
        if type_of == 'slider':
            st.slider(name, value=value, max_value=max_value, min_value=0)
        elif type_of == 'input':
            st.number_input(name, value=value, max_value=max_value, min_value=0)

    ac_powers, led_powers, pH_set, EC_set, Arm_freq, CO2_ppm = 30, 40, 3, 4, 29,800
    max_ac_powers, max_led_powers, max_pH_set,max_EC_set, max_Arm_freq, max_CO2_ppm = 100, 100, 6, 14, 60,2000

    col1, col2 = st.columns(2)

    with col1:
        controller('input','空调输出强度', ac_powers, max_ac_powers)
        controller('input', 'LED灯光强', led_powers, max_led_powers)
        controller('slider', 'CO2浓度', CO2_ppm, max_CO2_ppm)

    with col2:
        controller('slider', 'LED灯光强', led_powers, max_led_powers)
        controller('slider', '营养液pH值', pH_set, max_pH_set)
        controller('slider', '营养液EC值', EC_set, max_EC_set)
    
    controller('slider', '机械臂运作采收周期', Arm_freq, max_Arm_freq) 

    update_button = st.button("执行工程师自动调整控制参数")

    

    if st.button('清零状态信息'):
        state_new_info = ""
                    
