import cv2

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from pyorbbecsdk import Config
from pyorbbecsdk import OBError
from pyorbbecsdk import OBSensorType, OBFormat
from pyorbbecsdk import Pipeline, FrameSet
from pyorbbecsdk import VideoStreamProfile
from .utils import frame_to_bgr_image # ros2节点引用同目录python文件需要在前面加"."

ESC_KEY = 27


class CameraNode(Node):
    def __init__(self):
        super().__init__("camera_node")
        self.publisher_ = self.create_publisher(Image, "camera/image_raw", 10)
        self.timer = self.create_timer(0.1, self.publish_image)  # 每0.1秒发布一次图像

        config = Config()
        self.pipeline = Pipeline()
        try:
            profile_list = self.pipeline.get_stream_profile_list(
                OBSensorType.COLOR_SENSOR
            )
            try:
                color_profile: VideoStreamProfile = (
                    profile_list.get_video_stream_profile(640, 0, OBFormat.RGB, 30)
                )
            except OBError as e:
                print(e)
                color_profile = profile_list.get_default_video_stream_profile()
                print("color profile: ", color_profile)
            config.enable_stream(color_profile)
        except Exception as e:
            self.get_logger().error(e)
            self.destroy_node()
        self.pipeline.start(config)

        self.bridge = CvBridge()

    def publish_image(self):
        frames: FrameSet = self.pipeline.wait_for_frames(100)
        if frames is None:
            return
        color_frame = frames.get_color_frame()
        if color_frame is None:
            return
        # covert to RGB format
        color_image = frame_to_bgr_image(color_frame)
        if color_image is None:
            self.get_logger().error("failed to convert frame to image")
            return

        # 转换图像为ROS 2消息格式并发布
        image_msg = self.bridge.cv2_to_imgmsg(color_image, encoding="bgr8")
        self.publisher_.publish(image_msg)
        self.get_logger().info("Published image")

    def destroy_node(self):
        self.pipeline.stop()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    camera_node = CameraNode()

    try:
        rclpy.spin(camera_node)
    except KeyboardInterrupt:
        camera_node.get_logger().info("Shutting down camera node")
    finally:
        camera_node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
