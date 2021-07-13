import s3fs
import zarr


s3 = s3fs.S3FileSystem(anon=True, client_kwargs={'endpoint_url': 's3-server.org'})
print(s3.info('zarrtest'))

print(s3.ls('zarrtest'))
print(s3.ls('zarrtest/test7.zarr'))

z = zarr.open('s3-server.org/bucket-name/zarr-name')
attr_dict = dict(z.attrs)
print(attr_dict)