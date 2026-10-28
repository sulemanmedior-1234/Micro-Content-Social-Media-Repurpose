import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Micro-Content Repurposer", page_icon="📱", layout="wide"
)

st.markdown(
    "# 📱 AI Micro-Content & Social Media Repurposer"
)
st.markdown(
    "Transform a single long text, blog post, or transcript into multi-platform"
    " viral content instantly using Groq AI."
)
st.divider()

# Sidebar for API Key & Configuration
st.sidebar.header("⚙️ Configuration")
api_key_input = st.sidebar.text_input(
    "Groq API Key",
    value="",
    type="password",
    help=(
        "Enter your Groq API key here (starts with gsk_). Alternatively, you"
        " can set it as an environment variable GROQ_API_KEY."
    ),
)

# Use user input or fallback to environment variable
api_key = api_key_input or os.environ.get("GROQ_API_KEY")

selected_model = st.sidebar.selectbox(
    "Select Groq Model",
    ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
)

st.sidebar.divider()
st.sidebar.info(
    "💡 **Tip:** Paste your long-form blog post, article, or video transcript"
    " below, and the AI will generate content tailored for X/Twitter, LinkedIn,"
    " and TikTok/Reels simultaneously!"
)

# Main Input Area
st.subheader("📝 Input Source Content")
source_content = st.text_area(
    "Paste your blog post, essay, or transcript here:",
    height=200,
    placeholder=(
        "e.g., In this guide, we explore 5 ways artificial intelligence is"
        " transforming personal finance..."
    ),
)

generate_btn = st.button(
    "🚀 Repurposed Content across Platforms", type="primary"
)

if generate_btn:
  if not api_key:
    st.error(
        "⚠️ Please enter your Groq API key in the sidebar or set your"
        " GROQ_API_KEY environment variable to proceed."
    )
  elif not source_content.strip():
    st.warning("⚠️ Please provide some source content to repurpose.")
  else:
    try:
      # Initialize Groq Client
      client = Groq(api_key=api_key)

      with st.spinner(
          "🤖 AI is analyzing patterns and generating multi-platform"
          " assets..."
      ):
        # Prompt engineering for structured multi-platform output
        prompt = f"""
                You are an expert social media manager and content strategist. 
                Take the following source content and generate 3 distinct assets:
                
                1. X_TWITTER_THREAD: A viral, highly engaging 3 to 5 tweet thread with appropriate emojis and hooks. Separate tweets clearly.
                2. LINKEDIN_POST: A professional, insightful thought-leadership post structured for engagement on LinkedIn.
                3. TIKTOK_SCRIPT: A punchy 30-second short-form video script featuring a strong hook, body, and call-to-action.

                Source Content:
                {source_content}

                Format your output clearly with markdown headers for each platform:
                ### 🧵 X/Twitter Thread
                ### 💼 LinkedIn Post
                ### 🎬 TikTok / Reels Script
                """

        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            model=selected_model,
            temperature=0.7,
        )

        result_text = chat_completion.choices[0].message.content

        st.success("✨ Content successfully generated!")
        st.divider()

        # Display results in clean columns/tabs
        tab1, tab2, tab3 = st.tabs(
            ["🧵 X / Twitter Thread", "💼 LinkedIn Post", "🎬 TikTok / Script"]
        )

        # Simple parsing based on sections or displaying full response if formatting varies
        st.markdown(result_text)

        # Download option for the generated output
        st.download_button(
            label="📥 Download All Repurposed Content",
            data=result_text,
            file_name="repurposed_social_content.md",
            mime="text/markdown",
        )

    except Exception as e:
      st.error(f"❌ An error occurred while communicating with Groq API: {e}")