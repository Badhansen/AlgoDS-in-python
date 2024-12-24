# Parking Lot System Design

## 1. Problem Understanding

"Let me first make sure I understand the requirements correctly:
- We need to design a multi-floor parking lot system
- It supports two vehicle types: 2-wheelers and 4-wheelers
- Each floor has a grid of parking spots
- We need to implement two parking strategies
- We need to track vehicles and manage parking operations"

---

## 2. Core Classes and Design Patterns

### Vehicle Class (Data Class)
```python
from dataclasses import dataclass

def Vehicle:
    vehicle_type: int      # 2 or 4 wheeler
    vehicle_number: str    # Vehicle registration
    ticket_id: str         # Unique ticket
    spot_id: str           # Where it's parked
```

### Strategy Pattern for Parking
```python
from abc import ABC, abstractmethod

class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, parking_lot, vehicle_type: int) -> Optional[str]:
        pass

class FirstAvailableSpotStrategy(ParkingStrategy):
    # Finds the first available spot (lowest indices)
    pass

class MaxFreeSpotsFloorStrategy(ParkingStrategy):
    # Finds floor with maximum free spots
    pass
```

### Main ParkingLot Class
- Manages the overall system
- Holds the parking grid and vehicle tracking
- Implements core operations

---

## 3. Data Structures Used

"I'm using three main data structures:

1. **Parking Grid:**
   - `parking[floor][row][col]`: 3D array for parking grid

2. **Vehicle Map:**
   - Dictionary for quick vehicle lookups
   - Keys: vehicle number/ticket ID
   - Values: Vehicle objects

3. **Spot Map:**
   - Dictionary for occupied spots
   - Counters for free spots per floor/type"

---

## 4. Key Operations

### Parking a Vehicle
```python
def park(self, vehicle_type, vehicle_number, ticket_id, strategy):
    # 1. Validate vehicle isn't already parked
    # 2. Use selected strategy to find a spot
    # 3. Create Vehicle object and update maps
    # 4. Update free spot counts
    # 5. Return spot ID
```

### Removing a Vehicle
```python
def remove_vehicle(self, spot_id):
    # 1. Find vehicle in spot
    # 2. Update all tracking maps
    # 3. Update free spot count
```

### Searching
```python
def search_vehicle(self, query):
    # Simple lookup in vehicle_map
```

---

## 5. Time Complexity

"Let me explain the time complexities:
- **Parking:**
  - `O(F×R×C)` worst case for the first strategy
  - `O(F + R×C)` for the second strategy
- **Removal:** `O(1)` using hash maps
- **Search:** `O(1)` using hash maps
- **Get Free Spots:** `O(1)` using counters"

---

## 6. Design Benefits

"This design offers several advantages:

1. **Extensible:** New parking strategies can be added easily
2. **Efficient:** `O(1)` lookups for most operations
3. **Maintainable:** Clear separation of concerns
4. **Scalable:** Can handle multiple floors and vehicle types"

---

## 7. Potential Improvements

"We could enhance this by:
- Adding parking spot size validation
- Implementing parking fee calculation
- Adding vehicle type validation
- Adding concurrency support for multi-threading
- Implementing a logging system"

---

## 8. Conclusion

"This design satisfies all requirements while maintaining good software engineering principles and remaining extensible for future enhancements."

---

## Tips for Interview Delivery

1. Start with a high-level overview before diving into details.
2. Draw diagrams if possible.
3. Use examples to illustrate concepts.
4. Highlight design pattern usage.
5. Be ready to explain trade-offs.
6. Show enthusiasm and willingness to consider improvements.

### Remember to:
- Speak clearly and confidently.
- Use proper technical terminology.
- Be ready for follow-up questions.
- Acknowledge if you're unsure about something.
- Show your thought process.
