import argparse
import datetime
import json
import os

import cv2
import numpy as np
import pyrealsense2 as rs


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default='', help="images save path")
    parser.add_argument("--mode", type=int, default=0, help="0(auto) or 1(manual)")
    parser.add_argument("--image_format", type=int, default=0, help="option: 0->jpg 1->png")
    parser.add_argument("--image_width", type=int, default=1280, help="width of the image, recommended 1280 or 640")
    parser.add_argument("--image_height", type=int, default=720, help="height of the image, recommended 720 or 480")
    parser.add_argument("--fps", type=int, default=30, help="frame rate of shooting")
    opt = parser.parse_args()
    return opt


# 该函数作用是获取对齐后的图像（rgb和深度图对齐）
def get_aligned_images(dirname, aligned_frames, depth_scale):
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
    intr = color_frame.profile.as_video_stream_profile().intrinsics
    camera_parameters = {'fx': intr.fx, 'fy': intr.fy,
                         'ppx': intr.ppx, 'ppy': intr.ppy,
                         'height': intr.height, 'width': intr.width,
                         'depth_scale': profile.get_device().first_depth_sensor().get_depth_scale()
                         }
    with open(os.path.join(dirname, 'intrinsics.json'), 'w') as fp:
        json.dump(camera_parameters, fp)
    color_image = np.asanyarray(color_frame.get_data(), dtype=np.uint8)
    depth_image = np.asanyarray(aligned_depth_frame.get_data(), dtype=np.float32)
    mi_d = np.min(depth_image[depth_image > 0])
    ma_d = np.max(depth_image)
    depth = (255 * (depth_image - mi_d) / (ma_d - mi_d + 1e-8)).astype(np.uint8)
    depth_image_color = cv2.applyColorMap(depth, cv2.COLORMAP_JET)
    depth_image = np.asanyarray(aligned_depth_frame.get_data(), dtype=np.float32) * depth_scale * 1000
    return color_image, depth_image, depth_image_color


if __name__ == "__main__":
    opt = parse_opt()
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, opt.image_width, opt.image_height, rs.format.z16, opt.fps)
    config.enable_stream(rs.stream.color, opt.image_width, opt.image_height, rs.format.bgr8, opt.fps)
    profile = pipeline.start(config)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    align_to = rs.stream.color
    align = rs.align(align_to)
    now = datetime.datetime.now()
    if os.path.exists(os.path.join(opt.path, 'images')):
        dirname = opt.path
        if len(os.listdir(os.path.join(opt.path, 'images'))):
            li = sorted(os.listdir(os.path.join(opt.path, 'images')), key=lambda x: eval(x.split('.')[0]))
            n = eval(li[-1].split('.')[0])
        else:
            n = 0
    elif opt.path == '':
        n = 0
        dirname = os.path.join(opt.path, now.strftime("%Y_%m_%d_%H_%M_%S"))
    else:
        n = 0
        dirname = os.path.join(opt.path)
    color_dir = os.path.join(dirname, 'images')
    depth_dir = os.path.join(dirname, 'DepthImages')
    depth_color_dir = os.path.join(dirname, 'DepthColorImages')
    depth_npy_dir = os.path.join(dirname, 'DepthNpy')
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        os.mkdir(color_dir)
        os.mkdir(depth_dir)
        os.mkdir(depth_color_dir)
        os.mkdir(depth_npy_dir)
    flag = 0
    image_formats = ['.jpg', '.png']
    while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        try:
            rgb, depth, depth_rgb = get_aligned_images(dirname, aligned_frames, depth_scale)
            cv2.imshow('RGB image', rgb)
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'):
                pipeline.stop()
                break
            elif opt.mode:
                if key == ord('s') or key == ord('S'):
                    n = n + 1
                    cv2.imwrite(os.path.join(color_dir, str(n) + image_formats[opt.image_format]), rgb)
                    cv2.imwrite(os.path.join(depth_dir, str(n) + image_formats[opt.image_format]), depth)
                    cv2.imwrite(os.path.join(depth_color_dir, str(n) + image_formats[opt.image_format]), depth_rgb)
                    np.save(os.path.join(depth_npy_dir, str(n)), depth)
                    print('{}{} is saved!'.format(n, image_formats[opt.image_format]))
            else:
                if key == ord('s') or key == ord('S'):
                    flag = 1
                if key == ord('w') or key == ord('W'):
                    flag = 0
                if flag:
                    n = n + 1
                    cv2.imwrite(os.path.join(color_dir, str(n) + image_formats[opt.image_format]), rgb)
                    cv2.imwrite(os.path.join(depth_dir, str(n) + image_formats[opt.image_format]), depth)
                    cv2.imwrite(os.path.join(depth_color_dir, str(n) + image_formats[opt.image_format]), depth_rgb)
                    np.save(os.path.join(depth_npy_dir, str(n)), depth)
                    print('{}{} is saved!'.format(n, image_formats[opt.image_format]))
        except:
            pass
