import numpy as np
from app.utils import BUFFER_EMPTY_THRESHOLD
from app.utils import BUFFER_THRESHOLD


class Stream:

    def __init__(self, sensor=None, kinect=None):
        self.sensor = sensor
        self.kinect = kinect
        self.sensor_ignore = False
        self.buffer_ignore = False
        self.sensor_buffer_empty_count = 0
        self.video_buffer_empty_count = 0

    def get_data(self):
        data = list()
        for index, sensor in enumerate(self.sensor):
            msg_len = len(sensor.msg_buffer)
            if msg_len is not 0:
                msg = sensor.msg_buffer[0]
                if msg_len >= 2:
                    sensor.msg_buffer.pop(0)
                msg = msg.replace("[", "")
                msg = msg.replace("]", "")
                msg = msg.split(",")
                msg = [float(i) for i in msg]
                data.append(msg)
                if msg_len > BUFFER_THRESHOLD:
                    if self.sensor_ignore:
                        pass
                    else:
                        print(f"Overflowe at {sensor.info}: len {msg_len}")
                        raise BufferError
            else:
                print(f"Sensor-{index+1} data buffer is currently empty")
                self.sensor_buffer_empty_count += 1
                if self.sensor_buffer_empty_count > BUFFER_EMPTY_THRESHOLD:
                    print(f"Not connected to {sensor.info}")
                    raise BufferError
        return data

    def get_video_stream(self):
        video = list()
        depth = list()
        for index, kinect in enumerate(self.kinect):
            rgb_len = len(kinect.rgb_buffer)
            dp_len = len(kinect.depth_buffer)
            a_dp_len = len(kinect.azure_rgb_buffer)
            a_rgb_len = len(kinect.azure_depth_buffer)
            if rgb_len > 2 and dp_len > 0 and a_dp_len > 1 and a_rgb_len > 0:
                dp = kinect.depth_buffer.pop(0)
                vd = kinect.rgb_buffer.pop(0)
                a_vd = kinect.azure_rgb_buffer.pop(0)
                a_dp = kinect.azure_depth_buffer.pop(0)

                video.append(vd)
                depth.append(dp)
                video.append(a_vd)
                depth.append(a_dp)
                if rgb_len > BUFFER_THRESHOLD or dp_len > BUFFER_THRESHOLD:
                    if self.buffer_ignore:
                        pass
                    else:
                        print("Kinect data overflow error on", index)
                        print(f"rgb: {rgb_len}, depth: {dp_len}")
                        print(f'a_rgb: {a_rgb_len}, a_depth: {a_dp_len}')
                        raise BufferError
            else:
                print(f"Kinect-{index+1} data buffer is currently empty")
                self.video_buffer_empty_count += 1
                if self.video_buffer_empty_count > BUFFER_EMPTY_THRESHOLD:
                    print(f"Not connected to {kinect.id_name}:{kinect.type}")
                    raise BufferError
                return False, False
        return video, depth

    def set_error(self, s_ignore, b_ignore):
        self.sensor_ignore = s_ignore
        self.buffer_ignore = b_ignore
