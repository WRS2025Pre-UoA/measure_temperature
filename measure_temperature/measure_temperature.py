import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from std_msgs.msg import Float64

from cv_bridge import CvBridge, CvBridgeError

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
import process

class MeasureTemperature(Node):

    def __init__(self):
        super().__init__('measure_temperature')
        self.average_publisher = self.create_publisher(Float64, '/average', 10)
        self.image_publisher = self.create_publisher(
            Image, '/average_image', 10)
        self.subscription = self.create_subscription(
            Image,
            '/temperature_image',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        try:
            # ROS2のsensor_msgs/Image型からOpenCVで処理適量にcv::Mat型へ変換する。
            cv_image = self.bridge.imgmsg_to_cv2(msg, "mono8")
        except CvBridgeError as e:
            print(e)
            return

        average_image, ave = process.calc_average_temperature(cv_image, 180)

        pub_msg = Float64()
        pub_msg.data = ave

        self.average_publisher.publish(pub_msg)

        try:
            ros_image = self.bridge.cv2_to_imgmsg(average_image, "mono8")
        except CvBridgeError as e:
            print(e)
            return

        self.image_publisher.publish(ros_image)


def main(args=None):
    rclpy.init(args=args)

    node = MeasureTemperature()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
