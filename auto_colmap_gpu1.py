import os


def auto_colmap(workspace_path, img_path):

    db_path = workspace_path + 'database.db'
    sparse_path = workspace_path + 'sparse/'

    print('Colmap feature extracting...')
    os.system('colmap feature_extractor \
                --database_path {} \
                --image_path {} \
                --ImageReader.camera_model SIMPLE_RADIAL \
                --ImageReader.single_camera=1 \
                --SiftExtraction.gpu_index=1'.format(db_path, img_path))
    # Perform feature matching after performing feature extraction
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
    img_path = '{}'.format(scene) + '/'
    workspace_path = './colmap_results/{}/'.format(scene)
    os.makedirs('{}'.format(workspace_path), exist_ok=True)

    print('Scene {} on work...'.format(scene))
    auto_colmap(workspace_path, img_path)

def iteration(super_path, scene_list):
    os.chdir(super_path)
    os.makedirs('colmap_results', exist_ok=True)
    for i, scene in enumerate(scene_list):
        print('Scene#{} : {} is being used'.format(i, scene))
        scene_extractor(scene)

if __name__ == '__main__':
    # super_path = 'scenes/'
    super_path = '../mnt/NYU Depth Dataset V2/nyu_depth_v2_rgb/temp1/'
    # super_path = 'Z:/NYU Depth Dataset V2/nyu_v2_rgb_only/'

    scene_list = scene_list_extractor(super_path)
    iteration(super_path, scene_list)
    print('Job Finished')