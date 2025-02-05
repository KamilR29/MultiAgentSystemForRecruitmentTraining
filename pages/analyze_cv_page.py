import streamlit as st
from docx import Document
import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START,END
import pandas as pd



def importDox(label, key):
    """
    Upload and read the contents of a .docx file.

    :param label: Label for the Streamlit file uploader.
    :type label: str
    :param key: Unique key for the uploader widget.
    :type key: str
    :return: Extracted text content from the uploaded .docx file.
    :rtype: str
    """
    uploaded_file = st.file_uploader(label, type=["docx"], key=key)
    document_text = ""

    if uploaded_file is not None:
        st.write(f"File: {uploaded_file.name}")

        try:
            document = Document(uploaded_file)
            document_text = "\n".join([paragraph.text for paragraph in document.paragraphs])
        except Exception as e:
            st.error(f"Cannot read the file: {e}")

    return document_text
def app(cv_text,requirements_text):
    """
    Analyze a CV and job requirements using a multi-step graph-based workflow.

    :param cv_text: Text content of the uploaded CV.
    :type cv_text: str
    :param requirements_text: Text content of the uploaded job requirements.
    :type requirements_text: str
    """

    load_dotenv()

    class State(TypedDict):
        graph_state: object


    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the .env file")

    llm = ChatOpenAI(model="gpt-4o")




    def analise_cv_node(state):
        """
        Analyze the CV text and extract technical, soft, and language skills.

        :param state: Current graph state containing user and assistant messages.
        :type state: dict
        :return: Updated graph state.
        :rtype: dict
        """
        cv_text = state["graph_state"][-2]["content"]
        prompt = (
            f"Analyze this CV in terms of technical skills, soft skills, languages, and professional experience:\n"
            f"{cv_text}\n\n"
            f"Additionally, provide an assessment of the user's skills based on:\n"
            f"- Experience\n"
            f"- Technical abilities\n"
            f"- Language proficiency\n\n"
            f"Return the results in the following format:\n"
            f"[Detailed Summary: text with a comprehensive summary of skills,\n"
            f"Skill Assessment: Experience: number on a scale of 1-10, "
            f"Technical Skills: number on a scale of 1-10, "
            f"Languages: number on a scale of 1-10]"
        )
        llm_response = llm.invoke(prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_response.content)

        state["graph_state"].append({"role": "assistant", "content": llm_response.content})
        return state

    def analise_requirements_node(state):
        """
        Analyze the job requirements text and extract key skill and experience expectations.

        :param state: Current graph state.
        :type state: dict
        :return: Updated graph state.
        :rtype: dict
        """
        requirements_text = state["graph_state"][-2]["content"]
        prompt = (
            f"Analyze the job requirements in terms of technical skills, soft skills, languages, "
            f"and professional experience:\n{requirements_text}\n\n"
            f"Additionally, provide an evaluation of the requirements based on:\n"
            f"- Experience\n"
            f"- Technical skills\n"
            f"- Language proficiency\n\n"
            f"Return the results in the following format:\n"
            f"[Detailed Summary: text with a comprehensive summary of the requirements,\n"
            f"Requirements Assessment: Experience: number on a scale of 1-10, "
            f"Technical Skills: number on a scale of 1-10, "
            f"Languages: number on a scale of 1-10]"
        )

        llm_response = llm.invoke(prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_response.content)

        state["graph_state"].append({"role": "assistant", "content": llm_response.content})
        return state

    def skills_node(state):
        """
        Compare the skills in the CV against the job requirements and visualize the results.

        :param state: Current graph state.
        :type state: dict
        :return: Updated graph state.
        :rtype: dict
        """
        requirements_text = state["graph_state"][-1]["content"]
        cv_text = state["graph_state"][-2]["content"]

        prompt = (
            f"In these messages: {requirements_text} and {cv_text}, you have sections for "
            f"experience, technical skills, and languages. As a result, return a string in the "
            f"following format:\n"
            f"Line for requirements_text: number for experience, number for technical skills, "
            f"number for languages\n"
            f"Line for cv_text: number for experience, number for technical skills, number for languages\n\n"
            f"Example of a correct response:\n"
            f"1,2,5\n"
            f"4,6,3\n\n"
            f"Invoke a tool to convert the string and always return only the numbers, nothing else, "
            f"no additional text."
        )
        llm_response = llm.invoke(prompt)

        print(llm_response.content)

        lines = llm_response.content.strip().split("\n")
        lista1 = list(map(int, lines[0].split(",")))  # Druga linia jako lista liczb
        lista2 = list(map(int, lines[1].split(",")))  # Trzecia linia jako lista liczb
        dane = {
            'Kategoria': ['Experience', 'Technical Skills', 'Languages'],
            'You': lista1,
            'Requirements': lista2
        }
        df = pd.DataFrame(dane)

        df = df.set_index('Kategoria')

        st.bar_chart(df, horizontal=True)

        state["graph_state"].append({"role": "assistant", "content": str(llm_response.content)})
        return state

    def model_cv_node(state):
        """
        Generate a model CV tailored to job requirements and user-provided CV content.

        :param state: Current graph state.
        :type state: dict
        :return: Updated graph state.
        :rtype: dict
        """
        user_message = state["graph_state"][-2]["content"]
        cv = state["graph_state"][0]["content"]
        prompt = (
            f"Based on the provided information {user_message} and my CV {cv}, "
            f"create a professional model CV tailored to the given details. Ensure the CV follows "
            f"an industry-standard format with the following sections:\n"
            f"- Contact Information\n"
            f"- Professional Summary\n"
            f"- Skills (highlight technical and soft skills)\n"
            f"- Work Experience (list positions chronologically with relevant responsibilities)\n"
            f"- Education\n"
            f"- Additional Information (e.g., certifications, languages, or achievements)\n\n"
            f"The CV should be written in a clear, concise, and professional style."
        )

        llm_response = llm.invoke(prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_response.content)

        return state

    # Build the workflow graph
    builder = StateGraph(State)
    builder.add_node("analise_cv_node", analise_cv_node)
    builder.add_node("analise_requirements_node", analise_requirements_node)
    builder.add_node("skills_node", skills_node)
    builder.add_node("model_cv_node", model_cv_node)


    builder.add_edge(START, "analise_cv_node")
    builder.add_edge("analise_cv_node", "analise_requirements_node")
    builder.add_edge("analise_requirements_node", "skills_node")
    builder.add_edge("skills_node", "model_cv_node")
    builder.add_edge("model_cv_node", END)

    graph = builder.compile()
    state = {"graph_state": [{"role": "system", "content": cv_text}]}
    state["graph_state"].append({"role": "system", "content": requirements_text})
    graph.invoke(state)




def show():
    """
    Display the Streamlit UI to upload a CV and job requirements and perform their analysis.

    This function creates a two-column layout where the user can upload the CV and the job
    requirements. When the "Analyze" button is pressed, the uploaded files are processed.
    """
    st.title("Analyze CV")
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            cv_text = importDox("Upload your CV .docx", key="cv_upload")

        with col2:
            requirements_text = importDox("Upload requirements for the job .docx", key="job_requirements_upload")

        if st.button("Analyze"):
            if not cv_text or not requirements_text:
                st.error("Please upload cv and requirements files.")
            else:
                with st.spinner("Processing..."):

                    app(cv_text,requirements_text)
