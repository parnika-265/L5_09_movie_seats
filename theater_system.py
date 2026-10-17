
"""Manage movie show seat reservations and ticket codes."""

import hashlib
import json

SHOWS = {
    "SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
    "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []},
}


def reserve_seat(show_id, seat_number, system_logs=None):
    """Reserve a valid seat and record the result."""
    if system_logs is None:
        system_logs = []

    if show_id not in SHOWS:
        system_logs.append(f"Unknown show: {show_id}")
        return False

    show = SHOWS[show_id]

    if (
        not isinstance(seat_number, int)
        or isinstance(seat_number, bool)
        or not 1 <= seat_number <= show["seats"]
    ):
        system_logs.append(f"Invalid seat number: {seat_number}")
        return False

    if seat_number in show["booked"]:
        system_logs.append(
            f"Seat {seat_number} already taken for {show_id}"
        )
        return False

    show["booked"].append(seat_number)
    system_logs.append(f"Reserved seat {seat_number} for {show_id}")
    return True


def release_seat(show_id, seat_number):
    """Release a booked seat if it exists."""
    if show_id not in SHOWS:
        return False

    try:
        SHOWS[show_id]["booked"].remove(seat_number)
    except ValueError:
        return False

    return True


def ticket_code(show_id, seat_number):
    """Generate a short ticket identifier."""
    ticket_data = f"{show_id}:{seat_number}".encode("utf-8")
    return hashlib.sha256(ticket_data).hexdigest()[:8]


def dump_reservations(filename="seats.json"):
    """Save reservations to a JSON file."""
    with open(filename, "w", encoding="utf-8") as reservation_file:
        json.dump(SHOWS, reservation_file, indent=4)


def load_reservations(filename="seats.json"):
    """Load reservations from a JSON file."""
    with open(filename, "r", encoding="utf-8") as reservation_file:
        return json.load(reservation_file)


def print_seating_summary():
    """Print available and booked seats for each show."""
    for show in SHOWS.values():
        free_seats = show["seats"] - len(show["booked"])
        print(
            f'{show["title"]}: {free_seats} seats free, '
            f'booked = {show["booked"]}'
        )


def main():
    """Run the movie-seat reservation demonstration."""
    system_logs = []

    reserve_seat("SHOW-1", 5, system_logs)
    reserve_seat("SHOW-1", 5, system_logs)
    reserve_seat("SHOW-1", 25, system_logs)
    reserve_seat("SHOW-2", -1, system_logs)
    reserve_seat("SHOW-2", "A7", system_logs)
    release_seat("SHOW-2", 3)

    print("Ticket code:", ticket_code("SHOW-1", 5))

    seat_input = input(
        "Seat number to book for SHOW-2 (Enter for 4): "
    ).strip()

    if not seat_input:
        seat_number = 4
    elif seat_input.isdigit():
        seat_number = int(seat_input)
    else:
        seat_number = None

    if seat_number is None:
        print("Invalid seat number. Enter a whole number.")
    else:
        reserve_seat("SHOW-2", seat_number, system_logs)

    for log_entry in system_logs:
        print(log_entry)

    dump_reservations()
    loaded_shows = load_reservations()
    SHOWS.clear()
    SHOWS.update(loaded_shows)
    print_seating_summary()


if __name__ == "__main__":
    main()
