import streamlit as st
from openai import OpenAI

# ضع API Key هنا
client = OpenAI(api_key="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")

st.set_page_config(
    page_title="Club Outreach AI",
    page_icon="AIChE.png",
    layout="centered"
)

# ===== CSS بسيط لتحسين الشكل =====
st.markdown("""
<style>
.main {
    background-color: #f9fafb;
}
.stButton > button {
    background-color: #000000;
    color: white;
    padding: 0.6em 1.2em;
    border-radius: 8px;
    font-weight: 600;
}
.stTextArea textarea {
    background-color: #2563eb;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ===== Sidebar =====
st.sidebar.title("Message Settings")

message_type = st.sidebar.selectbox(
    "Message Type",
    ("Workshop Invitation", "Field Visit", "Sponsorship Opportunity")
)

name = st.sidebar.text_input("Name")
role = st.sidebar.text_input("Role / Position")
field = st.sidebar.text_input("Field of Expertise")

# ===== Main Content =====
st.title("AIChE Outreach AI")
st.write(
    "Generate **human-like LinkedIn messages** for workshops, visits, or sponsorships."
)

st.divider()

if st.button("Generate Message"):
    if not all([name, role, field]):
        st.warning("Please fill in all fields on the left.")
    else:
        if message_type == "Workshop Invitation":
            goal_text = "Invite this person to deliver a short online workshop for students."
        elif message_type == "Field Visit":
            goal_text = "Invite this person to host or guide a field visit for our club members."
        else:
            goal_text = "Ask this person or their organization about sponsoring student activities."

        prompt = f"""
You are writing a LinkedIn message as a real university student.

Rules:
- Simple, natural English
- Short sentences
- No marketing language
- No emojis
- No exaggeration
- Polite and human
- Do not sound like a template
- Do NOT mention AI

Person details:
Name: {name}
Role: {role}
Field: {field}

Context:
I am a chemical engineering student at faculty of hydrocarbons and chemistry and AIChE student chapter coordinator.

Goal:
{goal_text}

Write one concise LinkedIn message (5–7 lines).
Mention their field naturally.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.subheader("Generated Message")
        st.text_area(
            "Copy and paste this message into LinkedIn:",
            response.choices[0].message.content,
            height=220
        )