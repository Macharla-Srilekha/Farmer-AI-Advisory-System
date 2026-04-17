# -*- coding: utf-8 -*-
"""
Farmer AI Advisory System - Complete Flask Backend
Features: Chatbot, Crop Prediction, Fertilizer, Pest Detection, Irrigation, Weather, Market Prices
"""
import os
import sqlite3
import random
import datetime
import numpy as np
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
app.secret_key = 'farmer_ai_secret_key_2024'
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'farmer_advisory.db')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'disease_model.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'models', 'label_encoder.pkl')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    from database import init_db as create_db
    create_db()

def load_ml_model():
    try:
        import joblib
        model = joblib.load(MODEL_PATH)
        encoder = joblib.load(ENCODER_PATH)
        return model, encoder
    except:
        return None, None

MODEL, ENCODER = load_ml_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/crop_prediction')
def crop_prediction_page():
    return render_template('crop_prediction.html')

@app.route('/fertilizer')
def fertilizer_page():
    return render_template('fertilizer.html')

@app.route('/pest_detection')
def pest_detection_page():
    return render_template('pest_detection.html')

@app.route('/pest_control')
def pest_control_page():
    return render_template('pest_control.html')

@app.route('/irrigation')
def irrigation_page():
    return render_template('irrigation.html')

@app.route('/weather')
def weather_page():
    return render_template('weather.html')

@app.route('/market_price')
def market_price_page():
    return render_template('market_price.html')

@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    data = request.get_json()
    message = data.get('message', '').strip()
    selected_lang = data.get('language', 'en')
    
    response = get_response(message, selected_lang)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chat_history (user_message, bot_response, language) VALUES (?, ?, ?)',
                  (message, response, selected_lang))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'response': response, 'language': selected_lang})

