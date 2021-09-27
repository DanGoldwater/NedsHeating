from weather import *
import numpy as np

Windows_U_Uninsulated = 3.4
Windows_U_Insulated = 1.1
Floor_U_Interior = 0
Floor_U_Insulated = 0.6
Wall_U_Insulated = 0.6
Wall_U_Uninsulated = 2.2
Roof_U_Insulated = 0.6
VentBathroom = 200
VentKitchen = 1
Floor_U_Flat = 0.21
SkyLights_U = 3
Window_U_Flat = 1.6
Ceiling_U_Flat_Main = 0.14
Ceiling_U_Flat_Bathroom = 0.25
Wall_U_Flat_Main = 0.29
Wall_U_Flat_Bathroom = 0.3


class room(object):
    def __init__(
        self,
        wall1,
        wall2,
        height,
        windows_area,
        windows_U,
        floor_u,
        ext_proportion,
        walls_u,
        vent=0,
        ceiling=0,
        doors_area=0,
        skylight=0,
        ceiling_u=0,
        roof_u=0,
        ext_list=[],
        name="",
    ):
        self.wall1 = wall1
        self.wall2 = wall2
        self.height = height
        self.windows_area = windows_area
        self.windows_U = windows_U
        self.floor_U = floor_u
        self.walls_u = walls_u
        self.ext_proportion = ext_proportion
        self.vent = vent
        self.ceiling = ceiling
        self.ceiling_u = ceiling_u
        self.skylight = skylight
        self.doors_area = doors_area
        self.roof_u = roof_u
        self.ext_list = ext_list
        self.name = name

    def ext_wall_area(self):
        area = 0
        if len(self.ext_list) == 0:
            return 0

        for wall in self.ext_list:
            area += getattr(self, wall) * self.height
        return area
        # return (self.wall1 + self.wall2) * (self.height * 2 * self.ext_proportion)

    def wall_heat(self):
        return self.ext_wall_area() * self.walls_u

    def total_heat(self):
        total_heat = (
            self.wall_heat()
            + (self.skylight * SkyLights_U)
            + ((self.windows_area + self.doors_area) * self.windows_U)
            + ((self.wall1 * self.wall2) * self.ceiling_u)
            + ((self.wall1 * self.wall2) * self.floor_U)
            + (self.roof_u * (self.wall1 * self.wall2))
            + self.vent
        )
        return total_heat

    def print_heat_needs(self):
        need = self.total_heat()
        print(f"{self.name} needs {need:.2f} J / (K*s)")


def heat_for_roomlist(room_list):
    tot = 0
    for r in room_list:
        tot += r.total_heat()
    return tot


DanArgs = {
    "name": "Dan",
    "wall1": 4.5,
    "wall2": 4.5,
    "height": 2.7,
    "windows_area": 5,
    "windows_U": Windows_U_Uninsulated,
    "walls_u": Wall_U_Uninsulated,
    "floor_u": Floor_U_Insulated,
    "ext_proportion": 1 / 2,
    "vent": 0,
    "ext_list": ["wall1", "wall2"],
}


LivingRoomArgs = {
    "name": "House Living Room",
    "wall1": 4.5,
    "wall2": 4.5,
    "height": 2.7,
    "windows_area": 4,
    "windows_U": Windows_U_Uninsulated,
    "walls_u": Wall_U_Uninsulated,
    "floor_u": Floor_U_Insulated,
    "ext_proportion": 1 / 2,
    "vent": 0,
    "ext_list": ["wall1", "wall2"],
}

JenArgs = {
    "name": "Jen",
    "wall1": 4.5,
    "wall2": 4.5,
    "height": 2.7,
    "windows_area": 5,
    "windows_U": Windows_U_Insulated,
    "walls_u": Wall_U_Insulated,
    "floor_u": Floor_U_Insulated,
    "ext_proportion": 1 / 2,
    "vent": 0,
    "ext_list": ["wall1", "wall2"],
}

BryonyArgs = {
    "name": "Bryony",
    "wall1": 4,
    "wall2": 4,
    "height": 2.3,
    "windows_area": 3,
    "windows_U": Windows_U_Insulated,
    "walls_u": Wall_U_Insulated,
    "floor_u": Floor_U_Interior,
    "ext_proportion": 1 / 2,
    "vent": 0,
    "ext_list": ["wall1"],
}

