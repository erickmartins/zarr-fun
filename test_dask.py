from dask import delayed
from dask import array as da
import dask_image.ndfilters
from dask.distributed import Client
import zarr
import napari
from skimage.filters import gaussian
import timeit



if __name__ == "__main__":
    #run this bit first time around
    # zobj = zarr.open('data/example.zarr', mode='w', shape=(1000, 1000, 1000),chunks=(100, 100, 100), dtype='i4')
    # [_, _, zobj[:, :, :]] = np.meshgrid(np.arange(1000),np.arange(1000),np.arange(1000))

    client = Client(n_workers=4)

    zobj = zarr.open('data/example.zarr')
    print(zobj.shape)

    #the next two commented examples should work if our zarrs had .zarray...

    # tst = nio.read_zarr_dataset('https://s3-far.jax.org/zarrtest/test7.zarr')
    # print(tst)

    img = da.from_zarr(zobj, chunks=(100,100,100))
    print(img)

    time1 = timeit.timeit('gaussian(img, sigma=(1,1,1))', number=1, globals=globals())
    print(time1)
    time2= timeit.timeit('dask_image.ndfilters.gaussian_filter(img, sigma=[100, 100, 100])', number=1, globals=globals())
    gauss2=dask_image.ndfilters.gaussian_filter(img, sigma=[10, 10, 10])
    print(gauss2)
    print(time2)
    print(img[10:15,10:15,10:15].compute())
    print(gauss2[10:15,10:15,10:15].compute())
    # img2 = da.from_zarr('s3-server.org/bucket-name/zarr-name/1/1/10/0')

    viewer = napari.view_image(img)
    napari.run()


