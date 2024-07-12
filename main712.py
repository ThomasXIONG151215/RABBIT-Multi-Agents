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

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents.agent_types import AgentType
from langchain.utilities import WikipediaAPIWrapper

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
    
    @st.cache_data #保存结构化数据结果；出来的结果每次都是新的，不会因为前面一个session变过它，后面它就变
    #它会每次单独把计算结果做一个copy，所以不同的用户使用该函数并对函数结果进行修改都会得到相同结果
    #但是cache_resource是反过来，它不做任何copy，上线后大家看到的都是一样的。
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
    
    @st.cache_resource #保存的是非结构化数据，你不想重复加载的database connections，所以你session更新后它会保留前面的变化
    def wiki(prompt):
        wiki_research = WikipediaAPIWrapper().run(prompt)
        return wiki_research
    
    @st.cache_data
    def prompt_templated():
        data_problem_prompt_template = PromptTemplate(
            input_variables=['problem'],
            template='Convert the following problem into a data science problem:{problem}'
        )
        
        model_selection_prompt_template = PromptTemplate(
            input_variables=['data_problem'],
            template='List the name of the machine learning algorithms (only the name) that are suitable to solve this problem:{data_problem}, while using this Wikipedia research:{wiki_research}'
        )
        
        return data_problem_prompt_template, model_selection_prompt_template
    
    @st.cache_data
    def chains():
        data_problem_chain = LLMChain(llm=langchain_llm, 
                                      prompt=prompt_templated()[0],
                                      verbose=True,
                                      output_key='data_problem',
                                      )
        
        model_selection_chain = LLMChain(llm=langchain_llm,
                                      prompt=prompt_templated()[1],
                                      verbose=True,
                                      output_key='model_selection'
                                      )
        
        sequential_chain = SequentialChain(chains=[data_problem_chain, model_selection_chain],
                                                 input_variables=['problem','wiki_research'],
                                                 #output_key=['data_problem', 'model_selection'],
                                                 verbose=True,
                                                 #chain_type="stuff"
                                                 )
    
        return sequential_chain
    
    @st.cache_data
    def list_to_selectbox(my_model_selection):
        algorithm_lines = my_model_selection.split('\n')
        algorithms = [algorithm.split(':')[-1].split('.')[-1].strip() for algorithm in algorithm_lines if algorithm.strip()]
        algorithms.insert(0, "选择算法")
        formatted_list_output = [f"{algorithm}" for algorithm in algorithms if algorithm]
        return formatted_list_output
    
    def chains_output(prompt, wiki_research):
        my_chain = chains()
        my_chain_output = my_chain({"problem": prompt, "wiki_research": wiki_research})
        my_data_problem = my_chain_output['problem']
        my_model_selection = my_chain_output['model_selection']
        return my_data_problem, my_model_selection

    @st.cache_resource
    def python_agent():
        agent_executor = create_python_agent(
            llm=langchain_llm,
            tool=PythonREPLTool(),
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,

        )
        return agent_executor

    @st.cache_data
    def python_solution(my_data_problem, selected_algorithm, user_csv):
        
        solution = python_agent().run(f"Write a python script to solve this: {my_data_problem}, using this algorithm:{selected_algorithm} using this dataset {user_csv}")
    
        return solution
    
    with st.expander('数据分析'):
        question = '请解释下每列数据含义'
        #columns_meaning = agent_data_analysit.run(question)
        st.write('解释')
        #st.write(columns_meaning)
        #data_analysis()
    
    with st.expander('回答问题'):
        #st.write(answer_one_question())

        user_chosen_variable = st.selectbox("选择你所感兴趣的参数",options=df.columns, index = 0)
        #function_question_variable()

        data_problem_prompt_template, model_selection_prompt_template = prompt_templated()
        
        prompt = st.text_area('请输入你感兴趣的问题')
        if prompt:
            wiki_research = wiki(prompt)
            my_data_problem, my_model_selection = chains_output(prompt, wiki_research)
            #response = sequential_chain({'problem': prompt})
            st.write(my_data_problem)
            st.write(my_model_selection)
            #st.write(response['model_selection'])
            formatted_list = list_to_selectbox(my_model_selection)
            selected_algorithm = st.selectbox("选择机器学习算法", formatted_list)
            
            
            if selected_algorithm is not None and selected_algorithm != "选择算法":
                
                solution = python_solution(my_data_problem, selected_algorithm, df)
                st.write(solution)
            
            
            
        