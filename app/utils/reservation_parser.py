def parse_reservation_summary(text: str):

    if "Reservation Completed Successfully" not in text:
        return None

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    data = {}

    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()

    return data