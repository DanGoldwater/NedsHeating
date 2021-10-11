from weather import *
import numpy as np
from U_values import *


class room(object):
    def __init__(
        self,
        wall1,
        wall2,
        height,
        windows_area,
        windows_U,
        floor_u,
        vent=0,
        ceiling=0,
        doors_area=0,
        skylight=0,
        ceiling_u=0,
        roof_u=0,
        chimney=0,
        ext_list=[],
        name="",
        ach=ACH_House,
        roof_proportion=1
    ):
        self.wall1 = wall1
        self.wall2 = wall2
        self.height = height
        self.windows_area = windows_area
        self.windows_U = windows_U
        self.floor_U = floor_u
        self.vent = vent
        self.ceiling = ceiling
        self.ceiling_u = ceiling_u
        self.skylight = skylight
        self.doors_area = doors_area
        self.roof_u = roof_u
        self.ext_list = ext_list
        self.name = name
        self.chimney = chimney
        self.ach=ach
        self.roof_proportion = roof_proportion
        

    def floor_area(self):
        return self.wall1['length'] * self.wall2['length']
        

    def volume(self):
        return self.floor_area() * self.height 
    
    
    def wall_heat(self):
        loss = 0
        for wall in self.ext_list:
            wall_dict = getattr(self, wall)
            loss += self.height * wall_dict['length'] * wall_dict['U']
        loss += (self.windows_area + self.doors_area) * self.windows_U
        return loss
        
    
    def air_heat(self):
        return (self.volume() * self.ach / 3) + self.chimney + self.vent
    
    def floor_heat(self):
        return self.floor_area() * self.floor_U 
    
    def roof_heat(self):
        return self.floor_area() * self.roof_u * self.roof_proportion + (self.skylight * SkyLights_U)
    

    def total_heat(self):
        total_heat = (
            self.wall_heat() +
            self.floor_heat() +
            self.roof_heat() +
            self.air_heat()
        )
        return total_heat
    
    def print_details(self):
        print(f'Room: {self.name}')
        print(f'Exterior wall area of {self.ext_wall_area():.2f}')
        print(f'Heat lost through walls {self.wall_heat():.2f}')
        print(f'Heat lost through roof {self.roof_heat():.2f}')
        print(f'Heat lost through floor {self.floor_heat():.2f}')
        print(f'Heat lost through air change {self.air_heat():.2f}')
        print(f'Total heat lost {self.total_heat():.2f}\n\n')

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
    "wall1" : {'length': 4.9,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 4.6,
               'U': Wall_U_Uninsulated},
    "height": 3.1,
    "windows_area": 5,
    "windows_U": Windows_U_Uninsulated,
    "floor_u": Floor_U_Insulated,
    "vent": 0,
    "ext_list": ["wall1", "wall2"],
    "chimney": Chimney_value,
    "roof_u" : Roof_U_Interior
}


LivingRoomArgs = {
    "name": "House Living Room",
    "wall1" : {'length': 4.8,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 4.5,
               'U': Wall_U_Uninsulated},
    "height": 3.1,
    "windows_area": 4,
    "windows_U": Windows_U_Uninsulated,
    "floor_u": Floor_U_Insulated,
    "vent": 0,
    "ext_list": ["wall1", "wall2"],
    "roof_u" : Roof_U_Interior,
    "chimney": Chimney_value
}

JenArgs = {
    "name": "Jen",
    "wall1" : {'length': 4.7,
               'U': Wall_U_Insulated_1},
    "wall2" : {'length': 4.8,
               'U': Wall_U_Insulated_1},
    "height": 3.1,
    "windows_area": 5,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Insulated,
    "roof_u" : Roof_U_Interior,
    "vent": 0,
    "ext_list": ["wall1", "wall2"],
}

BryonyArgs = {
    "name": "Bryony",
    "wall1" : {'length': 4.8,
               'U': Wall_U_Insulated_1},
    "wall2" : {'length': 4.8,
               'U': Wall_U_Insulated_1},
    "height": 2.85,
    "windows_area": 3,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Interior,
    "vent": 0,
    "roof_proportion": .7,
    "roof_u": Roof_U_SLB,
    "ext_list": ["wall1"],
    "chimney": Chimney_value
}

