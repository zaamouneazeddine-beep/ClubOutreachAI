
import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Club Outreach AI",
    page_icon="AIChE.png",
    layout="centered"
)

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

st.sidebar.title("Message Settings")


message_type = st.sidebar.selectbox(
    "Message Type",
    ("Workshop Invitation", "Field Visit", "Sponsorship Opportunity")
)


sender_role = st.sidebar.selectbox(
    "Your Role in AIChE",
    (
        "Treasurer of AIChE",
        "President of AIChE",
        "Vice President of AIChE",
        "General Secretary of AIChE",
        "Human Resources of AIChE",
        "Coordinator of AIChE"
    )
)

name = st.sidebar.text_input("Recipient Name")
role = st.sidebar.text_input("Recipient Role / Position")
field = st.sidebar.text_input("Recipient Field of Expertise")

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

Sender role:
I am the {sender_role} of the AIChE student chapter.

Adjust the tone naturally based on my role.
- President / Vice President: confident and representative
- Treasurer: professional and finance-aware
- General Secretary: formal and organized
- Human Resources: people-focused and friendly
- Coordinator: collaborative and initiative-driven

Recipient details:
Name: {name}
Role: {role}
Field: {field}

Context:
I am a petroleum engineering student at the faculty of hydrocarbons and chemistry.

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
