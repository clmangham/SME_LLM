import streamlit as st
from rag import rag
from summaries import get_summaries


def main():

    # --- Streamlit page configuration ---

    # Set the title for the Streamlit app
    st.title("Summary and AI Chat with Trending Research Papers")
    st.caption("from https://paperswithcode.com/")

    st.write(
       """
        Trending research titles are scraped from paperswithcode.com and summaries are pulled from Arxiv. An AI chatbot assists with questions and answers based on these papers.
        """
    )

    st.write("Jump to Section:")
    st.markdown("[Summaries](#summaries)")
    st.markdown("[AI Chat](#aichat)")

    st.divider()
    st.header("Summaries", anchor='summaries', divider = 'gray')

    summaries = get_summaries()
    for summary in summaries:
        st.write(summary)

    # For RAG-CHAT
    st.header("AI Chat", anchor='aichat', divider = 'gray')
    
    with st.form(key='my_form', clear_on_submit=False):
        user_input = st.text_input("Prompt:", placeholder="Ask a question about this trending research", key='input')
        submit_button = st.form_submit_button(label='Ask')

    # If asking for OpenAI API Key
    # with st.sidebar:
    #     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    #     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    if user_input:
        result = rag(user_input)
        st.write(result)

    


if __name__ == "__main__":

    main()