def get_response(message, lang='en'):
    msg = message.lower()
    
    responses = {
        'en': {
            'greeting': ["Namaste! I'm your farming assistant. I can help you with:\n\n🌾 Crop selection & cultivation\n🧪 Fertilizers & NPK\n🐛 Pests & diseases\n💧 Irrigation & water\n🌦️ Weather & climate\n📈 Market prices\n🏛️ Government schemes\n🌱 Organic farming\n\nJust ask your question in any language!", "Hello! Welcome to Farmer AI. How can I help you today?\n\nI can answer questions about:\n• Which crop to grow in your soil\n• How much fertilizer to apply\n• Pest and disease control methods\n• Best irrigation practices\n• Government subsidies\n• Market prices (MSP)\n\nType your question or use the voice button!"],
            'fertilizer': ["🌱 **Fertilizer Guide:**\n\n**For Rice:** Urea 220kg + DAP 130kg + MOP 65kg per hectare.\n\n**For Wheat:** Urea 260kg + DAP 130kg + MOP 65kg per hectare.\n\n**For Cotton:** Urea 220kg + DAP 110kg + MOP 85kg per hectare.\n\n**For Maize:** Urea 260kg + DAP 130kg + MOP 65kg per hectare.\n\n💡 Tip: Always do soil test before applying. Split nitrogen application gives 20-30% better results."],
            'pest': ["🐛 **Pest Control:**\n\n**Aphids/Jassids:** \n• Organic: Neem oil 5ml/L or garlic spray\n• Chemical: Imidacloprid 0.5ml/L\n\n**Whitefly:** \n• Organic: Yellow sticky traps + Neem oil\n• Chemical: Acetamiprid 0.2g/L\n\n**Stem Borer:** \n• Organic: Pheromone traps + Trichogramma wasps\n• Chemical: Chlorpyrifos 2ml/L\n\n**Shoot Borer:**\n• Organic: Remove affected shoots\n• Chemical: Quinalphos 1.5ml/L"],
            'disease': ["🦠 **Disease Control:**\n\n**Powdery Mildew:**\n• Organic: Baking soda 1tbsp/L or sulfur dust\n• Chemical: Wettable Sulfur 3g/L or Tebuconazole\n\n**Rust:**\n• Organic: Remove infected leaves + neem cake\n• Chemical: Propiconazole 1ml/L or Mancozeb 2.5g/L\n\n**Late Blight:**\n• Organic: Copper-based sprays + improve air circulation\n• Chemical: Mancozeb 2.5g/L or Metalaxyl 2g/L\n\n**Bacterial Blight:**\n• Organic: Remove infected plants\n• Chemical: Copper oxychloride 3g/L"],
            'crop': ["🌾 **Crop Guide:**\n\n**Rice:** Kharif (June-Oct), Clay/Alluvial soil, 20-35°C, Water: 100-150cm\n\n**Wheat:** Rabi (Oct-Nov), Loamy soil, 15-25°C, Water: 40-50cm\n\n**Cotton:** Kharif (April-July), Black soil, 25-35°C, Water: 60-80cm\n\n**Maize:** Kharif (June-Oct), Well-drained soil, 20-30°C, Water: 50-80cm\n\n**Sugarcane:** Perennial, Deep loamy soil, 20-35°C, Water: 150-250cm\n\n**Groundnut:** Kharif (June-Oct), Sandy loam, 25-30°C, Water: 45-60cm"],
            'soil': ["🪴 **Soil Types:**\n\n**Black Soil (Cotton Soil):**\n• Best for: Cotton, Sorghum, Wheat\n• Good water retention\n• Needs organic matter\n\n**Red Soil:**\n• Best for: Groundnut, Rice, Maize, Finger millet\n• Low water retention\n• Needs regular fertilization\n\n**Alluvial Soil:**\n• Best for: Rice, Wheat, Sugarcane\n• Most fertile\n• Found in Indo-Gangetic plains\n\n**Sandy Soil:**\n• Best for: Bajra, Moong bean\n• Good drainage\n• Needs frequent irrigation"],
            'irrigation': ["💧 **Irrigation Methods:**\n\n**Drip (90% efficiency):**\n• Best for: Vegetables, Fruits, Cotton, Sugarcane\n• Saves 40-60% water\n• Cost: ₹30,000-60,000/acre + 55% PMKSY subsidy\n\n**Sprinkler (70-80%):**\n• Best for: Wheat, Pulses, Potato\n• Works on uneven land\n• Cost: ₹15,000-25,000/acre\n\n**Flood (30-50%):**\n• Best for: Rice, Sugarcane\n• Traditional method\n• High water waste\n\n💡 Best time: Early morning (5-9 AM) or evening (5-8 PM)"],
            'weather': ["🌦️ **Weather Advisory:**\n\n• Monsoon arrives June 15 in India\n• Don't spray if rain expected within 6 hours\n• Cover crops before frost\n• Avoid irrigation during heavy rain\n• Use weather forecasts for planning spraying\n\n**Current Season Tips:**\n• Monitor for pest outbreaks after rains\n• Ensure proper drainage in fields\n• Apply fungicides preventively in humid weather"],
            'market': ["📈 **MSP 2024-25:**\n• Paddy (Common): ₹2,183/quintal\n• Wheat: ₹2,275/quintal\n• Cotton (Medium Staple): ₹6,620/quintal\n• Maize: ₹2,225/quintal\n• Soybean: ₹4,892/quintal\n• Groundnut: ₹6,783/quintal\n• Sugarcane: ₹350/quintal (FRP)\n\n💡 Tip: Sell when market prices are above MSP. Store in controlled conditions if prices expected to rise."],
            'scheme': ["🏛️ **Government Schemes:**\n\n**PM-KISAN:** ₹6,000/year directly to bank account (3 installments of ₹2,000)\n\n**PM Fasal Bima Yojana:** Crop insurance at subsidized rates (2% premium for Kharif, 1.5% for Rabi)\n\n**PMKSY (Pradhan Mantri Krishi Sinchai Yojana):** 55% subsidy for drip irrigation, 50% for sprinkler\n\n**Kisan Credit Card:** Credit up to ₹3 lakhs at 4% interest\n\n**Soil Health Card:** Free soil testing at government labs"],
            'harvest': ["🌾 **Harvest Guide:**\n\n**Rice:**\n• When 80% grains turn golden\n• Moisture content: 14-17%\n• Harvest in morning to avoid grain shattering\n\n**Wheat:**\n• When grains become hard (30% moisture)\n• Golden yellow color\n• Thresh within 2-3 days of cutting\n\n**Cotton:**\n• When 60-70% bolls open\n• Morning picking gives better fiber quality\n\n**Maize:**\n• When husk cover turns brown\n• Grain moisture: 20-25%\n\n**Sugarcane:**\n• 10-12 months after planting\n• Brix value: 18-20%"],
            'seed': ["🌱 **Seed Management:**\n\n**Seed Rates:**\n• Rice: 20-25kg/ha (for 25-30 hills/m²)\n• Wheat: 100kg/ha\n• Cotton: 2-3kg/ha (hybrid), 15-20kg/ha (variety)\n• Maize: 20-25kg/ha\n• Groundnut: 80-100kg/ha\n\n**Seed Treatment:**\n• Carbendazim 2g/kg seed (fungicide)\n• Imidacloprid 5g/kg seed (insecticide)\n• For pulses: Rhizobium culture 5g/kg seed\n\n💡 Always use certified seeds for 15-20% higher yield!"],
            'organic': ["🌿 **Organic Farming:**\n\n**Organic Fertilizers:**\n• Vermicompost: 5-7 tons/ha\n• Farm Yard Manure: 10-20 tons/ha\n• Neem cake: 150-200kg/ha\n• Biofertilizers: Rhizobium, Azotobacter\n\n**Natural Pest Control:**\n• Neem oil 5ml/L water\n• Garlic-chili extract spray\n• Trichoderma viride (fungicide)\n• Pheromone traps for insects\n• Yellow/blue sticky traps\n\n**Benefits:**\n• Improves soil health\n• Residue-free produce\n• Premium market prices\n• Sustainable long-term"],
            'general': ["🌾 **Farming Tips:**\n• Soil test before every season\n• Use balanced NPK fertilizers\n• Adopt drip irrigation\n• Practice IPM for pest control\n• Use certified seeds\n• Practice crop rotation\n• Maintain proper plant spacing", "💰 **To Double Farm Income:**\n1. Diversify crops (include vegetables)\n2. Add value through processing\n3. Use modern technology (drones, sensors)\n4. Link directly to markets/mandi\n5. Practice organic farming for premium prices\n6. Apply for government schemes"],
            'help': ["I can help with:\n🌾 Crops - Which crop to grow\n🧪 Fertilizers - NPK and organic\n🐛 Pests - Organic and chemical control\n💧 Irrigation - Drip, sprinkler methods\n🌦️ Weather - Seasonal advisories\n📈 Market - MSP and selling tips\n🏛️ Schemes - Government subsidies\n🌱 Organic - Natural farming\n\nJust type your question or use voice input!"]
        },
        'hi': {
            'greeting': ["नमस्ते! मैं आपका खेती सहायक हूं। मैं फसल, खाद, कीट, सिंचाई, मौसम, बाजार के बारे में विस्तार से बता सकता हूं। अपना सवाल पूछें!", "हेलो! मैं किसान AI सहायक हूं। आज मैं आपकी क्या मदद कर सकता हूं?\n\nमैं हिंदी में भी जवाब दे सकता हूं!"],
            'fertilizer': ["🌱 **खाद गाइड:**\n\n**धान:** यूरिया 220kg + DAP 130kg + MOP 65kg/हेक्टेयर\n\n**गेहूं:** यूरिया 260kg + DAP 130kg + MOP 65kg/हेक्टेयर\n\n**कपास:** यूरिया 220kg + DAP 110kg + MOP 85kg/हेक्टेयर\n\n💡 सलाह: खाद डालने से पहले मिट्टी जांच जरूर करें। नाइट्रोजन बांटकर डालने से 20-30% बेहतर परिणाम।"],
            'pest': ["🐛 **कीट नियंत्रण:**\n\n**एफिड्स/जस्सिड्स:**\n• जैविक: नीम तेल 5ml/L\n• रासायनिक: इमिडाक्लोप्रिड 0.5ml/L\n\n**व्हाइटफ्लाई:**\n• जैविक: पीले ट्रैप + नीम तेल\n• रासायनिक: एसिटामिप्रिड 0.2g/L\n\n**तना छेदक:**\n• जैविक: फेरोमोन ट्रैप + ट्राइकोग्रामा\n• रासायनिक: क्लोरपाइरीफॉस 2ml/L"],
            'disease': ["🦠 **रोग नियंत्रण:**\n\n**चूर्णिल आसिता (पाउडरी मिल्ड्यू):**\n• जैविक: बेकिंग सोडा 1बड़ा चम्मच/L\n• रासायनिक: सल्फर 3g/L\n\n**रस्ट:**\n• जैविक: प्रभावित पत्तियां हटाएं\n• रासायनिक: प्रोपिकोनाजोल 1ml/L\n\n**पछेता झुलसा (लेट ब्लाइट):**\n• जैविक: तांबा आधारित छिड़काव\n• रासायनिक: मैंकोजेब 2.5g/L"],
            'crop': ["🌾 **फसल गाइड:**\n\n**धान:** खरीफ (जून-अक्टूबर), जलोढ़/चिकनी मिट्टी, 20-35°C\n\n**गेहूं:** रबी (अक्टूबर-नवंबर), दोमट मिट्टी, 15-25°C\n\n**कपास:** खरीफ (अप्रैल-जुलाई), काली मिट्टी, 25-35°C\n\n**मक्का:** खरीफ (जून-अक्टूबर), उर्वर दोमट, 20-30°C\n\n**मूंगफली:** खरीफ (जून-अक्टूबर), बलुई दोमट, 25-30°C"],
            'soil': ["🪴 **मिट्टी के प्रकार:**\n\n**काली मिट्टी:** कपास, गन्ना, ज्वार के लिए बेहतर। पानी रोकने की क्षमता अच्छी।\n\n**लाल मिट्टी:** मूंगफली, चना, बाजरा के लिए। नियमित खाद की जरूरत।\n\n**जलोढ़ मिट्टी:** धान, गेहूं, गन्ना के लिए सबसे उपजाऊ।\n\n**बलुई मिट्टी:** बाजरा, मूंग के लिए। जल निकास अच्छा।"],
            'irrigation': ["💧 **सिंचाई तरीके:**\n\n**ड्रिप (90% दक्षता):** सब्जियां, फल, कपास के लिए बेस्ट। 40-60% पानी बचाती है। PMKSY से 55% सब्सिडी।\n\n**स्प्रिंकलर (70-80%):** गेहूं, आलू, दालों के लिए अच्छी। 50% सब्सिडी।\n\n**बाढ़ (30-50%):** धान, गन्ना के लिए। पारंपरिक तरीका।\n\n💡 सबसे अच्छा समय: सुबह 5-9 बजे या शाम 5-8 बजे।"],
            'weather': ["🌦️ **मौसम सलाह:**\n\n• दक्षिण-पश्चिम मानसून 15 जून के आसपास शुरू\n• बारिश से 6 घंटे पहले छिड़काव न करें\n• पाला गिरने से पहले फसल ढकें\n• भारी बारिश में सिंचाई न करें\n\n**मौसम के अनुसार:**\n• बारिश के बाद कीट का खतरा\n• खेतों में उचित जल निकास सुनिश्चित करें"],
            'market': ["📈 **MSP 2024-25:**\n• धान (सामान्य): ₹2,183/क्विंटल\n• गेहूं: ₹2,275/क्विंटल\n• कपास (मध्यम स्टेपल): ₹6,620/क्विंटल\n• मक्का: ₹2,225/क्विंटल\n• सोयाबीन: ₹4,892/क्विंटल\n• मूंगफली: ₹6,783/क्विंटल\n\n💡 सलाह: MSP से ऊपर भाव में बेचें।"],
            'scheme': ["🏛️ **सरकारी योजनाएं:**\n\n**PM-KISAN:** ₹6,000/साल सीधे बैंक खाते में\n\n**PM फसल बीमा योजना:** कम प्रीमियम पर फसल बीमा\n\n**PMKSY:** ड्रिप पर 55%, स्प्रिंकलर पर 50% सब्सिडी\n\n**किसान क्रेडिट कार्ड:** 4% ब्याज दर पर ₹3 लाख तक क्रेडिट\n\n**मृदा स्वास्थ्य कार्ड:** मुफ्त मिट्टी जांच"],
            'harvest': ["🌾 **कटाई गाइड:**\n\n**धान:** 80% दाने सुनहरे होने पर। नमी 14-17%। सुबह कटाई करें।\n\n**गेहूं:** दाने कड़े होने पर। नमी 12-15%।\n\n**कपास:** 60-70% बॉल्स खुलने पर। सुबह तोड़ें।\n\n**मक्का:** छिलके भूरे होने पर। नमी 20-25%।"],
            'seed': ["🌱 **बीज प्रबंधन:**\n\n**बीज दर:**\n• धान: 20-25kg/ha\n• गेहूं: 100kg/ha\n• कपास: 2-3kg/ha (संकर), 15-20kg/ha (प्रजाति)\n\n**बीज उपचार:**\n• कार्बेंडाज़िम 2g/kg बीज\n• इमिडाक्लोप्रिड 5g/kg बीज\n\n💡 प्रमाणित बीज से 15-20% अधिक पैदावार!"],
            'organic': ["🌿 **जैविक खेती:**\n\n**जैविक खाद:**\n• वर्मीकम्पोस्ट: 5-7 टन/हेक्टेयर\n• गोबर की खाद: 10-20 टन/हेक्टेयर\n• नीम केक: 150-200kg/हेक्टेयर\n\n**प्राकृतिक कीट नियंत्रण:**\n• नीम तेल 5ml/L\n• लहसुन-मिर्च स्प्रे\n• ट्राइकोग्रामा घुन\n\n**लाभ:** मिट्टी स्वास्थ्य, रहित उपज, प्रीमियम भाव"],
            'general': ["🌾 **खेती के टिप्स:**\n• हर सीजन से पहले मिट्टी जांच कराएं\n• संतुलित NPK खाद का उपयोग करें\n• ड्रिप सिंचाई अपनाएं\n• IPM तरीका अपनाएं\n• प्रमाणित बीज का प्रयोग करें\n• फसल चक्र अपनाएं", "💰 **आय दोगुनी करने के उपाय:**\n1. सब्जियां उगाएं\n2. प्रोसेसिंग से जोड़ें\n3. सरकारी योजनाओं का लाभ उठाएं\n4. सीधे बाजार से जुड़ें"],
            'help': ["मैं इन विषयों पर मदद कर सकता हूं:\n🌾 फसलें\n🧪 खाद\n🐛 कीट\n💧 सिंचाई\n🌦️ मौसम\n📈 बाजार भाव\n🏛️ सरकारी योजनाएं\n\nअपना सवाल पूछें या वॉइस बटन का उपयोग करें!"]
        },
        'te': {
            'greeting': ["నమస్కారం! నేను మీ వ్యవసాయ సహాయకుడను. Crops, Fertilizers, Pests, Irrigation, Weather, Market గురించి వివరంగా చెప్పగలను।", "నమస్కారం! వ్యవసాయ AI సహాయకుడిని. ఏం అడగాలి?"],
            'fertilizer': ["🌱 **ఎరువు గైడ్:**\n\n**వరి:** యూరియా 220kg + DAP 130kg + MOP 65kg/హెక్టారు\n\n**గోధుమ:** యూరియా 260kg + DAP 130kg + MOP 65kg/హెక్టారు\n\n**పత్తి:** యూరియా 220kg + DAP 110kg + MOP 85kg/హెక్టారు\n\n💡 చిట్కా: ఎరువులు వేయడానికి ముందు నేల పరీక్ష చేయండి।"],
            'pest': ["🐛 **తెగుళ్ళ నియంత్రణ:**\n\n**ఏఫిడ్స్:**\n• జైవిక: నీమ్ ఆయిల్ 5ml/L\n• రసాయన: ఇమిడాక్లోప్రిడ్ 0.5ml/L\n\n**తెగుళ్ళు:**\n• జైవిక: పసుపు ట్ర్యాప్‌లు + నీమ్\n• రసాయన: క్లోర్పైరిఫాస్ 2ml/L"],
            'crop': ["🌾 **పంటల గైడ్:**\n\n**వరి:** ఖరీఫ్ (జూన్-అక్టోబర్), జలోఢ్/బంక్ నేల, 20-35°C\n\n**గోధుమ:** రబీ (అక్టోబర్-నవంబర్), లోమ్ నేల, 15-25°C\n\n**పత్తి:** ఖరీఫ్ (ఏప్రిల్-జూలై), నలుపు నేల, 25-35°C\n\n**మొక్కజొన్న:** ఖరీఫ్ (జూన్-అక్టోబర్), 20-30°C"],
            'irrigation': ["💧 **నీటి పారుదల విధానాలు:**\n\n**డ్రిప్ (90%):** కూరగాయలు, పండ్లకు ఉత్తమం. 40-60% నీరు ఆదా.\n\n**స్ప్రింక్లర్ (70-80%):** గోధుమ, బంగాళాదుంగకు మంచిది.\n\n💡 ఉత్తమ సమయం: ఉదయం 5-9 గంటలు లేదా సాయంత్రం 5-8 గంటలు।"],
            'weather': ["🌦️ **వాతావరణ సలహా:**\n\n• వర్షాకాలం జూన్ 15 నుండి\n• వర్షం 6 గంటల లోపల వస్తే స్ప్రే చేయకూడదు\n• Frost రాకముందు పంటలను కప్పండి"],
            'market': ["📈 **MSP 2024-25:**\n• వరి: ₹2,183/క్వింటాల్\n• గోధుమ: ₹2,275/క్వింటాల్\n• పత్తి: ₹6,620/క్వింటాల్\n• మొక్కజొన్న: ₹2,225/క్వింటాల్"],
            'scheme': ["🏛️ **ప్రభుత్వ పథకాలు:**\n\n**PM-KISAN:** ₹6,000/సంవత్సరం\n\n**PMKSY:** డ్రిప్‌పై 55% సబ్సిడీ\n\n**కిసాన్ క్రెడిట్ కార్డ్:** 4% వడ్డీకి ₹3 లక్షల వరకు"],
            'organic': ["🌿 **జైవిక వ్యవసాయం:**\n\n• వర్మీకంపోస్ట్: 5-7 టన్నులు/హెక్టారు\n• నీమ్ ఆయిల్ 5ml/L\n• ట్రైకోడర్మా\n\nలాభాలు: నేల ఆరోగ్యం, శుద్ధమైన పంట"],
            'general': ["🌾 **వ్యవసాయ చిట్కాలు:**\n• ప్రతి సీజన్‌కు ముందు నేల పరీక్ష\n• సమతుల్య NPK ఎరువులు\n• డ్రిప్ ఇరిగేషన్\n• ప్రమాణీకృత బియ్యం\n• పంట పరిభ్రమణం", "💰 **ఆదాయం రెట్టింపు:**\n1. కూరగాయలు జోడించు\n2. ప్రభుత్వ పథకాలు ఉపయోగించు\n3. మార్కెట్‌కు నేరుగా అనుసంధానమవు"],
            'help': ["నేను ఈ కింది వాటిలో సహాయం చేయగలను:\n🌾 పంటలు\n🧪 ఎరువులు\n🐛 తెగుళ్ళు\n💧 నీటి పారుదల\n🌦️ వాతావరణం\n📈 మార్కెట్\n🏛️ పథకాలు\n\nమీ प्रश्न అడగండి!"]
        },
        'ta': {
            'greeting': ["வணக்கம்! நான் உங்கள் விவசாய உதவியாளர். Crops, Fertilizers, Pests, Irrigation, Weather, Market பற்றி விளக்கமாக சொல்ல முடியும்।", "வணக்கம்! விவசாய AI உதவியாளர். உங்கள் கேள்வி என்ன?"],
            'fertilizer': ["🌱 **உரம் வழிகாட்டி:**\n\n**நெல்:** யூரியா 220kg + DAP 130kg + MOP 65kg/ஹெக்டேர்\n\n**கோதுமை:** யூரியா 260kg + DAP 130kg + MOP 65kg/ஹெக்டேர்\n\n**பருத்தி:** யூரியா 220kg + DAP 110kg + MOP 85kg/ஹெக்டேர்\n\n💡 குறிப்பு: உரம் போடுவதற்கு முன் மண் பரிசோதனை செய்யுங்கள்।"],
            'pest': ["🐛 **பூச்சி கட்டுப்பாடு:**\n\n**எஃபிட்ஸ்:**\n• இயற்கை: நீம் ஆயில் 5ml/L\n• வேதி: இமிடாக்ளோப்ரிட் 0.5ml/L\n\n**வெள்ளை ஈ:**\n• இயற்கை: மஞ்சள் பொறி + நீம் ஆயில்\n• வேதி: குளோர்பைரிஃபாஸ் 2ml/L"],
            'crop': ["🌾 **பயிர் வழிகாட்டி:**\n\n**நெல்:** खरीई (ஜூன்-அக்டோபர்), ஜலோத்/களிமண், 20-35°C\n\n**கோதுமை:** ரபி (அக்டோபர்-நவம்பர்), சதுர மண், 15-25°C\n\n**பருத்தி:** खरीई (ஏப்ரல்-ஜூலை), கருப்பு மண், 25-35°C\n\n**சோளம்:** खरीई (ஜூன்-அக்டோபர்), 20-30°C"],
            'irrigation': ["💧 **நீர் பாசன முறைகள்:**\n\n**டிரிப் (90%):** காய்கறிகள், பழங்களுக்கு சிறந்தது. 40-60% தண்ணீர் சேமிப்பு।\n\n**ஸ்பிரிங்க்ளர் (70-80%):** கோதுமை, உருளைக்கிழங்குக்கு நல்லது।\n\n💡 சிறந்த நேரம்: காலை 5-9 மணி அல்லது மாலை 5-8 மணி।"],
            'weather': ["🌦️ **வானிலை ஆலோசனை:**\n\n• பருவமழை ஜூன் 15ல்\n• மழை 6 மணி நேரத்தில் வரும் என்றால் தெளிக்க வேண்டாம்\n• Frost வருவதற்கு முன் பயிர்களை மூடுங்கள்"],
            'market': ["📈 **MSP 2024-25:**\n• நெல்: ₹2,183/க்விண்டால்\n• கோதுமை: ₹2,275/க்விண்டால்\n• பருத்தி: ₹6,620/க்விண்டால்\n• சோளம்: ₹2,225/க்விண்டால்"],
            'scheme': ["🏛️ **அரசு திட்டங்கள்:**\n\n**PM-KISAN:** ₹6,000/ஆண்டு\n\n**PMKSY:** டிரிப்புக்கு 55% Dotação\n\n**கிசான் கிரெடிட் கார்டு:** 4% வட்டிக்கு ₹3 லட்சம் வரை"],
            'organic': ["🌿 **இயற்கை விவசாயம்:**\n\n• வேர்மிகம்போஸ்ட்: 5-7 டன்/ஹெக்டேர்\n• நீம் ஆயில் 5ml/L\n• ட்ரைகோடெர்மா\n\nநன்மைகள்: மண் ஆரோக்கியம், தூய்மையான harvest"],
            'general': ["🌾 **விவசாய குறிப்புகள்:**\n• ஒவ்வொரு பருவத்திற்கும் முன் மண் பரிசோதனை\n• சமநிலை NPK உரங்கள்\n• டிரிப் பாசனம்\n• சான்று விதைகள்\n• பயிர் சுழற்சி", "💰 **வருமானம் இரட்டிப்பாக:**\n1. காய்கறிகள் சேர்த்தல்\n2. அரசு திட்டங்கள் பயன்படுத்தல்\n3. நேரடி சந்தையுடன் இணைதல்"],
            'help': ["நான் இவற்றில் உதவ முடியும்:\n🌾 பயிர்கள்\n🧪 உரங்கள்\n🐛 பூச்சிகள்\n💧 பாசனம்\n🌦️ வானிலை\n📈 சந்தை\n🏛️ திட்டங்கள்\n\nஉங்கள் سؤالைக் கேட்க!"]
        },
        'kn': {
            'greeting': ["ನಮಸ್ತೆ! ನಾನು ನಿಮ್ಮ ಕೃಷಿ ಸಹಾಯಕ. ಬೆಳೆ, ಗೊಬ್ಬರ, ಕೀಟ, ನೀರಾವರಿ, ಹವಾಮಾನ, ಮಾರುಕಟ್ಟೆ ಬಗ್ಗೆ ವಿವರವಾಗಿ ಹೇಳಬಲ್ಲೆ।", "ನಮಸ್ತೆ! ಕೃಷಿ AI ಸಹಾಯಕ. ಏನು ಕೇಳಬೇಕು?"],
            'fertilizer': ["🌱 **ಗೊಬ್ಬರ ಮಾರ್ಗದರ್ಶಿ:**\n\n**ಅಕ್ಕಿ:** ಯೂರಿಯಾ 220kg + DAP 130kg + MOP 65kg/ಹೆಕ್ಟೇರ್\n\n**ಗೋಧಿ:** ಯೂರಿಯಾ 260kg + DAP 130kg + MOP 65kg/ಹೆಕ್ಟೇರ್\n\n**ಹತ್ತಿ:** ಯೂರಿಯಾ 220kg + DAP 110kg + MOP 85kg/ಹೆಕ್ಟೇರ್\n\n💡 ಸಲಹೆ: ಗೊಬ್ಬರ ಹಾಕುವ ಮೊದಲು ಮಣ್ಣು ಪರೀಕ್ಷೆ ಮಾಡಿ।"],
            'pest': ["🐛 **ಕೀಟ ನಿಯಂತ್ರಣ:**\n\n**ಏಫಿಡ್ಸ್:**\n• ಜೈವಿಕ: ನೀಮ್ ಆಯಿಲ್ 5ml/L\n• ರಾಸಾಯನಿಕ: ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ 0.5ml/L\n\n**ಬಿಳಿನೊಣ:**\n• ಜೈವಿಕ: ಹಳದಿ ಪಾಶ್ಚಿಮಾರಿಕೆಗಳು + ನೀಮ್ ಆಯಿಲ್\n• ರಾಸಾಯನಿಕ: ಕ್ಲೋರ್ಪೈರಿಫಾಸ್ 2ml/L"],
            'crop': ["🌾 **ಬೆಳೆ ಮಾರ್ಗದರ್ಶಿ:**\n\n**ಅಕ್ಕಿ:** ಖರೀಫ್ (ಜೂನ್-ಅಕ್ಟೋಬರ್), ಜಲೋಢ್/ಜೇಡ್ ಮಣ್ಣು, 20-35°C\n\n**ಗೋಧಿ:** ರಬಿ (ಅಕ್ಟೋಬರ್-ನವೆಂಬರ್), ಲೋಮ್ ಮಣ್ಣು, 15-25°C\n\n**ಹತ್ತಿ:** ಖರೀಫ್ (ಏಪ್ರಿಲ್-ಜುಲೈ), ಕಪ್ಪು ಮಣ್ಣು, 25-35°C\n\n**ಮೆಕ್ಕೆ:** ಖರೀಫ್ (ಜೂನ್-ಅಕ್ಟೋಬರ್), 20-30°C"],
            'irrigation': ["💧 **ನೀರಾವರಿ ವಿಧಾನಗಳು:**\n\n**ಡ್ರಿಪ್ (90%):** ತರಕಾರಿ, ಹಣ್ಣುಗಳಿಗೆ ಉತ್ತಮ. 40-60% ನೀರು ಉಳಿತಾಯ।\n\n**ಸ್ಪ್ರಿಂಕ್ಲರ್ (70-80%):** ಗೋಧಿ, ಆಲೂಗಡ್ಡಿಗೆ ಒಳ್ಳೆಯದು।\n\n💡 ಉತ್ತಮ ಸಮಯ: ಬೆಳಿಗ್ಗೆ 5-9 ಗಂಟೆ ಅಥವಾ ಸಾಯಂಕಾಲ 5-8 ಗಂಟೆ।"],
            'weather': ["🌦️ **ಹವಾಮಾನ ಸಲಹೆ:**\n\n• ಮಳೆಗಾಲ ಜೂನ್ 15ರಿಂದ\n• ಮಳೆ 6 ಗಂಟೆಯೊಳಗೆ ಬರುತ್ತದೆ ಎಂದರೆ ಸಿಂಪಡಿಸಬಾರದು\n• ಹಿಮ ಬೀಳುವ ಮೊದಲು ಬೆಳೆಗಳನ್ನು ಆವರಿಸಿ"],
            'market': ["📈 **MSP 2024-25:**\n• ಅಕ್ಕಿ: ₹2,183/ಕ್ವಿಂಟಾಲ್\n• ಗೋಧಿ: ₹2,275/ಕ್ವಿಂಟಾಲ್\n• ಹತ್ತಿ: ₹6,620/ಕ್ವಿಂಟಾಲ್\n• ಮೆಕ್ಕೆ: ₹2,225/ಕ್ವಿಂಟಾಲ್"],
            'scheme': ["🏛️ **ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು:**\n\n**PM-KISAN:** ₹6,000/ವರ್ಷ\n\n**PMKSY:** ಡ್ರಿಪ್‌ಗೆ 55%  dotação\n\n**ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್:** 4% ಬಡ್ಡಿಗೆ ₹3 ಲಕ್ಷದವರೆಗೆ"],
            'organic': ["🌿 **ಸಾವಯವ ಕೃಷಿ:**\n\n• ವರ್ಮಿಕಂಪೋಸ್ಟ್: 5-7 ಟನ್/ಹೆಕ್ಟೇರ್\n• ನೀಮ್ ಆಯಿಲ್ 5ml/L\n• ಟ್ರೈಕೋಡರ್ಮಾ\n\nಪ್ರಯೋಜನಗಳು: ಮಣ್ಣಿನ ಆರೋಗ್ಯ, ಸಿಹಿ ಬೆಳೆ"],
            'general': ["🌾 **ಕೃಷಿ ಸಲಹೆಗಳು:**\n• ಪ್ರತಿ ಋತುವಿಗೆ ಮೊದಲು ಮಣ್ಣು ಪರೀಕ್ಷೆ\n• ಸಮತೋಲಿತ NPK ಗೊಬ್ಬರಗಳು\n• ಡ್ರಿಪ್ ನೀರಾವರಿ\n• ಪ್ರಮಾಣಿತ ಬಿತ್ತನೆ\n• ಬೆಳೆ ಸರ್ಕ್ಯೂಟ್", "💰 **ಆದಾಯ ದ್ವಿಗುಣ:**\n1. ತರಕಾರಿಗಳನ್ನು ಸೇರಿಸಿ\n2. ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಬಳಸಿ\n3. ನೇರ ಮಾರುಕಟ್ಟೆಗೆ ಸಂಪರ್ಕಿಸಿ"],
            'help': ["ನಾನು ಇವುಗಳಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ:\n🌾 ಬೆಳೆಗಳು\n🧪 ಗೊಬ್ಬರಗಳು\n🐛 ಕೀಟಗಳು\n💧 ನೀರಾವರಿ\n🌦️ ಹವಾಮಾನ\n📈 ಮಾರುಕಟ್ಟೆ\n🏛️ ಯೋಜನೆಗಳು\n\nನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ!"]
        }
    }
    
    keywords = {
        'fertilizer': ['fertilizer', 'urea', 'dap', 'npk', 'manure', 'compost', 'gypsum', 'fym', 'vermicompost', 'potash', 'nitrogen', 'phosphorus', 'potassium', 'खाद', 'ఎరువు', 'fertiliser', 'உரம்'],
        'pest': ['pest', 'insect', 'bug', 'worm', 'fly', 'maggot', 'borer', 'aphid', 'weevil', 'beetle', 'thrips', 'jassid', 'whitefly', 'कीट', 'తెగుళ్ళు', 'puchi', 'பூச்சி'],
        'disease': ['disease', 'blight', 'rot', 'mildew', 'rust', 'spot', 'wilt', 'virus', 'fungal', 'bacterial', 'रोग', 'వ్యాధి', 'rog', 'நோய்'],
        'crop': ['crop', 'plant', 'grow', 'cultivation', 'paddy', 'wheat', 'rice', 'cotton', 'maize', 'groundnut', 'sugarcane', 'soybean', 'tomato', 'potato', 'onion', 'bajra', 'पैदावार', 'పంట', 'pala', 'பயிர்'],
        'soil': ['soil', 'mitti', 'earth', 'land', 'field', 'ph', 'black', 'red', 'alluvial', 'sandy', 'clay', 'loam', 'मिट्टी', 'నేల', 'mitta', 'மண்'],
        'irrigation': ['water', 'irrigation', 'drip', 'sprinkler', 'flood', 'furrow', 'drain', 'moisture', 'pani', 'पानी', 'నీరు', 'jal', 'நீர்'],
        'weather': ['weather', 'rain', 'monsoon', 'humid', 'temperature', 'climate', 'storm', 'frost', 'mausam', 'मौसम', 'వాతావరణం', 'காலநிலை'],
        'market': ['market', 'price', 'msp', 'sell', 'buy', 'mandi', 'rate', 'quintal', 'भाव', 'ధర', 'bhav', 'சந்தை'],
        'scheme': ['scheme', 'yojana', 'pm kisan', 'government', 'subsidy', 'loan', 'credit', 'प्रधानमंत्री', 'పథకం', 'yojna', 'திட்டம்'],
        'harvest': ['harvest', 'yield', 'production', 'cut', 'collect', 'storage', 'dry', 'कटाई', 'pidi', 'அறுவடை'],
        'seed': ['seed', 'sowing', 'germination', 'variety', 'hybrid', 'बीज', 'beej', 'vith', 'விதை'],
        'organic': ['organic', 'natural', 'bio', 'eco', 'green', 'जैविक', 'నాణ్య', 'jemevi', 'கரிம'],
        'general': ['farming', 'agriculture', 'kheti', 'cultivation', 'farm', 'tips', 'advice', 'help', 'sheti', 'விவசாய']
    }
    
    lang_resp = responses.get(lang, responses['en'])
    
    greetings = ['hello', 'hi', 'namaste', 'namaskar', 'vanakkam', 'swagatha', 'howdy', 'good morning', 'good evening', 'नमस्ते', 'नमस्कार', 'வணக்கம்', 'ನಮಸ್ತೆ']
    if any(g in msg for g in greetings):
        return random.choice(lang_resp.get('greeting', lang_resp['help']))
    
    for category, words in keywords.items():
        if any(word in msg for word in words):
            return random.choice(lang_resp.get(category, lang_resp['general']))
    
    return random.choice(lang_resp.get('general', lang_resp['help']))

