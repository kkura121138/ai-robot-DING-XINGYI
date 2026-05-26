## 四足机器人入门 <br>
- Trot步态实现 <br>
1. 修复了机器狗方向错误（最重要） <br>
原始代码： <br>
start_orientation = p.getQuaternionFromEuler(
    [math.pi / 2, 0, math.pi / 2]
) <br>
修改后： <br>
start_orientation = p.getQuaternionFromEuler(
    [0, 0, 0]
) <br>
作用： <br>
修复机器人横着加载的问题
修复一启动就翻倒
修复身体方向错误
修复无法正常前进 <br>
2. 修改了关节编号 <br>
原始代码： <br>
self.leg_joints = {
    'LF': [0,1,2],
    'RF': [3,4,5],
    'LH': [6,7,8],
    'RH': [9,10,11]
} <br>
修改后： <br>
self.legs = {
    "FL": [0,1,2],
    "FR": [4,5,6],
    "RL": [8,9,10],
    "RR": [12,13,14]
} <br>
作用： <br>
修复控制错误关节
修复腿乱动
修复某些腿不受控制
因为 Laikago 的关节编号本来就不是连续的。 <br>
 
3. 增加了稳定站立姿态 <br>

新增： <br>

self.stand_pose = {
    "FL": [0.0, 0.67, -1.3],
    ...
} <br>

以及： <br>

controller.stand() <br>

作用： <br>

机器人先站稳
防止一启动摔倒
给行走做准备

原始代码没有“站立阶段”。 <br>

4. 力矩大幅增强 <br>

原始代码： <br>

force=20 <br>

修改后： <br>

force=500 <br>

作用： <br>

原来力太小撑不起身体
现在腿能真正支撑机器人

这是最关键修改之一。 <br>

5. 新增最大速度限制

新增： <br>

maxVelocity=5

作用：

防止关节瞬间抽搐
行走更加平滑
提高稳定性 <br>
6. 重写了步态算法

原始代码：

thigh = np.arctan2(x, target_height)
calf = -2 * thigh

修改后：

upper += -foot_forward * 0.8
lower += foot_forward * 1.2

作用：

不再使用错误简化逆运动学
改成更加稳定的步态控制
腿运动更加自然 <br>
7. 新增抬腿动作

新增：

upper -= foot_up * 0.5
lower += foot_up * 0.8

作用：

机器人真正抬腿
防止拖地
行走更自然 <br>
8. 新增对角步态（Trot） <br>

新增： <br>

phases = {
    "FL": 0,
    "RR": 0,
    "FR": math.pi,
    "RL": math.pi
} <br>

作用：

前左 + 后右同步
前右 + 后左同步
更符合真实四足机器人

原始代码虽然有相位，但实现不完整。 <br>

9. 新增摄像机控制

新增：

p.resetDebugVisualizerCamera(...)

作用：

自动对准机器人
更容易观察运动 <br>
10. 新增关节信息打印

新增：

print(i, info[1].decode("utf-8"))

作用：

调试方便
能查看真实关节编号 <br>
11. 修改了机器人高度

原始：

[0,0,0.5]

修改后：

[0,0,0.48]

后面又建议：

[0,0,0.55]

作用：

防止腿插地
提高稳定性 <br>
12. 新增 stand() 函数

新增：

def stand(self): <br>

作用： <br>

独立控制站立
结构更清晰
更容易后续扩展 <br>
13. 代码结构优化 <br>

原始代码： <br>

controller.step()

修改后： <br>

controller.stand()
controller.trot_gait()

作用： <br>

逻辑更清晰
更符合真实机器人控制流程 <br>
![这是效果图](2.png)