SophieArgs = {
    "name": "Sophie",
    "wall1": 4,
    "wall2": 4,
    "height": 2.3,
    "windows_area": 3,
    "windows_U": Windows_U_Insulated,
    "walls_u": Wall_U_Insulated,
    "floor_u": Floor_U_Interior,
    "ext_proportion": 1 / 2,
    "vent": 0,
    "ext_list": ["wall1", "wall2"],
}


SarahLoydArgs = {
    "name": "Sarah Lloyd",
    "wall1": 4,
    "wall2": 4,
    "height": 2.3,
    "windows_area": 3,
    "windows_U": Windows_U_Insulated,
    "walls_u": Wall_U_Insulated,
    "floor_u": Floor_U_Interior,
    "ext_proportion": 1 / 2,
    "vent": 0,
    "ext_list": ["wall1"],
}


TimArgs = {
    "name": "Tim",
    "wall1": 3.5,
    "wall2": 3,
    "height": 2,
    "windows_area": 1,
    "windows_U": Windows_U_Insulated,
    "walls_u": Wall_U_Insulated,
    "floor_u": Floor_U_Interior,
    "roof_u": Roof_U_Insulated,
    "ext_proportion": 3 / 2,
    "vent": 0,
    "ext_list": ["wall1", "wall2", "wall1"],
}


NelsArgs = {
    "name": "Nels",
    "wall1": 3.5,
    "wall2": 3,
    "height": 2,
    "windows_area": 1,
    "windows_U": Windows_U_Insulated,
    "walls_u": Wall_U_Insulated,
    "floor_u": Floor_U_Interior,
    "roof_u": Roof_U_Insulated,
    "ext_proportion": 3 / 2,
    "vent": 0,
    "ext_list": ["wall1", "wall2", "wall1"],
}


USKArgs = {
    "name": "Upstairs Kitchen",
    "wall1": 3,
    "wall2": 3,
    "height": 2.7,
    "windows_area": 1,
    "windows_U": Windows_U_Insulated,
    "walls_u": Wall_U_Insulated,
    "floor_u": Floor_U_Interior,
    "ext_proportion": 1 / 2,
    "vent": VentKitchen,
    "ext_list": ["wall1", "wall2"],
}


DSKArgs = {
    "name": "Downstairs Kitchen",
    "wall1": 3,
    "wall2": 3,
    "height": 2.7,
    "windows_area": 1,
    "windows_U": Windows_U_Insulated,
    "walls_u": Wall_U_Uninsulated,
    "floor_u": Floor_U_Insulated,
    "ext_proportion": 1 / 2,
    "vent": VentKitchen,
    "ext_list": ["wall1", "wall2"],
}


DSHallArgs = {
    "name": "Downstairs Hall",
    "wall1": 1.5,
    "wall2": 10,
    "height": 2,
    "windows_area": 0,
    "windows_U": Windows_U_Insulated,
    "walls_u": Wall_U_Insulated,
    "floor_u": Floor_U_Insulated,
    "ext_proportion": 1 / 5,
    "vent": 0,
    "ext_list": ["wall1", "wall2"],
}

USHallArgs = {
    "name": "Upstairs Hall",
    "wall1": 1.5,
    "wall2": 10,
    "height": 2,
    "windows_area": 2,
    "windows_U": Windows_U_Insulated,
    "walls_u": Wall_U_Insulated,
    "floor_u": Floor_U_Interior,
    "ext_proportion": 2 / 5,
    "vent": 0,
    "ext_list": ["wall1", "wall1"],
}

DSBArgs = {
    "name": "Downstairs Bathroom",
    "wall1": 1.5,
    "wall2": 3,
    "height": 2,
    "windows_area": 0.5,
    "windows_U": Windows_U_Uninsulated,
    "walls_u": Wall_U_Uninsulated,
    "floor_u": Floor_U_Insulated,
    "ext_proportion": 2 / 5,
    "vent": VentBathroom,
    "ext_list": ["wall1"],
}


USBArgs = {
    "name": "Upstairs Bathroom",
    "wall1": 1.5,
    "wall2": 3,
    "height": 2,
    "windows_area": 0.5,
    "windows_U": Windows_U_Uninsulated,
    "walls_u": Wall_U_Uninsulated,
    "floor_u": Floor_U_Insulated,
    "ext_proportion": 2 / 5,
    "vent": VentBathroom,
    "ext_list": ["wall1"],
}

FlatMainRoomArgs = {
    "name": "Flat Main Room",
    "wall1": 4.95,
    "wall2": 7.3,
    "height": 2.4,
    "windows_area": 0.5,
    "doors_area": 1 * 2.2 + 0.76 * 2.01,
    "skylight": 3 * 0.4 * 0.9,
    "windows_U": Window_U_Flat,
    "walls_u": Wall_U_Flat_Main,
    "floor_u": Floor_U_Flat,
    "ext_proportion": 4 / 5,
    "ext_list": ["wall2", "wall2"],
    "roof_u": Roof_U_Insulated,
}

