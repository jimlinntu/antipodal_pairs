import math
import numpy as np
import cv2

def distance(p1, p2, p):
    ''' The distance from p to a line formed by p1 and p2 '''
    return abs(((p2[1]-p1[1])*p[0] - (p2[0]-p1[0])*p[1] + p2[0]*p1[1] - p2[1]*p1[0]) /
        math.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2))

def find_antipodal_pairs(points, point_names):
    ''' points are in COUNTER clockwise order'''
    assert isinstance(points, np.ndarray)
    assert len(points) >= 3 and points.shape[1] == 2
    pairs = []
    n = len(points)
    i, j = 0, 1
    p0, p1 = points[0], points[1]

    #####################
    # Find the first antipodal pair
    # Actually, you can also break the loop when we encounter a decline!
    max_dis = 0
    for jj in range(1, n):
        d = distance(p0, p1, points[jj])
        if d > max_dis:
            j = jj
            max_dis = d

    pairs.append((point_names[i], point_names[j]))
    #####################

    # Rotating Caliper Algorithm (implemented by distance rather than angle computation)
    while j != 0:
        ii = (i + 1) % n
        jj = (j + 1) % n

        # the edge (i, i+1)
        p_i, p_ii = points[i], points[ii]
        # the edge (j, j+1)
        p_j, p_jj = points[j], points[jj]

        h_j = distance(p_i, p_ii, p_j)
        h_jj = distance(p_i, p_ii, p_jj)

        # Case 1: h_j == h_jj:
        #         this means the "rotated" line will reach (i, i+1) and (j, j+1) at the SAME time!
        # Case 2: h_j > h_jj:
        #         this means points[j] is an antipodal point for i, and the "rotated" line will first reach (i, i+1)
        #         Intuitively, this means from the perspective of line (i, i+1), point j is the "topest" one
        # Case 3: h_j < h_jj:
        #         this means points[j] is NOT an antipodal point for i, and the "rotated" line will first reach (j, j+1)
        #         Intuitively, this means from the perspective of line (i, i+1), point j is NOT the "topest" one!
        if math.isclose(h_j, h_jj):
            pairs.append((point_names[ii], point_names[j]))
            pairs.append((point_names[i], point_names[jj]))
            pairs.append((point_names[ii], point_names[jj]))
            i = ii
            j = jj
        elif h_j > h_jj:
            pairs.append((point_names[ii], point_names[j]))
            i = ii
        else:
            pairs.append((point_names[i], point_names[jj]))
            j = jj

    return pairs

def main():
    data = [(5, 7), (3, 6), (2, 5), (3, 2), (7, 1), (8, 2), (9, 5)]
    names = [chr(ord('A') + i) for i in range(len(data))]
    np_data = np.array(data, dtype=np.int32).reshape(-1, 2)

    vis_img = np.zeros((12, 12, 3), dtype=np.int32)
    vis_img = cv2.polylines(vis_img, [np_data], True, (0, 255, 0))
    cv2.imwrite("vis_img.png", vis_img)

    pairs = find_antipodal_pairs(np_data, names)
    print(pairs)

if __name__ == "__main__":
    main()