@app.route('/api/crop', methods=['POST'])
def crop_api():
    data = request.get_json()
    soil = data.get('soil_type', '').lower()
    season = data.get('season', '').lower()
    
    crops_db = {
        'black': {
            'kharif': [{'crop': 'Cotton', 'confidence': 95}, {'crop': 'Soybean', 'confidence': 88}, {'crop': 'Sugarcane', 'confidence': 85}],
            'rabi': [{'crop': 'Wheat', 'confidence': 90}, {'crop': 'Chickpea', 'confidence': 82}],
            'zaid': [{'crop': 'Moong Bean', 'confidence': 85}, {'crop': 'Watermelon', 'confidence': 80}]
        },
        'red': {
            'kharif': [{'crop': 'Groundnut', 'confidence': 92}, {'crop': 'Rice', 'confidence': 85}],
            'rabi': [{'crop': 'Wheat', 'confidence': 88}, {'crop': 'Potato', 'confidence': 85}],
            'zaid': [{'crop': 'Maize', 'confidence': 88}, {'crop': 'Green Gram', 'confidence': 82}]
        },
        'alluvial': {
            'kharif': [{'crop': 'Rice', 'confidence': 98}, {'crop': 'Sugarcane', 'confidence': 92}],
            'rabi': [{'crop': 'Wheat', 'confidence': 95}, {'crop': 'Potato', 'confidence': 90}],
            'zaid': [{'crop': 'Rice', 'confidence': 88}]
        },
        'sandy': {
            'kharif': [{'crop': 'Groundnut', 'confidence': 90}, {'crop': 'Bajra', 'confidence': 88}],
            'rabi': [{'crop': 'Chickpea', 'confidence': 85}, {'crop': 'Barley', 'confidence': 82}],
            'zaid': [{'crop': 'Moong Bean', 'confidence': 90}, {'crop': 'Sesame', 'confidence': 85}]
        },
        'clay': {
            'kharif': [{'crop': 'Rice', 'confidence': 95}, {'crop': 'Sugarcane', 'confidence': 90}],
            'rabi': [{'crop': 'Wheat', 'confidence': 88}, {'crop': 'Peas', 'confidence': 82}],
            'zaid': [{'crop': 'Rice', 'confidence': 85}]
        }
    }
    
    crops = crops_db.get(soil, {}).get(season, [{'crop': 'Wheat', 'confidence': 70}])
    return jsonify({'status': 'success', 'crops': crops})

