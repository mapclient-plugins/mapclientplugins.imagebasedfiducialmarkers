
from opencmiss.utils.zinc import createFiniteElementField, createNodes, createNode


class TrackingPointsModel(object):

    def __init__(self, master_model):
        self._master_model = master_model
        self._region = None
        self._coordinate_field = None
        self._data_points = []

    def get_region(self):
        return self._region

    def get_coordinate_field(self):
        return self._coordinate_field

    def create_key_points(self, key_points):
        key_points_coordinates = [[float(key_point[0]), float(key_point[1]), 0.0] for key_point in key_points]
        createNodes(self._coordinate_field, key_points_coordinates, 'datapoints')

    def create_model(self):
        default_region = self._master_model.get_default_region()
        if self._region is not None:
            default_region.removeChild(self._region)

        self._region = default_region.createChild('tracking')
        self._coordinate_field = createFiniteElementField(self._region)