SophieArgs = {
    "name": "Sophie",
    "wall1" : {'length': 4,
               'U': Wall_U_Sophie_Plain_Wall},
    "wall2" : {'length': 4,
               'U': Wall_U_Sophie_Window_Wall},
    "height": 2.3,
    "windows_area": 3,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Interior,
    "roof_proportion": 2/5,
    "roof_u": Roof_U_Insulated,
    "vent": 0,
    "ext_list": ["wall1", "wall2"],
    'roof_proportion': .8,
    'roof_u': Roof_U_Sophie
}


SarahLoydArgs = {
    "name": "Sarah Lloyd",
    "wall1" : {'length': 4.8,
               'U': Wall_U_Insulated_1},
    "wall2" : {'length': 4.5,
               'U': Wall_U_Insulated_1},
    "height": 2.85,
    "windows_area": 3,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Interior,
    "roof_proportion": .7,
    "roof_u": Roof_U_SLB,
    "vent": 0,
    "ext_list": ["wall1"],
}


TimArgs = {

    "name": "Tim",
    "wall1" : {'length': 4.4,
               'U': Wall_U_Topfloor_Void},
    "wall2" : {'length': 3.6,
               'U': Wall_U_Topfloor_end},
    "height": 2.85,
    "windows_area": 1,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Interior,
    "roof_u": Roof_U_Tim_Nels,
    "vent": 0,
    "ext_list": ["wall1", "wall2", "wall1"],
}


NelsArgs = {
    "name": "Nels",
    "wall1" : {'length': 4.4,
               'U': Wall_U_Topfloor_Void},
    "wall2" : {'length': 3.6,
               'U': Wall_U_Topfloor_end},
    "height": 2.2,
    "windows_area": 1,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Interior,
    "roof_u": Roof_U_Tim_Nels,
    "vent": 0,
    "ext_list": ["wall1", "wall2", "wall1"],
}


USKArgs = {
    "name": "Upstairs Kitchen",
    "wall1" : {'length': 3.2,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 4.0,
               'U': Wall_U_Uninsulated},
    "height": 2.85,
    "windows_area": 1,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Interior,
    "vent": VentKitchen,
    "ext_list": ["wall1", "wall2"],
    "roof_u" : Roof_U_Uninsulated,
    'roof_proportion' : 1
}


DSKArgs = {
    "name": "Downstairs Kitchen",
    "wall1" : {'length': 4.2,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 3.1,
               'U': Wall_U_Uninsulated},
    "height": 3.1,
    "windows_area": 1,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Uninsulated,
    "vent": VentKitchen,
    "ext_list": ["wall1", "wall2"],
}


DSHallArgs = {
    "name": "Downstairs Hall",
    "wall1" : {'length': 7.6,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 1.3,
               'U': Wall_U_Uninsulated},
    "height": 3.1,
    "windows_area": 0,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Insulated,
    "vent": 0,
    "ext_list": ["wall2", "wall2"],
}


DSHallLobbyArgs = {
    "name": "Downstairs Lobby",
    "wall1" : {'length': 2.3,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 2,
               'U': Wall_U_Uninsulated},
    "height": 2.5,
    "windows_area": 0,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Insulated,
    "vent": 0,
    "ext_list": ["wall2", "wall2", "wall1"],
}

USHallArgs = {
    "name": "Upstairs Hall",
    "wall1" : {'length': 2.1,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 9.8,
               'U': Wall_U_Uninsulated},
    "height": 2,
    "windows_area": 2,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Interior,
    "vent": 0,
    "ext_list": ["wall1", "wall1"],
}

LandingToiletArgs = {
    "name": "Landing Toilet",
    "wall1" : {'length': 2.1,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 1.3,
               'U': Wall_U_Uninsulated},
    "height": 3.1,
    "windows_area": 2,
    "windows_U": Windows_U_Insulated,
    "floor_u": Floor_U_Interior,
    "roof_u": Roof_U_Insulated,
    "vent": 0,
    "ext_list": ["wall1", "wall1"],
}

DSBArgs = {
    "name": "Downstairs Bathroom",
    "wall1" : {'length': 4.1,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 1.5,
               'U': Wall_U_Uninsulated},
    "height": 3,
    "windows_area": 0.5,
    "windows_U": Windows_U_Uninsulated,
    "floor_u": Floor_U_Insulated,
    "vent": VentBathroom,
    "ext_list": ["wall2"],
}


