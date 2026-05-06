# 🏥 India Healthcare Intelligence System

An AI-powered full-stack web application that searches, scores, and maps 10,000+ healthcare facilities across India in real time.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-orange)
![Leaflet](https://img.shields.io/badge/Leaflet.js-Map-brightgreen)

---

## 🚨 The Problem It Solves

In India, 70% of people live in rural areas. When someone is sick, they often:
- Travel hours to reach a hospital
- Arrive only to find it lacks the equipment they need
- Waste precious time during emergencies

This system solves that by giving **accurate, AI-verified information** about 10,000 hospitals before you travel.

---

## 🎯 How It Works

**Step 1 — You type a search**
> Example: `"ICU emergency surgery Bihar"`

**Step 2 — AI understands your query**
Google Gemini breaks down what you need — location, capabilities, doctor type etc.

**Step 3 — System searches 10,000 facilities**
Filters hospitals matching your needs from the entire database.

**Step 4 — AI reads hospital notes**
For each result, Gemini reads unstructured text like *"Hospital has ICU with 10 beds, 24/7 emergency services"* and extracts key capabilities.

**Step 5 — Trust Score is calculated**
The system checks if hospital claims make sense. If a hospital claims surgery but has no anesthesiologist → trust score drops.

**Step 6 — Results shown on map**
50 results appear on an interactive map of India with color-coded dots:
- 🟢 Green = High Trust (80–100)
- 🟠 Orange = Medium Trust (50–79)
- 🔴 Red = Low Trust (0–49)

---

## ⚡ Why 50 Results Instead of 200?

Originally the system processed 200 facilities per search — meaning **200 Gemini API calls** every time a user searched. This caused slow responses and hit rate limits fast.

**Solution — Hybrid Processing:**
| Results | Method | Speed |
|---------|--------|-------|
| Top 20 | Google Gemini AI (deep, context-aware) | ~20s |
| Remaining 30 | Fast keyword matching | Instant |

This cut response time dramatically while keeping the most relevant results AI-powered.

---

## 🌟 Features

- 🔍 **Smart Search** — Natural language queries understood by Gemini AI
- 🗺️ **Interactive Map** — Live Leaflet.js map with color-coded hospital markers
- 🤖 **AI Extraction** — Extracts ICU, Surgery, Emergency, Oxygen, 24/7 from raw notes
- 📊 **Trust Scoring** — Flags inconsistencies with citations and detailed reasoning
- ✅ **Validator Agent** — Double-checks AI extracted data for accuracy
- ⚡ **Hybrid Processing** — Gemini AI for top results, keyword matching for speed

---

## 🛠️ Libraries & Tools — How Each One Works in This Project

### 🐍 Backend

#### **Python**
The core programming language for the entire backend. All data processing, API logic, AI calls, and trust scoring are written in Python.

#### **Flask**
A lightweight web framework that runs the backend server. In this project, Flask creates two API endpoints:
- `/search` — receives a query from frontend, runs AI search, returns results as JSON
- `/stats` — returns total facility count, states, and districts to display in the stats bar

#### **Flask-CORS**
Stands for Cross-Origin Resource Sharing. When the frontend (HTML file) tries to call the Flask backend, the browser blocks it by default for security. Flask-CORS tells the browser "this is allowed" so the frontend and backend can communicate freely.

#### **Pandas**
A data processing library. In this project it:
- Loads the 10,000-row Excel dataset into memory at startup
- Cleans and standardizes column names
- Filters hospitals by location (e.g. all hospitals in Bihar)
- Returns matching rows for each search query

#### **OpenPyXL**
Used by Pandas behind the scenes to read the `.xlsx` Excel file. Without it, Pandas cannot open Excel files — it only handles the file format parsing.

#### **Google Generative AI (google-genai)**
The official Python SDK for Google's Gemini AI. In this project it is used in two places:
1. `search_agent.py` — sends the user's query to Gemini and gets back structured filters (location, capabilities needed)
2. `extractor.py` — sends raw hospital notes to Gemini and gets back a JSON object of extracted capabilities (has_icu, has_surgery, available_24_7 etc.)

#### **Python Dotenv**
Loads environment variables from the `.env` file into Python. This means the Gemini API key is stored in `.env` and not hardcoded in the source code — keeping it safe and out of GitHub.

---

### 🌐 Frontend

#### **HTML / CSS / JavaScript**
The entire frontend is a single `index.html` file. It handles:
- Search input and button
- Displaying result cards with trust scores, capability tags, flags
- Calling the Flask backend API using `fetch()`
- Updating the stats bar (total facilities, states, districts)

#### **Leaflet.js**
An open-source JavaScript library for interactive maps. In this project it:
- Renders a full map of India on the right side of the screen
- Places a colored circle marker for each search result based on its coordinates
- Shows a popup with hospital name, location, trust score, and capabilities when a marker is clicked
- Automatically zooms to a facility when you click its result card

#### **OpenStreetMap**
Provides the free map tile images that Leaflet.js displays as the map background. Every zoom level and map tile is served by OpenStreetMap's servers — no API key or cost required.

---

### 🤖 AI

#### **Google Gemini 2.0 Flash**
The AI model used for two tasks:
1. **Query Understanding** — Given a search like `"ICU Bihar"`, Gemini returns structured JSON: `{"location": "bihar", "required_capabilities": ["has_icu"]}`
2. **Capability Extraction** — Given raw hospital notes, Gemini returns structured JSON: `{"has_icu": true, "has_surgery": false, "available_24_7": true, ...}`

Gemini 2.0 Flash is chosen because it is fast, cost-efficient, and handles unstructured medical text well.

---

### ⚙️ Trust Scoring Engine

#### **trust_scorer.py**
A custom rule-based engine (no AI needed) that scores each hospital from 0 to 100 by checking logical consistency:
- Surgery claimed but no anesthesiologist → **-30 points**
- ICU claimed but not 24/7 → **-20 points**
- Emergency claimed but no oxygen → **-15 points**
- Facility under renovation or closed → **-25 points**

Each deduction comes with a citation explaining the rule, finding, and impact — displayed on the result card.

---

### 🔧 Developer Tools

#### **Git**
Version control system that tracks every change made to the project. Used to commit code changes locally with meaningful messages like `"Add frontend and backend"`.

#### **GitHub**
Hosts the project code online at `https://github.com/Zeenat-12/healthcare-intelligence-India`. Allows sharing, collaboration, and version history.

#### **VS Code**
The code editor used to write all Python, HTML, CSS, and JavaScript files. Extensions like Python, Pylance, and Live Server make development faster.

#### **PowerShell**
The Windows terminal used to run all commands — starting the Flask server (`python app.py`), installing libraries (`pip install`), and pushing code to GitHub (`git push`).

---

## 📁 Project Structure
healthcare-intelligence-India/
'''
│
├── backend/
│   ├── app.py              # Flask API server
│   ├── data_loader.py      # Loads and cleans Excel dataset
│   ├── extractor.py        # Gemini AI capability extraction
│   ├── search_agent.py     # Smart location + query filtering
│   ├── trust_scorer.py     # Trust score calculation engine
│   └── validator.py        # Data validation logic
│
├── frontend/
│   └── index.html          # Full frontend (map + search UI)
│
├── .env                    # API keys (not pushed to GitHub)
├── requirements.txt        # Python dependencies
└── README.md
'''
---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API key ([Get one here](https://aistudio.google.com/))

### Installation

```bash
# Clone the repository
git clone https://github.com/Zeenat-12/healthcare-intelligence-India.git
cd healthcare-intelligence-India

# Install dependencies
pip install flask flask-cors pandas openpyxl google-genai python-dotenv

# Add your Gemini API key to .env file
echo GEMINI_KEY=your-api-key-here > .env

# Start the backend
cd backend
python app.py
```

Then open `frontend/index.html` in your browser.

---

## 🌍 Real World Impact

| Who | How They Use It |
|-----|----------------|
| 🏥 Patients | Find the nearest capable hospital before travelling |
| 🚑 Ambulance Drivers | Locate emergency facilities instantly |
| 📋 NGOs | Identify medical deserts in underserved areas |
| 🏛️ Government | Plan new hospital locations based on data |

---

## 🙌 Acknowledgements

- Dataset: VF Hackathon India Healthcare Dataset (10,000 facilities)
- Map tiles: OpenStreetMap
- AI: Google Gemini 2.0 Flash

