import h5py

file_name = 'HS_mean.dat'
with h5py.File(file_name, 'r') as f:
    print("Groups in HDF5 file:")
    for group in f.keys():
        print(group)

    #for group in f.keys():
        #print("\nDatasets in group '{}':".format(group))
        #for dataset in f[group]:
            #print(dataset)
            #print(dataset.shape)

    dataset_name = 't_zonal_mean'
    data = f[dataset_name][()]

    print("\nData in dataset '{}':".format(dataset_name))
    print(data.shape)



