
'''
input : point [x,y,z] , force [fx,fy,fz]
output : torque [tx, ty, tz]
'''
import copy

from scipy.spatial.distance import cosine
from sklearn.metrics import pairwise
import numpy as np
import open3d as o3d
import pickle

'''
input : pcd (array), contact force (array)
output : point with closest estimation (array)
'''
def local2EE(pcd):
    temp = copy.deepcopy(pcd)
    temp[:,1] = - pcd[:,1]
    temp[:,2] = - pcd[:,2]
    return temp

def contact_location(pcd, cnt_force):
    def cosine_distances(embedding_matrix, extracted_embedding):
        return cosine(embedding_matrix, extracted_embedding)

    # cosine_distances = np.vectorize(cosine_distances, signature='(m),(d)->()')

    pcd_ori = np.array(pcd.points)
    pcd = local2EE(pcd_ori)

    force = cnt_force[:3]
    wrench_est = np.cross(pcd, force)

    dist = np.linalg.norm(wrench_est- cnt_force[3:], axis=1, ord = 2)
    print("torque", cnt_force[3:])

    # dist = abs(1-  cosine_distances(wrench_est, cnt_force[3:]))

    cnt_idx = np.argmax(dist)
    print("CNT_IDX", cnt_idx, "with distance ", np.amin(dist),  np.amax(dist))
    return pcd_ori[cnt_idx,:]

def load_pcd(path):
    pcd = o3d.io.read_point_cloud(path)
    print("load_pcd_shape", np.amin(np.array(pcd.points), axis= 0 ))
    print("load_pcd_shape", np.array(pcd.points).shape)
    pcd = pcd.voxel_down_sample(voxel_size=0.001) # allow 1mm of error
    # print("load_pcd_shape", np.array(pcd.points).shape)
    return pcd

def load_wrench(path, task_num):
    with open(path, 'rb') as handle:
        wrench = np.asarray(pickle.load(handle)).reshape(-1, 6)
    return wrench[task_num]

def gt_wrench(path_wrench_cnt, path_wrench_b4_cnt, task_num):
    '''
        contact force = wrench in contact - gravity effect (wrench just before the contact)
    '''

    wrench = load_wrench(path_wrench_cnt, task_num)
    # wrench[:3]-= load_wrench(path_wrench_b4_cnt, 0)[:3]

    wrench -= load_wrench(path_wrench_b4_cnt, 0)
    print(load_wrench(path_wrench_cnt, task_num), load_wrench(path_wrench_b4_cnt, task_num))
    return wrench

def visualize_cnt_loc(pcd, cnt_loc_est):
    cnt = o3d.geometry.TriangleMesh.create_sphere(radius=0.003)
    cnt.compute_vertex_normals()
    cnt.paint_uniform_color([0.9, 0.1, 0.1])
    cnt.translate(cnt_loc_est)

    o3d.visualization.draw_geometries([pcd, cnt])

