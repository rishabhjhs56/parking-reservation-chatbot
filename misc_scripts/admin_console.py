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
        print("4. Revert Reservation to Pending")
        print("5. Exit")

        choice = input("\nEnter your choice: ").strip()

        # -----------------------------------------
        # View Pending Reservations
        # -----------------------------------------

        if choice == "1":

            admin.show_pending_reservations()

        # -----------------------------------------
        # Approve Reservation
        # -----------------------------------------

        elif choice == "2":

            reservation_id = input(
                "\nEnter Reservation ID to Approve: "
            ).strip()

            if reservation_id.isdigit():

                admin.approve_reservation(int(reservation_id))

            else:

                print("❌ Invalid Reservation ID.")

        # -----------------------------------------
        # Reject Reservation
        # -----------------------------------------

        elif choice == "3":

            reservation_id = input(
                "\nEnter Reservation ID to Reject: "
            ).strip()

            if reservation_id.isdigit():

                admin.reject_reservation(int(reservation_id))

            else:

                print("❌ Invalid Reservation ID.")

        # -----------------------------------------
        # Revert Reservation to Pending
        # -----------------------------------------

        elif choice == "4":

            reservation_id = input(
                "\nEnter Reservation ID to Move Back to Pending: "
            ).strip()

            if reservation_id.isdigit():

                admin.pending_reservation(int(reservation_id))

            else:

                print("❌ Invalid Reservation ID.")

        # -----------------------------------------
        # Exit
        # -----------------------------------------

        elif choice == "5":

            print("\n👋 Exiting Admin Console...\n")
            break

        # -----------------------------------------
        # Invalid Choice
        # -----------------------------------------

        else:

            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()