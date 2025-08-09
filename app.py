import streamlit as st
import json
from model.ollama_runner import build_prompt
from model.groq_runner import query_groq
from dotenv import load_dotenv

load_dotenv()

# UI Layout
st.set_page_config(page_title="Reel Script Generator", layout="centered")
st.title("AI Reel Script Generator")
st.write("Generate viral, high-converting short-form video scripts using AI.")

# Input Fields
role_options = [
    "Business Owner", "Service Provider", "Influencer / Creator",
    "Startup Founder / SaaS", "Educator / Thought Leader",
    "Health / Wellness Expert", "Lifestyle / Self-Improvement", "Other"
]

role = st.selectbox("Who are you?", role_options)
if role == "Other":
    role = st.text_input("Enter your custom role:")

tone = st.selectbox("Tone", ["Excited", "Friendly", "Professional", "Dramatic", "Funny"])
format = st.selectbox("Format", ["Hook → Problem → Solution", "Story → Struggle → Breakthrough", "Question → Fact → Call to Action"])
cta = st.selectbox("Choose Call to Action", ["Like & Save", "Comment Your Thoughts", "Hit follow", "Follow for More", "Share this with a friend"])
idea = st.text_area("Core Idea", placeholder="What's the idea, product, or insight you want to convey?")

# Generate Button
if "generated" not in st.session_state:
    st.session_state["generated"] = False

btn_label = "Generate Script" if not st.session_state["generated"] else "Regenerate Script"

if st.button(btn_label):
    if not all([role, tone, format, idea]):
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Generating..."):
            prompt = build_prompt(format, role, tone, cta, idea)
            output = query_groq(prompt)
            st.subheader("Generated Script")
            st.markdown(output)
            st.download_button("Download Script", output, file_name="reel_script.txt")
            st.session_state["generated"] = True
