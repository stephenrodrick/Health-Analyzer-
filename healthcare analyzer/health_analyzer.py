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
            
            # Check oxygen level
            if oxygen < self.thresholds['oxygen_level']['concerning']:
                low_ox_count += 1
            
            # Check temperature
            if temp > self.thresholds['temperature']['elevated']:
                high_temp_count += 1
        
        # Calculate percentages
        high_bp_percent = (high_bp_count / total_readings) * 100
        high_hr_percent = (high_hr_count / total_readings) * 100
        low_ox_percent = (low_ox_count / total_readings) * 100
        high_temp_percent = (high_temp_count / total_readings) * 100
        
        # Identify potential conditions based on patterns
        potential_conditions = []
        
        if high_bp_percent >= 50:
            potential_conditions.append({
                "condition": "Hypertension Risk",
                "confidence": f"{high_bp_percent:.1f}%",
                "description": "Consistently elevated blood pressure readings suggest hypertension risk."
            })
        
        if high_hr_percent >= 40:
            potential_conditions.append({
                "condition": "Tachycardia Tendency",
                "confidence": f"{high_hr_percent:.1f}%",
                "description": "Frequent elevated heart rate may indicate stress or cardiac issues."
            })
        
        if low_ox_percent >= 30:
            potential_conditions.append({
                "condition": "Respiratory Concern",
                "confidence": f"{low_ox_percent:.1f}%",
                "description": "Recurring low oxygen levels may indicate respiratory issues."
            })
        
        if high_temp_percent >= 20:
            potential_conditions.append({
                "condition": "Recurring Fever",
                "confidence": f"{high_temp_percent:.1f}%",
                "description": "Multiple elevated temperature readings suggest infection or inflammation."
            })
        
        return potential_conditions