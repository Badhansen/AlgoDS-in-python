using System;
using System.Collections.Generic;

namespace ParkingLotSystem
{
    // Vehicle class to represent a parked vehicle
    public class Vehicle
    {
        public int VehicleType { get; set; } // 2 or 4 wheeler
        public string VehicleNumber { get; set; } // Vehicle registration
        public string TicketId { get; set; } // Unique ticket
        public string SpotId { get; set; } // Where it's parked

        public Vehicle(int vehicleType, string vehicleNumber, string ticketId, string spotId)
        {
            VehicleType = vehicleType;
            VehicleNumber = vehicleNumber;
            TicketId = ticketId;
            SpotId = spotId;
        }
    }

    // Strategy Pattern: Abstract base class for parking strategies
    public interface IParkingStrategy
    {
        string FindSpot(ParkingLot parkingLot, int vehicleType);
    }

    // Concrete Strategy: Find first available spot
    public class FirstAvailableSpotStrategy : IParkingStrategy
    {
        public string FindSpot(ParkingLot parkingLot, int vehicleType)
        {
            for (int floor = 0; floor < parkingLot.Floors; floor++)
            {
                for (int row = 0; row < parkingLot.Rows; row++)
                {
                    for (int col = 0; col < parkingLot.Cols; col++)
                    {
                        if (parkingLot.Parking[floor][row][col] == vehicleType &&
                            !parkingLot.SpotMap.ContainsKey(parkingLot.GetSpotId(floor, row, col)))
                        {
                            return parkingLot.GetSpotId(floor, row, col);
                        }
                    }
                }
            }
            return null;
        }
    }

    // Concrete Strategy: Find spot on floor with maximum free spots
    public class MaxFreeSpotsFloorStrategy : IParkingStrategy
    {
        public string FindSpot(ParkingLot parkingLot, int vehicleType)
        {
            int maxSpots = -1;
            int chosenFloor = -1;

            for (int floor = 0; floor < parkingLot.Floors; floor++)
            {
                int freeCount = parkingLot.FreeSpots[floor][vehicleType];
                if (freeCount > maxSpots)
                {
                    maxSpots = freeCount;
                    chosenFloor = floor;
                }
            }

            if (chosenFloor == -1) return null;

            for (int row = 0; row < parkingLot.Rows; row++)
            {
                for (int col = 0; col < parkingLot.Cols; col++)
                {
                    if (parkingLot.Parking[chosenFloor][row][col] == vehicleType &&
                        !parkingLot.SpotMap.ContainsKey(parkingLot.GetSpotId(chosenFloor, row, col)))
                    {
                        return parkingLot.GetSpotId(chosenFloor, row, col);
                    }
                }
            }
            return null;
        }
    }

    // ParkingLot class to manage the parking system
    public class ParkingLot
    {
        public int Floors { get; }
        public int Rows { get; }
        public int Cols { get; }
        public int[][][] Parking { get; }
        public Dictionary<string, Vehicle> VehicleMap { get; }
        public Dictionary<string, Vehicle> SpotMap { get; }
        public Dictionary<int, Dictionary<int, int>> FreeSpots { get; }
        public Dictionary<int, IParkingStrategy> Strategies { get; }

        public ParkingLot(int[][][] parking)
        {
            Parking = parking;
            Floors = parking.Length;
            Rows = parking[0].Length;
            Cols = parking[0][0].Length;

            VehicleMap = new Dictionary<string, Vehicle>();
            SpotMap = new Dictionary<string, Vehicle>();
            FreeSpots = new Dictionary<int, Dictionary<int, int>>();

            Strategies = new Dictionary<int, IParkingStrategy>
            {
                { 0, new FirstAvailableSpotStrategy() },
                { 1, new MaxFreeSpotsFloorStrategy() }
            };

            InitializeFreeSpots();
        }

        private void InitializeFreeSpots()
        {
            for (int floor = 0; floor < Floors; floor++)
            {
                FreeSpots[floor] = new Dictionary<int, int>
                {
                    { 2, 0 },
                    { 4, 0 }
                };

                for (int row = 0; row < Rows; row++)
                {
                    for (int col = 0; col < Cols; col++)
                    {
                        int spotType = Parking[floor][row][col];
                        if (spotType == 2 || spotType == 4)
                        {
                            FreeSpots[floor][spotType]++;
                        }
                    }
                }
            }
        }

        public string GetSpotId(int floor, int row, int col)
        {
            return $"{floor}-{row}-{col}";
        }

        public string Park(int vehicleType, string vehicleNumber, string ticketId, int parkingStrategy)
        {
            if (VehicleMap.ContainsKey(vehicleNumber) || VehicleMap.ContainsKey(ticketId))
            {
                Console.WriteLine($"Vehicle {vehicleNumber} or ticket {ticketId} is already parked.");
                return null;
            }

            var strategy = Strategies[parkingStrategy];
            string spotId = strategy.FindSpot(this, vehicleType);
            if (spotId == null)
            {
                Console.WriteLine($"No available spot for vehicle type {vehicleType}.");
                return null;
            }

            var vehicle = new Vehicle(vehicleType, vehicleNumber, ticketId, spotId);
            VehicleMap[vehicleNumber] = vehicle;
            VehicleMap[ticketId] = vehicle;
            SpotMap[spotId] = vehicle;

            int floor = int.Parse(spotId.Split('-')[0]);
            FreeSpots[floor][vehicleType]--;

            Console.WriteLine($"Vehicle {vehicleNumber} parked at {spotId}.");
            return spotId;
        }

        public bool RemoveVehicle(string spotId)
        {
            if (!SpotMap.ContainsKey(spotId))
            {
                Console.WriteLine($"Spot ID {spotId} not found.");
                return false;
            }

            var vehicle = SpotMap[spotId];
            int floor = int.Parse(spotId.Split('-')[0]);

            VehicleMap.Remove(vehicle.VehicleNumber);
            VehicleMap.Remove(vehicle.TicketId);
            SpotMap.Remove(spotId);
            FreeSpots[floor][vehicle.VehicleType]++;

            Console.WriteLine($"Vehicle {vehicle.VehicleNumber} removed from {spotId}.");
            return true;
        }

        public string SearchVehicle(string query)
        {
            if (VehicleMap.ContainsKey(query))
            {
                string spotId = VehicleMap[query].SpotId;
                Console.WriteLine($"Vehicle {query} found at {spotId}.");
                return spotId;
            }
            Console.WriteLine($"Vehicle {query} not found.");
            return null;
        }

        public int GetFreeSpotsCount(int floor, int vehicleType)
        {
            return FreeSpots[floor][vehicleType];
        }
    }

    // Example usage
    class Program
    {
        static void Main(string[] args)
        {
            int[][][] parking = new int[][][]
            {
                new int[][] 
                {
                    new int[] { 4, 4, 2, 2 },
                    new int[] { 2, 4, 2, 0 },
                    new int[] { 0, 2, 2, 2 },
                    new int[] { 4, 4, 4, 0 }
                }
            };

            var lot = new ParkingLot(parking);

            // Test parking
            string spot1 = lot.Park(2, "bh234", "tkt4534", 0);
            string spot2 = lot.Park(4, "bh235", "tkt4535", 1);

            // Test searching
            lot.SearchVehicle("bh234");

            // Test removal
            lot.RemoveVehicle(spot1);
        }
    }
}
