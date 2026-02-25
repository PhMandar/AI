class CaseDiscussionAgent:
    def process(self, data):
        print(f"LOG: Case discussion for patient {data['patient_id']} initiated with Dr. {data['target_doctor']}")