USBArgs = {
    "name": "Upstairs Bathroom",
    "wall1" : {'length': 4.3,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 1.5,
               'U': Wall_U_Uninsulated},
    "height": 3,
    "windows_area": 0.5,
    "windows_U": Windows_U_Uninsulated,
    "floor_u": Floor_U_Insulated,
    "vent": VentBathroom,
    "ext_list": ["wall2"],
}
TopLanding_Plus_BroomArgs = {
    "name": "Top Landing and Broom Cupboard",
    "wall1" : {'length': 7,
               'U': Wall_U_Uninsulated},
    "wall2" : {'length': 2.1,
               'U': Wall_U_Uninsulated},
    "height": 3,
    "windows_area": 0.5,
    "windows_U": Windows_U_Uninsulated,
    "floor_u": Floor_U_Insulated,
    "vent": VentBathroom,
    "ext_list": ["wall2", "wall2"],
    "roof_proportion" : 1,
    "roof_u" : TopLanddingRoofU
}







#############################################################
##### ARGUMENTS FOR FLAT ##################



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
    "ext_list": ["wall2", "wall2"],
    "roof_u": Roof_U_Insulated,
    "ach":ACH_Flat,
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
    "vent": VentBathroom,
    "roof_u": Roof_U_Insulated,
    "ext_list": ["wall1", "wall2"],
    "ach":ACH_Flat,
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
    "vent": VentBathroom,
    "ext_list": ["wall2", "wall2", "wall1"],
    "roof_u": Roof_U_Insulated,
    "ach":ACH_Flat,
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
    "vent": VentBathroom,
    "roof_u": Roof_U_Insulated,
    "ext_list": ["wall1", "wall2"],
    "ach":ACH_Flat,
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
LandingToilet = room(**LandingToiletArgs)
DSHallLobby = room(**DSHallLobbyArgs)
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
    LandingToilet,
    DSHallLobby
]

def finished_args(list_of_args):
    finished_args_list = []
    for args in list_of_args:
        args_finished = args.copy()
        if 'roof_u' in args_finished.keys():
            if args_finished['roof_u'] > Roof_U_Tim_Nels:
                args_finished['roof_u'] = Roof_U_Tim_Nels
        if 'windows_u' in args_finished.keys():
            if args_finished['windows_u'] > Windows_U_Insulated:
                args_finished['roof_u'] = Windows_U_Insulated
        if 'chimney' in args_finished.keys():
            args_finished['chimney'] = 0
        if args_finished['floor_u'] > Floor_U_Insulated:
            args_finished['floor_u'] = Floor_U_Insulated
        if args_finished['wall1']['U'] > Wall_U_Insulated_1:
            args_finished['wall1']['U'] = Wall_U_Insulated_1
        if args_finished['wall2']['U'] > Wall_U_Insulated_1:
            args_finished['wall2']['U'] = Wall_U_Insulated_1
        args_finished['ach'] = ACH_DraughtProof
        finished_args_list += [args_finished]
    return finished_args_list


Dan_Finished = room(**DanArgs)
Jen_Finished = room(**JenArgs)
Bryony_Finished = room(**BryonyArgs)
Sophie_Finished = room(**SophieArgs)
SarahL_Finished = room(**SarahLoydArgs)
Tim_Finished = room(**TimArgs)
Nels_Finished = room(**NelsArgs)
DSK_Finished = room(**DSKArgs)
USK_Finished = room(**USKArgs)
LivingRoom_Finished = room(**LivingRoomArgs)
DSHall_Finished = room(**DSHallArgs)
USHAll_Finished = room(**USHallArgs)
DSB_Finished = room(**DSBArgs)
LandingToilet_Finished = room(**LandingToiletArgs)
DSHallLobby_Finished = room(**DSHallLobbyArgs)

house_args_list = [DanArgs, JenArgs, BryonyArgs, SophieArgs, SarahLoydArgs, TimArgs, NelsArgs, DSKArgs, USKArgs, LivingRoomArgs, DSHallArgs, USHallArgs, DSBArgs, LandingToiletArgs, DSHallLobbyArgs]
HouseHeat = sum([h.total_heat() for h in HouseList])

Finished_House_Args = finished_args(house_args_list)
Finished_House_List = [room(**a) for a in Finished_House_Args]
HouseHeatFinished = sum([h.total_heat() for h in Finished_House_List])



# FlatMainRoom = room(**FlatMainRoomArgs)
# FlatBthrm = room(**FlatBthrmArgs)
# FlatSmlBdrm = room(**FlatSmlBdrmArgs)
# FlatLRGBdrm = room(**FlatLrgBdrmArgs)


# FlatList = [FlatLRGBdrm, FlatBthrm, FlatMainRoom, FlatSmlBdrm]

# TotalList = FlatList + HouseList

# FlatHeat = heat_for_roomlist(FlatList)

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
