from app.agents.admin_agent import AdminAgent


def main():

    admin = AdminAgent()

    while True:

        print("\n" + "=" * 50)
        print(" SMARTPARK AI - ADMIN CONSOLE ")
        print("=" * 50)

        print("1. View Pending Reservations")
        print("2. Approve Reservation")
        print("3. Reject Reservation")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            admin.show_pending_reservations()

        elif choice == "2":

            reservation_id = input(
                "\nEnter Reservation ID to Approve: "
            ).strip()

            if reservation_id.isdigit():

                admin.approve_reservation(int(reservation_id))

            else:

                print("❌ Invalid Reservation ID.")

        elif choice == "3":

            reservation_id = input(
                "\nEnter Reservation ID to Reject: "
            ).strip()

            if reservation_id.isdigit():

                admin.reject_reservation(int(reservation_id))

            else:

                print("❌ Invalid Reservation ID.")

        elif choice == "4":

            print("\n👋 Exiting Admin Console...\n")
            break

        else:

            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()