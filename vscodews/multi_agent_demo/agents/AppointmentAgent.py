class AppointmentAgent:
    def process(self, data):
        print(f"LOG: Appointment booked with {data['doctor']} at {data['time']} for patient {data['patient_id']}")