@app.route('/api/crops/list', methods=['GET'])
def crops_list_api():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT name, soil_type, season, water_requirement, temp_range FROM crops')
    crops = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'status': 'success', 'crops': crops})

@app.route('/api/fertilizer', methods=['POST'])
def fertilizer_api():
    data = request.get_json()
    crop = data.get('crop', '').lower()
    
    fertilizer_db = {
        'rice': {'name': 'Rice', 'npk': '100:60:40 kg/ha', 'urea': '220 kg/ha (3 doses)', 'dap': '130 kg/ha', 'mop': '65 kg/ha', 'fym': '10 tons/ha', 'schedule': 'Basal DAP+MOP → Urea at 21, 45, 65 days', 'tips': ['Apply zinc sulfate 25kg/ha', 'Maintain 5cm water depth', 'Split nitrogen for better efficiency'], 'best_fertilizers': [{'name': 'Urea 46% N', 'description': 'Primary nitrogen source for rapid growth', 'dose': '220 kg/ha in 3 splits', 'icon': 'fas fa-fire text-danger'}, {'name': 'DAP 18:46:0', 'description': 'Best for basal application at sowing', 'dose': '130 kg/ha', 'icon': 'fas fa-dna text-primary'}, {'name': 'Vermicompost', 'description': 'Organic supplement improves soil health', 'dose': '5 tons/ha', 'icon': 'fas fa-leaf text-success'}, {'name': 'Zinc Sulfate', 'description': 'Essential micronutrient for rice', 'dose': '25 kg/ha once', 'icon': 'fas fa-star text-warning'}]},
        'wheat': {'name': 'Wheat', 'npk': '120:60:40 kg/ha', 'urea': '260 kg/ha (2 doses)', 'dap': '130 kg/ha', 'mop': '65 kg/ha', 'fym': '15 tons/ha', 'schedule': 'Basal DAP+MOP → Urea at 21 & 45 days', 'tips': ['Apply at crown root initiation', 'Irrigate after nitrogen application', 'Use need-based nitrogen'], 'best_fertilizers': [{'name': 'Urea 46% N', 'description': 'Main nitrogen source for grain filling', 'dose': '260 kg/ha in 2 splits', 'icon': 'fas fa-fire text-danger'}, {'name': 'DAP 18:46:0', 'description': 'Phosphorus for root development', 'dose': '130 kg/ha basal', 'icon': 'fas fa-dna text-primary'}, {'name': 'MOP 60% K2O', 'description': 'Potassium for grain quality', 'dose': '65 kg/ha basal', 'icon': 'fas fa-lemon text-warning'}, {'name': 'FYM', 'description': 'Improves soil structure and water retention', 'dose': '15 tons/ha', 'icon': 'fas fa-leaf text-success'}]},
        'cotton': {'name': 'Cotton', 'npk': '100:50:50 kg/ha', 'urea': '220 kg/ha (4 doses)', 'dap': '110 kg/ha', 'mop': '85 kg/ha', 'fym': '10 tons/ha', 'schedule': 'Basal → Urea at 30, 45, 60, 90 days', 'tips': ['Apply boron 0.2% foliar spray', 'Use drip fertigation', 'Monitor boll development'], 'best_fertilizers': [{'name': 'Urea 46% N', 'description': 'Split application for continuous growth', 'dose': '220 kg/ha in 4 splits', 'icon': 'fas fa-fire text-danger'}, {'name': 'DAP 18:46:0', 'description': 'For early root and boll development', 'dose': '110 kg/ha basal', 'icon': 'fas fa-dna text-primary'}, {'name': 'MOP 60% K2O', 'description': 'Essential for boll opening', 'dose': '85 kg/ha', 'icon': 'fas fa-lemon text-warning'}, {'name': 'Boron 0.2%', 'description': 'Critical for cotton flowering', 'dose': 'Foliar spray 2 times', 'icon': 'fas fa-star text-info'}]},
        'maize': {'name': 'Maize', 'npk': '120:60:40 kg/ha', 'urea': '260 kg/ha (3 doses)', 'dap': '130 kg/ha', 'mop': '65 kg/ha', 'fym': '10 tons/ha', 'schedule': 'Basal DAP+MOP → Urea at 21 & 45 days', 'tips': ['Apply zinc sulfate 25kg/ha', 'Critical at knee height stage', 'Avoid water stress'], 'best_fertilizers': [{'name': 'Urea 46% N', 'description': 'For rapid growth at knee height', 'dose': '260 kg/ha in 3 splits', 'icon': 'fas fa-fire text-danger'}, {'name': 'DAP 18:46:0', 'description': 'Phosphorus for early vigor', 'dose': '130 kg/ha basal', 'icon': 'fas fa-dna text-primary'}, {'name': 'Zinc Sulfate', 'description': 'Prevents white seedling disease', 'dose': '25 kg/ha basal', 'icon': 'fas fa-star text-warning'}, {'name': 'Neem Cake', 'description': 'Organic N supplement with pest control', 'dose': '150 kg/ha', 'icon': 'fas fa-leaf text-success'}]},
        'groundnut': {'name': 'Groundnut', 'npk': '20:40:40 kg/ha', 'urea': '25 kg/ha', 'dap': '87 kg/ha', 'mop': '65 kg/ha', 'fym': '5 tons/ha', 'schedule': 'Basal + Gypsum 400kg at 45 days', 'tips': ['Gypsum increases yield by 20%', 'Apply at pegging stage', 'Calcium essential for pods'], 'best_fertilizers': [{'name': 'Gypsum', 'description': 'Best for pod development and calcium', 'dose': '400 kg/ha at pegging', 'icon': 'fas fa-star text-info'}, {'name': 'DAP 18:46:0', 'description': 'Phosphorus for root nodules', 'dose': '87 kg/ha basal', 'icon': 'fas fa-dna text-primary'}, {'name': 'MOP 60% K2O', 'description': 'Potassium for oil content', 'dose': '65 kg/ha', 'icon': 'fas fa-lemon text-warning'}, {'name': 'Vermicompost', 'description': 'Organic matter for soil health', 'dose': '5 tons/ha', 'icon': 'fas fa-leaf text-success'}]},
        'sugarcane': {'name': 'Sugarcane', 'npk': '250:60:120 kg/ha', 'urea': '325 kg/ha (3 doses)', 'dap': '130 kg/ha', 'mop': '200 kg/ha', 'fym': '25 tons/ha', 'schedule': 'Basal → Urea at 45, 90, 135 days', 'tips': ['Trash mulching conserves moisture', 'Apply N in splits', 'Earth up at 45 days'], 'best_fertilizers': [{'name': 'Urea 46% N', 'description': 'Heavy N requirement for tall cane', 'dose': '325 kg/ha in 3 splits', 'icon': 'fas fa-fire text-danger'}, {'name': 'MOP 60% K2O', 'description': 'High potassium for sucrose content', 'dose': '200 kg/ha', 'icon': 'fas fa-lemon text-warning'}, {'name': 'DAP 18:46:0', 'description': 'Initial phosphorus for sprouting', 'dose': '130 kg/ha basal', 'icon': 'fas fa-dna text-primary'}, {'name': 'FYM', 'description': 'Organic matter improves ratoon crop', 'dose': '25 tons/ha', 'icon': 'fas fa-leaf text-success'}]},
        'tomato': {'name': 'Tomato', 'npk': '150:100:100 kg/ha', 'urea': '200 kg/ha (weekly)', 'dap': '200 kg/ha', 'mop': '165 kg/ha', 'fym': '20 tons/ha', 'schedule': 'Weekly urea 1% foliar after flowering', 'tips': ['Calcium prevents blossom end rot', 'Drip fertigation is best', 'Avoid excess nitrogen'], 'best_fertilizers': [{'name': 'DAP 18:46:0', 'description': 'For strong vegetative growth', 'dose': '200 kg/ha basal', 'icon': 'fas fa-dna text-primary'}, {'name': 'MOP 60% K2O', 'description': 'For fruit development and quality', 'dose': '165 kg/ha', 'icon': 'fas fa-lemon text-warning'}, {'name': 'Calcium Nitrate', 'description': 'Prevents blossom end rot', 'dose': '10 kg/acre at flowering', 'icon': 'fas fa-star text-info'}, {'name': 'Vermicompost', 'description': 'Organic base for soil health', 'dose': '20 tons/ha', 'icon': 'fas fa-leaf text-success'}]},
        'potato': {'name': 'Potato', 'npk': '120:80:120 kg/ha', 'urea': '180 kg/ha (2 doses)', 'dap': '175 kg/ha', 'mop': '200 kg/ha', 'fym': '20 tons/ha', 'schedule': 'Basal → Urea at 30 days', 'tips': ['Hilling up buries stolons', 'Tuber initiation needs cool soil', 'Avoid high nitrogen'], 'best_fertilizers': [{'name': 'MOP 60% K2O', 'description': 'High K for tuber size and quality', 'dose': '200 kg/ha', 'icon': 'fas fa-lemon text-warning'}, {'name': 'DAP 18:46:0', 'description': 'Phosphorus for tuber initiation', 'dose': '175 kg/ha basal', 'icon': 'fas fa-dna text-primary'}, {'name': 'Urea 46% N', 'description': 'Nitrogen for foliage growth', 'dose': '180 kg/ha in 2 splits', 'icon': 'fas fa-fire text-danger'}, {'name': 'FYM', 'description': 'Improves soil texture for tubers', 'dose': '20 tons/ha', 'icon': 'fas fa-leaf text-success'}]}
    }
    
    result = fertilizer_db.get(crop, {
        'name': crop.title() if crop else 'General',
        'npk': '100:60:40 kg/ha (general)',
        'urea': '200 kg/ha (split application)',
        'dap': '100 kg/ha at sowing',
        'mop': '60 kg/ha',
        'fym': '10 tons/ha',
        'schedule': 'Basal + Split nitrogen',
        'tips': ['Always do soil test', 'Use balanced NPK', 'Combine organic + chemical'],
        'best_fertilizers': [{'name': 'Urea 46% N', 'description': 'Primary nitrogen source', 'dose': '200 kg/ha split', 'icon': 'fas fa-fire text-danger'}, {'name': 'DAP 18:46:0', 'description': 'Phosphorus for root development', 'dose': '100 kg/ha basal', 'icon': 'fas fa-dna text-primary'}, {'name': 'MOP 60% K2O', 'description': 'Potassium for quality', 'dose': '60 kg/ha', 'icon': 'fas fa-lemon text-warning'}, {'name': 'Vermicompost', 'description': 'Organic matter for soil health', 'dose': '10 tons/ha', 'icon': 'fas fa-leaf text-success'}]
    })
    
    return jsonify({'status': 'success', 'fertilizer': result})

