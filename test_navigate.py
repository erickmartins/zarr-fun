import zarr

zobj = zarr.open('s3-server.org/bucket-name/zarr-name', mode='r')
print (zobj.attrs.asdict()['plate']['wells'])
print(len(zobj.attrs.asdict()['plate']['wells']))

for i in range(len(zobj.attrs.asdict()['plate']['wells'])):
    print(zobj.attrs.asdict()['plate']['wells'][i]['path'])
    print(zobj[zobj.attrs.asdict()['plate']['wells'][i]['path']+'/1/0'].shape)
