class AmbulanceAgent:
    def process(self, data):
        print(f"LOG: Ambulance booked for patient {data['patient_id']} to {data['destination']}")