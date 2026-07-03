from flask import Flask
from app.database.sqlite_client import SQLiteClient

app = Flask(__name__)




@app.route("/")
def home():
    return "SmartPark Admin API Running"


@app.route("/approve/<int:reservation_id>")
def approve(reservation_id):

    db = SQLiteClient()

    db.approve_reservation(reservation_id)

    db.close()

    return f"""
    <h2>✅ Reservation {reservation_id} Approved Successfully</h2>

    <a href="/pending/{reservation_id}">
        Revert To Pending
    </a>
    """


@app.route("/reject/<int:reservation_id>")
def reject(reservation_id):

    db = SQLiteClient()

    db.reject_reservation(reservation_id)

    db.close()

    return f"""
    <h2>❌ Reservation {reservation_id} Rejected Successfully</h2>

    <a href="/pending/{reservation_id}">
        Revert To Pending
    </a>
    """


@app.route("/pending/<int:reservation_id>")
def pending(reservation_id):

    db = SQLiteClient()

    db.pending_reservation(reservation_id)

    db.close()

    return f"""
    <h2>🟡 Reservation {reservation_id} moved back to Pending.</h2>
    """


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)