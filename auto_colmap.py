import os

'''
% The maximum depth used, in meters.
maxDepth = 10;

% RGB Intrinsic Parameters
fx_rgb = 5.1885790117450188e+02;
fy_rgb = 5.1946961112127485e+02;
cx_rgb = 3.2558244941119034e+02;
cy_rgb = 2.5373616633400465e+02;

% RGB Distortion Parameters
k1_rgb =  2.0796615318809061e-01;
k2_rgb = -5.8613825163911781e-01;
p1_rgb = 7.2231363135888329e-04;
p2_rgb = 1.0479627195765181e-03;
k3_rgb = 4.9856986684705107e-01;

-> FULL_OPENCV 사용한 것으로 보임
fx, fy, cx, cy, k1, k2, p1, p2, k3, k4, k5, k6 = 
5.1885790117450188e+02, 5.1946961112127485e+02, 3.2558244941119034e+02, 2.5373616633400465e+02, 2.0796615318809061e-01, -5.8613825163911781e-01,
7.2231363135888329e-04, 1.0479627195765181e-03, 4.9856986684705107e-01, 0, 0, 0
'''


def auto_colmap(workspace_path, img_path):
    '''
    CUDA 쓸거면 그냥 사용하면 됨
    CPU 쓸거면 --SiftExtraction.use_gpu 0, --SiftMatching.use_gpu 0 추가하면 됨
    fx fy cx cy
    k1 k2 p1 p2 k3 k4 k5 k6
    '''
    db_path = workspace_path + 'database.db'
    sparse_path = workspace_path + 'sparse/'

    # Camera parameters
    # fx = 5.1885790117450188e+02
    # fy = 5.1946961112127485e+02
    # cx = 3.2558244941119034e+02
    # cy = 2.5373616633400465e+02
    # k1 = 2.0796615318809061e-01
    # k2 = 5.8613825163911781e-01
    # p1 = 7.2231363135888329e-04
    # p2 = 1.0479627195765181e-03
    # k3 = 4.9856986684705107e-01
    # k4 = 0.0
    # k5 = 0.0
    # k6 = 0.0
    
    # camera_params = '"{} {} {} {} {} {} {} {} {} {} {} {}"'.format(fx,fy,cx,cy,k1,k2,p1,p2,k3,k4,k5,k6)#
    # camera_params = '"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"'.format(fx,fy,cx,cy,k1,k2,p1,p2,k3,k4,k5,k6)
    # camera_type = 'FULL_OPENCV'
    proj_path = 'C:/Users/user/Desktop/code/auto_col/preset.ini'
    # camera_params = 'Z:/NYU Depth Dataset V2/cameras.txt'
    # Perform feature extraction for a set of images

    '''
    colmap feature_extractor
        --database_path db_path
        --image_path img_path
        --ImageReader.camera_model FULL_OPENCV
        --ImageReader.single_camera 1 를 하면 결과물은 다음과 같다

    database.db
    
        --project_path proj_path 까지 해줘야 project.ini가 저장되는 것 같다.
        즉 db 파일에 camera model과 parameter를 저장하는 방식인 것 같음
        -> 이에 접근해서 수정하는 방법을 찾아봐야함

    preset처럼 project.ini 파일을 만들어서 배포하는 방식은 어떨까
    
    '''
    print('Colmap feature extracting...')
    os.system('colmap feature_extractor \
                --database_path {} \
                --image_path {} \
                --ImageReader.camera_model SIMPLE_RADIAL \
                --ImageReader.single_camera=1'.format(db_path, img_path))
    # Perform feature matching after performing feature extraction
    '''
       exhaustive_matcher, mapper, model_converter에 project_path를 활성화해보는건 어떨까
    '''
    print('Colmap feature matching...')
    os.system('colmap exhaustive_matcher \
                --database_path {}'.format(db_path))
    # Perform sparse 3D reconstruction and mapping of the dataset using SfM after performing feature extraction and matching
    os.makedirs(sparse_path, exist_ok=True)
    print('Colmap mapping...')
    os.system('colmap mapper \
                --database_path {} \
                --image_path {} \
                --output_path {}'.format(db_path, img_path, sparse_path))
    
    # Convert bin files to txt files for debugging
    print('Colmap making output files...')
    os.system('colmap model_converter \
                --input_path {} \
                --output_path {} \
                --output_type TXT'.format(sparse_path + '0/', sparse_path + '0/'))

def scene_list_extractor(super_path):
    scene_list = os.listdir(super_path)
    temp = -1
    for i, scene in enumerate(scene_list):
        if scene == 'colmap_results':
            temp=i
    if temp != -1:
        del scene_list[temp]
    print('Total #(scene) : {}\n'.format(len(scene_list)))
    return scene_list

def scene_extractor(scene):
    # os.system('colmap')
    img_path = '{}'.format(scene) + '/'
    # 'Z:/NYU Depth Dataset V2/nyu_v2_rgb_only/'
    workspace_path = './colmap_results/{}/'.format(scene)
    os.makedirs('{}'.format(workspace_path), exist_ok=True)

    print('Scene {} on work...'.format(scene))
    # os.system('colmap automatic_reconstructor \
    #                 --workspace_path {} \
    #                 --image_path {} \
    #                     '.format(workspace_path, img_path))
    #                 # --SiftExtraction.gpu_index=0'.format(workspace_path, img_path))
    auto_colmap(workspace_path, img_path)

def iteration(super_path, scene_list):
    os.chdir(super_path)
    os.makedirs('colmap_results', exist_ok=True)
    for i, scene in enumerate(scene_list):
        print('Scene#{} : {} is being used'.format(i, scene))
        scene_extractor(scene)

if __name__ == '__main__':
    # super_path = 'scenes/'
    super_path = 'Z:/NYU Depth Dataset V2/nyu_v2_rgb_only/'
    '''
    image 폴더는 다음과 같다고 가정한다.
    super_path : /path/to/project/
    {super_path}/...
    +--- scene_name
    |   +--- image1.jpg
    |   +--- image2.jpg
    |   +--- ...
    |   +--- imageN.jpg
    '''

    scene_list = scene_list_extractor(super_path)
    iteration(super_path, scene_list)
    print('Job Finished')

'''
colmap automatic_reconstructor는 해결됨
이제 각각을 나눠서 해야 함

'''