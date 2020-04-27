import os
import time
import can
import math
import numpy as np
from constants import *
bus_filters = [{"can_id": CAN_DRIVERLESS_ID, "can_mask": 0xfff, "extended": False}]
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000, receive_own_messages=False)
bus.set_filters(bus_filters)


steering_target = 0
steering_real = 0
motor_rpm = MOTOR_RPM
car_real_pos = [-9,-5,math.radians(90),0]
#car_real_pos = [0,0,math.radians(0),0]


t0_update = time.time()
def update_car():
    global car_real_pos
    global t0_update
    global motor_rpm
    global steering_real
    x,y,theta,steer = car_real_pos
    delta_t = time.time() - t0_update
    speed = (RPM_TO_MS*motor_rpm)
    x += speed * math.cos(theta) * delta_t
    y += speed * math.sin(theta) * delta_t
    theta += speed/CAR_LENGHT * math.tan(-steer) * delta_t
    car_real_pos[0] = float(x + np.random.normal(0,SIMULATION_POS_ERROR,1))
    car_real_pos[1] = float(y + np.random.normal(0,SIMULATION_POS_ERROR,1))
    car_real_pos[2] = float(theta + np.random.normal(0,SIMULATION_THETA_ERROR,1))
    t0_update = time.time()



def send_can(motor_rpm, real_steer):
    rpm_hex = motor_rpm.to_bytes(4, 'big')
    msg_VCU_Info_1_freq = 100
    msg_VCU_Info_1 = can.Message(arbitration_id=CAN_MOTOR_RPM_ID,
                      data=[0, 0, 0, 0, rpm_hex[0], rpm_hex[1], rpm_hex[2], rpm_hex[3]],
                      is_extended_id=False)
    # TODO FIX THIS
    # simulate steer sensor
    steer_sensor = min(STEER_MAX, real_steer)
    steer_sensor = max(STEER_MIN, real_steer)
    steer_sensor -= STEERING_OFFSET
    if steer_sensor < -STEERING_OFFSET:
        steer_sensor = 360 + steer_sensor

    steer_sensor += STEERING_OFFSET

    steer_sensor *= (65535/360)
    steer_hex = int(steer_sensor).to_bytes(2, 'big')
    msg_steering_freq = 100
    msg_steering = can.Message(arbitration_id=CAN_STEERING_ID,
                      data=[steer_hex[0], steer_hex[1], 0, 0, 0, 0, 0, 0],
                      is_extended_id=False)


    bus.send(msg_VCU_Info_1)
    bus.send(msg_steering)

def receive_can():
    global steering_target
    msg = bus.recv(0.1)
    if msg is not None:
        if msg.arbitration_id == CAN_DRIVERLESS_ID:
            steer_data = int(msg.data[7])
            steering_target  = steer_data - 128



t0_control = time.time()
def control_steer():
    global t0_control
    global steering_real
    global steering_target
    global car_real_pos
    delta_time =time.time() - t0_control 
    t0_control = time.time()
    err = steering_real - steering_target

    if abs(err) > STEER_DEAD_ZONE:
        if err > 0:
            steering_real -= STEER_SPEED * delta_time
        else:
            steering_real += STEER_SPEED * delta_time

    steering_real = max(steering_real, STEER_MIN)
    steering_real = min(steering_real, STEER_MAX)
    car_real_pos[3] = STEER_TO_WHEEL *  steering_real
    car_real_pos[3] = min(car_real_pos[3], STEER_WHEEL_MAX)
    car_real_pos[3] = max(car_real_pos[3], STEER_WHEEL_MIN)
    car_real_pos[3] = math.radians(car_real_pos[3])


def run_forever():
    global car_real_pos
    while(True):
        send_can(motor_rpm, steering_real)
        receive_can()
        control_steer()
        update_car()

if __name__ == "__main__":
    print("Running tests")
    run_forever()
    print("Tests ended")