@app.route('/api/irrigation', methods=['POST'])
def irrigation_api():
    data = request.get_json()
    method = data.get('method', 'drip').lower()
    crop = data.get('crop', 'general')
    
    irrigation_db = {
        'drip': {'name': 'Drip Irrigation', 'efficiency': '90-95%', 'water_saving': '40-60%', 'cost': '₹30,000-60,000/acre', 'subsidy': '55% under PMKSY', 'best_for': 'Vegetables, Fruits, Cotton, Sugarcane', 'pros': ['Maximum water efficiency', 'Direct to root zone', 'Less weed growth', 'Fertilizer through system'], 'cons': ['High initial cost', 'Clogging issues', 'Needs filtration']},
        'sprinkler': {'name': 'Sprinkler Irrigation', 'efficiency': '70-80%', 'water_saving': '30-40%', 'cost': '₹15,000-25,000/acre', 'subsidy': '50% under PMKSY', 'best_for': 'Wheat, Pulses, Potato, Uneven land', 'pros': ['Works on uneven land', 'Good for close crops', 'Portable systems', 'Automated'], 'cons': ['High evaporation', 'Not for tall crops', 'Wind affects distribution']},
        'flood': {'name': 'Flood Irrigation', 'efficiency': '30-50%', 'water_saving': 'Least', 'cost': '₹5,000-10,000/acre', 'subsidy': 'None', 'best_for': 'Rice, Sugarcane', 'pros': ['Low cost', 'Simple', 'Good for rice'], 'cons': ['High waste', 'Uneven', 'Weeds']},
        'furrow': {'name': 'Furrow Irrigation', 'efficiency': '50-60%', 'water_saving': 'Moderate', 'cost': '₹8,000-15,000/acre', 'subsidy': 'None', 'best_for': 'Row crops - Tomato, Cotton, Maize', 'pros': ['Better than flood', 'Less plant contact', 'Easy'], 'cons': ['Still wasteful', 'Labor intensive', 'Needs leveling']}
    }
    
    result = irrigation_db.get(method, irrigation_db['drip'])
    
    crop_schedule = {
        'rice': 'Maintain 5cm standing water. Flood 2-3 days after transplanting.',
        'wheat': 'Critical: CRI (21 days), Tillering (35), Jointing (55), Flowering (75).',
        'cotton': 'First irrigation 30-35 DAS. Every 7-10 days. Critical: Flowering & boll development.',
        'vegetables': 'Daily or alternate day. Drip preferred. Avoid wetting leaves.',
        'general': 'Irrigate early morning or evening. Check soil moisture before irrigating.'
    }
    
    result['crop_schedule'] = crop_schedule.get(crop, crop_schedule['general'])
    result['timing'] = 'Best time: Early morning (5-9 AM) or evening (5-8 PM)'
    
    return jsonify({'status': 'success', 'irrigation': result})

