
# 🏥 India Healthcare Intelligence System

A smart AI-powered system to search and analyze 10,000+ medical facilities across India.

## 🎯 What It Does
- Search 10,000 hospitals and clinics across India
- AI extracts capabilities from unstructured hospital notes
- Trust scoring system flags suspicious or incomplete data
- Interactive map shows facility locations across India
- Shows 200 results per search

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Leaflet.js
- **AI:** Google Gemini 2.0 Flash
- **Data:** Pandas, OpenPyXL
- **Dataset:** 10,000 Indian medical facilities

## 📊 Features
- ✅ 10,000 facilities loaded
- ✅ 200 results per search
- ✅ AI-powered capability extraction
- ✅ Trust scoring system
- ✅ Interactive map of India
- ✅ Validator agent checks data consistency


## 📁 Project Structure

healthcare-intelligence-India/
│
├── backend/
│   ├── app.py
│   ├── data_loader.py
│   ├── extractor.py
│   ├── search_agent.py
│   ├── trust_scorer.py
│   ├── validator.py
│   └── VF_Hackathon_Dataset_India_Large.xlsx
│
├── frontend/
│   ├── index.html
│   └── requirements.txt
│
├── .env
└── README.md


This is an AI-powered web application that helps people find the right hospital or medical facility across India. Instead of just searching by name, it uses Artificial Intelligence to understand what a hospital can actually do.

The Problem it Solves
In India, 70% of people live in rural areas. When someone is sick, they often:

Travel hours to reach a hospital
Arrive only to find it lacks the equipment they need
Waste precious time during emergencies

This system solves that by giving accurate, verified information about 10,000 hospitals before you travel.

How it Works
Step 1 — You type a search
Like: "ICU emergency surgery Bihar"
Step 2 — AI understands your query
Google Gemini AI breaks down what you are looking for — location, capabilities, doctor type etc.
Step 3 — System searches 10,000 facilities
It filters hospitals that match your needs from the entire database.
Step 4 — AI reads hospital notes
For each result, AI reads unstructured text like "Hospital has ICU with 10 beds, 24/7 emergency services" and extracts key capabilities.
Step 5 — Trust Score is calculated
The system checks if hospital claims make sense. For example if a hospital claims surgery but has no anesthesiologist, it gets a lower trust score.
Step 6 — Results shown on map
200 results appear on an interactive map of India with color coded dots — green for high trust, orange for medium, red for low.

Key Features

🔍 Smart SearchAI understands natural language queries
🗺️ Interactive MapSee all hospitals on India map
⭐ Trust ScoringFlags hospitals with suspicious claims
✅ Validator AgentDouble checks AI extracted data
📊 10,000 FacilitiesCovers hospitals across all of India200 ResultsShows up to 200 hospitals per search

Tech Used and Libraries 

Python + Flask — Backend server
Google Gemini AI — Understanding queries and extracting data
Leaflet.js — Interactive map
Pandas — Processing 10,000 rows of data
HTML/CSS/JavaScript — Frontend interface

Flask — Python framework that runs the backend server.
Flask-CORS — Allows frontend and backend to communicate with each other.
Pandas — Loads and filters the 10,000 hospital records from Excel.
OpenPyXL — Reads the .xlsx Excel dataset file.
Google Generative AI — Connects to Google Gemini AI for smart search and data extraction.
Python Dotenv — Safely loads the API key from the .env file.
Requests — Handles HTTP communication between system components.
JSON — Formats data exchange between backend and frontend.
Leaflet.js — Displays the interactive map of India with hospital markers.
OpenStreetMap — Provides the free map background tiles.
Google Gemini 2.0 Flash — AI model that understands queries and reads hospital notes.
Git — Tracks and manages all code changes.
GitHub — Hosts the project code online for team collaboration.
VS Code — Code editor used to write the entire project.
PowerShell — Terminal used to run Python and Git commands.

Real World Impact

🏥 Patients finding nearest capable hospital
🚑 Ambulance drivers locating emergency facilities
📋 NGOs identifying medical deserts
🏛️ Government planning new hospital locations

