import streamlit as st
from pyswip import Prolog
import pandas as pd
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from prognosis_ml import initialize_model, predict_recovery
from search_engine import run_routing
from advanced_features import analyze_feedback, run_face_detection
import time

st.set_page_config(page_title="Smart Hospital Management System", layout="wide")

st.markdown("""
<style>
body { background-color: #F4F8FF; }
.header { font-size:32px; color:#0A66C2; font-weight:bold; }
.card {
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0 4px 10px rgba(0,0,0,0.1);
    margin-bottom:15px;
}
.stButton>button {
    background:#0A66C2;
    color:white;
    border-radius:8px;
    height:45px;
    width:100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='header'>Smart Hospital Management System</div>", unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1
if "patient" not in st.session_state:
    st.session_state.patient = {}
if "hospital" not in st.session_state:
    st.session_state.hospital = None

def reset_app():
    st.session_state.step = 1
    st.session_state.patient = {}
    st.session_state.hospital = None


prolog = Prolog()
prolog.consult("medical_logic.pl")
model, _ = initialize_model()


steps = ["Diagnosis","Emergency","Hospital","Routing","Recovery","AI"]
st.progress(st.session_state.step/6)
st.write(f"### Step {st.session_state.step}: {steps[st.session_state.step-1]}")


if st.session_state.step == 1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    name = st.text_input("Patient Name")
    age = st.number_input("Age",1,100)
    loc = st.text_input("Location","Bhopal, India")

    symptoms = st.multiselect("Symptoms",[
        "fever","cough","fatigue","body_ache",
        "high_fever","chills","sweating","nausea"
    ])

    if st.button("Diagnose", key="s1"):
        if len(symptoms) >= 2:
            result = list(prolog.query(f"best_diagnosis({symptoms}, D, Score)"))

            if result:
                d = result[0]["D"]
                r = list(prolog.query(f"risk_level({d}, R)"))[0]["R"]

                st.session_state.patient = {
                    "name":name,
                    "age":age,
                    "loc":loc,
                    "risk":r
                }

                st.success(f"Condition: {d.upper()}")
                st.session_state.step = 2
        else:
            st.warning("Select at least 2 symptoms")

    st.markdown("</div>", unsafe_allow_html=True)


if st.session_state.step == 2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if st.session_state.patient["risk"] in ["high","critical"]:
        st.error("Alert! Emergency")
    else:
        st.success("Stable")

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Back", key="b2"):
            st.session_state.step = 1

    with col2:
        if st.button("Next", key="n2"):
            st.session_state.step = 3

    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.step == 3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    geo = Nominatim(user_agent="app")
    loc = geo.geocode(st.session_state.patient["loc"])

    if loc is None:
        st.error("Location not found")
        st.stop()

    pat_lat, pat_lon = loc.latitude, loc.longitude

    hospitals = [
        ("Apollo Hospital",(pat_lat+0.02, pat_lon)),
        ("Fortis Hospital",(pat_lat-0.01, pat_lon)),
        ("AIIMS Hospital",(pat_lat, pat_lon+0.015))
    ]

    map_data = []

    map_data.append({"lat":pat_lat,"lon":pat_lon,"color":[0,200,0]})

    for h in hospitals:
        map_data.append({
            "lat":h[1][0],
            "lon":h[1][1],
            "color":[200,0,0]
        })

    df = pd.DataFrame(map_data)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=500,
    )

    view = pdk.ViewState(latitude=pat_lat, longitude=pat_lon, zoom=12)

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

    names = [h[0] for h in hospitals]
    selected = st.selectbox("Select Hospital", names)

    for h in hospitals:
        if h[0]==selected:
            st.session_state.hospital = h[1]

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Back", key="b3"):
            st.session_state.step = 2

    with col2:
        if st.button("Next", key="n3"):
            st.session_state.step = 4

    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.step == 4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Ambulance Routing")

    result = run_routing()

    st.write("BFS:", result["BFS"])
    st.write("A*:", result["ASTAR"])

    st.subheader("Live Tracking")

    path = result["ASTAR"]["path"]
    prog = st.progress(0)

    for i in range(len(path)):
        prog.progress(int((i/len(path))*100))
        time.sleep(0.05)

    st.success("Ambulance Arrived!")

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Back", key="b4"):
            st.session_state.step = 3

    with col2:
        if st.button("Next", key="n4"):
            st.session_state.step = 5

    st.markdown("</div>", unsafe_allow_html=True)


if st.session_state.step == 5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    p = st.session_state.patient
    sev_map = {"low":3,"moderate":6,"high":8,"critical":10}

    pred = predict_recovery(model, p["age"], sev_map[p["risk"]])
    st.metric("Recovery Time", f"{pred} days")

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Back", key="b5"):
            st.session_state.step = 4

    with col2:
        if st.button("Next", key="n5"):
            st.session_state.step = 6

    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.step == 6:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("AI Features")

    if st.button("Face Detection", key="face"):
        run_face_detection()

    review = st.text_area("Patient Feedback")

    if st.button("Analyze Sentiment", key="nlp"):
        if review.strip() == "":
            st.warning("Enter feedback first")
        else:
            res = analyze_feedback(review)
            if res:
                st.success(res["sentiment"])
                st.write(res["suggestion"])

    st.markdown("---")
    if st.button("Start New Patient", key="reset"):
        reset_app()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)