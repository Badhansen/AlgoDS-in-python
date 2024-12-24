from typing import List, Dict, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Data class to represent a Cinema
@dataclass
class Cinema:
    cinema_id: int
    city_id: int
    screens: List['Screen'] = field(default_factory=list)

# Data class to represent a Screen
@dataclass
class Screen:
    screen_index: int
    rows: int
    columns: int
    shows: List['Show'] = field(default_factory=list)
    seats: List[List[bool]] = field(init=False)

    def __post_init__(self):
        self.seats = [[False] * self.columns for _ in range(self.rows)]  # False means seat is free

# Data class to represent a Show
@dataclass
class Show:
    show_id: int
    movie_id: int
    screen: Screen
    start_time: int
    end_time: int

# Data class to represent a Ticket
@dataclass
class Ticket:
    ticket_id: str
    show: Show
    seats: List[str]

class BookingSystem:
    def __init__(self):
        self.cinemas: Dict[int, Cinema] = {}
        self.tickets: Dict[str, Ticket] = {}

    def add_cinema(self, cinema_id: int, city_id: int, screen_count: int, screen_row: int, screen_column: int):
        cinema = Cinema(cinema_id, city_id)
        for i in range(screen_count):
            cinema.screens.append(Screen(i, screen_row, screen_column))
        self.cinemas[cinema_id] = cinema
        logging.info(f"Added cinema {cinema_id} in city {city_id} with {screen_count} screens.")

    def add_show(self, show_id: int, movie_id: int, cinema_id: int, screen_index: int, start_time: int, end_time: int):
        cinema = self.cinemas.get(cinema_id)
        if cinema:
            screen = cinema.screens[screen_index]
            show = Show(show_id, movie_id, screen, start_time, end_time)
            screen.shows.append(show)
            logging.info(f"Added show {show_id} for movie {movie_id} in cinema {cinema_id}, screen {screen_index}.")

    def book_ticket(self, ticket_id: str, show_id: int, tickets_count: int) -> List[str]:
        for cinema in self.cinemas.values():
            for screen in cinema.screens:
                for show in screen.shows:
                    if show.show_id == show_id:
                        seats = self._find_seats(screen, tickets_count)
                        if seats:
                            ticket = Ticket(ticket_id, show, seats)
                            self.tickets[ticket_id] = ticket
                            logging.info(f"Booked ticket {ticket_id} for show {show_id}: {seats}.")
                            return seats
        logging.warning(f"Failed to book ticket {ticket_id} for show {show_id}. Not enough seats available.")
        return []

    def _find_seats(self, screen: Screen, tickets_count: int) -> Optional[List[str]]:
        # Try to find continuous seats first
        for row in range(screen.rows):
            for col in range(screen.columns - tickets_count + 1):
                if all(not screen.seats[row][col + i] for i in range(tickets_count)):
                    for i in range(tickets_count):
                        screen.seats[row][col + i] = True  # Mark seats as booked
                    return [f"{row}-{col + i}" for i in range(tickets_count)]

        # If continuous seats are not available, find any available seats
        available_seats = []
        for row in range(screen.rows):
            for col in range(screen.columns):
                if not screen.seats[row][col]:
                    available_seats.append(f"{row}-{col}")
                    if len(available_seats) == tickets_count:
                        for seat in available_seats:
                            r, c = map(int, seat.split('-'))
                            screen.seats[r][c] = True  # Mark seats as booked
                        return available_seats
        return None

    def cancel_ticket(self, ticket_id: str) -> bool:
        ticket = self.tickets.pop(ticket_id, None)
        if ticket:
            for seat in ticket.seats:
                row, col = map(int, seat.split('-'))
                ticket.show.screen.seats[row][col] = False  # Mark seat as free
            logging.info(f"Cancelled ticket {ticket_id}.")
            return True
        logging.warning(f"Ticket {ticket_id} does not exist or is already cancelled.")
        return False

    def get_free_seats_count(self, show_id: int) -> int:
        for cinema in self.cinemas.values():
            for screen in cinema.screens:
                for show in screen.shows:
                    if show.show_id == show_id:
                        free_count = sum(not seat for row in screen.seats for seat in row)
                        logging.info(f"Free seats count for show {show_id}: {free_count}.")
                        return free_count
        logging.warning(f"No show found with ID {show_id}.")
        return 0

    def list_cinemas(self, movie_id: int, city_id: int) -> List[int]:
        cinema_ids = [cinema.cinema_id for cinema in self.cinemas.values() if cinema.city_id == city_id and
                      any(show.movie_id == movie_id for screen in cinema.screens for show in screen.shows)]
        logging.info(f"Cinemas in city {city_id} showing movie {movie_id}: {cinema_ids}.")
        return sorted(cinema_ids)

    def list_shows(self, movie_id: int, cinema_id: int) -> List[int]:
        cinema = self.cinemas.get(cinema_id)
        if cinema:
            show_ids = [
                show.show_id for screen in cinema.screens for show in screen.shows if show.movie_id == movie_id
            ]
            # Sort show_ids based on the start time and then by show_id
            show_ids.sort(key=lambda x: (
                next(show for screen in cinema.screens for show in screen.shows if show.show_id == x).start_time,
                x
            ), reverse=True)
            logging.info(f"Shows for movie {movie_id} in cinema {cinema_id}: {show_ids}.")
            return show_ids
        logging.warning(f"No cinema found with ID {cinema_id}.")
        return []


def main():
    system = BookingSystem()
    system.add_cinema(cinema_id=0, city_id=1, screen_count=4, screen_row=5, screen_column=10)
    system.add_show(show_id=1, movie_id=4, cinema_id=0, screen_index=0, start_time=1710516108725, end_time=1710523308725)
    system.add_show(show_id=2, movie_id=11, cinema_id=0, screen_index=1, start_time=1710516108725, end_time=1710523308725)

    print(system.list_cinemas(movie_id=4, city_id=1))  # Should return [0]
    print(system.list_shows(movie_id=4, cinema_id=0))  # Should return [1]
    print(system.get_free_seats_count(show_id=1))  # Should return 50
    print(system.book_ticket(ticket_id='tkt-1', show_id=1, tickets_count=4))  # Should return booked seats
    print(system.get_free_seats_count(show_id=1))  # Should return 46
    print(system.cancel_ticket(ticket_id='tkt-1'))  # Should return True
    print(system.get_free_seats_count(show_id=1))  # Should return 50

if __name__ == "__main__":
    main()