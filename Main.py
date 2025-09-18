# main.py
from booking import BookingSystem
from data import CONTACT_PHONE

def main():
    print("===================================")
    print(" BLS Appointment Booking System")
    print(" Contact: " + CONTACT_PHONE)
    print("===================================\n")

    system = BookingSystem()

    while True:
        print("\nMain Menu:")
        print("1. View available slots")
        print("2. Book an appointment")
        print("3. View my bookings")
        print("4. Cancel a booking")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            system.show_available_slots()
        elif choice == "2":
            name = input("Enter full name: ").strip()
            email = input("Enter email: ").strip()
            phone = input("Enter phone number: ").strip()
            slot_id = input("Enter slot ID to book: ").strip()
            success, msg = system.create_booking(name, email, phone, slot_id)
            print(msg)
        elif choice == "3":
            phone = input("Enter phone number used to book: ").strip()
            system.show_bookings_for_phone(phone)
        elif choice == "4":
            booking_id = input("Enter booking ID to cancel: ").strip()
            success, msg = system.cancel_booking(booking_id)
            print(msg)
        elif choice == "5":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()