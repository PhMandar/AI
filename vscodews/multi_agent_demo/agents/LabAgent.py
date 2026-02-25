class LabAgent:
    def process(self, data):
        print(f"LOG: Lab test {data['test_type']} booked for patient {data['patient_id']} at {data['lab_name']}")