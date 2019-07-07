
# coding: utf-8

# In[62]:


# class Route():
    
#     def __init__(self,id,buses = [],points = []):
#         self.id = id
#         bs = []
#         for b in buses:
#             bs.append(Bus(b,self.id))
#         self.buses = dict(zip(buses, bs))
#         self.points = list(set(points))
#         self.count = len(self.buses)
       
    
#     def getId(self):
#         return self.id
        
#     def addBus(self,bus_id):
#         self.buses[bus_id] = Bus(bus_id,self.id)
#         self.count = len(self.buses)
        
     
#     def removeBus(self,bus_id):
#         del(self.buses[bus_id])
#         self.count = len(self.buses)
        
#     def getBuses(self):
#         return self.buses
    
#     def getPoints(self):
#         return self.points
        
        



class Bus():
    
    def __init__(self,id_bus,id_route,outcome ,weight, end_time):
        self.id = id_bus
        self.id_route= id_route
        if outcome is not None:

            self.outcome = outcome
        else:
            self.outcome = 0
        self.weight = weight
        #self.points = Route(route_id).getPoints()
        #self.points_count = dict((el,0) for el in self.points)
        #self.now_point = now_point
        self.end_time = end_time

    def change(self,id_route,outcome):
        self.id_route = id_route
        if outcome is None:
            self.outcome = 0
        else:
            self.outcome = outcome
        
    def getId(self):
        return self.id

    def getEndTime(self):
        return self.end_time
        
    def getPoints(self):
        return self.points
        
    def setNowCount(self,new_count):
        self.now_cokunt = new_count
    
    def setNowPoint(self,now_point_id):
        self.now_point = now_point_id
        
    def getNowPoint(self):
        return self.now_point
    
    def setPointCount(self,point_id,point_count):
        self.points_count[point_id] = point_count
    
    def getPointCount(self,point_id):
        return self.points_count[point_id] 
    


# In[55]:
from datetime import datetime
import random
import requests
import json
from time import sleep
#self,id,route_id,now_count = 0,weight, end_time
class Life():
    
    def __init__(self):
        self.buses = []
        buses = requests.get("http://10a7b29c.ngrok.io/bus/all").json()
        for i in buses:
            if False:
                end_time = datetime.strptime(i.get("next_time"),'%Y-%m-%d')
            else:
                end_time = None
            if i.get("outcome") is None:
                outcome = 0
            else:
                outcome = i.get("outcome")
            self.buses.append(Bus(id_bus = i.get("id_bus"),id_route = i.get("id_route"),outcome = outcome,weight = i.get("weight"),end_time =end_time))

            print("self",outcome)
    def addBus(self,i):
        self.buses.append(Bus(i.get("id_bus"),i.get("id_route"),i.get("outcome"),i.get("weight"),None))

    def removeBus(self,bus):
        self.buses.remove(bus)
            

    def run(self):
        print("run,len",len(self.buses))
        while(True):
            print("while")
            for bus in self.buses:

                if bus.outcome!=0:
                    bus_output = random.randint(0,bus.outcome)
                else:
                    bus_output = 0
                if bus.outcome + bus_output == bus.weight:
                    bus_input = 0
                else:
                    bus_input = random.randint(0, bus.weight -bus.outcome + bus_output)  

                print("post request ","\n\n")
                requests.post("http://10a7b29c.ngrok.io/transaction",json = {
                                                                "id_bus":bus.id,
                                                                "id_route":bus.id_route,
                                                                "input":bus_input,
                                                                "output":bus_output,
                    })
                data = json.dumps({
                                                                "id_bus":bus.id,
                                                                "id_route":bus.id_route,
                                                                "input":bus_input,
                                                                "output":bus_output,
                    })
                print(json.loads(data))
                
                #post
            print("get request")
            life = requests.get("http://10a7b29c.ngrok.io/bus/all").json()
            now_buses = self.buses
            match = 0
            new_life = []
            new_buses = []  
            new_life[:] =[d for d in life]
            new_buses[:] =[d for d in now_buses]
            for bus in life:
                for i in now_buses:
                    if bus.get('id_bus') == i.id:
                        i.change(id_route = bus.get("id_route"),outcome = bus.get("outcome"))
                        new_life[:] = [d for d in new_life if d.get('id_bus') != bus.get('id_bus')]
                        new_buses[:] =[d for d in new_buses if d.id != bus.get('id_bus')] 
                        # life.remove(bus)
                        # now_buses.remove(i)
                        # life[:] = [d for d in life if d.get('id_bus') != i.id]
                        match+=1
                        # now_buses.remove(i)

                        
                        break

            print("\nmatch",match,"\n\n")
            print("but to add",new_life)
            print("bus to del",new_buses)
            for i in new_life:
                self.addBus(i)

            for i in new_buses:
                self.removeBus(i)
            print("sleep")
            # sleep(1)
if __name__ == "__main__":

    life = Life()
    life.run()

            # for route in routes:
            #     print("ROUTE:{}".format(route.getId()))
            #     for bus in route.getBuses():
            #         bus = Bus(bus,route.getId())
            #         print("BUS:{}".format(bus.getId()))
            #         print("Now point: {}, change: {}, total: {}".format(bus.getId(),bus.getNowPoint(),bus.getPointCount(bus.getNowPoint())))
            
        
    
        
            

