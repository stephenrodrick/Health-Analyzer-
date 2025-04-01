import sqlite3
import datetime
import random

def create_database():
    """Create the SQLite database with tables for users, health data, medications, and conditions"""
    conn = sqlite3.connect('health_monitor.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        height REAL NOT NULL,
        weight REAL NOT NULL,
        blood_type TEXT,
        emergency_contact TEXT,
        doctor TEXT
    )
    ''')
    
    # Create health data table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS health_data (
        record_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        heart_rate INTEGER NOT NULL,
        blood_pressure_systolic INTEGER NOT NULL,
        blood_pressure_diastolic INTEGER NOT NULL,
        oxygen_level REAL NOT NULL,
        temperature REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    # Create medications table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medications (
        medication_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        dosage TEXT NOT NULL,
        frequency TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT,
        purpose TEXT,
        prescribing_doctor TEXT,
        side_effects TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    # Create medical conditions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medical_conditions (
        condition_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        diagnosis_date TEXT NOT NULL,
        severity TEXT,
        treatment_plan TEXT,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    # Insert sample users if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        insert_sample_data(conn)
    
    conn.commit()
    conn.close()

def insert_sample_data(conn):
    """Insert sample data into the database"""
    cursor = conn.cursor()
    
    # Sample users
    users = [
        (1, "John Smith", 45, "Male", 178, 82, "A+", "Sarah Smith: 555-1234", "Dr. Wilson"),
        (2, "Emily Johnson", 32, "Female", 165, 58, "O-", "Michael Johnson: 555-2345", "Dr. Martinez"),
        (3, "Michael Brown", 67, "Male", 175, 88, "B+", "Linda Brown: 555-3456", "Dr. Anderson"),
        (4, "Sarah Davis", 28, "Female", 162, 55, "AB+", "Robert Davis: 555-4567", "Dr. Taylor"),
        (5, "Robert Wilson", 52, "Male", 180, 95, "A-", "Jennifer Wilson: 555-5678", "Dr. Thomas"),
        (6, "Jennifer Martinez", 41, "Female", 168, 63, "O+", "David Martinez: 555-6789", "Dr. Harris"),
        (7, "David Anderson", 73, "Male", 172, 78, "B-", "Susan Anderson: 555-7890", "Dr. Wilson"),
        (8, "Susan Taylor", 35, "Female", 170, 67, "A+", "James Taylor: 555-8901", "Dr. Martinez"),
        (9, "James Thomas", 58, "Male", 182, 90, "O+", "Patricia Thomas: 555-9012", "Dr. Anderson"),
        (10, "Patricia Harris", 49, "Female", 163, 61, "AB-", "John Harris: 555-0123", "Dr. Taylor"),
        (11, "Christopher Lee", 62, "Male", 177, 85, "A+", "Mary Lee: 555-1234", "Dr. Wilson"),
        (12, "Mary Clark", 39, "Female", 166, 59, "B+", "Daniel Clark: 555-2345", "Dr. Martinez"),
        (13, "Daniel Lewis", 55, "Male", 179, 92, "O-", "Elizabeth Lewis: 555-3456", "Dr. Anderson"),
        (14, "Elizabeth Walker", 31, "Female", 164, 56, "A-", "Richard Walker: 555-4567", "Dr. Taylor"),
        (15, "Richard Hall", 70, "Male", 174, 80, "AB+", "Barbara Hall: 555-5678", "Dr. Harris")
    ]
    
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", users)
    
    # Generate sample health data for each user
    now = datetime.datetime.now()
    health_data = []
    record_id = 1
    
    # Medical conditions with their typical vital sign patterns
    conditions = {
        "Hypertension": {"hr": (70, 90), "bp_sys": (140, 180), "bp_dia": (90, 110), "o2": (94, 99), "temp": (36.5, 37.2)},
        "Hypotension": {"hr": (55, 75), "bp_sys": (85, 110), "bp_dia": (50, 70), "o2": (94, 99), "temp": (36.5, 37.2)},
        "Tachycardia": {"hr": (100, 130), "bp_sys": (110, 140), "bp_dia": (70, 90), "o2": (94, 99), "temp": (36.5, 37.2)},
        "Bradycardia": {"hr": (40, 55), "bp_sys": (110, 140), "bp_dia": (70, 90), "o2": (94, 99), "temp": (36.5, 37.2)},
        "Fever": {"hr": (75, 100), "bp_sys": (110, 140), "bp_dia": (70, 90), "o2": (94, 99), "temp": (38.0, 39.5)},
        "Hypothermia": {"hr": (50, 70), "bp_sys": (100, 130), "bp_dia": (60, 80), "o2": (94, 99), "temp": (35.0, 36.0)},
        "Hypoxemia": {"hr": (85, 110), "bp_sys": (110, 140), "bp_dia": (70, 90), "o2": (85, 92), "temp": (36.5, 37.2)},
        "Diabetes": {"hr": (70, 90), "bp_sys": (120, 150), "bp_dia": (80, 95), "o2": (94, 99), "temp": (36.5, 37.2)},
        "Asthma": {"hr": (75, 95), "bp_sys": (110, 140), "bp_dia": (70, 90), "o2": (90, 96), "temp": (36.5, 37.2)},
        "COPD": {"hr": (80, 100), "bp_sys": (120, 150), "bp_dia": (80, 95), "o2": (88, 94), "temp": (36.5, 37.2)},
        "Healthy": {"hr": (60, 80), "bp_sys": (110, 130), "bp_dia": (70, 85), "o2": (96, 100), "temp": (36.5, 37.2)}
    }
    
    # Assign conditions to users
    user_conditions = {
        1: ["Hypertension", "Diabetes"],
        2: ["Healthy"],
        3: ["COPD", "Hypertension"],
        4: ["Asthma"],
        5: ["Hypertension", "Tachycardia"],
        6: ["Healthy"],
        7: ["Bradycardia", "Hypotension"],
        8: ["Healthy"],
        9: ["Diabetes", "Hypertension"],
        10: ["Asthma"],
        11: ["COPD"],
        12: ["Healthy"],
        13: ["Hypertension"],
        14: ["Hypoxemia"],
        15: ["Bradycardia"]
    }
    
    # Generate health data for the past 30 days for each user
    for user_id in range(1, 16):
        user_condition = user_conditions[user_id]
        
        # Generate multiple readings per day for the past 30 days
        for day in range(30, -1, -1):
            # Generate 1-3 readings per day
            for reading in range(random.randint(1, 3)):
                timestamp = now - datetime.timedelta(days=day, hours=random.randint(0, 23), minutes=random.randint(0, 59))
                
                # Select a random condition from the user's conditions for this reading
                if user_condition[0] == "Healthy":
                    condition = "Healthy"
                else:
                    condition = random.choice(user_condition)
                
                # Get vital sign ranges for this condition
                ranges = conditions[condition]
                
                # Generate vital signs within the condition's typical ranges
                heart_rate = random.randint(ranges["hr"][0], ranges["hr"][1])
                bp_sys = random.randint(ranges["bp_sys"][0], ranges["bp_sys"][1])
                bp_dia = random.randint(ranges["bp_dia"][0], ranges["bp_dia"][1])
                oxygen = round(random.uniform(ranges["o2"][0], ranges["o2"][1]), 1)
                temp = round(random.uniform(ranges["temp"][0], ranges["temp"][1]), 1)
                
                # Add some random variation
                heart_rate += random.randint(-5, 5)
                bp_sys += random.randint(-5, 5)
                bp_dia += random.randint(-3, 3)
                oxygen += round(random.uniform(-0.5, 0.5), 1)
                temp += round(random.uniform(-0.2, 0.2), 1)
                
                # Ensure values are within reasonable ranges
                heart_rate = max(40, min(heart_rate, 180))
                bp_sys = max(80, min(bp_sys, 200))
                bp_dia = max(40, min(bp_dia, 120))
                oxygen = max(80, min(oxygen, 100))
                temp = max(34.5, min(temp, 41.0))
                
                health_data.append((
                    record_id,
                    user_id,
                    timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    heart_rate,
                    bp_sys,
                    bp_dia,
                    oxygen,
                    temp
                ))
                record_id += 1
    
    cursor.executemany("INSERT INTO health_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)", health_data)
    
    # Sample medications
    medications = [
        (1, 1, "Lisinopril", "10mg", "Once daily", "2023-01-15", None, "Hypertension", "Dr. Wilson", "Dry cough, dizziness"),
        (2, 1, "Metformin", "500mg", "Twice daily", "2023-02-10", None, "Diabetes", "Dr. Wilson", "Nausea, diarrhea"),
        (3, 3, "Albuterol", "90mcg", "As needed", "2023-01-05", None, "COPD", "Dr. Anderson", "Tremors, nervousness"),
        (4, 3, "Amlodipine", "5mg", "Once daily", "2023-03-20", None, "Hypertension", "Dr. Anderson", "Swelling, headache"),
        (5, 4, "Fluticasone", "110mcg", "Twice daily", "2023-02-15", None, "Asthma", "Dr. Taylor", "Throat irritation"),
        (6, 5, "Losartan", "50mg", "Once daily", "2023-01-10", None, "Hypertension", "Dr. Thomas", "Dizziness, fatigue"),
        (7, 5, "Metoprolol", "25mg", "Twice daily", "2023-03-05", None, "Tachycardia", "Dr. Thomas", "Fatigue, dizziness"),
        (8, 7, "Fludrocortisone", "0.1mg", "Once daily", "2023-02-20", None, "Hypotension", "Dr. Wilson", "Headache, swelling"),
        (9, 9, "Glipizide", "5mg", "Once daily", "2023-01-25", None, "Diabetes", "Dr. Anderson", "Hypoglycemia"),
        (10, 9, "Hydrochlorothiazide", "12.5mg", "Once daily", "2023-03-10", None, "Hypertension", "Dr. Anderson", "Dehydration"),
        (11, 10, "Montelukast", "10mg", "Once daily", "2023-02-05", None, "Asthma", "Dr. Taylor", "Headache, fatigue"),
        (12, 11, "Tiotropium", "18mcg", "Once daily", "2023-01-20", None, "COPD", "Dr. Wilson", "Dry mouth, constipation"),
        (13, 13, "Valsartan", "80mg", "Once daily", "2023-03-15", None, "Hypertension", "Dr. Anderson", "Dizziness, headache"),
        (14, 14, "Supplemental Oxygen", "2L/min", "As needed", "2023-02-25", None, "Hypoxemia", "Dr. Taylor", "Nasal dryness"),
        (15, 15, "Atropine", "0.5mg", "As needed", "2023-01-30", None, "Bradycardia", "Dr. Harris", "Dry mouth, blurred vision")
    ]
    
    cursor.executemany("INSERT INTO medications VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", medications)
    
    # Sample medical conditions
    medical_conditions = [
        (1, 1, "Hypertension", "2022-05-10", "Moderate", "Medication and lifestyle changes", "Controlled with medication"),
        (2, 1, "Type 2 Diabetes", "2022-06-15", "Mild", "Medication and diet control", "Good glucose control"),
        (3, 3, "COPD", "2015-03-20", "Severe", "Bronchodilators and oxygen therapy", "Progressive condition"),
        (4, 3, "Hypertension", "2018-07-05", "Moderate", "Medication", "Well controlled"),
        (5, 4, "Asthma", "2010-09-12", "Mild", "Inhalers and avoiding triggers", "Occasional exacerbations"),
        (6, 5, "Hypertension", "2019-11-30", "Moderate", "Medication and diet", "Fluctuating control"),
        (7, 5, "Atrial Fibrillation", "2020-02-25", "Moderate", "Rate control medication", "Occasional tachycardia"),
        (8, 7, "Orthostatic Hypotension", "2021-04-18", "Mild", "Medication and lifestyle adjustments", "Symptoms when standing"),
        (9, 7, "Sinus Bradycardia", "2021-05-22", "Mild", "Monitoring", "Asymptomatic"),
        (10, 9, "Type 2 Diabetes", "2017-08-14", "Moderate", "Medication and diet", "Fair control"),
        (11, 9, "Hypertension", "2016-10-05", "Moderate", "Medication", "Well controlled"),
        (12, 10, "Asthma", "2005-12-20", "Moderate", "Inhalers and allergy management", "Seasonal exacerbations"),
        (13, 11, "COPD", "2012-01-15", "Moderate", "Bronchodilators", "Stable condition"),
        (14, 13, "Hypertension", "2020-03-10", "Mild", "Medication and exercise", "Well controlled"),
        (15, 14, "Sleep Apnea", "2021-06-25", "Moderate", "CPAP therapy", "Causes occasional hypoxemia"),
        (16, 15, "Sick Sinus Syndrome", "2019-09-08", "Moderate", "Medication", "Bradycardia episodes")
    ]
    
    cursor.executemany("INSERT INTO medical_conditions VALUES (?, ?, ?, ?, ?, ?, ?)", medical_conditions)
    
    conn.commit()
    cursor.close()
    print("Sample data inserted successfully.")
                