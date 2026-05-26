import pybullet as p
import pybullet_data
import time
import math
import numpy as np


class QuadrupedController:
    def __init__(self, robot_id):
        self.robot_id = robot_id

        # Laikago 正确关节ID
        self.legs = {
            "FL": [0, 1, 2],
            "FR": [4, 5, 6],
            "RL": [8, 9, 10],
            "RR": [12, 13, 14]
        }

        # 默认站立姿态
        self.stand_pose = {
            "FL": [0.0, 0.67, -1.3],
            "FR": [0.0, 0.67, -1.3],
            "RL": [0.0, 0.67, -1.3],
            "RR": [0.0, 0.67, -1.3]
        }

        # 步态参数
        self.step_height = 0.15
        self.step_length = 0.25
        self.frequency = 1.2

    def set_leg_angles(self, leg_name, angles, force=500):
        joints = self.legs[leg_name]

        for joint_id, angle in zip(joints, angles):
            p.setJointMotorControl2(
                bodyIndex=self.robot_id,
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=angle,
                force=force,
                maxVelocity=5
            )

    def stand(self):
        """让机器人稳定站立"""
        for leg_name in self.legs:
            self.set_leg_angles(
                leg_name,
                self.stand_pose[leg_name]
            )

    def trot_gait(self, t):
        """Trot步态"""

        # 对角腿同步
        phases = {
            "FL": 0,
            "RR": 0,
            "FR": math.pi,
            "RL": math.pi
        }

        for leg_name in self.legs:

            phase = phases[leg_name]

            gait_phase = (
                2 * math.pi * self.frequency * t + phase
            ) % (2 * math.pi)

            # 默认角度
            hip = 0.0
            upper = 0.67
            lower = -1.3

            # 摆动相
            if gait_phase < math.pi:

                progress = gait_phase / math.pi

                foot_up = (
                    self.step_height *
                    math.sin(math.pi * progress)
                )

                foot_forward = (
                    self.step_length *
                    (progress - 0.5)
                )

            # 支撑相
            else:

                progress = (
                    gait_phase - math.pi
                ) / math.pi

                foot_up = 0

                foot_forward = (
                    self.step_length *
                    (0.5 - progress)
                )

            # 转换为关节运动
            upper += -foot_forward * 0.8
            lower += foot_forward * 1.2

            # 抬腿
            upper -= foot_up * 0.5
            lower += foot_up * 0.8

            self.set_leg_angles(
                leg_name,
                [hip, upper, lower],
                force=500
            )


def main():

    # 连接GUI
    p.connect(p.GUI)

    # 设置搜索路径
    p.setAdditionalSearchPath(
        pybullet_data.getDataPath()
    )

    # 重力
    p.setGravity(0, 0, -9.8)

    # 仿真步长
    p.setTimeStep(1.0 / 240.0)

    # 地面
    p.loadURDF("plane.urdf")

    # 摄像机
    p.resetDebugVisualizerCamera(
        cameraDistance=2.0,
        cameraYaw=50,
        cameraPitch=-30,
        cameraTargetPosition=[0, 0, 0.3]
    )

    # 初始位置
    start_pos = [0, 0, 0.48]

    # 正确朝向
    start_orientation = p.getQuaternionFromEuler(
        [0, 0, 0]
    )

    # 加载机器人
    start_orientation = p.getQuaternionFromEuler([math.pi / 2, 0, math.pi / 2]) # Keeps the robot facing forward
    robotId = p.loadURDF("laikago/laikago_toes.urdf", [0, 0, 0.5],start_orientation)
    

    # 打印关节信息
    print("====== Joint Info ======")

    for i in range(p.getNumJoints(robotId)):
        info = p.getJointInfo(robotId, i)
        print(i, info[1].decode("utf-8"))

    # 创建控制器
    controller = QuadrupedController(robotId)

    # 先站立稳定
    print("机器人正在站立...")

    for _ in range(500):

        controller.stand()

        p.stepSimulation()

        time.sleep(1.0 / 240.0)

    print("开始行走...")

    # 主循环
    t = 0

    try:

        while True:

            controller.trot_gait(t)

            p.stepSimulation()

            time.sleep(1.0 / 240.0)

            t += 1.0 / 240.0

    except KeyboardInterrupt:

        print("仿真结束")

    p.disconnect()


if __name__ == "__main__":
    main()