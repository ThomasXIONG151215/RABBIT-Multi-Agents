import streamlit as st 
import pyttsx3
from langchain.prompts import PromptTemplate
import streamlit as st 
import os 
import pandas as pd 
from langchain_community.llms import Tongyi
from langchain_community.llms.moonshot import Moonshot
from langchain_experimental.agents import create_pandas_dataframe_agent
from dashscope import MultiModalConversation
from dataset import df

os.environ["DASHSCOPE_API_KEY"] = "sk-a36dbf13c32f4b28a7dfc3ba81275fa8"
os.environ["MOONSHOT_API_KEY"] = "sk-wQJ6rfZixFKs8eKyPmAzXBfS1qdObnPbCIEoMyr6nq3i4IMd"

#llms agents
langchain_llm = Tongyi(temperature = 0,
                     #api_key="sk-a36dbf13c32f4b28a7dfc3ba81275fa8",
                     #base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                     )

moonshot_llm = Moonshot(model="moonshot-v1-128k") 

agent_data_analyst = create_pandas_dataframe_agent(langchain_llm, df, verbose=True,allow_dangerous_code=True)

@st.cache_data 
def data_analysis():
    preset_question1 = "**这里是否缺失数据?**"
    st.write(preset_question1)
    avatar = ':material/cruelty_free:'
    message = st.chat_message(name="ai",
                                avatar=avatar
                                ) 
    answer1 = agent_data_analyst.run(preset_question1)
    message.write(answer1)

    #text_to_audio(missing_values)

    preset_question2 = "**请对当前种植情况做一个整体评价**"
    st.write(preset_question2)
    message = st.chat_message(name="ai",
                                avatar=avatar
                                )
    answer2 = agent_data_analyst.run(preset_question2+"，请做出批判性评价")
    message.write(answer2)
    #text_to_audio(missing_values)

    preset_question3 = "**当前室内温度对作物的影响如何？**"
    st.write(preset_question3)
    message = st.chat_message(name="ai",
                                avatar=avatar
                                )
    answer3 = agent_data_analyst.run(preset_question3)
    message.write(answer3)

    combined_info = preset_question1 + "\n" + answer1 + "\n" +  preset_question2 + "\n" + answer2 + "\n" +  preset_question3 + "\n"+ answer3

    return combined_info

@st.cache_resource
def manual_chat(prompt):
    my_data_problem = agent_data_analyst.run(prompt)
    avatar = ':material/cruelty_free:'
    message = st.chat_message(name="ai",
                            avatar=avatar
                            )
    return message, my_data_problem

def text_to_audio(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

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


@st.cache_data #图像识别
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