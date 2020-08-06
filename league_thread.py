from threading import Thread
from urllib3.exceptions import InsecureRequestWarning
import requests
import time
from queue import Queue
from patterns import Wave, Stop

# api-endpoint
URL_name = "https://127.0.0.1:2999/liveclientdata/activeplayername"
URL_events = "https://127.0.0.1:2999/liveclientdata/eventdata"

# sending get request and saving the response as response object
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class League_Thread(Thread):
    def __init__(self, queue: Queue):
        self.queue = queue
        super().__init__()
    
    def run(self):
        name = None
        last_event = -1
        last_time = None
        duration = 15
        intensity = 35
        while True:
            try:
                r = requests.get(url=URL_events, verify=False)
                data = r.json()
                if name is None:
                    r = requests.get(url=URL_name, verify=False)
                    name = r.json()
                #print("LOL THREAD:", data)
                events = data["Events"]
                if last_event == -1:
                    last_event = events[-1]["EventID"]
                    last_time = time.time()
                    duration = 15
                    intensity = 35
                else:
                    #print("LENS:", len(events), last_event)
                    if len(events) > last_event+1:
                        for i in range(last_event+1, len(events)):
                            #print("\n\n\n\n")
                            last_event = i
                            if ("KillerName" in events[i] and events[i]["KillerName"] == name
                                    or "Assisters" in events[i] and name in events[i]["Assisters"]):
                                if "VictimName" in events[i] and events[i]["VictimName"] == name:
                                    self.queue.put(Stop())
                                    duration = 15
                                if events[i]["EventName"] != "Multikill":
                                    if time.time() - last_time > 15:
                                        intensity = 35
                                    elif intensity < 80:
                                        intensity += 15
                                    duration += 5
                                    if events[i]["EventName"] == "GameEnd":
                                        if events[i]["Result"] == "Win":
                                            self.queue.put(Wave(60, 75))
                                    self.queue.put(Wave(duration, intensity))
                time.sleep(0.25)
            except requests.exceptions.ConnectionError:
                time.sleep(5)
                name = None
                last_event = -1
            except KeyError as e:
                #print("ERROR Key:", e)
                time.sleep(0.25)
            except IndexError as e:
                #print("ERROR Index:", e)
                time.sleep(0.25)
