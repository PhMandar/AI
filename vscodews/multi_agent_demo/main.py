from DoctorBot import DoctorBot


bot = DoctorBot()

bot.handle_input("appointment", {
    "patient_id": "P123",
    "doctor": "Dr. Smith",
    "time": "3 PM"
})
