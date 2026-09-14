import streamlit as st
import pandas as pd
import pickle
import time

st.set_page_config(page_title="IPL AI Winner Predictor", page_icon="🏏", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
:root { --gold:#f6c453; --cyan:#38bdf8; --glass:rgba(255,255,255,.10); --border:rgba(255,255,255,.16); }
.stApp { background:radial-gradient(circle at 15% 10%,rgba(56,189,248,.18),transparent 28%),radial-gradient(circle at 85% 15%,rgba(109,40,217,.22),transparent 30%),linear-gradient(135deg,#06101d 0%,#0a1d34 45%,#111827 100%); color:#f8fafc; }
.block-container { max-width:1180px; padding-top:1.4rem; padding-bottom:2rem; }
h1,h2,h3,p,label,.stMarkdown { color:#f8fafc; }
.hero { padding:28px 30px; margin-bottom:20px; border-radius:24px; background:linear-gradient(120deg,rgba(16,60,110,.88),rgba(109,40,217,.75)); border:1px solid rgba(255,255,255,.16); box-shadow:0 18px 50px rgba(0,0,0,.30); position:relative; overflow:hidden; }
.hero:after { content:"🏏"; position:absolute; right:28px; top:4px; font-size:92px; opacity:.18; transform:rotate(-10deg); }
.hero-title { font-size:42px; font-weight:800; margin:0 0 8px 0; letter-spacing:-.5px; }
.hero-subtitle { font-size:17px; color:#dbeafe; margin:0; }
.hero-badge { display:inline-block; margin-top:14px; padding:7px 12px; border-radius:999px; background:rgba(246,196,83,.16); border:1px solid rgba(246,196,83,.45); color:#fde68a; font-weight:700; font-size:13px; }
div[data-testid="stMetric"] { background:linear-gradient(145deg,rgba(255,255,255,.12),rgba(255,255,255,.06)); border-radius:18px; padding:18px; border:1px solid var(--border); box-shadow:0 10px 28px rgba(0,0,0,.20); backdrop-filter:blur(10px); }
div[data-testid="stExpander"] { background:rgba(255,255,255,.06); border:1px solid var(--border); border-radius:16px; overflow:hidden; }
div[data-testid="stSidebar"] { background:linear-gradient(180deg,#06101d 0%,#101827 100%); border-right:1px solid rgba(255,255,255,.08); }
.stButton > button { width:100%; border-radius:14px; font-size:18px; font-weight:800; padding:.78rem 1rem; border:1px solid rgba(255,255,255,.18); background:linear-gradient(90deg,#2563eb,#7c3aed); color:white; box-shadow:0 10px 26px rgba(37,99,235,.28); transition:transform .18s ease,box-shadow .18s ease; }
.stButton > button:hover { transform:translateY(-2px); box-shadow:0 14px 32px rgba(124,58,237,.38); border-color:rgba(255,255,255,.35); }
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, .stNumberInput input { border-radius:12px !important; }
.section-kicker { color:#7dd3fc; text-transform:uppercase; letter-spacing:1.5px; font-size:12px; font-weight:800; margin-bottom:4px; }
.footer-note { text-align:center; color:#94a3b8; font-size:13px; padding-top:10px; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    with open("ipl_winner_model.pkl", "rb") as file:
        return pickle.load(file)

try:
    model_data = load_model()
    model = model_data["model"]
    options = model_data["options"]
except FileNotFoundError:
    st.error("❌ ipl_winner_model.pkl file not found.")
    st.stop()
except Exception as error:
    st.error(f"❌ Error while loading model: {error}")
    st.stop()

st.markdown("""
<div class="hero">
<div class="section-kicker">Machine Learning • Cricket Analytics</div>
<div class="hero-title">IPL AI Winner Predictor</div>
<p class="hero-subtitle">Compare two IPL teams, set the venue and toss details, and let the model estimate the winning probability.</p>
<span class="hero-badge">⚡ Interactive Streamlit Prediction App</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("👤 User Profile")
    st.write("Personalize your prediction experience.")
    user_name = st.text_input("Your Name", placeholder="Enter your name")
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    city = st.text_input("City", placeholder="Example: Chennai")
    favourite_team = st.selectbox("Favourite IPL Team", options["teams"])
    cricket_interest = st.select_slider("Cricket Interest", options=["Beginner","Casual Fan","Regular Viewer","Cricket Expert"], value="Regular Viewer")

if user_name:
    st.success(f"👋 Welcome {user_name}! Ready for the prediction?")

with st.expander("👤 View My Profile"):
    c1,c2=st.columns(2)
    with c1:
        st.write(f"**Name:** {user_name if user_name else 'Not entered'}")
        st.write(f"**Age:** {age}")
        st.write(f"**City:** {city if city else 'Not entered'}")
    with c2:
        st.write(f"**Favourite Team:** {favourite_team}")
        st.write(f"**Cricket Interest:** {cricket_interest}")

st.header("🏟️ Match Prediction")
st.write("Enter the match information below.")
team_col1,team_col2=st.columns(2)
with team_col1:
    team1=st.selectbox("🏏 Team 1",options["teams"])
team2_options=[team for team in options["teams"] if team!=team1]
with team_col2:
    team2=st.selectbox("🏏 Team 2",team2_options)
venue=st.selectbox("🏟️ Match Venue",options["venues"])
toss_col1,toss_col2=st.columns(2)
with toss_col1:
    toss_winner=st.selectbox("🪙 Toss Winner",[team1,team2])
with toss_col2:
    toss_decision=st.selectbox("🎯 Toss Decision",options["toss_decisions"])

st.subheader("📋 Match Summary")
s1,s2=st.columns(2)
with s1:
    st.write(f"🏏 **Team 1:** {team1}")
    st.write(f"🏏 **Team 2:** {team2}")
    st.write(f"🏟️ **Venue:** {venue}")
with s2:
    st.write(f"🪙 **Toss Winner:** {toss_winner}")
    st.write(f"🎯 **Toss Decision:** {toss_decision}")

predict_button=st.button("🔮 Predict Winner",type="primary",use_container_width=True)
if predict_button:
    if not user_name.strip():
        st.warning("⚠️ Please enter your name in the sidebar.")
        st.stop()
    progress_bar=st.progress(0); status_text=st.empty()
    messages=["Analysing teams...","Checking venue...","Evaluating toss information...","Running Machine Learning model...","Calculating winning probability..."]
    for i in range(100):
        progress_bar.progress(i+1); status_text.write(messages[min(i//20,4)]); time.sleep(.01)
    progress_bar.empty(); status_text.empty()
    input_data=pd.DataFrame({"Team1":[team1],"Team2":[team2],"Venue":[venue],"TossWinner":[toss_winner],"TossDecision":[toss_decision]})
    try:
        probabilities=model.predict_proba(input_data)[0]; classes=model.classes_; probability_dict=dict(zip(classes,probabilities))
        team1_probability=probability_dict.get(team1,0); team2_probability=probability_dict.get(team2,0); total_probability=team1_probability+team2_probability
        if total_probability<=0:
            st.error("Unable to calculate probability for selected teams."); st.stop()
        team1_probability/=total_probability; team2_probability/=total_probability
        if team1_probability>=team2_probability:
            winner=team1; winner_probability=team1_probability
        else:
            winner=team2; winner_probability=team2_probability
        st.balloons(); st.success(f"🏆 Predicted Winner: {winner}"); st.subheader("📊 Winning Probability")
        r1,r2=st.columns(2)
        with r1:
            st.metric(label=team1,value=f"{team1_probability*100:.2f}%"); st.progress(float(team1_probability))
        with r2:
            st.metric(label=team2,value=f"{team2_probability*100:.2f}%"); st.progress(float(team2_probability))
        st.metric("🎯 Prediction Confidence",f"{winner_probability*100:.2f}%")
        if winner==favourite_team:
            st.success(f"🎉 {user_name}, your favourite team {favourite_team} is predicted to win!")
        else:
            st.info(f"🏏 {user_name}, the model predicts {winner} to win this match.")
        st.subheader("🧠 Prediction Summary")
        st.write(f"**User:** {user_name}"); st.write(f"**City:** {city if city else 'Not entered'}"); st.write(f"**Favourite Team:** {favourite_team}"); st.write(f"**Match:** {team1} vs {team2}"); st.write(f"**Venue:** {venue}"); st.write(f"**Toss Winner:** {toss_winner}"); st.write(f"**Toss Decision:** {toss_decision}"); st.write(f"**🏆 Predicted Winner:** {winner}"); st.write(f"**Prediction Confidence:** {winner_probability*100:.2f}%")
    except Exception as error:
        st.error(f"Prediction error: {error}")

st.divider()
st.warning("⚠️ This application uses historical IPL data and Machine Learning for educational purposes. The predicted winner is not guaranteed to match the actual cricket result.")
st.markdown("<p class='footer-note'>🏏 IPL AI Predictor • Python • Machine Learning • Streamlit</p>",unsafe_allow_html=True)
