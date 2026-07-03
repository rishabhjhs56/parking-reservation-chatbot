from app.agents.admin_agent import AdminAgent

admin = AdminAgent()

admin.show_pending_reservations()

reservation_id = int(input("\nReservation ID: "))

decision = input("Approve (A) / Reject (R): ").upper()

if decision == "A":
    admin.approve_reservation(reservation_id)
else:
    admin.reject_reservation(reservation_id)

admin.show_pending_reservations()