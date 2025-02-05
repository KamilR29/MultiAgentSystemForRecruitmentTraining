import os

from dotenv import load_dotenv

from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from typing import Literal
from langgraph.graph import StateGraph, START,END
import streamlit as st

# --- STATE MANAGEMENT FUNCTIONS ---
def initialize_state():
    """
    Initialize the graph state in the Streamlit session if not already set.

    This function checks if the key ``graph_state`` exists in :data:`st.session_state`
    and, if absent, initializes it as an empty list.
    """
    if "graph_state" not in st.session_state:
        st.session_state.graph_state = []

def get_last_message():
    """
    Retrieve the second-to-last message from the graph state.

    :return: The second-to-last message as a dictionary, or None if no messages exist.
    :rtype: dict or None
    """
    if st.session_state.graph_state:
        return st.session_state.graph_state[-2]
    else:
        return None


def add_message(role, content):
    """
    Add a new message to the graph state.

    :param role: Role of the sender (e.g., 'user', 'assistant').
    :type role: str
    :param content: Message content.
    :type content: str
    """
    st.session_state.graph_state.append({"role": role, "content": content})

def get_message():
    """
    Retrieve the last message from the graph state.

    :return: The last message as a dictionary, or an empty list if no messages exist.
    :rtype: dict or list
    """
    if "graph_state" in st.session_state:
        last_message = st.session_state.graph_state[-1]
        return last_message
    else:
        return []



def display_messages():
    """
    Display all messages stored in the graph state using Streamlit's chat interface.
    """
    for message in st.session_state.graph_state:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_last_messages():
    """
    Retrieve the last 50 messages from the graph state, or fewer if not available.

    :return: A list of the most recent messages.
    :rtype: list
    """
    if "graph_state" in st.session_state:
        last_messages = st.session_state.graph_state[-50:]
        return last_messages
    else:
        return []

def options():
    """
    Display a sidebar interface for selecting technologies and job level.

    In the sidebar, the user can choose a set of technologies and a job level. If valid inputs are
    provided, the recruitment process is initiated by calling :func:`app`.
    """
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
        st.text('Chose the options and write "hi", "hello" or something to start recruitment process')

    if selected_technologies != [] and job_level != "Chose level":
        app(programming_languages, job_level)


def app(programming_languages, job_level):
    """
    Main application logic for managing the recruitment workflow using Streamlit and LangChain.

    This function sets up the necessary state, loads environment variables, and defines the workflow
    nodes for processing recruitment interview questions and responses.

    :param programming_languages: Selected programming technologies.
    :type programming_languages: str
    :param job_level: Selected job level.
    :type job_level: str
    :raises ValueError: If the OPENAI_API_KEY is not set in the environment.
    """
    initialize_state()
    load_dotenv()

    class State(TypedDict):
        graph_state: str

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the .env file")

    llm = ChatOpenAI(model="gpt-4o")


    def rating_node(state):
        """
        Evaluate the user's answer and rate it on a scale of 1-10.

        :param state: Current graph state.
        :type state: dict
        :return: Updated graph state.
        :rtype: dict
        """
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
        """
        Generate a model answer for the given question.

        :param state: Current graph state.
        :type state: dict
        :return: Updated graph state.
        :rtype: dict
        """
        last_message = state["graph_state"][-3]
        question = last_message["content"]

        model_answer_prompt = (
            f"You are a professional recruiter specializing in hiring developers for roles involving {programming_languages}. "
            f"The candidates are being recruited for positions at the {job_level} level. Based on your expertise as a recruiter, "
            f"and developer write a model answer for that question: {question}. The answer shouldn't be long. Focus on the most important information."
        )

        llm_response = llm.invoke(model_answer_prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_response.content)
        # st.session_state.graph_state = state["graph_state"]
        state["graph_state"].append({"role": "assistant", "content": llm_response.content})
        return state

    def congratulation_node(state):
        """
        Evaluate the user's answer and provide congratulations if appropriate.

        :param state: Current graph state.
        :type state: dict
        :return: Updated graph state.
        :rtype: dict
        """
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
        """
        Analyze recent messages to identify areas where the user struggles and suggest improvements.

        :param state: Current graph state.
        :type state: dict
        :return: Updated graph state.
        :rtype: dict
        """
        last_messages = get_last_messages()
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
        """
        Determine the next node based on the rating provided for the user's answer.

        :param state: Current graph state.
        :type state: dict
        :return: The name of the next node ("model_answer_node" or "congratulation_node").
        :rtype: Literal["model_answer_node", "congratulation_node"]
        """
        last_message = state["graph_state"][-1]
        last_message_content = last_message["content"]
        try:
            if int(last_message_content) < 7:
                return "model_answer_node"
            return "congratulation_node"
        except ValueError:

            print(f"Nieprawidłowa wartość oceny: {last_message_content}")
            return "model_answer_node"

    # --- WORKFLOW SETUP ---
    builder1 = StateGraph(State)
    builder1.add_node("model_answer_node", model_answer_node)
    builder1.add_node("rating_node", rating_node)
    builder1.add_node("congratulation_node", congratulation_node)
    builder1.add_node("checking_node", checking_node)

    builder1.add_edge(START, "rating_node")
    builder1.add_conditional_edges("rating_node", rating_mode)
    builder1.add_edge("model_answer_node", "checking_node")
    builder1.add_edge("congratulation_node", "checking_node")
    builder1.add_edge("checking_node", END)

    graph1 = builder1.compile()


    def run(programming_languages, job_level,message_for_question):
        """
        Generate and display a professional interview question based on the selected programming languages and job level.

        :param programming_languages: Selected programming technologies.
        :type programming_languages: str
        :param job_level: Selected job level.
        :type job_level: str
        :param message_for_question: Additional conclusions or context for question generation.
        :type message_for_question: str
        :return: Generated interview question.
        :rtype: str
        """
        main_prompt = (
            f"You are a professional recruiter specializing in hiring developers for roles involving {programming_languages}. "
            f"The candidates are being recruited for positions at the {job_level} level. Your sole task is to ask professional "
            f"and relevant interview questions appropriate for this role. Do not provide any explanations, feedback, or additional "
            f"commentary—focus exclusively on formulating the questions. One question should be specific for one language. Ask only one question."
            f"In constructing the question, you can take these conclusions {message_for_question} into account but you dont need to, biger prioryty is to ask question for  all {programming_languages}"
        )

        llm_response = llm.invoke(main_prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_response.content)
        add_message("assistant",llm_response.content)
        return llm_response.content


    display_messages()
    if prompt := st.chat_input("Answer"):

        if len(st.session_state.graph_state) == 0:
            with st.chat_message("user"):
                st.markdown(prompt)
            add_message("user", prompt)
            llm_response = llm.invoke("Write a hi and tell that you are assistant to help in recruitment process")
            with st.chat_message("assistant"):
                st.markdown(llm_response.content)
            add_message("assistant", llm_response.content)
            message_for_question = get_message()
            run(programming_languages, job_level,message_for_question)
        else:
            with st.chat_message("user"):
                st.markdown(prompt)
            add_message("user", prompt)
            answer = prompt
            state = {"graph_state": [{"role": "system", "content": get_last_message()}]}
            state["graph_state"].append({"role": "assistant", "content": answer})
            graph1.invoke(state)
            message_for_question = get_message()
            run(programming_languages, job_level,message_for_question)
            if "graph_state" in st.session_state:
                print(f"Liczba rekordów w graph_state: {len(st.session_state.graph_state)}")




def show():
    """
    Main entry point for the Streamlit application.

    This function displays the sidebar and initiates the recruitment workflow.
    """
    options()




