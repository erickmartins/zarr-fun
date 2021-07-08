import zarr
import napari

zobj = zarr.open('https://s3-server.org/bucket-name/zarr-name', mode='r')
print(zobj['1/1/10/0'].info)

viewer = napari.view_image(zobj['1/1/10/0'])
napari.run()
