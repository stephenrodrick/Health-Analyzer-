import datetime

class MedicationManager:
    """Class to manage medication schedules and reminders"""
    
    def __init__(self, db_manager):
        """Initialize with a database manager"""
        self.db_manager = db_manager
    
    def get_daily_schedule(self, user_id):
        """Get the daily medication schedule for a user"""
        medications = self.db_manager.get_user_medications(user_id)
        
        if not medications:
            return []
        
        # Organize medications by frequency
        schedule = []
        
        for med in medications:
            times = self._parse_frequency(med['frequency'])
            
            for time_slot in times:
                schedule.append({
                    'name': med['name'],
                    'dosage': med['dosage'],
                    'time': time_slot,
                    'purpose': med['purpose'],
                    'notes': f"Prescribed by {med['prescribing_doctor']}"
                })
        
        # Sort by time
        schedule.sort(key=lambda x: self._time_to_minutes(x['time']))
        
        return schedule
    
    def _parse_frequency(self, frequency):
        """Parse medication frequency into specific times"""
        frequency = frequency.lower()
        
        if "once daily" in frequency:
            return ["08:00"]
        elif "twice daily" in frequency:
            return ["08:00", "20:00"]
        elif "three times daily" in frequency:
            return ["08:00", "14:00", "20:00"]
        elif "four times daily" in frequency:
            return ["08:00", "12:00", "16:00", "20:00"]
        elif "with breakfast" in frequency:
            return ["08:00"]
        elif "with dinner" in frequency:
            return ["19:00"]
        elif "before bed" in frequency:
            return ["22:00"]
        elif "as needed" in frequency:
            return ["As needed"]
        else:
            return ["08:00"]  # Default
    
    def _time_to_minutes(self, time_str):
        """Convert time string to minutes for sorting"""
        if time_str == "As needed":
            return 24 * 60  # Put at the end
        
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    def get_medication_interactions(self, user_id):
        """Check for potential medication interactions"""
        medications = self.db_manager.get_user_medications(user_id)
        
        if not medications or len(medications) < 2:
            return []
        
        # This is a simplified example - in a real system, you would use a comprehensive
        # drug interaction database or API
        
        # Define some example interactions
        interaction_pairs = [
            ("Lisinopril", "Potassium supplements", "May cause high potassium levels"),
            ("Metformin", "Ibuprofen", "May affect kidney function"),
            ("Warfarin", "Aspirin", "Increased bleeding risk"),
            ("Simvastatin", "Amlodipine", "Increased risk of muscle pain"),
            ("Fluoxetine", "Tramadol", "Risk of serotonin syndrome"),
            ("Levothyroxine", "Calcium supplements", "Reduced absorption of thyroid medication")
        ]
        
        # Check for interactions
        found_interactions = []
        med_names = [med['name'] for med in medications]
        
        for med1, med2, warning in interaction_pairs:
            if med1 in med_names and med2 in med_names:
                found_interactions.append({
                    'medications': [med1, med2],
                    'warning': warning,
                    'severity': 'Moderate'  # In a real system, this would vary
                })
        
        return found_interactions
    
    def get_medication_adherence(self, user_id, days=30):
        """
        Calculate medication adherence
        This is a simplified example - in a real system, you would track actual medication intake
        """
        medications = self.db_manager.get_user_medications(user_id)
        
        if not medications:
            return []
        
        # In a real system, you would have actual adherence data
        # Here we'll simulate it with random but realistic values
        import random
        
        adherence_data = []
        
        for med in medications:
            # Generate simulated adherence data
            adherence_rate = random.uniform(0.7, 1.0)  # 70-100% adherence
            missed_doses = int((1 - adherence_rate) * days)
            
            adherence_data.append({
                'medication': med['name'],
                'adherence_rate': round(adherence_rate * 100, 1),
                'missed_doses': missed_doses,
                'days_tracked': days,
                'status': self._get_adherence_status(adherence_rate)
            })
        
        return adherence_data
    
    def _get_adherence_status(self, rate):
        """Get a status description based on adherence rate"""
        if rate >= 0.95:
            return "Excellent"
        elif rate >= 0.85:
            return "Good"
        elif rate >= 0.75:
            return "Fair"
        else:
            return "Poor"
