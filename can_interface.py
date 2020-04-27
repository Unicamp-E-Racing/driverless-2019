import can
import os
from constants import *
import time

if "CAR_SIMULATION" in RUN_FLAGS:
    can_channel = "vcan0"
else:
    can_channel = "can0"
    os.system("sudo ip link set up can0 type can bitrate 500000")
        
bus_filters = [{"can_id": CAN_MOTOR_RPM_ID, "can_mask": 0xfff, "extended": False},
                {"can_id": CAN_STEERING_ID, "can_mask": 0xfff, "extended": False}]
bus = can.interface.Bus(can_channel, bustype='socketcan', receive_own_messages=True)
bus.set_filters(bus_filters)

motor_rpm = 0
car_speed = 0
steering_sensor = 0



def createTargetMessage(angle):
        steering = angle
        pedal = 1000
        brake = 1000
        mission_finished  = 0
        ebs = 0

        # Format message values
        #steering += STEERING_OFFSET
        steering = steering
        if steering > 90:
            steering = 90
        if steering < -90:
            steering = -90
        steering +=128
        steering = int(steering)

        steer_hex = steering.to_bytes(1, "little")
        msg_data = [0, 0,
                    0, 0, 
                    0, 0,
                    0,steer_hex[0]]

        return can.Message(arbitration_id=CAN_DRIVERLESS_ID, data=msg_data, extended_id=False)


def receive():
    global motor_rpm, steering_sensor, car_speed, bus
    pass
    print_info = ""
    msg = bus.recv(0.5)
    if msg is None:
        print("ERROR: Not reciving CAN messages")
    elif msg.arbitration_id == CAN_MOTOR_RPM_ID:
        motor_rpm = int.from_bytes(msg.data[4:], "big")
        car_speed = motor_rpm * RPM_TO_MS

    # NEED FIX
    elif msg.arbitration_id == CAN_STEERING_ID:
        steer_data = int.from_bytes(msg.data[:2], "big")
        steering_sensor = steer_data * (360/ 65536)
        steering_sensor -= STEERING_OFFSET
        if steering_sensor >= 360-STEER_MAX+STEERING_OFFSET:
            steering_sensor = steering_sensor -360

    return motor_rpm,steering_sensor, print_info

def receive_thread():
    global motor_rpm, steering_sensor, car_speed
    while True:
        receive()

def run(angle):
    global motor_rpm, steering_sensor, car_speed
    can_msg = createTargetMessage(angle)
    bus.send(can_msg)


if __name__ == "__main__":
    angle = int(input("steer"))
    run(angle)
