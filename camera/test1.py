import numpy as np
import cv2

histogram = np.sum(img[img.shape[0]//2:,:], axis=0)
plt.plot(histogram)

def video_pipeline(source_img):
    src_pts, dst_pts = define_perspective_points(source_img)
    source_img = undistort_image(source_img, mtx, dist)
    thresh_img = color_thresh_combined(source_img, s_thresh, l_thresh, v_thresh, b_thresh)
    warp_img = perspective_transformation(thresh_img, src_pts, dst_pts, False)
    left_fit_, right_fit_, lines_img, mean_curverad, position = find_lines_video(warp_img)
    inv_matrix, unwarp_img = invert_perspective(warp_img, src_pts, dst_pts)
    lane_img = superimpose_lane_area(source_img, warp_img, left_fit_, right_fit_, inv_matrix, mean_curverad, position)
    return lane_img

def undistort_image(img, camera_matrix, distortion_coeffs):
    img1 = cv2.undistort(img, camera_matrix, distortion_coeffs)
    return img

def color_thresh_combined(img, s_thresh, l_thresh, v_thresh, b_thresh):
    V_binary = HSV_thresh(img, v_thresh)
    S_binary = HLS_thresh(img, s_thresh)
    L_binary = LUV_thresh(img, l_thresh)
    color_binary = np.zeros_like(V_binary)                           
    color_binary[(V_binary == 1) & (S_binary == 1) & (L_binary == 1)] = 1
    return color_binary

mean_curverad, position = radius_curvature(ploty, left_fitx, right_fitx, window_img.shape)#The final curvature is the average for the left and right lane lines.
ym_per_pix = 30/720 # meters per pixel in y dimension
xm_per_pix = 3.7/700 # meters per pixel in x dimension
