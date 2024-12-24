import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class Vehicle:
    vehicle_type: int      # 2 or 4 wheeler
    vehicle_number: str    # Vehicle registration
    ticket_id: str         # Unique ticket
    spot_id: str           # Where it's parked

# Strategy Pattern: Abstract base class for parking strategies
class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, parking_lot, vehicle_type: int) -> Optional[str]:
        """Find a parking spot based on the strategy"""
        pass

# Concrete Strategy: Find first available spot
class FirstAvailableSpotStrategy(ParkingStrategy):
    def find_spot(self, parking_lot, vehicle_type: int) -> Optional[str]:
        """Find first available spot (lowest indices)"""
        for floor in range(parking_lot.floors):
            for row in range(parking_lot.rows):
                for col in range(parking_lot.cols):
                    if (parking_lot.parking[floor][row][col] == vehicle_type and 
                        parking_lot._get_spot_id(floor, row, col) not in parking_lot.spot_map):
                        return parking_lot._get_spot_id(floor, row, col)
        return None

# Concrete Strategy: Find spot on floor with maximum free spots
class MaxFreeSpotsFloorStrategy(ParkingStrategy):
    def find_spot(self, parking_lot, vehicle_type: int) -> Optional[str]:
        """Find spot on floor with maximum free spots"""
        max_spots = -1
        chosen_floor = -1
        
        # Find floor with maximum free spots
        for floor in range(parking_lot.floors):
            free_count = parking_lot.free_spots[floor][vehicle_type]
            if free_count > max_spots:
                max_spots = free_count
                chosen_floor = floor
        
        if chosen_floor == -1:
            return None
            
        # Find first available spot on chosen floor
        for row in range(parking_lot.rows):
            for col in range(parking_lot.cols):
                if (parking_lot.parking[chosen_floor][row][col] == vehicle_type and 
                    parking_lot._get_spot_id(chosen_floor, row, col) not in parking_lot.spot_map):
                    return parking_lot._get_spot_id(chosen_floor, row, col)
        return None

class ParkingLot:
    def __init__(self, parking: List[List[List[int]]]):
        self.parking = parking
        self.floors = len(parking)
        self.rows = len(parking[0])
        self.cols = len(parking[0][0])
        
        # Maps to track vehicle locations and spots
        self.vehicle_map: Dict[str, Vehicle] = {}
        self.spot_map: Dict[str, Vehicle] = {}
        
        # Initialize counts of free spots per floor and type
        self.free_spots = defaultdict(lambda: defaultdict(int))
        self._initialize_free_spots()
        
        # Initialize parking strategies
        self.strategies = {
            0: FirstAvailableSpotStrategy(),
            1: MaxFreeSpotsFloorStrategy()
        }
    
    def _initialize_free_spots(self):
        """Initialize the count of free spots for each floor and vehicle type"""
        for floor in range(self.floors):
            for row in range(self.rows):
                for col in range(self.cols):
                    spot_type = self.parking[floor][row][col]
                    if spot_type in (2, 4):  # Active spots only
                        self.free_spots[floor][spot_type] += 1
    
    def _get_spot_id(self, floor: int, row: int, col: int) -> str:
        """Generate spot ID from coordinates"""
        return f"{floor}-{row}-{col}"
    
    def park(self, vehicle_type: int, vehicle_number: str, ticket_id: str, 
            parking_strategy: int) -> str:
        """Park a vehicle using the specified strategy"""
        # Check if vehicle is already parked
        if vehicle_number in self.vehicle_map or ticket_id in self.vehicle_map:
            logging.warning(f"Vehicle {vehicle_number} or ticket {ticket_id} is already parked.")
            return ""
            
        # Get the appropriate strategy and find spot
        strategy = self.strategies.get(parking_strategy)
        if not strategy:
            logging.error("Invalid parking strategy.")
            return ""
            
        spot_id = strategy.find_spot(self, vehicle_type)
        if not spot_id:
            logging.info(f"No available spot for vehicle type {vehicle_type}.")
            return ""
            
        # Create and store vehicle information
        vehicle = Vehicle(vehicle_type, vehicle_number, ticket_id, spot_id)
        self.vehicle_map[vehicle_number] = vehicle
        self.vehicle_map[ticket_id] = vehicle
        self.spot_map[spot_id] = vehicle
        
        # Update free spots count
        floor = int(spot_id.split("-")[0])
        self.free_spots[floor][vehicle_type] -= 1
        
        logging.info(f"Vehicle {vehicle_number} parked at {spot_id}.")
        return spot_id
    
    def remove_vehicle(self, spot_id: str) -> bool:
        """Remove a vehicle from its parking spot"""
        if spot_id not in self.spot_map:
            logging.warning(f"Spot ID {spot_id} not found.")
            return False
            
        vehicle = self.spot_map[spot_id]
        floor = int(spot_id.split("-")[0])
        
        # Update maps and free spots count
        del self.vehicle_map[vehicle.vehicle_number]
        del self.vehicle_map[vehicle.ticket_id]
        del self.spot_map[spot_id]
        self.free_spots[floor][vehicle.vehicle_type] += 1
        
        logging.info(f"Vehicle {vehicle.vehicle_number} removed from {spot_id}.")
        return True
    
    def search_vehicle(self, query: str) -> str:
        """Search for a vehicle by number or ticket ID"""
        if query in self.vehicle_map:
            spot_id = self.vehicle_map[query].spot_id
            logging.info(f"Vehicle {query} found at {spot_id}.")
            return spot_id
        logging.warning(f"Vehicle {query} not found.")
        return ""
    
    def get_free_spots_count(self, floor: int, vehicle_type: int) -> int:
        """Get count of free spots for a vehicle type on a floor"""
        return self.free_spots[floor][vehicle_type]

# Example usage
def main():
    parking = [[[4, 4, 2, 2],
                [2, 4, 2, 0],
                [0, 2, 2, 2],
                [4, 4, 4, 0]]]
    
    lot = ParkingLot(parking)
    
    # Test parking
    spot1 = lot.park(2, "bh234", "tkt4534", 0)
    spot2 = lot.park(4, "bh235", "tkt4535", 1)
    
    # Test searching
    lot.search_vehicle("bh234")
    
    # Test removal
    lot.remove_vehicle(spot1)

if __name__ == "__main__":
    main()


"""
@dataclass
class Vehicle:
    vehicle_type: int      # 2 or 4 wheeler
    vehicle_number: str    # Vehicle registration
    ticket_id: str         # Unique ticket
    spot_id: str           # Where it's parked

class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, parking_lot, vehicle_type: int) -> Optional[str]:
        pass

class FirstAvailableSpotStrategy(ParkingStrategy):
    def find_spot(self, parking_lot, vehicle_type: int) -> Optional[str]:
        pass
        
class MaxFreeSpotsFloorStrategy(ParkingStrategy):
    def find_spot(self, parking_lot, vehicle_type: int) -> Optional[str]:
        pass

class ParkingLot:
    def __init__(self, parking):
        pass
    def park(self, vehicle_type: int, vehicle_number: str, ticket_id: str, 
            parking_strategy: int) -> str:
        pass
    def remove_vehicle(self, spot_id: str) -> bool:
        pass
    def search_vehicle(self, query: str) -> str:
        pass
    def get_free_spots_count(self, floor: int, vehicle_type: int) -> int:
        pass
    
"""