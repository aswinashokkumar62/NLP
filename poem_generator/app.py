import os
import streamlit as st
import google.generativeai as genai

def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1519682577862-22b62b24e493?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80");
            background-attachment: fixed;
            background-size: cover;
        }}
        .main-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            color: black;  /* Set text color to black */
        }}
        .stTextArea textarea {{
            background-color: rgba(255, 255, 255, 0.9);
            color: black;  /* Set textarea text color to black */
        }}
        .stButton>button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: bold;
            transition: background-color 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #45a049;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    set_background()

    # Set your Gemini API key directly here
    api_key = 'AIzaSyCH87zyIMfvAYPQ3IqRjAB-qPecGJFA_es'
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("🎭 Poetic Muse")
    st.markdown("### Unleash your creativity with AI-generated poems")

    # User input for poem prompt
    user_prompt = st.text_area(
        "Describe the theme or style of your desired poem:",
        placeholder="e.g., 'A sonnet about the beauty of autumn'",
        height=80
    )

    # Button to generate the poem
    if st.button("✨ Generate Poem"):
        if user_prompt.strip():
            with st.spinner("Crafting your masterpiece..."):
                prompt = f"""
                Generate a poem based on the following theme or style:

                "{user_prompt}"

                Provide a creative and original poem.
                """

                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    poem = response.text

                    st.session_state.generated_poem = poem
                    st.session_state.copy_status = "📋 Copy Poem"

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.warning("We couldn't generate the poem. Please try again later.")
        else:
            st.warning("Please provide a description for the poem.")

    # Display generated poem
    if 'generated_poem' in st.session_state:
        st.markdown("### 📜 Your Generated Poem:")
        st.markdown(f"```\n{st.session_state.generated_poem}\n```")

        col1, col2 = st.columns([1, 4])
        with col1:
            copy_button = st.button(st.session_state.get('copy_status', "📋 Copy Poem"), key="copy_button")

        if copy_button:
            st.write(f"""
                <script>
                const poemText = `{st.session_state.generated_poem}`;
                navigator.clipboard.writeText(poemText).then(() => {{
                    document.getElementById('copy_button').innerText = '✅ Copied!';
                }});
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "✅ Copied!"

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
