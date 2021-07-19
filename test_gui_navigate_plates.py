import napari
import warnings
from magicgui import magicgui
import zarr

zobj=None
viewer = napari.Viewer()

@magicgui(auto_call=True,
            row={"max": 1},
            column={"max": 1},
            field={"max": 1},
            resolution={"max": 0, "label": "Downscaling (2^n)"},
            viewer={'bind': viewer})
def pick_area(viewer: napari.Viewer, row=0, column=0, field=0, resolution=0):
    global zobj
    viewer.layers.clear()
    f_max = retrieve_fields(zobj, row, column)
    if f_max:
        pick_area.field.max = f_max
        pick_area.field.min = 1
        pick_area.resolution.max = retrieve_res(zobj, row, column, field)
        pick_area.resolution.min = 0
        path = str(row)+"/"+str(column)+"/"+str(field)+"/"+str(resolution)
        viewer.add_image(zobj[path])
    viewer.reset_view()
    return 


def retrieve_maxima(zarr_obj):
    attrs = zarr_obj.attrs.asdict()
    columns = len(attrs['plate']['columns'])
    rows = len(attrs['plate']['rows']) 
    return rows, columns


def retrieve_fields(zarr_obj, row, column):
    well = str(row)+'/'+str(column)
    print(f"well is {well}")
    fields = None
    try:
        fields = len(zarr_obj[well].attrs.asdict()['well']['images'])
    except KeyError:
        warnings.warn("Warning: well not found")
    return fields


def retrieve_res(zarr_obj, row, col, field):
    fieldpath = str(row)+'/'+str(col)+'/'+str(field)
    return len(zarr_obj[fieldpath].attrs.asdict()['multiscales'][0]['datasets']) - 1


@magicgui(call_button="open",
            result_widget=True)
def open_zarr(address=''):
    global zobj
    try:
        zobj = zarr.open(address, mode='r')
        if zobj.attrs.asdict():
            result='Loaded successfully!'
            row, col = retrieve_maxima(zobj)
            # for now, relying on rows/cols being 1-max - the right way
            # would be to create a dropdown/enum from metadata
            pick_area.row.max = row
            pick_area.row.min = 1
            pick_area.column.max = col
            pick_area.column.min = 1
            pick_area.field.max = retrieve_fields(zobj, pick_area.row.value, pick_area.column.value)
            pick_area.field.min = 1
            pick_area.resolution.max = retrieve_res(zobj, pick_area.row.value, pick_area.column.value, pick_area.field.value)
            pick_area.resolution.min = 0
            pick_area.resolution.value = pick_area.resolution.max
            pick_area.enabled = True
            pick_area.show()
            return result
        else: 
            result = 'No zattrs found - loading what we can'
            viewer.add_image(zobj)
            pick_area.hide()
            pick_area.enabled = False
            return result
    except ValueError:
        result = 'Address not found!'
        pick_area.hide()
        pick_area.enabled = False
        return result
        
pick_area.enabled = False
open_dock = viewer.window.add_dock_widget(open_zarr, area='top')
pick_dock = viewer.window.add_dock_widget(pick_area, area='right')
pick_area.visible = False
viewer.reset_view()
napari.run()

