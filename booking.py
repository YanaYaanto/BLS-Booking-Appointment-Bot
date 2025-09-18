# booking.py
import uuid
import json
from datetime import datetime, timedelta
from data import SAMPLE_SLOTS_FILE, BOOKINGS_FILE
from utils import load_json_file, save_json_file

class BookingSystem:
    def __init__(self):
        # load or initialize slots and bookings
        self.slots = load_json_file(SAMPLE_SLOTS_FILE)
        if not self.slots:
            self.slots = self._generate_sample_slots()
            save_json_file(SAMPLE_SLOTS_FILE, self.slots)

        self.bookings = load_json_file(BOOKINGS_FILE) or []

    def _generate_sample_slots(self):
        slots = []
        base = datetime.now() + timedelta(days=1)
        for day in range(7):  # next 7 days
            date = (base + timedelta(days=day)).strftime("%Y-%m-%d")
            for hour in (9, 10, 11, 14, 15, 16):
                slot_id = str(uuid.uuid4())[:8]
                slots.append({
                    "id": slot_id,
                    "date": date,
                    "time": f"{hour}:00",
                    "available": True
                })
        return slots

    def show_available_slots(self):
        available = [s for s in self.slots if s.get("available", True)]
        if not available:
            print("No available slots at the moment.")
            return
        print("\nAvailable Slots:")
        for s in available:
            print(f"ID: {s['id']}  Date: {s['date']}  Time: {s['time']}")
        print("Use the slot ID to book a slot.")

    def create_booking(self, name, email, phone, slot_id):
        # find slot
        slot = next((s for s in self.slots if s["id"] == slot_id and s.get("available", True)), None)
        if not slot:
            return False, "Selected slot is not available. Please check the slot ID."

        booking_id = str(uuid.uuid4())[:10]
        booking = {
            "booking_id": booking_id,
            "name": name,
            "email": email,
            "phone": phone,
            "slot_id": slot_id,
            "date": slot["date"],
            "time": slot["time"],
            "created_at": datetime.now().isoformat()
        }
        self.bookings.append(booking)
        # mark slot unavailable
        for s in self.slots:
            if s["id"] == slot_id:
                s["available"] = False
        # persist
        save_json_file(BOOKINGS_FILE, self.bookings)
        save_json_file(SAMPLE_SLOTS_FILE, self.slots)
        msg = f"Booking confirmed. Booking ID: {booking_id} | {slot['date']} {slot['time']}"
        return True, msg

    def show_bookings_for_phone(self, phone):
        user_bookings = [b for b in self.bookings if b["phone"] == phone]
        if not user_bookings:
            print("No bookings found for that phone number.")
            return
        print("\nYour Bookings:")
        for b in user_bookings:
            print(f"Booking ID: {b['booking_id']}  Date: {b['date']}  Time: {b['time']}  Name: {b['name']}")

    def cancel_booking(self, booking_id):
        booking = next((b for b in self.bookings if b["booking_id"] == booking_id), None)
        if not booking:
            return False, "Booking ID not found."
        # free the slot
        for s in self.slots:
            if s["id"] == booking["slot_id"]:
                s["available"] = True
        # remove booking
        self.bookings = [b for b in self.bookings if b["booking_id"] != booking_id]
        save_json_file(BOOKINGS_FILE, self.bookings)
        save_json_file(SAMPLE_SLOTS_FILE, self.slots)
        return True, "Booking canceled successfully."