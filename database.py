"""
Farmer AI Advisory System - Database Schema
Creates SQLite database with all required tables
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'farmer_advisory.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.executescript('''
        -- Crops Table
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            soil_type TEXT,
            season TEXT,
            water_requirement TEXT,
            temp_range TEXT,
            yield_estimate TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Fertilizers Table
        CREATE TABLE IF NOT EXISTS fertilizers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_id INTEGER,
            npk_ratio TEXT,
            urea_kg_per_ha REAL,
            dap_kg_per_ha REAL,
            mop_kg_per_ha REAL,
            fym_tons_per_ha REAL,
            application_schedule TEXT,
            tips TEXT,
            FOREIGN KEY (crop_id) REFERENCES crops(id)
        );
        
        -- Pest Diseases Table
        CREATE TABLE IF NOT EXISTS pest_diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_id INTEGER,
            disease_name TEXT,
            symptoms TEXT,
            treatment TEXT,
            prevention TEXT,
            severity TEXT,
            FOREIGN KEY (crop_id) REFERENCES crops(id)
        );
        
        -- Irrigation Methods Table
        CREATE TABLE IF NOT EXISTS irrigation_methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method_name TEXT NOT NULL,
            efficiency TEXT,
            water_saving TEXT,
            cost_per_acre TEXT,
            subsidy TEXT,
            best_for TEXT,
            pros TEXT,
            cons TEXT
        );
        
        -- Market Prices Table
        CREATE TABLE IF NOT EXISTS market_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity TEXT NOT NULL,
            price REAL,
            unit TEXT,
            msp REAL,
            trend TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Weather Cache Table
        CREATE TABLE IF NOT EXISTS weather_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            temperature REAL,
            humidity REAL,
            condition TEXT,
            forecast TEXT,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Chat History Table
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            language TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- User Queries Table (for analytics)
        CREATE TABLE IF NOT EXISTS user_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT,
            query_type TEXT,
            language TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    cursor.executescript('''
        -- Insert Crops Data
        INSERT OR IGNORE INTO crops (name, soil_type, season, water_requirement, temp_range, yield_estimate) VALUES
        ('Rice', 'Alluvial/Clay', 'Kharif', 'High', '20-35°C', '4-6 tons/ha'),
        ('Wheat', 'Loamy', 'Rabi', 'Medium', '15-25°C', '3-5 tons/ha'),
        ('Cotton', 'Black', 'Kharif', 'Medium', '25-35°C', '2-3 tons/ha'),
        ('Maize', 'Loamy', 'Kharif', 'Medium', '20-30°C', '4-8 tons/ha'),
        ('Groundnut', 'Sandy Loam', 'Kharif', 'Low-Medium', '25-30°C', '2-3 tons/ha'),
        ('Sugarcane', 'Black/Alluvial', 'Annual', 'High', '20-35°C', '60-70 tons/ha'),
        ('Soybean', 'Black/Red', 'Kharif', 'Medium', '20-30°C', '2-3 tons/ha'),
        ('Tomato', 'Loamy', 'Rabi', 'Medium', '20-30°C', '30-40 tons/ha'),
        ('Potato', 'Sandy Loam', 'Rabi', 'Medium', '15-25°C', '20-30 tons/ha'),
        ('Onion', 'Loamy', 'Rabi', 'Low', '15-25°C', '20-30 tons/ha');
        
        -- Insert Fertilizers Data
        INSERT OR IGNORE INTO fertilizers (crop_id, npk_ratio, urea_kg_per_ha, dap_kg_per_ha, mop_kg_per_ha, fym_tons_per_ha, application_schedule, tips) VALUES
        (1, '100:60:40', 220, 130, 65, 10, 'Basal DAP+MOP, Urea at 21,45,65 days', 'Apply zinc sulfate 25kg/ha'),
        (2, '120:60:40', 260, 130, 65, 15, 'Basal, Urea at 21 & 45 days', 'Apply at CRI stage'),
        (3, '100:50:50', 220, 110, 85, 10, 'Basal, Urea at 30,45,60,90 days', 'Apply boron 0.2% foliar'),
        (4, '120:60:40', 260, 130, 65, 10, 'Basal, Urea at 21 & 45 days', 'Apply zinc sulfate'),
        (5, '20:40:40', 25, 87, 65, 5, 'Basal + Gypsum 400kg at 45 days', 'Gypsum increases yield by 20%'),
        (6, '250:60:120', 325, 130, 200, 25, 'Basal, Urea at 45,90,135 days', 'Trash mulching conserves moisture'),
        (7, '20:60:20', 50, 130, 33, 5, 'Basal, Urea at 30 days', 'Inoculate with rhizobium'),
        (8, '150:100:100', 200, 200, 165, 20, 'Weekly urea 1% foliar', 'Calcium prevents blossom end rot'),
        (9, '120:80:120', 180, 175, 200, 20, 'Basal, Urea at 30 days', 'Hilling up at earthing up'),
        (10, '80:40:60', 175, 85, 100, 15, 'Basal, Urea at 30 & 60 days', 'Nitrogen critical for bulb');
        
        -- Insert Pest Diseases Data
        INSERT OR IGNORE INTO pest_diseases (crop_id, disease_name, symptoms, treatment, prevention, severity) VALUES
        (1, 'Rice Blast', 'Diamond shaped lesions on leaves', 'Tricyclazole 0.6g/L', 'Use resistant varieties, avoid excess N', 'High'),
        (1, 'Bacterial Leaf Blight', 'Yellow to white lesions from leaf tip', 'Copper bactericides', 'Use certified seeds, avoid wet work', 'Medium'),
        (2, 'Wheat Rust', 'Orange/brown pustules on leaves', 'Propiconazole 1ml/L', 'Use resistant varieties', 'High'),
        (2, 'Powdery Mildew', 'White powdery coating on leaves', 'Sulfur fungicide', 'Improve air circulation', 'Medium'),
        (3, 'Pink Bollworm', 'Pink larvae in cotton bolls', 'Chlorpyrifos 2ml/L', 'Pheromone traps, early sowing', 'High'),
        (5, 'Tikka Disease', 'Brown spots on leaves', 'Chlorothalonil 2g/L', 'Use certified seeds', 'Medium'),
        (8, 'Late Blight', 'Water soaked lesions, white mold', 'Mancozeb 2.5g/L', 'Avoid overhead irrigation', 'High'),
        (9, 'Late Blight', 'Water soaked lesions', 'Metalaxyl 2g/L', 'Use healthy seed potatoes', 'High');
        
        -- Insert Irrigation Methods Data
        INSERT OR IGNORE INTO irrigation_methods (method_name, efficiency, water_saving, cost_per_acre, subsidy, best_for, pros, cons) VALUES
        ('Drip Irrigation', '90-95%', '40-60%', '₹30,000-60,000', '55% under PMKSY', 'Vegetables, Fruits, Cotton, Sugarcane', 'Maximum efficiency, Direct to root, Less weeds', 'High initial cost, Clogging issues'),
        ('Sprinkler Irrigation', '70-80%', '30-40%', '₹15,000-25,000', '50% under PMKSY', 'Wheat, Pulses, Potato, Uneven land', 'Works on uneven land, Portable', 'High evaporation, Wind affects'),
        ('Flood Irrigation', '30-50%', 'Least', '₹5,000-10,000', 'None', 'Rice, Sugarcane', 'Low cost, Simple', 'High waste, Uneven distribution'),
        ('Furrow Irrigation', '50-60%', 'Moderate', '₹8,000-15,000', 'None', 'Row crops - Tomato, Cotton, Maize', 'Better than flood, Easy', 'Still wasteful, Labor intensive');
        
        -- Insert Market Prices Data
        INSERT OR IGNORE INTO market_prices (commodity, price, unit, msp, trend) VALUES
        ('Rice (धान)', 2183, 'quintal', 2183, 'up'),
        ('Wheat (गेहूं)', 2325, 'quintal', 2275, 'down'),
        ('Cotton (कपास)', 6650, 'quintal', 6620, 'up'),
        ('Maize (मक्का)', 2050, 'quintal', 2225, 'up'),
        ('Soybean (सोयाबीन)', 4950, 'quintal', 4892, 'up'),
        ('Groundnut (मूंगफली)', 5350, 'quintal', 6783, 'down'),
        ('Sugarcane (गन्ना)', 350, 'quintal', 350, 'stable'),
        ('Mustard (सरसों)', 4800, 'quintal', 5950, 'up'),
        ('Onion (प्याज)', 2200, 'quintal', 0, 'up'),
        ('Potato (आलू)', 1250, 'quintal', 0, 'down');
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")

if __name__ == '__main__':
    init_db()
