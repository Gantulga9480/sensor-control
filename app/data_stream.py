import paho.mqtt.client as mqtt
import numpy as np


class Stream:

    def __init__(self, clients=None, ignore=False):
        self.clients = clients
        self.ignore = ignore

    def get_data(self):
        data = list()
        for index, client in enumerate(self.clients):
            if client.msg is not None:
                try:
                    msg = client.msg.replace("[", "")
                    msg = msg.replace("]", "")
                    msg = msg.split(",")
                    msg = [float(i) for i in msg]
                    data.append(msg)
                except:
                    pass
            else:
                if not self.ignore:
                    print("Please check sensor", index+1,)
                    raise Exception
                else:
                    pass
        return data