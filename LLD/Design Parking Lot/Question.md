Design a Parking Lot - Single Thread

Write code for low level design of a parking lot with multiple floors.
The parking lot has two kinds of parking spaces: type = 2, for 2 wheeler vehicles and type = 4, for 4 wheeler vehicles.

There are multiple floors in the parking lot. On each floor, vehicles are parked in parking spots arranged in rows and columns.
For simplicity, lets assume that each floor will have same number of rows and each row will have same number of columns.

You can solve this question in either Java or Python
Implement the below methods in Solution class:

init(Helper helper, int [][][] parking)
- helper has methods like, helper.print("") and helper.println("") which you can use for printing logs
- parking[i][j][k] : parking spot on i-th floor, j-th row and k-th column.
- each item in parking array is of the following type.
    4 : 4 wheeler parking spot,
    2 : 2 wheeler parking spot,
    0 : inactive spot, no vehicle can be parked here

park(int vehicleType, String vehicleNumber, String ticketId, int parkingStrategy)
returns spotId
- This function assigns an empty parking spot to vehicle and maps vehicleNumber and ticketId to the assigned spotId
- spotId is floor+"-"+row+"-"+column
e.g. parking[2][0][15] = parking spot at 2nd floor , 0th row and 15th column (0 based index),
its spotId will be: "2-0-15"
- parkingStrategy has two values, 0 and 1

parkingStrategy = 0
- Get the parking spot at lowest index i.e. lowest floor, row and column
e.g. park() is called with vehicleType 4 and we have free 4-wheeler spots at
parking[0][0][0], parking[0][0][1] and parking[1][0][2]
here we will return parking[0][0][0] because its index (floor, row, column) comes before the other two.

parkingStrategy = 1 :
- Get the floor with maximum number of free spots for the given vehicle type.
- If multiple floors have maximum free spots then choose the floor at lowest index from them.
e.g. park() is called with vehicleType 4 and floor[0] has 2 free 4 wheeler parking spots and
floor[1] and floor[3] both have 3 empty 4-wheeler parking spots.
here we will return the free 4-wheeler parking spot at lowest index from floor[1],
because apart from having highest number of free 4-wheeler spots it also comes before floor[3],
which also has 3 empty 4-wheeler parking spots.

removeVehicle(String spotId)
- Unparks or removes vehicle from parking spot.
- returns true if vehicle is removed
- returns false if vehicle not found or any other error


String searchVehicle(String query)
- searches the latest parking details of a vehicle parked in previous park() method calls.
- returns spotId e.g. 2-0-15 or empty string ""
- Query will be either vehicleNumber or ticketId.

int getFreeSpotsCount(int floor, int vehicleType)
- At any point of time get the number of free spots of vehicle type (2 or 4 wheeler).
- 0>= floor < parking.length (parking array from init() method).


Constraints:
- type = 2 for two-wheeler vehicle, type = 4 for 4 wheeler vehicle
- 1<=floors<=5, 1<=rows<=10,000, 1<=columns<=10,000, 1<=rows*columns<=10,000

Input Example
parking = [[
[4, 4, 2, 2],
[2, 4, 2, 0],
[0, 2, 2, 2],
[4, 4, 4, 0]]]
Above input has 1 floor.
It has 4 rows and 4 columns on floor 0.
Total 7 active 2-wheeler vehicles and
6 active 4-wheeler vehicles are there.

e.g park(2, "bh234", "tkt4534", 0)
will return spotId: "0-0-2"
i.e. parking spot from floor 0, row 0 and column 2 is assigned.

- search("bh234") or search("tkt4534")
at this point should return spotId = "0-0-2"
i.e. we can use vehicleNumber: "bh234" or ticketId: "tkt4534" to find the parking spot id where vehicle is parked.

- getFreeSpotsCount(0, 2)
will return 6.

- removeVehicle("0-0-2")
should unpark the parked vehicle and

- getFreeSpotsCount(0, 2)
after unparking, getFreeSpotsCount will now return 7.