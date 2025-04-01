import sqlite3
import datetime
import random

class DatabaseManager:
    """Class to manage database operations for the health monitoring system"""
    
    def __init__(self, db_path='health_monitor.db'):
        """Initialize the database manager"""
        self.db_path = db_path
        self.create_database()
        
        # Test connection
        self._execute_query("SELECT 1")
    
    def create_database(self):
        """Create database with tables and sample data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create users table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    height REAL,
                    weight REAL
                )''')
                
                # Create health_data table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_data (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    heart_rate INTEGER,
                    blood_pressure_sys INTEGER,
                    blood_pressure_dia INTEGER,
                    oxygen_level REAL,
                    temperature REAL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )''')

                # Check if users table is empty
                cursor.execute("SELECT COUNT(*) FROM users")
                if cursor.fetchone()[0] == 0:
                    # Insert sample users with complete information
                    sample_users = [
                        ('John Smith', 65, 'Male', 175.0, 82.0),
                        ('Sarah Johnson', 42, 'Female', 165.0, 58.0),
                        ('Michael Brown', 55, 'Male', 180.0, 95.0),
                        ('Emma Davis', 28, 'Female', 160.0, 55.0),
                        ('Robert Wilson', 72, 'Male', 172.0, 78.0),
                        ('Lisa Anderson', 41, 'Female', 168.0, 63.0),
                        ('David Martinez', 58, 'Male', 178.0, 88.0),
                        ('Jennifer Taylor', 35, 'Female', 163.0, 57.0),
                        ('William Lee', 50, 'Male', 170.0, 72.0),
                        ('Maria Garcia', 44, 'Female', 165.0, 61.0),
                        ('James Thompson', 68, 'Male', 176.0, 82.0),
                        ('Susan White', 47, 'Female', 167.0, 65.0),
                        ('Thomas Moore', 53, 'Male', 182.0, 88.0),
                        ('Patricia Clark', 39, 'Female', 164.0, 59.0),
                        ('Richard Harris', 60, 'Male', 173.0, 76.0)
                    ]
                    
                    cursor.executemany('''
                    INSERT INTO users (name, age, gender, height, weight)
                    VALUES (?, ?, ?, ?, ?)
                    ''', sample_users)
                    
                    # Generate sample health data for each user
                    for user_id in range(1, 16):
                        # Generate 30 days of data
                        for day in range(30):
                            # Generate 4 readings per day
                            for hour in [6, 12, 18, 23]:
                                timestamp = datetime.datetime.now() - datetime.timedelta(days=day, hours=24-hour)
                                
                                # Generate appropriate health metrics based on user conditions
                                heart_rate = 75 + random.randint(-10, 10)
                                blood_pressure_sys = 120 + random.randint(-10, 10)
                                blood_pressure_dia = 80 + random.randint(-5, 5)
                                oxygen_level = 98 + random.random() * 2 - 1  # 97-99%
                                temperature = 36.6 + random.random() * 0.8 - 0.4  # 36.2-37.0
                                
                                cursor.execute('''
                                INSERT INTO health_data 
                                (user_id, timestamp, heart_rate, blood_pressure_sys, 
                                blood_pressure_dia, oxygen_level, temperature)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                ''', (user_id, timestamp, heart_rate, blood_pressure_sys, 
                                     blood_pressure_dia, oxygen_level, temperature))
                    
                    conn.commit()
                
        except sqlite3.Error as e:
            print(f"Database creation error: {e}")
            raise

    def _execute_query(self, query, params=None, fetch=True):
        """Execute a query and optionally return results"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = None
        except sqlite3.Error as e:
            conn.close()
            raise e
        
        conn.close()
        return result
    
    def get_user_names(self):
        """Get a list of all user IDs and names"""
        query = "SELECT user_id, name FROM users ORDER BY name"
        result = self._execute_query(query)
        return [(row['user_id'], row['name']) for row in result]
    
    def get_user_info(self, user_id):
        """Get detailed information about a user"""
        query = "SELECT * FROM users WHERE user_id = ?"
        result = self._execute_query(query, (user_id,))
        
        if result:
            row = result[0]
            return (
                row['user_id'],
                row['name'],
                row['age'],
                row['gender'],
                row['height'],
                row['weight'],
                row['blood_type'],
                row['emergency_contact'],
                row['doctor']
            )
        return None
    
    def get_latest_health_data(self, user_id):
        """Get the latest health data for a user"""
        query = """
        SELECT * FROM health_data 
        WHERE user_id = ? 
        ORDER BY timestamp DESC 
        LIMIT 1
        """
        result = self._execute_query(query, (user_id,))
        
        if result:
            row = result[0]
            return (
                row['record_id'],
                row['user_id'],
                row['timestamp'],
                row['heart_rate'],
                row['blood_pressure_systolic'],
                row['blood_pressure_diastolic'],
                row['oxygen_level'],
                row['temperature']
            )
        return None
    
    def get_health_data_by_timeframe(self, user_id, days):
        """Get health data for a user within the specified number of days"""
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        SELECT * FROM health_data 
        WHERE user_id = ? AND timestamp >= ? 
        ORDER BY timestamp
        """
        result = self._execute_query(query, (user_id, cutoff_date))
        
        return [
            (
                row['record_id'],
                row['user_id'],
                row['timestamp'],
                row['heart_rate'],
                row['blood_pressure_systolic'],
                row['blood_pressure_diastolic'],
                row['oxygen_level'],
                row['temperature']
            )
            for row in result
        ]
    
    def get_health_data_by_date_range(self, user_id, start_date, end_date):
        """Get health data for a user within a specific date range"""
        query = """
        SELECT * FROM health_data 
        WHERE user_id = ? AND timestamp >= ? AND timestamp <= ? 
        ORDER BY timestamp
        """
        result = self._execute_query(query, (user_id, start_date, end_date))
        
        return [
            (
                row['record_id'],
                row['user_id'],
                row['timestamp'],
                row['heart_rate'],
                row['blood_pressure_systolic'],
                row['blood_pressure_diastolic'],
                row['oxygen_level'],
                row['temperature']
            )
            for row in result
        ]
    
    def get_user_medications(self, user_id):
        """Get all medications for a user"""
        query = """
        SELECT * FROM medications 
        WHERE user_id = ? 
        ORDER BY name
        """
        result = self._execute_query(query, (user_id,))
        
        return [
            {
                'medication_id': row['medication_id'],
                'name': row['name'],
                'dosage': row['dosage'],
                'frequency': row['frequency'],
                'start_date': row['start_date'],
                'end_date': row['end_date'],
                'purpose': row['purpose'],
                'prescribing_doctor': row['prescribing_doctor'],
                'side_effects': row['side_effects']
            }
            for row in result
        ]
    
    def get_user_medical_conditions(self, user_id):
        """Get all medical conditions for a user"""
        query = """
        SELECT * FROM medical_conditions 
        WHERE user_id = ? 
        ORDER BY diagnosis_date DESC
        """
        result = self._execute_query(query, (user_id,))
        
        return [
            {
                'condition_id': row['condition_id'],
                'name': row['name'],
                'diagnosis_date': row['diagnosis_date'],
                'severity': row['severity'],
                'treatment_plan': row['treatment_plan'],
                'notes': row['notes']
            }
            for row in result
        ]
    
    def add_health_data(self, user_id, heart_rate, bp_sys, bp_dia, oxygen, temp):
        """Add new health data for a user"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        INSERT INTO health_data 
        (user_id, timestamp, heart_rate, blood_pressure_systolic, blood_pressure_diastolic, oxygen_level, temperature) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self._execute_query(query, (user_id, timestamp, heart_rate, bp_sys, bp_dia, oxygen, temp), fetch=False)
    
    def add_medication(self, user_id, name, dosage, frequency, start_date, end_date, purpose, doctor, side_effects):
        """Add a new medication for a user"""
        query = """
        INSERT INTO medications 
        (user_id, name, dosage, frequency, start_date, end_date, purpose, prescribing_doctor, side_effects) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self._execute_query(query, (user_id, name, dosage, frequency, start_date, end_date, purpose, doctor, side_effects), fetch=False)
    
    def add_medical_condition(self, user_id, name, diagnosis_date, severity, treatment_plan, notes):
        """Add a new medical condition for a user"""
        query = """
        INSERT INTO medical_conditions 
        (user_id, name, diagnosis_date, severity, treatment_plan, notes) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self._execute_query(query, (user_id, name, diagnosis_date, severity, treatment_plan, notes), fetch=False)
    
    def get_health_stats(self, user_id, days=30):
        """Get health statistics for a user over a period"""
        health_data = self.get_health_data_by_timeframe(user_id, days)
        
        if not health_data:
            return None
        
        # Calculate statistics
        heart_rates = [record[3] for record in health_data]
        bp_systolic = [record[4] for record in health_data]
        bp_diastolic = [record[5] for record in health_data]
        oxygen_levels = [record[6] for record in health_data]
        temperatures = [record[7] for record in health_data]
        
        stats = {
            'heart_rate': {
                'min': min(heart_rates),
                'max': max(heart_rates),
                'avg': sum(heart_rates) / len(heart_rates)
            },
            'blood_pressure': {
                'systolic_min': min(bp_systolic),
                'systolic_max': max(bp_systolic),
                'systolic_avg': sum(bp_systolic) / len(bp_systolic),
                'diastolic_min': min(bp_diastolic),
                'diastolic_max': max(bp_diastolic),
                'diastolic_avg': sum(bp_diastolic) / len(bp_diastolic)
            },
            'oxygen_level': {
                'min': min(oxygen_levels),
                'max': max(oxygen_levels),
                'avg': sum(oxygen_levels) / len(oxygen_levels)
            },
            'temperature': {
                'min': min(temperatures),
                'max': max(temperatures),
                'avg': sum(temperatures) / len(temperatures)
            },
            'readings_count': len(health_data)
        }
        
        return stats
    
    def get_medication_compliance(self, user_id, days=30):
        """
        Calculate medication compliance based on health readings
        This is a simplified example - in a real system, you would track actual medication intake
        """
        # Get medications
        medications = self.get_user_medications(user_id)
        
        # Get health data
        health_data = self.get_health_data_by_timeframe(user_id, days)
        
        if not medications or not health_data:
            return []
        
        # For this example, we'll simulate compliance based on health metrics
        # In a real system, you would have actual medication intake tracking
        compliance_results = []
        
        for med in medications:
            # Determine which health metric this medication affects
            target_metric = None
            expected_effect = None
            
            if "hypertension" in med['purpose'].lower():
                target_metric = "blood_pressure"
                expected_effect = "lower"
            elif "hypotension" in med['purpose'].lower():
                target_metric = "blood_pressure"
                expected_effect = "raise"
            elif "tachycardia" in med['purpose'].lower():
                target_metric = "heart_rate"
                expected_effect = "lower"
            elif "bradycardia" in med['purpose'].lower():
                target_metric = "heart_rate"
                expected_effect = "raise"
            elif "diabetes" in med['purpose'].lower():
                target_metric = "other"  # Would be blood glucose in a real system
                expected_effect = "stabilize"
            elif "asthma" in med['purpose'].lower() or "copd" in med['purpose'].lower():
                target_metric = "oxygen_level"
                expected_effect = "raise"
            
            # Calculate a simulated compliance score (0-100%)
            if target_metric:
                if target_metric == "blood_pressure":
                    # Check if blood pressure is in target range
                    systolic_values = [record[4] for record in health_data]
                    diastolic_values = [record[5] for record in health_data]
                    
                    if expected_effect == "lower":
                        # For hypertension meds, lower is better
                        systolic_in_range = sum(1 for v in systolic_values if v < 140) / len(systolic_values)
                        diastolic_in_range = sum(1 for v in diastolic_values if v < 90) / len(diastolic_values)
                        compliance = (systolic_in_range + diastolic_in_range) / 2 * 100
                    else:
                        # For hypotension meds, higher is better
                        systolic_in_range = sum(1 for v in systolic_values if v > 100) / len(systolic_values)
                        diastolic_in_range = sum(1 for v in diastolic_values if v > 60) / len(diastolic_values)
                        compliance = (systolic_in_range + diastolic_in_range) / 2 * 100
                
                elif target_metric == "heart_rate":
                    heart_rates = [record[3] for record in health_data]
                    
                    if expected_effect == "lower":
                        # For tachycardia meds, lower is better
                        in_range = sum(1 for v in heart_rates if v < 100) / len(heart_rates)
                    else:
                        # For bradycardia meds, higher is better
                        in_range = sum(1 for v in heart_rates if v > 60) / len(heart_rates)
                    
                    compliance = in_range * 100
                
                elif target_metric == "oxygen_level":
                    oxygen_levels = [record[6] for record in health_data]
                    in_range = sum(1 for v in oxygen_levels if v >= 95) / len(oxygen_levels)
                    in_range = sum(1 for v in oxygen_levels if v >= 95) / len(oxygen_levels)
                    compliance = in_range * 100
                
                else:
                    # Default compliance estimate
                    compliance = 80.0  # Arbitrary default
            else:
                compliance = 80.0  # Arbitrary default for medications without clear metrics
            
            # Add to results
            compliance_results.append({
                'medication_name': med['name'],
                'purpose': med['purpose'],
                'compliance_score': round(compliance, 1),
                'dosage': med['dosage'],
                'frequency': med['frequency']
            })
        
        return compliance_results

    def get_condition_progression(self, user_id, condition_name, days=90):
        """
        Analyze the progression of a specific condition based on relevant health metrics
        """
        # Get health data for the specified period
        health_data = self.get_health_data_by_timeframe(user_id, days)
        
        if not health_data:
            return None
        
        # Determine which metrics to track based on the condition
        metrics = []
        if "hypertension" in condition_name.lower():
            metrics = ["blood_pressure_systolic", "blood_pressure_diastolic"]
        elif "tachycardia" in condition_name.lower():
            metrics = ["heart_rate"]
        elif "bradycardia" in condition_name.lower():
            metrics = ["heart_rate"]
        elif "hypoxemia" in condition_name.lower() or "copd" in condition_name.lower() or "asthma" in condition_name.lower():
            metrics = ["oxygen_level"]
        elif "fever" in condition_name.lower():
            metrics = ["temperature"]
        else:
            # Default to tracking all metrics
            metrics = ["heart_rate", "blood_pressure_systolic", "blood_pressure_diastolic", "oxygen_level", "temperature"]
        
        # Group data by week for trend analysis
        weeks = {}
        start_date = datetime.datetime.strptime(health_data[0][2], '%Y-%m-%d %H:%M:%S')
        
        for record in health_data:
            record_date = datetime.datetime.strptime(record[2], '%Y-%m-%d %H:%M:%S')
            week_num = (record_date - start_date).days // 7
            
            if week_num not in weeks:
                weeks[week_num] = {
                    'heart_rate': [],
                    'blood_pressure_systolic': [],
                    'blood_pressure_diastolic': [],
                    'oxygen_level': [],
                    'temperature': []
                }
            
            weeks[week_num]['heart_rate'].append(record[3])
            weeks[week_num]['blood_pressure_systolic'].append(record[4])
            weeks[week_num]['blood_pressure_diastolic'].append(record[5])
            weeks[week_num]['oxygen_level'].append(record[6])
            weeks[week_num]['temperature'].append(record[7])
        
        # Calculate weekly averages
        progression = []
        for week_num in sorted(weeks.keys()):
            week_data = {
                'week': week_num + 1,
                'date_range': (start_date + datetime.timedelta(days=week_num*7)).strftime('%Y-%m-%d')
            }
            
            for metric in metrics:
                if weeks[week_num][metric]:
                    week_data[metric] = sum(weeks[week_num][metric]) / len(weeks[week_num][metric])
                else:
                    week_data[metric] = None
            
            progression.append(week_data)
        
        return {
            'condition': condition_name,
            'metrics_tracked': metrics,
            'progression': progression
        }

