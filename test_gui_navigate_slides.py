import napari
from magicgui import magicgui
import zarr
from numpy import moveaxis

zobj=None
viewer = napari.Viewer()

@magicgui(auto_call=True,
            img={"max": 1},
            resolution={"max": 0, "label": "Downscaling (2^n)"},
            viewer={'bind': viewer})
def pick_img(viewer: napari.Viewer, img=1, resolution=0):
    global zobj
    
    viewer.layers.clear()
    pick_img.resolution.max = retrieve_res(zobj, img)
    if (pick_img.resolution.value > pick_img.resolution.max or resolution > pick_img.resolution.max):
        pick_img.resolution.value = pick_img.resolution.max
        resolution = pick_img.resolution.value
    pick_img.resolution.min = 0
    path = str(img - 1)+"/"+str(resolution)
    
    #reshape for RGB
    img = moveaxis(zobj[path], 1, -1)       
    viewer.add_image(img, rgb=True)
    viewer.reset_view()
    return 


def retrieve_maximum(zarr_obj):
    imgs = 0
    att_size = len(zarr_obj[imgs].attrs.asdict())
    while (att_size > 0):
        imgs += 1
        try:
            att_size = len(zarr_obj[imgs].attrs.asdict())
        except KeyError:
            break
    
    return imgs


def retrieve_res(zarr_obj, img):
    imgpath = str(img-1)
    try:
        res = len(zarr_obj[imgpath].attrs.asdict()['multiscales'][0]['datasets']) - 1
    except KeyError:
        return None
    return res

@magicgui(call_button="open",
            result_widget=True)
def open_zarr(address=''):
    global zobj
    try:
        zobj = zarr.open(address, mode='r')
        if zobj.attrs.asdict():
            result='Loaded successfully!'
            pick_img.resolution.max = retrieve_res(zobj, 1)
            pick_img.resolution.min = 0
            pick_img.resolution.value = pick_img.resolution.max
            imgs = retrieve_maximum(zobj)
            
            pick_img.img.max = imgs
            pick_img.img.min = 1
            
            pick_img.enabled = True
            pick_img.show()

            return result
        else: 
            result = 'No zattrs found - loading what we can'
            viewer.add_image(zobj)
            pick_img.hide()
            pick_img.enabled = False
            return result

    except ValueError:
        result = 'Address not found!'
        pick_img.hide()
        pick_img.enabled = False
        return result

pick_img.enabled = False
open_dock = viewer.window.add_dock_widget(open_zarr, area='top')
pick_dock = viewer.window.add_dock_widget(pick_img, area='right')
pick_img.visible = False
viewer.reset_view()
napari.run()

