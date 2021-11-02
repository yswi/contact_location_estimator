from utils import *

PATH_POINTCLOUD = 'data/plastic_845_830/scan_5.ply'
PATH_WRENCH_CNT = 'wrench/scraping_plastic/scrape_gt_845_835.pickle'
PATH_WRENCH_B4_CNT = 'wrench/scraping_plastic/scrape_gt_845_835.pickle' #'wrench/scraping_plastic/mg_wrench.pickle'

if __name__ == '__main__':
    pcd = load_pcd(PATH_POINTCLOUD)
    cnt_force = gt_wrench(PATH_WRENCH_CNT, PATH_WRENCH_B4_CNT, 5)
    print("cnt_force", cnt_force)
    cnt_loc_est = contact_location(pcd, cnt_force)
    visualize_cnt_loc(pcd, cnt_loc_est)