class PharmacyAgent:
    def process(self, data):
        print(f"LOG: Medicine order for patient {data['patient_id']} sent to {data['store_name']}")