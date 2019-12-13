import cv2
assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'

import numpy as np
import os
import glob
import sys

# You should replace these 3 lines with the output in calibration step
#DIM=XXX
#K=np.array(YYY)
#D=np.array(ZZZ)

DIM=(1024, 768)
K=np.array([[519.9193064206078, 0.0, 528.697570215532], [0.0, 527.995007066815, 365.62086684123926], [0.0, 0.0, 1.0]])
D=np.array([[-0.021477320143423725], [-0.1313655175622944], [0.13791191678842682], [-0.048545137189861344]])

def undistort(img_path):    

    img = cv2.imread(img_path)
    h,w = img.shape[:2]    

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)    
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)
