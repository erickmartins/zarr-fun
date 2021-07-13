from dask import delayed
from dask import array as da
import zarr
import napari
import napari.utils.io as nio
import numpy as np

zobj = zarr.open('data/example.zarr', mode='w', shape=(1000, 1000, 1000),chunks=(100, 100, 100), dtype='i4')
[_, _, zobj[:, :, :]] = np.meshgrid(np.arange(1000),np.arange(1000),np.arange(1000))

print(zobj.shape)

#the next two commented examples should work if our zarrs had .zarray...

# tst = nio.read_zarr_dataset('https://s3-far.jax.org/zarrtest/test7.zarr')
# print(tst)

img = da.from_zarr(zobj)
img2 = da.from_zarr('s3-server.org/bucket-name/zarr-name/1/1/10/0')

viewer = napari.view_image(img2)
napari.run()