FlatLrgBdrmArgs = {
    "name": "Flat Large Bedroom",
    "wall1": 2.9,
    "wall2": 3.2,
    "height": 2.4,
    "windows_area": 1.04 * 1.42,
    "windows_U": Window_U_Flat,
    "walls_u": Wall_U_Flat_Main,
    "floor_u": Floor_U_Flat,
    "ext_proportion": 4 / 5,
    "vent": VentBathroom,
    "roof_u": Roof_U_Insulated,
    "ext_list": ["wall1", "wall2"],
}

FlatSmlBdrmArgs = {
    "name": "Flat Small Bedroom",
    "wall1": 2.05,
    "wall2": 3.2,
    "height": 2.4,
    "windows_area": 0.47 * 1.16,
    "windows_U": Window_U_Flat,
    "walls_u": Wall_U_Flat_Main,
    "floor_u": Floor_U_Flat,
    "ext_proportion": 4 / 5,
    "vent": VentBathroom,
    "ext_list": ["wall2", "wall2", "wall1"],
    "roof_u": Roof_U_Insulated,
}

FlatBthrmArgs = {
    "name": "Flat Bathroom",
    "wall1": 2.55,
    "wall2": 1.7,
    "height": 2.2,
    "windows_area": 0.68 * 0.9,
    "skylight": 0.38 * 0.76,
    "windows_U": Window_U_Flat,
    "walls_u": Wall_U_Flat_Bathroom,
    "floor_u": Floor_U_Flat,
    "ext_proportion": 4 / 5,
    "vent": VentBathroom,
    "roof_u": Roof_U_Insulated,
    "ext_list": ["wall1", "wall2"],
}

Dan = room(**DanArgs)
Jen = room(**JenArgs)
Bryony = room(**BryonyArgs)
Sophie = room(**SophieArgs)
SarahL = room(**SarahLoydArgs)
Tim = room(**TimArgs)
Nels = room(**NelsArgs)
DSK = room(**DSKArgs)
USK = room(**USKArgs)
LivingRoom = room(**LivingRoomArgs)
DSHall = room(**DSHallArgs)
USHAll = room(**USHallArgs)
DSB = room(**DSBArgs)
FlatMainRoom = room(**FlatMainRoomArgs)
FlatBthrm = room(**FlatBthrmArgs)
FlatSmlBdrm = room(**FlatSmlBdrmArgs)
FlatLRGBdrm = room(**FlatLrgBdrmArgs)


FlatList = [FlatLRGBdrm, FlatBthrm, FlatMainRoom, FlatSmlBdrm]
HouseList = [
    Dan,
    Jen,
    Bryony,
    Sophie,
    SarahL,
    Tim,
    Nels,
    DSK,
    USK,
    LivingRoom,
    DSHall,
    USHAll,
    DSB,
]
TotalList = FlatList + HouseList

HouseHeat = heat_for_roomlist(HouseList)
FlatHeat = heat_for_roomlist(FlatList)

Desired_Temp = 18
Threshold_Temp = 18


def yearly_heating_needs(year, room_list):
    heat = heat_for_roomlist(room_list)
    years_temps = get_year_avg_list(year)
    diff_list = [Desired_Temp - t for t in years_temps if t <= Threshold_Temp]
    # print(diff_list)
    year_diff_sum = sum(diff_list)
    return year_diff_sum * heat * 24 * 3600


def yearly_cost(year, roomlist, price):
    heat_need = yearly_heating_needs(year, roomlist)
    heat_need_in_kwh = heat_need / (60 * 60 * 1000)
    cost = price * heat_need_in_kwh
    return cost


Price = 0.18
# house_2018_cost = yearly_cost(2018, HouseList, Price)
# flat_2018_cost = yearly_cost(2018, FlatList, Price)
# print(f'House need is {heat_for_roomlist(HouseList)}')
# print(f'Flat need is {heat_for_roomlist(FlatList)}')
# print(f'House need is {heat_for_roomlist(HouseList)}')

# print(f'House cost for 2018 is {house_2018_cost}, or {house_2018_cost / 120} each per month')
# print(f'flat cost for 2018 is {flat_2018_cost}')

# print(FlatMainRoom.total_heat())
# print(Dan.ext_wall_area()*Dan.walls_u)
