from agents.VitalsAgent import VitalsAgent;
from agents.AppointmentAgent import AppointmentAgent;
from agents.CaseDiscussionAgent import CaseDiscussionAgent;
from agents.AmbulanceAgent import AmbulanceAgent;
from agents.PharmacyAgent import PharmacyAgent;
from agents.LabAgent import LabAgent;

class DoctorBot:
    def handle_input(self, input_type, data):
        if input_type == "vitals":
            print("LOG: Processing vitals request")
            VitalsAgent().process(data)
        elif input_type == "appointment":
            print(f"LOG: Processing appointment request for patient {data['patient_id']}")
            AppointmentAgent().process(data)
        elif input_type == "discussion":
            print("LOG: Processing case discussion request")
            CaseDiscussionAgent().process(data)
        elif input_type == "ambulance":
            print("LOG: Processing ambulance request")
            AmbulanceAgent().process(data)
        elif input_type == "pharmacy":
            print("LOG: Processing pharmacy request")
            PharmacyAgent().process(data)
        elif input_type == "lab":
            print("LOG: Processing lab request")
            LabAgent().process(data)
        else:
            print("LOG: Unknown request type")
