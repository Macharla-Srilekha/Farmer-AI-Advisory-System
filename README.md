# 🌾 Farmer AI Advisory System

> **An intelligent, AI-powered web application that helps Indian farmers make better decisions about crops, fertilizers, pest control, irrigation, weather, and market prices — all in their own language.**

---

## 📑 Table of Contents

1. [What Is This Project?](#-what-is-this-project)
2. [Features at a Glance](#-features-at-a-glance)
3. [How the Application Works (Big Picture)](#-how-the-application-works-big-picture)
4. [Tech Stack](#-tech-stack)
5. [Project Folder Structure](#-project-folder-structure)
6. [File-by-File Code Explanation](#-file-by-file-code-explanation)
7. [Prerequisites (What You Need Before Starting)](#-prerequisites-what-you-need-before-starting)
8. [Step-by-Step Installation & Execution Guide](#-step-by-step-installation--execution-guide)
9. [Using the Application](#-using-the-application)
10. [API Endpoints Reference](#-api-endpoints-reference)
11. [Database Schema](#-database-schema)
12. [How the ML Model Works](#-how-the-ml-model-works)
13. [Troubleshooting Common Errors](#-troubleshooting-common-errors)
14. [Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)

---

## 🌱 What Is This Project?

The **Farmer AI Advisory System** is a web application built to support Indian farmers. Think of it as a "smart farming assistant" that lives in your browser. A farmer can:

- **Chat with an AI bot** — ask any farming question in English, Hindi, Telugu, Tamil, or Kannada. They can even use their **voice** instead of typing.
- **Find out which crop to grow** — based on the soil in their field and the current season.
- **Know how much fertilizer to apply** — detailed NPK (Nitrogen-Phosphorus-Potassium) dosage for each crop.
- **Detect plant diseases from a photo** — upload a picture of a sick leaf, and the AI tells them what's wrong and how to fix it.
- **Compare irrigation methods** — drip vs. sprinkler vs. flood, with costs and government subsidies.
- **Check the weather forecast** — 7-day forecast with agriculture-specific advice.
- **See market prices** — live-style MSP (Minimum Support Price) and mandi rates for major crops.

---

## ✨ Features at a Glance

| Feature | What It Does |
|---|---|
| 🤖 **AI Chatbot** | Answers farming questions in 5 languages (text + voice) |
| 🌾 **Crop Prediction** | Recommends best crops for your soil type and season |
| 🧪 **Fertilizer Guide** | NPK dosage, schedule, and tips for 8+ crops |
| 🔬 **Pest & Disease Detection** | Upload a leaf photo → AI identifies the disease |
| 🛡️ **Pest Control Library** | Organic & chemical treatment for all major pests |
| 💧 **Irrigation Planner** | Compare drip/sprinkler/flood with costs & subsidies |
| 🌦️ **Weather Forecast** | 7-day forecast with farming advisories |
| 📈 **Market Prices** | MSP and mandi prices for 10+ commodities |
| 🌐 **Multilingual** | English, हिंदी, తెలుగు, தமிழ், ಕನ್ನಡ |

---

## 🧩 How the Application Works (Big Picture)

If you're new to web development, here's the simplest way to understand:

```
┌─────────────────────────────────────────────┐
│               YOUR BROWSER                  │
│  (HTML pages styled with CSS & Bootstrap)   │
│                                             │
│   User clicks a button or types a message   │
│              ↓ sends request ↓              │
└──────────────────┬──────────────────────────┘
                   │  HTTP Request (e.g., /api/chatbot)
                   ▼
┌─────────────────────────────────────────────┐
│            FLASK SERVER (app.py)             │
│   (Python code running on your computer)    │
│                                             │
│   1. Receives the request                   │
│   2. Processes it (database/ML/logic)       │
│   3. Sends back a JSON response             │
└──────┬──────────────┬───────────────────────┘
       │              │
       ▼              ▼
┌────────────┐  ┌──────────────┐
│  DATABASE  │  │   ML MODEL   │
│  (SQLite)  │  │ (disease     │
│            │  │  detection)  │
└────────────┘  └──────────────┘
```

**In plain English:**
1. You open a web page in your browser.
2. When you do something (like ask the chatbot a question), JavaScript on the page sends a message to the Flask server.
3. The Flask server processes it — maybe looking up data in the database, or running the ML model.
4. The server sends back an answer, and the page updates to show it.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | Python 3.8+ with Flask | Handles all server logic and API routes |
| **Frontend** | HTML5 + CSS3 + Bootstrap 5 | Page structure and responsive styling |
| **Icons** | Font Awesome 6 | Beautiful icons throughout the UI |
| **Database** | SQLite | Stores crops, fertilizers, pest data, chat history |
| **ML / AI** | scikit-learn (Random Forest) | Leaf disease detection from images |
| **Image Processing** | Pillow (PIL) + NumPy | Analyze leaf photos for color ratios |
| **Data Handling** | Pandas | Read CSV dataset for ML training |
| **Voice Input** | Web Speech API (browser built-in) | Speech-to-text for the chatbot |
| **Cross-Origin** | Flask-CORS | Allows frontend-backend communication |

---

## 📁 Project Folder Structure

Here's every file and folder in the project, with an explanation of what each one does:

```
FarmerAIAdvisorySystem/
│
├── app.py                    # 🚀 MAIN FILE — the Flask server (start here!)
├── database.py               # 🗄️ Creates the database and fills it with data
├── requirements.txt          # 📦 List of Python packages needed
├── farmer_advisory.db        # 💾 The SQLite database file (auto-created)
├── README.md                 # 📖 This file — project documentation
│
├── ml/                       # 🤖 Machine Learning folder
│   └── train_model.py        # 🧠 Script to train the disease detection model
│
├── models/                   # 📊 Saved ML model files
│   ├── disease_model.pkl     # 🔮 Trained Random Forest model
│   └── label_encoder.pkl     # 🏷️ Converts model output to disease names
│
├── data/                     # 📂 Training data folder
│   └── leaf_disease_dataset.csv  # 📋 82 rows of leaf disease data
│
├── static/                   # 🎨 Static assets (CSS, JS, images)
│   ├── css/
│   │   └── style.css         # 💅 Custom styling for all pages
│   ├── js/                   # 📜 JavaScript files (currently empty)
│   └── uploads/              # 📸 Temporary folder for uploaded leaf images
│
└── templates/                # 📄 HTML page templates
    ├── index.html            # 🏠 Landing/home page
    ├── dashboard.html        # 📊 Main dashboard with quick links
    ├── chatbot.html          # 💬 AI chatbot interface (voice + text)
    ├── crop_prediction.html  # 🌾 Crop recommendation page
    ├── fertilizer.html       # 🧪 Fertilizer guide page
    ├── pest_detection.html   # 🔬 Leaf disease detection (image upload)
    ├── pest_control.html     # 🛡️ Pest and disease library
    ├── irrigation.html       # 💧 Irrigation methods comparison
    ├── weather.html          # 🌦️ Weather forecast page
    └── market_price.html     # 📈 Market price dashboard
```

---

## 📝 File-by-File Code Explanation

### 1. `app.py` — The Heart of the Application (552 lines)

This is the **main file** that runs the entire application. Here's what each part does:

#### Imports & Setup (Lines 1–22)
```python
from flask import Flask, render_template, request, jsonify, session
from PIL import Image
import numpy as np
```
- **Flask** is the web framework — it handles incoming browser requests and sends back responses.
- **PIL (Pillow)** is for opening and processing uploaded leaf images.
- **NumPy** is for fast mathematical calculations on image pixel data.

#### Route Handlers (Lines 44–82)
```python
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
```
- `@app.route('/dashboard')` means: *"When someone visits `http://localhost:5000/dashboard`, run this function."*
- `render_template('dashboard.html')` means: *"Send the `dashboard.html` file to the browser."*
- There are **10 routes** like this — one for each page.

#### Chatbot API (Lines 84–206)
```python
@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
```
- This is the brain of the chatbot.
- When a user sends a message, this function receives it.
- It checks the message against **keyword lists** (e.g., if the message contains "fertilizer", "urea", or "खाद", it returns fertilizer advice).
- Responses are stored in a **dictionary** organized by language (`en`, `hi`, `te`, `ta`, `kn`) and topic (`crop`, `pest`, `weather`, etc.).
- Chat history is saved to the database.

**How keyword matching works:**
```
User types: "How much urea for wheat?"
→ System finds "urea" in the 'fertilizer' keyword list
→ Returns the fertilizer response in the user's selected language
```

#### Crop Prediction API (Lines 208–243)
```python
@app.route('/api/crop', methods=['POST'])
def crop_api():
```
- Takes `soil_type` (Black, Red, Alluvial, Sandy, Clay) and `season` (Kharif, Rabi, Zaid).
- Looks up the best crops from a hardcoded dictionary.
- Returns crop names with confidence scores.

#### Fertilizer API (Lines 254–282)
- Takes a `crop` name and returns detailed fertilizer info:
  - NPK ratio, Urea/DAP/MOP amounts per hectare
  - Application schedule (when to apply each dose)
  - Pro tips
  - Best fertilizer products with icons

#### Pest Detection API (Lines 377–526)
This is the most complex API. When a user uploads a leaf photo:

1. **Opens the image** and resizes it to 224×224 pixels
2. **Analyzes pixel colors** to calculate:
   - `green_ratio` — how much of the leaf is green (healthy)
   - `brown_ratio` — brown spots (possible disease)
   - `yellow_ratio` — yellowing (nutrient deficiency or disease)
   - `dark_ratio` — dark spots (possible fungal infection)
   - `white_ratio` — white/gray areas (powdery mildew)
3. **Runs the ML model** (if available) to predict the disease
4. **Cross-references** with a crop-specific disease database
5. **Returns** the disease name, confidence %, and treatment tips

#### Weather & Market APIs (Lines 312–364)
- **Weather:** Generates simulated 7-day forecast data with temperature, humidity, wind, and farming advisories.
- **Market:** Returns MSP and current mandi prices for 10 commodities (Rice, Wheat, Cotton, Maize, etc.).

#### Server Startup (Lines 537–551)
```python
if __name__ == '__main__':
    init_database()         # Create/seed the database
    app.run(debug=True)     # Start the web server
```

---

### 2. `database.py` — Database Setup (172 lines)

This file creates an SQLite database called `farmer_advisory.db` with **7 tables**:

| Table | Purpose | Example Data |
|---|---|---|
| `crops` | Stores crop information | Rice, Wheat, Cotton... |
| `fertilizers` | NPK/dosage per crop | Urea 220kg/ha for Rice |
| `pest_diseases` | Known pests per crop | Rice Blast, Wheat Rust |
| `irrigation_methods` | 4 irrigation types | Drip, Sprinkler, Flood, Furrow |
| `market_prices` | Commodity pricing | Rice ₹2,183/quintal |
| `chat_history` | Logs all chatbot conversations | User messages + bot responses |
| `weather_cache` | Cached weather data | Temperature, humidity, etc. |

**When does this run?** Automatically when you start the app (`app.py` calls `init_database()` on startup). If the database already exists, it skips creation (uses `CREATE TABLE IF NOT EXISTS`).

---

### 3. `ml/train_model.py` — ML Model Training (115 lines)

This script trains the **leaf disease detection model**. Here's the process:

```
CSV Dataset (82 samples)
        ↓
  Split: 80% Training / 20% Testing
        ↓
  Train Random Forest Classifier (100 trees)
        ↓
  Save model → models/disease_model.pkl
  Save label encoder → models/label_encoder.pkl
```

**What is a Random Forest?** Imagine 100 "experts" each looking at different aspects of a leaf. Each expert makes a guess about the disease. The final answer is whatever the majority of experts agree on. That's Random Forest!

**The 7 features the model uses:**

| Feature | What It Measures |
|---|---|
| `leaf_color_avg` | Average brightness of the leaf |
| `green_ratio` | Percentage of green pixels (healthy tissue) |
| `brown_spots_ratio` | Percentage of brown pixels (necrosis) |
| `yellow_spots_ratio` | Percentage of yellow pixels (chlorosis) |
| `dark_spots_ratio` | Percentage of dark pixels (fungal spots) |
| `lesion_size` | Estimated size of damaged area |
| `spot_count` | Number of distinct spots detected |

---

### 4. `data/leaf_disease_dataset.csv` — Training Data

Contains **82 rows** of labeled leaf data across **9 crops**: Rice, Wheat, Cotton, Maize, Groundnut, Tomato, Potato, Sugarcane, and Soybean.

Each row has the 7 features above plus the disease name (e.g., `rice_blast`, `healthy`, `late_blight`).

---

### 5. `templates/` — HTML Pages

Each HTML file is a complete web page using:
- **Bootstrap 5** for responsive layout (works on phone + desktop)
- **Font Awesome** for icons
- **Inline JavaScript** for API calls and dynamic content

**Key pages:**
- `chatbot.html` (26,132 bytes) — The most feature-rich page. Includes voice input via Web Speech API, language selector dropdown, animated chat bubbles, and auto-scroll.
- `pest_detection.html` — Has a file upload form, image preview, and results display with treatment recommendations.
- `pest_control.html` (31,864 bytes) — Largest template; contains a comprehensive pest/disease library with search and filter.

---

### 6. `static/css/style.css` — Custom Styling

Adds visual polish on top of Bootstrap — hero section gradients, card hover effects, chatbot bubble styling, color-coded badges, responsive adjustments, etc.

---

### 7. `requirements.txt` — Python Dependencies

```
flask==3.0.0          # Web framework
flask-cors==4.0.0     # Cross-origin support
werkzeug==3.0.1       # HTTP utilities (used by Flask)
pillow==10.1.0        # Image processing
numpy==1.24.3         # Math/array operations
scikit-learn==1.3.2   # Machine learning (Random Forest)
pandas==2.1.3         # Data reading (CSV)
python-dateutil==2.8.2 # Date parsing utilities
```

---

## 📋 Prerequisites (What You Need Before Starting)

Before you can run this project, you need to install a few things on your computer. Follow these steps:

### 1. Install Python (version 3.8 or higher)

Python is the programming language this project is written in.

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the latest version (e.g., Python 3.11 or 3.12)
3. **IMPORTANT:** During installation, check the box that says **"Add Python to PATH"** ✅
4. Click "Install Now"

**To verify Python is installed**, open a terminal/command prompt and type:
```bash
python --version
```
You should see something like: `Python 3.11.5`

### 2. Install pip (Python package manager)

`pip` usually comes with Python. To verify:
```bash
pip --version
```
If it shows a version number, you're good!

### 3. Install Git (optional but recommended)

If you want to clone the project from a repository:
1. Go to [https://git-scm.com/downloads](https://git-scm.com/downloads)
2. Download and install for your OS

---

## 🚀 Step-by-Step Installation & Execution Guide

Follow these steps **in order**. Each step builds on the previous one.

### Step 1: Get the Project Files

**Option A — If you have the folder already:**
Open a terminal/command prompt and navigate to the project folder:
```bash
cd C:\Users\DELL\Desktop\FarmerAIAdvisorySystem
```

**Option B — If you're cloning from Git:**
```bash
git clone <repository-url>
cd FarmerAIAdvisorySystem
```

### Step 2: Create a Virtual Environment (Recommended)

A virtual environment keeps this project's packages separate from your other Python projects. This prevents version conflicts.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your terminal prompt will change to show `(venv)` at the beginning. Like:
```
(venv) C:\Users\DELL\Desktop\FarmerAIAdvisorySystem>
```

### Step 3: Install Required Packages

This reads `requirements.txt` and installs all the libraries the project needs:
```bash
pip install -r requirements.txt
```

This will install: Flask, Pillow, NumPy, scikit-learn, Pandas, and others. This may take **1-3 minutes** depending on your internet speed.

**If you see errors about `joblib`:** It is included with scikit-learn, so no separate install is needed.

### Step 4: Train the Machine Learning Model (First Time Only)

The ML model is what detects leaf diseases from photos. You need to train it once:

```bash
python ml/train_model.py
```

**Expected output:**
```
==================================================
Leaf Disease Detection - ML Model Training
==================================================

Dataset loaded: 82 samples
Features: ['crop_name', 'leaf_color_avg', 'green_ratio', ...]

Disease classes: 30+ classes
Training Random Forest Classifier...

Model Training Complete!
Accuracy: 85-95%

Model saved to: models/disease_model.pkl
Label encoder saved to: models/label_encoder.pkl
```

> **Note:** The trained model files (`disease_model.pkl` and `label_encoder.pkl`) are already included in the `models/` folder. You only need to re-train if you modify the dataset.

### Step 5: Run the Application

Start the Flask server:
```bash
python app.py
```

**Expected output:**
```
============================================================
FARMER AI ADVISORY SYSTEM
============================================================
Initializing database...
Database initialized at: ...\farmer_advisory.db
Loading ML model...
ML Model loaded successfully
============================================================
Server running at: http://127.0.0.1:5000/
============================================================
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
Press CTRL+C to quit
```

### Step 6: Open in Your Browser

Open any web browser (Chrome, Firefox, Edge) and go to:

```
http://127.0.0.1:5000/
```

or equivalently:

```
http://localhost:5000/
```

🎉 **You should see the Farmer AI Advisory System home page!**

### Step 7: Stop the Server (When Done)

Press `Ctrl + C` in the terminal to stop the server.

---

## 🖥️ Using the Application

### Home Page (`/`)
The landing page with links to all features. Click any card to navigate.

### Dashboard (`/dashboard`)
A quick-access panel showing all available tools.

### AI Chatbot (`/chatbot`)
1. Select your language from the dropdown (English, Hindi, Telugu, Tamil, Kannada)
2. Type your farming question OR click the 🎤 microphone button to speak
3. The bot responds with detailed advice
4. Try questions like:
   - "How much fertilizer for wheat?"
   - "Tell me about drip irrigation"
   - "कपास में कौन सी खाद डालें?" (Hindi)
   - "వరి పంటకు ఏ ఎరువు వేయాలి?" (Telugu)

### Crop Prediction (`/crop_prediction`)
1. Select your **soil type** (Black, Red, Alluvial, Sandy, Clay)
2. Select the **season** (Kharif, Rabi, Zaid)
3. Click "Predict" to see recommended crops with confidence scores

### Fertilizer Guide (`/fertilizer`)
1. Select a crop name
2. See detailed NPK dosage, application schedule, and pro tips

### Pest Detection (`/pest_detection`)
1. Select your crop type from the dropdown
2. Upload a photo of the affected leaf
3. The AI analyzes the image and shows:
   - Disease name
   - Confidence percentage
   - Treatment recommendations

### Pest Control Library (`/pest_control`)
Browse all known pests and diseases with symptoms, treatments, and prevention tips.

### Irrigation Planner (`/irrigation`)
Compare 4 irrigation methods with efficiency, costs, and government subsidy info.

### Weather Forecast (`/weather`)
View a 7-day weather forecast with farming-specific advisories.

### Market Prices (`/market_price`)
Check MSP and current mandi prices for all major commodities. See buy/sell/hold recommendations.

---

## 🔌 API Endpoints Reference

All API endpoints return JSON responses. Here's a quick reference:

| Method | Endpoint | Purpose | Request Body |
|---|---|---|---|
| `POST` | `/api/chatbot` | Send chatbot message | `{"message": "...", "language": "en"}` |
| `POST` | `/api/crop` | Get crop recommendation | `{"soil_type": "black", "season": "kharif"}` |
| `GET` | `/api/crops/list` | List all crops in DB | — |
| `POST` | `/api/fertilizer` | Get fertilizer guide | `{"crop": "rice"}` |
| `POST` | `/api/irrigation` | Get irrigation info | `{"method": "drip", "crop": "rice"}` |
| `GET` | `/api/weather` | Get weather forecast | Query: `?location=Central India` |
| `GET` | `/api/market` | Get market prices | — |
| `GET` | `/api/pest_control` | Get all pest/disease data | — |
| `POST` | `/api/pest_detection` | Upload leaf image for analysis | Form data: `image` (file), `cropType` (text) |
| `GET` | `/api/chat_history` | Get last 50 chat messages | — |

### Example: Testing with `curl`

```bash
# Test the chatbot
curl -X POST http://localhost:5000/api/chatbot \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"How much fertilizer for rice?\", \"language\": \"en\"}"

# Test crop prediction
curl -X POST http://localhost:5000/api/crop \
  -H "Content-Type: application/json" \
  -d "{\"soil_type\": \"black\", \"season\": \"kharif\"}"
```

---

## 🗄️ Database Schema

The SQLite database (`farmer_advisory.db`) contains 7 tables:

```
┌──────────────────────┐
│        crops         │ ← Core crop information
├──────────────────────┤
│ id (PRIMARY KEY)     │
│ name (TEXT UNIQUE)   │
│ soil_type (TEXT)     │
│ season (TEXT)        │
│ water_requirement    │
│ temp_range (TEXT)    │
│ yield_estimate (TEXT)│
│ created_at (TIMESTAMP)│
└──────────┬───────────┘
           │ Referenced by:
           ▼
┌──────────────────────┐    ┌──────────────────────┐
│     fertilizers      │    │    pest_diseases      │
├──────────────────────┤    ├──────────────────────┤
│ id (PK)              │    │ id (PK)              │
│ crop_id (FK → crops) │    │ crop_id (FK → crops) │
│ npk_ratio (TEXT)     │    │ disease_name (TEXT)   │
│ urea_kg_per_ha       │    │ symptoms (TEXT)       │
│ dap_kg_per_ha        │    │ treatment (TEXT)      │
│ mop_kg_per_ha        │    │ prevention (TEXT)     │
│ fym_tons_per_ha      │    │ severity (TEXT)       │
│ application_schedule │    └──────────────────────┘
│ tips (TEXT)          │
└──────────────────────┘

┌──────────────────────┐    ┌──────────────────────┐
│  irrigation_methods  │    │    market_prices      │
├──────────────────────┤    ├──────────────────────┤
│ id (PK)              │    │ id (PK)              │
│ method_name (TEXT)   │    │ commodity (TEXT)      │
│ efficiency (TEXT)    │    │ price (REAL)          │
│ water_saving (TEXT)  │    │ unit (TEXT)           │
│ cost_per_acre (TEXT) │    │ msp (REAL)            │
│ subsidy (TEXT)       │    │ trend (TEXT)          │
│ best_for (TEXT)      │    │ last_updated          │
│ pros / cons (TEXT)   │    └──────────────────────┘
└──────────────────────┘

┌──────────────────────┐    ┌──────────────────────┐
│    chat_history      │    │    weather_cache      │
├──────────────────────┤    ├──────────────────────┤
│ id (PK)              │    │ id (PK)              │
│ user_message (TEXT)  │    │ location (TEXT)       │
│ bot_response (TEXT)  │    │ temperature (REAL)    │
│ language (TEXT)      │    │ humidity (REAL)       │
│ created_at           │    │ condition (TEXT)      │
└──────────────────────┘    │ forecast (TEXT)       │
                            │ cached_at             │
                            └──────────────────────┘
```

---

## 🧠 How the ML Model Works

### The Problem
Farmers need to quickly identify what disease is affecting their crops.

### The Solution
A **Random Forest Classifier** that analyzes the color composition of a leaf photo.

### Step-by-Step Process

```
📸 User uploads leaf photo
        ↓
🔲 Image resized to 224×224 pixels
        ↓
🎨 Extract 7 color-based features:
   • Average brightness
   • Green ratio (healthy tissue %)
   • Brown spots ratio (necrosis %)
   • Yellow spots ratio (chlorosis %)
   • Dark spots ratio (fungal %)
   • Estimated lesion size
   • Spot count
        ↓
🌲 Feed features into Random Forest (100 decision trees)
        ↓
🏷️ Model outputs disease name + confidence %
        ↓
💊 System looks up treatment recommendations
        ↓
📋 Results displayed to user
```

### Why Random Forest?
- Works well with small datasets (we only have 82 samples)
- Doesn't need GPU or special hardware
- Gives probability scores (confidence %)
- Resistant to overfitting with proper tuning

---

## 🔧 Troubleshooting Common Errors

### ❌ `ModuleNotFoundError: No module named 'flask'`
**Cause:** Python packages not installed.
**Fix:**
```bash
pip install -r requirements.txt
```

### ❌ `python: command not found`
**Cause:** Python not in your PATH.
**Fix:** Reinstall Python and check **"Add Python to PATH"** during installation. On some systems, try `python3` instead of `python`.

### ❌ `ML Model not found - Run ml/train_model.py first`
**Cause:** The disease detection model hasn't been trained.
**Fix:**
```bash
python ml/train_model.py
```

### ❌ `Address already in use` (Port 5000 is busy)
**Cause:** Another application is using port 5000.
**Fix:** Either close the other application, or change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

### ❌ `PermissionError: [Errno 13]` on database file
**Cause:** The database file is locked or read-only.
**Fix:** Close any other program using `farmer_advisory.db`, or delete it and restart the app (it will be recreated).

### ❌ Voice input not working in chatbot
**Cause:** Web Speech API only works in Chrome/Edge and requires HTTPS or localhost.
**Fix:** Use Google Chrome and access via `http://localhost:5000/chatbot`. Make sure microphone permission is granted.

### ❌ Uploaded image shows "Not recognized as plant leaf"
**Cause:** The image doesn't have enough green pixels to be identified as a leaf.
**Fix:** Ensure the photo clearly shows the leaf filling most of the frame, with good lighting.

---

## ❓ Frequently Asked Questions (FAQ)

### Q: Do I need internet to run this?
**A:** You need internet **only once** — to install the Python packages (`pip install`). After that, the app runs completely offline. However, Bootstrap and Font Awesome icons load from CDN, so the styling may be affected without internet.

### Q: Can I run this on my phone?
**A:** You can't run the server on a phone, but once it's running on your computer, you can access it from your phone's browser. Both devices must be on the same Wi-Fi network. Use the `http://192.168.x.x:5000` address shown in the terminal.

### Q: Is the weather data real?
**A:** Currently, weather data is simulated/randomized. In a production version, you would connect to a weather API like OpenWeatherMap.

### Q: How accurate is the disease detection?
**A:** The model is trained on a small dataset (82 samples) and uses color-based features, so it's a demonstration. For production use, you would need a larger dataset and a deep learning model (like a CNN with TensorFlow).

### Q: Can I add more languages?
**A:** Yes! In `app.py`, the `responses` dictionary and `keywords` dictionary can be extended. Add a new language code (e.g., `'mr'` for Marathi) with translations for each topic.

### Q: What is MSP?
**A:** MSP stands for **Minimum Support Price** — the price at which the Indian government guarantees to buy crops from farmers.

### Q: Can I connect a real weather API?
**A:** Yes. Replace the `weather_api()` function in `app.py` with an API call to OpenWeatherMap or IMD (India Meteorological Department). You'll need to sign up for a free API key.

---

## 📜 License

This project is built for educational purposes. Feel free to modify and use it for learning, academic projects, or to build upon for real-world farming applications.

---

## 🙏 Acknowledgements

- **Flask** — Python web framework
- **scikit-learn** — Machine learning library
- **Bootstrap 5** — Responsive CSS framework
- **Font Awesome** — Icon library
- Government of India's agricultural data for MSP prices and scheme information

---

<div align="center">

**Built with ❤️ for Indian Farmers**

🌾 *"Technology can transform farming and improve the lives of millions of farmers."* 🌾

</div>
