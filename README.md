# Smart Hospital Management System

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)
![Prolog](https://img.shields.io/badge/Prolog-SWI--Prolog-yellow.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8.svg)
![Course](https://img.shields.io/badge/Course-CSA2001_AI_%26_ML-brightgreen.svg)


**An AI-Driven Approach to Healthcare Triage, Routing, and Administration**

This repository contains the source code for the "Smart Hospital Management System," developed as a Bring Your Own Project (BYOP) for the **CSA2001 - Fundamentals in AI and ML** course at VIT Bhopal. 

This interactive web application integrates multiple Artificial Intelligence paradigms—including Symbolic AI (Prolog), Graph Search Algorithms (A* and BFS), Machine Learning (Linear Regression), Computer Vision (OpenCV), and Natural Language Processing (TextBlob)—to solve real-world healthcare bottlenecks.

---

## Tech Stack & AI Methodologies

This project proves that real-world problem solving rarely relies on a single algorithm, but rather a pipeline of complementary AI techniques:

* **Frontend / UI:** Streamlit
* **Symbolic AI (Expert System):** SWI-Prolog, `pyswip`
* **Graph Search & Routing:** Python, `networkx`
* **Machine Learning (Regression):** `scikit-learn`, `numpy`, `pandas`
* **Geospatial Mapping:** `geopy`, `pydeck`
* **Computer Vision:** OpenCV (`cv2`), Haar Cascade Classifiers
* **Natural Language Processing:** `textblob`

---

## Features & Course Mapping

The application is structured as a 6-step workflow, seamlessly passing data through various AI models:

1. **AI Diagnosis & Triage (Prolog):** A rule-based expert system that takes patient symptoms, accounts for fuzzy matching, and outputs the most likely disease and emergency risk level.
2. **Emergency Protocol:** Automatically categorizes the patient's stability based on Prolog's risk assessment.
3. **Hospital Geospatial Mapping (PyDeck):** Maps the patient's real-world location alongside nearby simulated hospital facilities on an interactive 3D map.
4. **Ambulance Routing (NetworkX):** Simulates a city grid and compares Breadth-First Search (BFS) against the A* Search Algorithm (using a Manhattan distance heuristic) to dispatch an ambulance optimally.
5. **Recovery Prognosis (Scikit-Learn):** A Multiple Linear Regression model trained on synthetic medical data to predict the patient's required recovery days based on age and disease severity.
6. **Administrative AI Tools (OpenCV & TextBlob):** Features real-time facial detection for automated patient check-in and NLP-driven sentiment analysis to classify and act upon patient feedback.

---

## Project Structure
```
├── app.py                 # The main Streamlit web application & UI logic
├── medical_logic.pl       # Prolog Knowledge Base (Diseases, Symptoms, Rules)
├── search_engine.py       # BFS and A* routing algorithms using NetworkX
├── prognosis_ml.py        # Dataset generation & Linear Regression model
├── advanced_features.py   # OpenCV face detection and TextBlob sentiment analysis
└── README.md              # Project documentation
```

---

## Prerequisites & Installation

To run this project locally, you must have **Python 3.8+** installed. 

**CRITICAL DEPENDENCY: SWI-Prolog**
Because this project bridges Python and Prolog using the `pyswip` library, you **must** install the SWI-Prolog software on your machine before running the app. 
* Download and install it from the official site: [SWI-Prolog Downloads](https://www.swi-prolog.org/Download.html)
* Ensure SWI-Prolog is added to your system's `PATH` environment variable during installation.

### Step-by-Step Setup:

**1. Clone the repository**
\`\`\`bash
git clone [KethineniVenkataAvinash/Smart-Hospital-Management-System.git](https://github.com/KethineniVenkataAvinash/Smart-Hospital-Management-System.git)

cd smart-hospital-management


**2. Create a virtual environment (Recommended)**
\`\`\`bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
\`\`\`

**3. Install Python dependencies**
Run the following command to install all required libraries:
\`\`\`bash
pip install streamlit pyswip pandas pydeck geopy networkx scikit-learn opencv-python textblob
\`\`\`

*(Note: For Face Detection to work, ensure you have a functioning webcam connected to your computer).*

---

## How to Run the Application

Once all dependencies and SWI-Prolog are installed, you can launch the app using Streamlit:

\`\`\`bash
streamlit run app.py
\`\`\`

This will open a local web server (usually at `http://localhost:8501`) in your default web browser. 

### Usage Guide:
* **Step 1:** Enter a patient's name, age, and location. Select at least 2 symptoms from the dropdown and click "Diagnose".
* **Step 2:** Review the Emergency risk level and click "Next".
* **Step 3:** Interact with the 3D map to see the patient's location and select a destination hospital from the dropdown.
* **Step 4:** Watch the live-tracking progress bar as the system runs the A* routing algorithm.
* **Step 5:** View the ML-predicted recovery days.
* **Step 6:** Test the NLP Feedback analyzer by typing a review, or click "Face Detection" to launch the webcam check-in simulator (press 'q' to close the webcam window).

---

## Result
<img width="1627" height="832" alt="Screenshot 2026-03-31 192642" src="https://github.com/user-attachments/assets/1087c3e8-3884-49e6-947d-9c2c4aed69d8" />


## Future Roadmap
Deep Learning Diagnostics: Replace the Prolog symptom-checker with a Convolutional Neural Network (CNN) capable of diagnosing conditions directly from medical imagery (e.g., X-Rays).

Live Traffic API: Upgrade the search_engine.py from a simulated grid to utilize the Google Maps Directions API for real-world, traffic-adjusted routing.

Persistent Storage: Connect the patient registry to a persistent SQL database (like PostgreSQL) instead of storing records dynamically in Prolog's runtime memory.

## Summary
This project aims to solve critical bottlenecks in modern urban healthcare systems by developing a unified, AI-driven Smart Hospital Management System. The application seamlessly integrates multiple subfields of Artificial Intelligence—including Symbolic AI (Expert Systems), Graph Search Algorithms, Machine Learning, Computer Vision, and Natural Language Processing (NLP) into a single, user-friendly Streamlit web application. By automating triage, ambulance routing, recovery prediction, and feedback analysis.
