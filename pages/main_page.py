import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import time


def show():
    """
    Display a Streamlit application with a progress bar and LLM interaction.

    This function performs the following steps:

    1. Loads environment variables using :func:`load_dotenv`.
    2. Sets the page title to "Hello" using :func:`st.title`.
    3. Initializes the language model via :class:`ChatOpenAI` with the ``gpt-4o`` model.
    4. Creates and updates a progress bar that simulates a long-running operation.
    5. At 50% progress, sends a recruitment-related prompt to the language model.
    6. At 99% progress, displays the LLM's response as a chat message using :func:`st.chat_message`.
    7. Finally, clears the progress bar.

    Raises
    ------
    Exception
        Any exception raised during the invocation of the language model or Streamlit operations.
    """
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




