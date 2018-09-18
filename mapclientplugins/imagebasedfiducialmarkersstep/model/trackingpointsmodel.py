
from opencmiss.utils.zinc import createFiniteElementField, createNodes, createNode


class NodeCreator(object):

    def __init__(self, coordinates):
        self._coordinates = coordinates

    def coordinates(self):
        return self._coordinates


class TrackingPointsModel(object):

    def __init__(self, master_model):
        self._master_model = master_model
        self._region = None
        self._coordinate_field = None
        self._selection_group = None
        self._selection_group_field = None
        self._data_points = []

    def get_region(self):
        return self._region

    def get_coordinate_field(self):
        return self._coordinate_field

    def select_node(self, identifier):
        node = self.get_node(identifier)
        self._selection_group.removeAllNodes()
        self._selection_group.addNode(node)

    def deselect_node(self, identifier):
        node = self.get_node(identifier)
        self._selection_group.removeNode(node)

    def is_selected(self, identifier):
        node = self.get_node(identifier)
        return self._selection_group.containsNode(node)

    def create_node(self, location):
        time = self._master_model.get_timekeeper_time()
        field_module = self._coordinate_field.getFieldmodule()
        identifier = createNode(field_module, ['coordinates'], NodeCreator(location), node_set_name='datapoints', time=time)
        node = self.get_node(identifier)
        self._selection_group.removeAllNodes()
        self._selection_group.addNode(node)

        return node

    def set_node_location(self, node, location):
        time = self._master_model.get_timekeeper_time()
        field_module = self._coordinate_field.getFieldmodule()
        field_module.beginChange()
        field_cache = field_module.createFieldcache()
        field_cache.setTime(time)
        field_cache.setNode(node)
        self._coordinate_field.assignReal(field_cache, location)
        field_module.endChange()

    def remove_node(self, identifier):
        node = self.get_node(identifier)
        node_set = node.getNodeset()
        node_set.destroyNode(node)

    def get_node(self, identifier):
        node_set = self._selection_group.getMasterNodeset()
        return node_set.findNodeByIdentifier(identifier)

    def get_selection_field(self):
        return self._selection_group_field

    def create_key_points(self, key_points):
        time = self._master_model.get_timekeeper_time()
        key_points_coordinates = [[float(key_point[0]), float(key_point[1]), 0.0] for key_point in key_points]
        createNodes(self._coordinate_field, key_points_coordinates, node_set_name='datapoints', time=time)

    def get_key_points(self):
        key_points = []
        field_module = self._region.getFieldmodule()
        field_cache = field_module.createFieldcache()
        node_set = field_module.findNodesetByName('datapoints')
        node_set_iterator = node_set.createNodeiterator()
        node = node_set_iterator.next()
        while node and node.isValid():
            coords = self._coordinate_field.evaluateReal(field_cache, 3)
            print(coords)
            node = node_set_iterator.next()

        return key_points

    def create_model(self):
        default_region = self._master_model.get_default_region()
        if self._region is not None:
            default_region.removeChild(self._region)

        self._region = default_region.createChild('tracking')
        self._coordinate_field = createFiniteElementField(self._region)

        field_module = self._region.getFieldmodule()
        field_module.beginChange()
        node_set = field_module.findNodesetByName('datapoints')

        # Setup the selection fields
        self._selection_group_field = field_module.createFieldGroup()
        selection_group = self._selection_group_field.createFieldNodeGroup(node_set)
        self._selection_group = selection_group.getNodesetGroup()
        field_module.endChange()
