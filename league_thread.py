from threading import Thread
from urllib3.exceptions import InsecureRequestWarning
import requests
import time
from queue import Queue

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
        last_request_was_ok = False
        name = None
        last_event = -1
        while True:
            try:
                r = requests.get(url=URL_events, verify=False)
                data = r.json()
                if name is None:
                    r = requests.get(url=URL_name, verify=False)
                    name = r.json()
                last_request_was_ok = True
                print("LOL THREAD:", data)
                events = data["Events"]
                if last_event == -1:
                    last_event = events[-1]["EventID"]
                else:
                    print("LENS:", len(events), last_event)
                    if len(events) > last_event+1:
                        for i in range(last_event+1, len(events)):
                            print("\n\n\n\n")
                            last_event = i
                            if events[i]["KillerName"] == name or name in events[i]["Assisters"]:
                                self.queue.put(events[i]["EventName"])
                time.sleep(5)
            except requests.exceptions.ConnectionError:
                time.sleep(5)
                last_request_was_ok = False
                name = None
                last_event = -1
            except KeyError as e:
                print("ERROR:", e)
                time.sleep(2)
            except IndexError as e:
                print("ERROR", e)
                time.sleep(2)
