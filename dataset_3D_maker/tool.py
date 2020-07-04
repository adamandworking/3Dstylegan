from binvox_rw import read_as_3d_array

def binvox_to_nparray(binvox_path):
    with open(binvox_path, 'rb') as f:
        model = read_as_3d_array(f)
    return model.data