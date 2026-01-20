import streamlit as st
from huggingface_hub import InferenceClient  


#page configuration
st.set_page_config(
    page_title="MENTAL HEALTH CHATBOT",
    page_icon="✨",
    layout="centered"
)
st.title("✨ MENTAL HEALTH CHATBOT")
st.write("Welcome ! Your chatbot is running successfully")


#hugging face token
HF_TOKEN = st.secrets["HF_TOKEN"]
client= InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token= HF_TOKEN)

#initialise session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []
if "mood" not in st.session_state:
    st.session_state.moode="🙂 Normal"

#side bar emoji mood tracker
st.sidebar.header("🤍 MOOD TRACKER")
mood = st.sidebar.radio(
    "How are you feeling today?",
    [ " 🙂 Normal ","😊 Happy", "😟 Sad ", "😡 Angry ", "😑 Bored " , " 🫩Tired" ,
     " ✅ Productive ", "🤩 Energetic" ,"😖 stressed","😎 Confident","😌 Peaceful"]
)
st.session_state.mood= mood
st.sidebar.success(f"selected mood: {mood}")
st.sidebar.markdown("☺️ *You can talk to me about anything you're going through.*")


# AI response function
def get_response(user_input, mood):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a compassionate mental health chatbot for students. "
                "Respond with empathy, positivity, and one simple self-care tip. "
                "End with a gentle follow-up question."
            )
        },
        {
            "role": "user",
            "content": f"I feel {mood}. {user_input}"
        }
    ]

    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )

        reply = response.choices[0].message["content"]

        if not reply or not reply.strip():
            return "I'm here with you ❤️ Would you like to share a bit more?"

        return reply.strip()

    except Exception as e:
        print("Model error:", e)
        return "I'm here to listen ❤️ Please try again."
    
    
#Tabs for chatting and journaling
tab1, tab2 = st.tabs(["💬 Chat", "📝 Journal"])
with tab1:
    st.subheader("Chat with your AI")
    user_input = st.text_input("Type your message here👇",
                               placeholder= "........"
                               )
    if user_input:
        reply = get_response(user_input,st.session_state.mood)
        
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot",reply))

#Display chat history
for sender , message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"You:{message}")
    else:
        st.markdown(f"Bot:{message}")

#Journal tab
with tab2:
    st.subheader("📝 Personal Journal")

    journal_text = st.text_area(
        "Write your thoughts here:",
        placeholder="Today I felt..."
    )

    if st.button("Save Entry"):
        if journal_text.strip():
            st.session_state.journal_entries.append(journal_text)
            st.success("Journal entry saved successfully 💙")
        else:
            st.warning("Please write something before saving.")

    if st.session_state.journal_entries:
        st.markdown("### 📖 Your Previous Entries")
        for i, entry in enumerate(st.session_state.journal_entries, 1):
            st.markdown(f"**Entry {i}:** {entry}")


