import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import asyncio
from websockets.server import serve
import json
import time 


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)
        asyncio.run(self.timer_callback())
        self.i = 0

    async def echo(self,websocket):
        i=0
        sj=0.0
        stj=0.0
        async for message in websocket:
                print(message)
                y=json.loads(message)
                hello_str = JointState()
                hello_str.header = Header()
                hello_str.header.stamp.sec = i
                hello_str.header.stamp.nanosec=i
                hello_str.header.frame_id=str(i)
                print(y["drive"])
                print(y["steer"])
                sj+=((((y["drive"]+1)/(2)))*(0.9))-0.45
                hello_str.name = ['shaft_joint', 'steer_joint']
                stj=((((y["steer"]+1)/(2)))*(0.4))-0.2
                print(y["steer"])
                hello_str.position = [sj,stj]
                hello_str.velocity = []
                hello_str.effort = []                
                self.publisher_.publish(hello_str)
                self.get_logger().info('Publishing: "%s"' % hello_str.position)
                i += 1

    async def timer_callback(self):
        async with serve(self.echo, "0.0.0.0", 8765):
            await asyncio.Future()


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()