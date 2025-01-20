import openai
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import time


def show():
    load_dotenv()


    st.title("Hello")
    llm = ChatOpenAI(model="gpt-4o")

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
        if percent_complete == 50:
            prompt = (
                f"You are an assistant helping with recruitment interviews. You have two main functionalities: "
                f'1. "Analyze CV" and 2. "Technical Review." Introduce yourself warmly, explain your purpose, '
                f"and inform the user about the available options. Make the message professional, engaging, "
                f"and friendly. Highlight how each functionality can help the user prepare effectively for their interview."
            )

            llm_response = llm.invoke(prompt)
        elif percent_complete == 99:
            with st.chat_message("assistant"):
                st.markdown(llm_response.content)


    time.sleep(1)
    my_bar.empty()