# Update the health analyzer to include medication and condition analysis

# File: health_analyzer.py
class HealthAnalyzer:
    def __init__(self):
        # Define health thresholds
        self.thresholds = {
            'heart_rate': {
                'low': 60,
                'high': 100,
                'very_high': 120
            },
            'blood_pressure': {
                'normal_systolic': 120,
                'elevated_systolic': 130,
                'high_systolic_1': 140,
                'high_systolic_2': 180,
                'normal_diastolic': 80,
                'high_diastolic_1': 90,
                'high_diastolic_2': 120
            },
            'oxygen_level': {
                'normal': 95,
                'concerning': 92,
                'low': 90
            },
            'temperature': {
                'low': 36.1,
                'normal_low': 36.5,
                'normal_high': 37.5,
                'elevated': 38.0,
                'high': 39.0
            }
        }
        
        # Define condition-specific thresholds and recommendations
        self.condition_guidelines = {
            'Hypertension': {
                'blood_pressure': {
                    'target_systolic': 130,
                    'target_diastolic': 80
                },
                'recommendations': [
                    "Monitor blood pressure regularly",
                    "Take medications as prescribed",
                    "Reduce sodium intake",
                    "Regular physical activity",
                    "Maintain healthy weight",
                    "Limit alcohol consumption"
                ]
            },
            'Diabetes': {
                'recommendations': [
                    "Monitor blood glucose regularly",
                    "Take medications as prescribed",
                    "Follow a balanced diet",
                    "Regular physical activity",
                    "Monitor for signs of hypoglycemia",
                    "Regular foot examinations"
                ]
            },
            'COPD': {
                'oxygen_level': {
                    'target_minimum': 88
                },
                'recommendations': [
                    "Use prescribed inhalers correctly",
                    "Avoid smoke and air pollutants",
                    "Pulmonary rehabilitation exercises",
                    "Get vaccinated against flu and pneumonia",
                    "Oxygen therapy as prescribed",
                    "Report increased shortness of breath"
                ]
            },
            'Asthma': {
                'oxygen_level': {
                    'target_minimum': 92
                },
                'recommendations': [
                    "Use controller medications daily",
                    "Have rescue inhaler available",
                    "Identify and avoid triggers",
                    "Follow asthma action plan",
                    "Regular check-ups with healthcare provider"
                ]
            },
            'Atrial Fibrillation': {
                'heart_rate': {
                    'target_range': (60, 100)
                },
                'recommendations': [
                    "Take anticoagulants as prescribed",
                    "Take rate control medications",
                    "Monitor pulse regularly",
                    "Report palpitations or dizziness",
                    "Regular check-ups with cardiologist"
                ]
            }
        }
    
    def analyze_heart_rate(self, heart_rate):
        """Analyze heart rate and return status and message"""
        if heart_rate < self.thresholds['heart_rate']['low']:
            return "Warning", f"Heart rate is low ({heart_rate} BPM)"
        elif heart_rate > self.thresholds['heart_rate']['very_high']:
            return "Danger", f"Heart rate is very high ({heart_rate} BPM)"
        elif heart_rate > self.thresholds['heart_rate']['high']:
            return "Warning", f"Heart rate is elevated ({heart_rate} BPM)"
        else:
            return "Normal", f"Heart rate is normal ({heart_rate} BPM)"
    
    def analyze_blood_pressure(self, systolic, diastolic):
        """Analyze blood pressure and return status and message"""
        # Check systolic pressure
        if systolic >= self.thresholds['blood_pressure']['high_systolic_2']:
            sys_status = "Danger"
            sys_msg = f"Systolic pressure is very high ({systolic} mmHg)"
        elif systolic >= self.thresholds['blood_pressure']['high_systolic_1']:
            sys_status = "Warning"
            sys_msg = f"Systolic pressure is high ({systolic} mmHg)"
        elif systolic >= self.thresholds['blood_pressure']['elevated_systolic']:
            sys_status = "Caution"
            sys_msg = f"Systolic pressure is elevated ({systolic} mmHg)"
        else:
            sys_status = "Normal"
            sys_msg = f"Systolic pressure is normal ({systolic} mmHg)"
        
        # Check diastolic pressure
        if diastolic >= self.thresholds['blood_pressure']['high_diastolic_2']:
            dia_status = "Danger"
            dia_msg = f"Diastolic pressure is very high ({diastolic} mmHg)"
        elif diastolic >= self.thresholds['blood_pressure']['high_diastolic_1']:
            dia_status = "Warning"
            dia_msg = f"Diastolic pressure is high ({diastolic} mmHg)"
        else:
            dia_status = "Normal"
            dia_msg = f"Diastolic pressure is normal ({diastolic} mmHg)"
        
        # Determine overall status (take the worse of the two)
        if "Danger" in [sys_status, dia_status]:
            overall_status = "Danger"
        elif "Warning" in [sys_status, dia_status]:
            overall_status = "Warning"
        elif "Caution" in [sys_status, dia_status]:
            overall_status = "Caution"
        else:
            overall_status = "Normal"
        
        overall_msg = f"BP: {systolic}/{diastolic} mmHg"
        
        return overall_status, overall_msg, sys_msg, dia_msg
    
    def analyze_oxygen_level(self, oxygen):
        """Analyze oxygen saturation level and return status and message"""
        if oxygen < self.thresholds['oxygen_level']['low']:
            return "Danger", f"Oxygen level is critically low ({oxygen}%)"
        elif oxygen < self.thresholds['oxygen_level']['concerning']:
            return "Warning", f"Oxygen level is concerning ({oxygen}%)"
        elif oxygen < self.thresholds['oxygen_level']['normal']:
            return "Caution", f"Oxygen level is slightly below normal ({oxygen}%)"
        else:
            return "Normal", f"Oxygen level is normal ({oxygen}%)"
    
    def analyze_temperature(self, temp):
        """Analyze body temperature and return status and message"""
        if temp > self.thresholds['temperature']['high']:
            return "Danger", f"High fever detected ({temp}°C)"
        elif temp > self.thresholds['temperature']['elevated']:
            return "Warning", f"Elevated temperature ({temp}°C)"
        elif temp > self.thresholds['temperature']['normal_high']:
            return "Caution", f"Slightly elevated temperature ({temp}°C)"
        elif temp < self.thresholds['temperature']['low']:
            return "Warning", f"Temperature is below normal ({temp}°C)"
        else:
            return "Normal", f"Temperature is normal ({temp}°C)"
    
    def get_overall_health_status(self, health_data):
        """
        Analyze all health metrics and provide an overall assessment
        health_data should be a tuple with (record_id, user_id, timestamp, heart_rate, 
        blood_pressure_systolic, blood_pressure_diastolic, oxygen_level, temperature)
        """
        if not health_data:
            return "Unknown", "No health data available"
        
        record_id, user_id, timestamp, heart_rate, bp_sys, bp_dia, oxygen, temp = health_data
        
        # Analyze individual metrics
        hr_status, hr_msg = self.analyze_heart_rate(heart_rate)
        bp_status, bp_msg, sys_msg, dia_msg = self.analyze_blood_pressure(bp_sys, bp_dia)
        ox_status, ox_msg = self.analyze_oxygen_level(oxygen)
        temp_status, temp_msg = self.analyze_temperature(temp)
        
        # Collect all warnings and alerts
        warnings = []
        if hr_status != "Normal":
            warnings.append(hr_msg)
        if bp_status != "Normal":
            warnings.append(bp_msg)
        if ox_status != "Normal":
            warnings.append(ox_msg)
        if temp_status != "Normal":
            warnings.append(temp_msg)
        
        # Determine overall status (take the worst status)
        statuses = [hr_status, bp_status, ox_status, temp_status]
        if "Danger" in statuses:
            overall_status = "Danger"
        elif "Warning" in statuses:
            overall_status = "Warning"
        elif "Caution" in statuses:
            overall_status = "Caution"
        else:
            overall_status = "Normal"
        
        # Create overall message
        if warnings:
            overall_msg = "Health concerns: " + "; ".join(warnings)
        else:
            overall_msg = "All health metrics are within normal ranges"
        
        return overall_status, overall_msg
    
    def predict_potential_conditions(self, health_data_history):
        """
        Analyze historical health data to predict potential health conditions
        health_data_history should be a list of health data records
        """
        if not health_data_history:
            return []
        
        # Count how many readings fall into concerning ranges
        high_bp_count = 0
        high_hr_count = 0
        low_hr_count = 0
        low_ox_count = 0
        high_temp_count = 0
        
        total_readings = len(health_data_history)
        
        for record in health_data_history:
            _, _, _, heart_rate, bp_sys, bp_dia, oxygen, temp = record
            
            # Check blood pressure
            if bp_sys >= self.thresholds['blood_pressure']['high_systolic_1'] or \
               bp_dia >= self.thresholds['blood_pressure']['high_diastolic_1']:
                high_bp_count += 1
            
            # Check heart rate
            if heart_rate > self.thresholds['heart_rate']['high']:
                high_hr_count += 1
            elif heart_rate < self.thresholds['heart_rate']['low']:
                low_hr_count += 1
            
            # Check oxygen level
            if oxygen < self.thresholds['oxygen_level']['concerning']:
                low_ox_count += 1
            
            # Check temperature
            if temp > self.thresholds['temperature']['elevated']:
                high_temp_count += 1
        
        # Calculate percentages
        high_bp_percent = (high_bp_count / total_readings) * 100
        high_hr_percent = (high_hr_count / total_readings) * 100
        low_hr_percent = (low_hr_count / total_readings) * 100
        low_ox_percent = (low_ox_count / total_readings) * 100
        high_temp_percent = (high_temp_count / total_readings) * 100
        
        # Identify potential conditions based on patterns
        potential_conditions = []
        
        if high_bp_percent >= 50:
            potential_conditions.append({
                "condition": "Hypertension Risk",
                "confidence": f"{high_bp_percent:.1f}%",
                "description": "Consistently elevated blood pressure readings suggest hypertension risk. Hypertension can lead to heart disease, stroke, and kidney problems if left untreated."
            })
        
        if high_hr_percent >= 40:
            potential_conditions.append({
                "condition": "Tachycardia Tendency",
                "confidence": f"{high_hr_percent:.1f}%",
                "description": "Frequent elevated heart rate may indicate stress, anxiety, or cardiac issues. Persistent tachycardia can lead to heart failure or stroke over time."
            })
        
        if low_hr_percent >= 40:
            potential_conditions.append({
                "condition": "Bradycardia Tendency",
                "confidence": f"{low_hr_percent:.1f}%",
                "description": "Frequent low heart rate may indicate a conduction disorder or could be a side effect of certain medications. Severe bradycardia can cause fatigue, dizziness, or fainting."
            })
        
        if low_ox_percent >= 30:
            potential_conditions.append({
                "condition": "Respiratory Concern",
                "confidence": f"{low_ox_percent:.1f}%",
                "description": "Recurring low oxygen levels may indicate respiratory issues such as COPD, asthma, or sleep apnea. Chronic hypoxemia can affect heart function and cognitive abilities."
            })
        
        if high_temp_percent >= 20:
            potential_conditions.append({
                "condition": "Recurring Fever",
                "confidence": f"{high_temp_percent:.1f}%",
                "description": "Multiple elevated temperature readings suggest infection, inflammation, or immune system disorders. Persistent fever requires medical evaluation to identify the underlying cause."
            })
        
        return potential_conditions
    
    def analyze_medication_effectiveness(self, medications, health_data_history, condition):
        """
        Analyze how effective medications are for managing a specific condition
        """
        if not medications or not health_data_history:
            return []
        
        # Filter medications relevant to the condition
        relevant_meds = [med for med in medications if condition.lower() in med['purpose'].lower()]
        
        if not relevant_meds:
            return []
        
        # Determine which metrics to track based on the condition
        target_metrics = []
        target_ranges = {}
        
        if "hypertension" in condition.lower():
            target_metrics = ["blood_pressure_systolic", "blood_pressure_diastolic"]
            target_ranges = {
                "blood_pressure_systolic": (90, 130),
                "blood_pressure_diastolic": (60, 80)
            }
        elif "tachycardia" in condition.lower():
            target_metrics = ["heart_rate"]
            target_ranges = {"heart_rate": (60, 100)}
        elif "bradycardia" in condition.lower():
            target_metrics = ["heart_rate"]
            target_ranges = {"heart_rate": (60, 100)}
        elif "asthma" in condition.lower() or "copd" in condition.lower():
            target_metrics = ["oxygen_level"]
            target_ranges = {"oxygen_level": (95, 100)}
        
        # Group readings by week to see trends
        readings_by_week = {}
        start_date = None
        
        for record in health_data_history:
            timestamp = record[2]
            record_date = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            
            if start_date is None:
                start_date = record_date
            
            week_num = (record_date - start_date).days // 7
            
            if week_num not in readings_by_week:
                readings_by_week[week_num] = []
            
            readings_by_week[week_num].append(record)
        
        # Analyze effectiveness over time
        effectiveness_data = []
        
        for week_num in sorted(readings_by_week.keys()):
            week_records = readings_by_week[week_num]
            week_start = start_date + datetime.timedelta(days=week_num*7)
            week_end = week_start + datetime.timedelta(days=6)
            
            week_data = {
                "week": week_num + 1,
                "date_range": f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}",
                "metrics": {}
            }
            
            # Calculate metrics for this week
            for metric in target_metrics:
                if metric == "blood_pressure_systolic":
                    values = [record[4] for record in week_records]
                    in_range = sum(1 for v in values if target_ranges[metric][0] <= v <= target_ranges[metric][1])
                    week_data["metrics"][metric] = {
                        "average": sum(values) / len(values),
                        "in_range_percent": (in_range / len(values)) * 100
                    }
                elif metric == "blood_pressure_diastolic":
                    values = [record[5] for record in week_records]
                    in_range = sum(1 for v in values if target_ranges[metric][0] <= v <= target_ranges[metric][1])
                    week_data["metrics"][metric] = {
                        "average": sum(values) / len(values),
                        "in_range_percent": (in_range / len(values)) * 100
                    }
                elif metric == "heart_rate":
                    values = [record[3] for record in week_records]
                    in_range = sum(1 for v in values if target_ranges[metric][0] <= v <= target_ranges[metric][1])
                    week_data["metrics"][metric] = {
                        "average": sum(values) / len(values),
                        "in_range_percent": (in_range / len(values)) * 100
                    }
                elif metric == "oxygen_level":
                    values = [record[6] for record in week_records]
                    in_range = sum(1 for v in values if target_ranges[metric][0] <= v <= target_ranges[metric][1])
                    week_data["metrics"][metric] = {
                        "average": sum(values) / len(values),
                        "in_range_percent": (in_range / len(values)) * 100
                    }
            
            effectiveness_data.append(week_data)
        
        # Calculate overall effectiveness
        overall_effectiveness = {}
        
        for metric in target_metrics:
            in_range_percents = [week["metrics"][metric]["in_range_percent"] for week in effectiveness_data if metric in week["metrics"]]
            if in_range_percents:
                overall_effectiveness[metric] = sum(in_range_percents) / len(in_range_percents)
            else:
                overall_effectiveness[metric] = 0
        
        # Determine overall effectiveness score
        if overall_effectiveness:
            overall_score = sum(overall_effectiveness.values()) / len(overall_effectiveness)
        else:
            overall_score = 0
        
        # Create effectiveness assessment
        effectiveness_assessment = {
            "condition": condition,
            "medications": [med["name"] for med in relevant_meds],
            "overall_effectiveness_score": overall_score,
            "weekly_data": effectiveness_data,
            "assessment": self._get_effectiveness_assessment(overall_score)
        }
        
        return effectiveness_assessment
    
    def _get_effectiveness_assessment(self, score):
        """Generate a textual assessment based on effectiveness score"""
        if score >= 90:
            return "Excellent control. Current medication regimen appears highly effective."
        elif score >= 75:
            return "Good control. Medication regimen is effective but occasional readings outside target range."
        elif score >= 60:
            return "Moderate control. Medication provides benefit but adjustments may improve outcomes."
        elif score >= 40:
            return "Fair control. Medication shows some effect but significant improvement needed."
        else:
            return "Poor control. Current medication regimen appears ineffective. Medical review recommended."
    
    def get_condition_specific_recommendations(self, conditions):
        """
        Get specific recommendations based on diagnosed conditions
        """
        if not conditions:
            return []
        
        recommendations = []
        
        for condition in conditions:
            condition_name = condition['name']
            
            # Check if we have specific guidelines for this condition
            for guideline_condition, guidelines in self.condition_guidelines.items():
                if guideline_condition.lower() in condition_name.lower():
                    # Add recommendations for this condition
                    for rec in guidelines.get('recommendations', []):
                        if rec not in recommendations:
                            recommendations.append(rec)
        
        # If no specific recommendations found, add general ones
        if not recommendations:
            recommendations = [
                "Regular monitoring of vital signs",
                "Take medications as prescribed",
                "Maintain a healthy diet and exercise regimen",
                "Regular check-ups with healthcare provider"
            ]
        
        return recommendations