@app.route('/api/weather', methods=['GET'])
def weather_api():
    conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Heavy Rain']
    temp = random.randint(28, 38)
    
    return jsonify({
        'status': 'success',
        'location': request.args.get('location', 'Central India'),
        'current': {
            'temp': temp,
            'condition': random.choice(conditions),
            'humidity': random.randint(45, 85),
            'wind': random.randint(5, 20),
            'rainfall': random.randint(0, 15),
            'uv': random.randint(5, 11)
        },
        'forecast': [
            {'day': 'Today', 'high': temp+3, 'low': temp-8, 'condition': random.choice(conditions), 'rain': random.randint(0, 60)},
            {'day': 'Tomorrow', 'high': temp+4, 'low': temp-7, 'condition': random.choice(conditions), 'rain': random.randint(0, 70)},
            {'day': 'Day 3', 'high': temp+2, 'low': temp-6, 'condition': random.choice(conditions), 'rain': random.randint(10, 80)},
            {'day': 'Day 4', 'high': temp+5, 'low': temp-9, 'condition': random.choice(conditions), 'rain': random.randint(20, 90)},
            {'day': 'Day 5', 'high': temp+3, 'low': temp-7, 'condition': random.choice(conditions), 'rain': random.randint(0, 50)},
            {'day': 'Day 6', 'high': temp+4, 'low': temp-8, 'condition': random.choice(conditions), 'rain': random.randint(0, 40)},
            {'day': 'Day 7', 'high': temp+2, 'low': temp-6, 'condition': random.choice(conditions), 'rain': random.randint(0, 30)}
        ],
        'advisory': 'Monitor crops for pests. Avoid spray if rain expected. Irrigate early morning.',
        'last_updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    })

@app.route('/api/market', methods=['GET'])
def market_api():
    return jsonify({
        'status': 'success',
        'region': 'Central India Mandi',
        'last_updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        'commodities': [
            {'name': 'Rice (धान)', 'price': 2183, 'unit': 'quintal', 'msp': 2183, 'change': '+50', 'trend': 'up'},
            {'name': 'Wheat (गेहूं)', 'price': random.randint(2200, 2400), 'unit': 'quintal', 'msp': 2275, 'change': '-25', 'trend': 'down'},
            {'name': 'Cotton (कपास)', 'price': random.randint(6500, 6800), 'unit': 'quintal', 'msp': 6620, 'change': '+120', 'trend': 'up'},
            {'name': 'Maize (मक्का)', 'price': random.randint(1900, 2100), 'unit': 'quintal', 'msp': 2225, 'change': '+12', 'trend': 'up'},
            {'name': 'Soybean (सोयाबीन)', 'price': random.randint(4700, 5100), 'unit': 'quintal', 'msp': 4892, 'change': '+70', 'trend': 'up'},
            {'name': 'Groundnut (मूंगफली)', 'price': random.randint(5200, 5500), 'unit': 'quintal', 'msp': 6783, 'change': '-72', 'trend': 'down'},
            {'name': 'Sugarcane (गन्ना)', 'price': 350, 'unit': 'quintal', 'msp': 350, 'change': '0', 'trend': 'stable'},
            {'name': 'Mustard (सरसों)', 'price': random.randint(4500, 5000), 'unit': 'quintal', 'msp': 5950, 'change': '+50', 'trend': 'up'},
            {'name': 'Onion (प्याज)', 'price': random.randint(1500, 2500), 'unit': 'quintal', 'msp': 'N/A', 'change': '+250', 'trend': 'up'},
            {'name': 'Potato (आलू)', 'price': random.randint(1000, 1500), 'unit': 'quintal', 'msp': 'N/A', 'change': '-75', 'trend': 'down'}
        ],
        'recommendations': {
            'sell_now': ['Cotton - Prices rising', 'Onion - Supply shortage'],
            'hold': ['Wheat - Prices may rise post-Diwali', 'Potato - Winter demand'],
            'buy': ['Groundnut - Below MSP prices']
        }
    })

@app.route('/api/pest_control', methods=['GET'])
def pest_control_api():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT pd.disease_name, pd.symptoms, pd.treatment, pd.prevention, c.name as crop 
                      FROM pest_diseases pd 
                      JOIN crops c ON pd.crop_id = c.id''')
    pests = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'status': 'success', 'pests': pests})

@app.route('/api/pest_detection', methods=['POST'])
def pest_detection_api():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image provided'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No image selected'})
    
    crop_type = request.form.get('cropType', 'general').lower()
    
    try:
        img = Image.open(file.stream).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img)
        
        height, width, _ = img_array.shape
        total_pixels = height * width
        
        green_pixels = np.sum((img_array[:,:,1] > img_array[:,:,0]) & (img_array[:,:,1] > img_array[:,:,2]) & (img_array[:,:,1] > 50))
        green_ratio = green_pixels / total_pixels
        
        gray = np.mean(img_array, axis=2)
        
        brown_spots = np.sum((img_array[:,:,0] > 100) & (img_array[:,:,0] < 180) & (img_array[:,:,1] > 60) & (img_array[:,:,1] < 120) & (img_array[:,:,2] < 60))
        brown_ratio = brown_spots / total_pixels
        
        yellow_spots = np.sum((img_array[:,:,0] > 180) & (img_array[:,:,1] > 180) & (img_array[:,:,2] < 100))
        yellow_ratio = yellow_spots / total_pixels
        
        dark_spots = np.sum(gray < 60)
        dark_ratio = dark_spots / total_pixels
        
        white_gray = np.sum((gray > 150) & (gray < 220))
        white_ratio = white_gray / total_pixels
        
        leaf_color_avg = float(np.mean(img_array))
        
        lesion_size = max(0.5, (brown_ratio + dark_ratio) * 20)
        spot_count = int((brown_ratio + yellow_ratio + dark_ratio) * 100)
        
        if MODEL is not None and ENCODER is not None:
            features = [[leaf_color_avg, green_ratio, brown_ratio, yellow_ratio, dark_ratio, lesion_size, spot_count]]
            prediction = MODEL.predict(features)
            probability = MODEL.predict_proba(features)
            predicted_disease = ENCODER.inverse_transform(prediction)[0]
            ml_confidence = float(max(probability[0]) * 100)
        else:
            predicted_disease = None
            ml_confidence = 0
        
        if green_ratio > 0.15:
            disease_info = analyze_leaf_disease(crop_type, green_ratio, brown_ratio, yellow_ratio, dark_ratio, white_ratio)
            disease_info['ml_prediction'] = predicted_disease
            disease_info['ml_confidence'] = ml_confidence
        else:
            disease_info = {
                'success': True,
                'result': '<strong>⚠️ Image Not Recognized as Plant Leaf</strong><br>Please upload a clear photo of a plant leaf.',
                'confidence': 'N/A',
                'tips': ['Take photo in good lighting', 'Focus on affected leaf area', 'Ensure leaf fills most of the frame'],
                'is_leaf': False,
                'ml_prediction': None,
                'ml_confidence': 0
            }
        
        return jsonify(disease_info)
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Analysis failed: {str(e)}'})

def analyze_leaf_disease(crop_type, green_ratio, brown_ratio, yellow_ratio, dark_ratio, white_ratio):
    disease_db = {
        'rice': [
            {'name': 'Rice Blast', 'ratio': (brown_ratio, 0.05, 0.25), 'conf': 88, 'treat': ['Apply Tricyclazole 0.6g/L', 'Spray twice at 15 days interval', 'Drain fields']},
            {'name': 'Bacterial Leaf Blight', 'ratio': (yellow_ratio, 0.03, 0.15), 'conf': 85, 'treat': ['Apply copper bactericides', 'Remove infected leaves', 'Avoid excess nitrogen']},
            {'name': 'Sheath Blight', 'ratio': (dark_ratio, 0.10, 0.30), 'conf': 82, 'treat': ['Apply Hexaconazole 2ml/L', 'Reduce plant density', 'Drain excess water']},
            {'name': 'Brown Spot', 'ratio': (brown_ratio, 0.02, 0.10), 'conf': 80, 'treat': ['Apply Mancozeb 2.5g/L', 'Improve drainage', 'Balanced fertilization']}
        ],
        'wheat': [
            {'name': 'Rust Disease', 'ratio': (yellow_ratio, 0.05, 0.20), 'conf': 90, 'treat': ['Apply Propiconazole 1ml/L', 'Remove infected plants', 'Use resistant varieties']},
            {'name': 'Powdery Mildew', 'ratio': (white_ratio, 0.15, 0.40), 'conf': 87, 'treat': ['Apply Sulfur fungicide', 'Improve air circulation', 'Avoid excess nitrogen']},
            {'name': 'Leaf Blight', 'ratio': (brown_ratio, 0.05, 0.15), 'conf': 83, 'treat': ['Apply Mancozeb 2.5g/L', 'Remove debris', 'Crop rotation']}
        ],
        'cotton': [
            {'name': 'Leaf Curl Virus', 'ratio': (dark_ratio, 0.10, 0.25), 'conf': 86, 'treat': ['Remove infected plants', 'Control whitefly vectors', 'Use Imidacloprid spray']},
            {'name': 'Bacterial Blight', 'ratio': (brown_ratio, 0.05, 0.15), 'conf': 84, 'treat': ['Apply copper oxychloride 3g/L', 'Avoid wet field work', 'Use resistant varieties']}
        ],
        'tomato': [
            {'name': 'Late Blight', 'ratio': (dark_ratio, 0.15, 0.35), 'conf': 92, 'treat': ['Apply Mancozeb or Metalaxyl 2g/L', 'Remove infected plants', 'Avoid overhead irrigation']},
            {'name': 'Early Blight', 'ratio': (brown_ratio, 0.05, 0.20), 'conf': 88, 'treat': ['Apply Chlorothalonil 2g/L', 'Remove lower leaves', 'Mulching recommended']}
        ],
        'potato': [
            {'name': 'Late Blight', 'ratio': (dark_ratio, 0.15, 0.35), 'conf': 91, 'treat': ['Apply Mancozeb 2.5g/L', 'Remove infected tubers', 'Proper storage']},
            {'name': 'Early Blight', 'ratio': (brown_ratio, 0.05, 0.20), 'conf': 86, 'treat': ['Apply Azoxystrobin', 'Balanced fertilization', 'Remove debris']}
        ],
        'groundnut': [
            {'name': 'Tikka Disease', 'ratio': (brown_ratio, 0.10, 0.30), 'conf': 89, 'treat': ['Apply Chlorothalonil 2g/L', 'Spray 3 times at 15 days', 'Remove infected leaves']},
            {'name': 'Rust Disease', 'ratio': (yellow_ratio, 0.05, 0.20), 'conf': 84, 'treat': ['Apply Mancozeb 2.5g/L', 'Remove infected plants', 'Use resistant varieties']}
        ]
    }
    
    default_diseases = [
        {'name': 'Leaf Spot', 'ratio': (brown_ratio, 0.03, 0.15), 'conf': 80, 'treat': ['Apply fungicide', 'Remove infected parts', 'Improve air circulation']},
        {'name': 'Powdery Mildew', 'ratio': (white_ratio, 0.10, 0.30), 'conf': 82, 'treat': ['Apply sulfur fungicide', 'Reduce humidity', 'Proper spacing']},
        {'name': 'Rust', 'ratio': (yellow_ratio, 0.03, 0.15), 'conf': 78, 'treat': ['Apply fungicide spray', 'Remove infected leaves', 'Use resistant varieties']}
    ]
    
    crop_diseases = disease_db.get(crop_type, default_diseases)
    
    detected = None
    max_score = 0
    best_conf = 0
    best_tips = []
    
    for disease in crop_diseases:
        ratio_type, min_r, max_r = disease['ratio']
        if min_r <= ratio_type <= max_r:
            score = disease['conf'] * (1 - abs(ratio_type - (min_r + max_r) / 2))
            if score > max_score:
                max_score = score
                detected = disease['name']
                best_conf = min(95, disease['conf'] + int(ratio_type * 30))
                best_tips = disease['treat']
    
    if detected:
        return {
            'success': True,
            'result': f'<strong>🔍 Detected Disease:</strong> {detected}<br><strong>Affected Crop:</strong> {crop_type.title()}',
            'confidence': f'{best_conf}% confidence',
            'tips': best_tips + ['Monitor regularly', 'Use certified seeds', 'Practice crop rotation'],
            'is_leaf': True
        }
    else:
        if green_ratio > 0.4:
            return {
                'success': True,
                'result': f'<strong>✅ Healthy Leaf Detected</strong><br>No visible disease symptoms.',
                'confidence': f'{min(95, int(green_ratio * 100))}% confidence',
                'tips': ['Continue regular monitoring', 'Maintain current practices', 'Follow balanced fertilizer schedule'],
                'is_leaf': True
            }
        else:
            return {
                'success': True,
                'result': f'<strong>⚠️ Minor Stress Detected</strong><br>Leaf shows minor discoloration.',
                'confidence': '65%',
                'tips': ['Monitor closely', 'Ensure proper irrigation', 'Apply preventive fungicide'],
                'is_leaf': True
            }

@app.route('/api/chat_history', methods=['GET'])
def chat_history_api():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chat_history ORDER BY created_at DESC LIMIT 50')
    history = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'status': 'success', 'history': history})

if __name__ == '__main__':
    print('=' * 60)
    print('FARMER AI ADVISORY SYSTEM')
    print('=' * 60)
    print('Initializing database...')
    init_database()
    print('Loading ML model...')
    if MODEL:
        print('ML Model loaded successfully')
    else:
        print('ML Model not found - Run ml/train_model.py first')
    print('=' * 60)
    print('Server running at: http://127.0.0.1:5000/')
    print('=' * 60)
    app.run(debug=True, port=5000, host='0.0.0.0')
