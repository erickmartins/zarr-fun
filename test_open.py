import zarr
import napari

zobj = zarr.open('s3-server.org/bucket-name/zarr-name', mode='r')
print (zobj.attrs.asdict()['plate'])
print(zobj.tree())
print(zobj['3/7/24/1'].info)

viewer = napari.view_image(zobj['1/1/10/0'])
napari.run()
