class VitalsAgent:
    def process(self, data):
        print(f"LOG: Vitals received for patient {data['patient_id']}: {data['vitals']}")