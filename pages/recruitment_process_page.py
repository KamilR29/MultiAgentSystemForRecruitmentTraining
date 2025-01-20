import os

from dotenv import load_dotenv
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from typing import Literal
from langgraph.graph import StateGraph, START,END
import streamlit as st


def initialize_state():
    if "graph_state" not in st.session_state:
        st.session_state.graph_state = []

def get_last_message():

    if st.session_state.graph_state:
        return st.session_state.graph_state[-2]
    else:
        return None


def add_message(role, content):
    st.session_state.graph_state.append({"role": role, "content": content})



def display_messages():
    for message in st.session_state.graph_state:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def options():
    with st.sidebar:
        st.subheader("Select Technologies")

        technologies = [
            "AI/ML", "JS", "HTML", "PHP", "Ruby", "Python", "Java", ".NET", "Scala", "C",
            "Mobile", "Testing", "DevOps", "Admin", "UX/UI", "PM", "Game",
            "Analytics", "Security", "Data", "Go", "Support", "ERP"
        ]

        selected_technologies = st.multiselect(
            "Choose technologies:",
            technologies
        )

        st.subheader("Select Job Level")
        job_level = st.selectbox(
            "Choose the job level:",
            ["Chose level","Junior", "Mid", "Senior"]
        )
        programming_languages = str(selected_technologies)
        job_level = str(job_level)
        flag = True
        st.text('Chose the options and write "hi" to start recruitment process')

    if selected_technologies != [] and job_level != "Chose level":
        app(programming_languages, job_level, flag)


def app(programming_languages, job_level, flag):


    initialize_state()
    load_dotenv()

    class State(TypedDict):
        graph_state: str

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the .env file")

    llm = ChatOpenAI(model="gpt-4o")


    def rating_node(state):
        # st.text("--- rating_node ---")
        sys_message = state["graph_state"][-2]["content"]
        last_message = state["graph_state"][-1]

        rating_prompt = (
            f"You are a professional recruiter specializing in hiring developers for roles involving {programming_languages}. "
            f"The candidates are being recruited for positions at the {job_level} level. "
            f"Your task is to rate the answer for the question. Based on your expertise as a recruiter, evaluate the given answer. "
            f"The question is: {sys_message}. Rate the answer to the question: {last_message['content']} on a scale of 1-10. Return only a number, nothing else."
        )

        llm_response = llm.invoke(rating_prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_response.content)
        add_message("assistant", llm_response.content)
        state["graph_state"].append({"role": "assistant", "content": llm_response.content})
        return state

    def model_answer_node(state):

        last_message = state["graph_state"][-3]
        question = last_message["content"]

        model_answer_prompt = (
            f"You are a professional recruiter specializing in hiring developers for roles involving {programming_languages}. "
            f"The candidates are being recruited for positions at the {job_level} level. Based on your expertise as a recruiter, "
            f"and developer write a model answer for that question: {question}. The answer shouldn't be long. Focus on the most important information."
        )
        # model_answer_prompt = (
        #     f" Write short answer for that question: {question}"
        # )

        llm_response = llm.invoke(model_answer_prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_response.content)
        st.session_state.graph_state = state["graph_state"]
        state["graph_state"].append({"role": "assistant", "content": llm_response.content})
        return state

    def congratulation_node(state):
        last_message = state["graph_state"][-3]
        last_message_content = last_message["content"]

        congratulation_prompt = (
            f"You are a professional recruiter specializing in hiring developers for roles involving {programming_languages}. "
            f"The candidates are being recruited for positions at the {job_level} level. Evaluate the provided answer: {last_message_content}. "
            f"If the answer is good, congratulate the candidate and return a concise list of the key strengths or positive aspects of the answer."
        )

        llm_response = llm.invoke(congratulation_prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_response.content)
        add_message("assistant", llm_response.content)
        state["graph_state"].append({"role": "assistant", "content": llm_response.content})
        return state

    def checking_node(state):
        last_messages = state["graph_state"][-5:] if len(state["graph_state"]) >= 5 else state["graph_state"]
        messages_content = [str(msg["content"]) for msg in last_messages if "content" in msg]
        combined_content = "\n".join(messages_content)

        analysis_prompt = (
            f"You are a professional recruiter specializing in hiring developers for roles involving {programming_languages}. "
            f"The candidates are being recruited for positions at the {job_level} level. Analyze the following messages and "
            f"identify the areas where the user struggles the most. Return a short list of things worth revising. "
            f"Analyze these messages: {combined_content}. Return only a short list of points."
        )

        llm_response = llm.invoke(analysis_prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_response.content)
        # st.session_state.graph_state = state["graph_state"]
        add_message("assistant", llm_response.content)

        new_question_prompt = (
            f"You are a professional recruiter specializing in hiring developers for roles involving {programming_languages}. "
            f"The candidates are being recruited for positions at the {job_level} level. Your sole task is to ask professional "
            f"and relevant interview questions appropriate for this role. Do not provide any explanations, feedback, or additional "
            f"commentary—focus exclusively on formulating the questions. One question should be specific for one language. Ask only one question."
        )

        state["graph_state"].append({"role": "assistant", "content": new_question_prompt})
        return state

    def rating_mode(state) -> Literal["model_answer_node", "congratulation_node"]:
        last_message = state["graph_state"][-1]
        last_message_content = last_message["content"]
        try:
            if int(last_message_content) < 7:
                return "model_answer_node"
            return "congratulation_node"
        except ValueError:

            print(f"Nieprawidłowa wartość oceny: {last_message_content}")
            return "model_answer_node"




    builder1 = StateGraph(State)
    builder1.add_node("model_answer_node", model_answer_node)
    builder1.add_node("rating_node", rating_node)
    builder1.add_node("congratulation_node", congratulation_node)
    builder1.add_node("checking_node", checking_node)

    builder1.add_edge(START, "rating_node")
    builder1.add_conditional_edges("rating_node", rating_mode)
    builder1.add_edge("model_answer_node", "checking_node")
    builder1.add_edge("congratulation_node", "checking_node")
    # builder.add_conditional_edges("checking_node", exit_mode)
    builder1.add_edge("checking_node", END)

    graph1 = builder1.compile()


    def run(programming_languages, job_level):
        main_prompt = (
            f"You are a professional recruiter specializing in hiring developers for roles involving {programming_languages}. "
            f"The candidates are being recruited for positions at the {job_level} level. Your sole task is to ask professional "
            f"and relevant interview questions appropriate for this role. Do not provide any explanations, feedback, or additional "
            f"commentary—focus exclusively on formulating the questions. One question should be specific for one language. Ask only one question."
        )

        llm_response = llm.invoke(main_prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_response.content)
        add_message("assistant",llm_response.content)
        return llm_response.content


    display_messages()
    if prompt := st.chat_input("Answer"):
        if prompt == "hi":
            with st.chat_message("user"):
                st.markdown(prompt)
            add_message("user", prompt)
            llm_response = llm.invoke("Write a hi and tell that you are assistant to help in recruitment process")
            with st.chat_message("assistant"):
                st.markdown(llm_response.content)
            add_message("assistant", llm_response.content)
            run(programming_languages, job_level)
        else:
            with st.chat_message("user"):
                st.markdown(prompt)
            add_message("user", prompt)
            answer = prompt
            state = {"graph_state": [{"role": "system", "content": get_last_message()}]}
            state["graph_state"].append({"role": "assistant", "content": answer})
            graph1.invoke(state)
            run(programming_languages, job_level)




def show():
    options()




