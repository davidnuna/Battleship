# The module that contains the coordinates class

class coordinates:
    def __init__(self, coordinate_x, coordinate_y):
        # Every coordinate is defined by 2 instances: the x coordinate and the y coordinate
        # Input: self - the current object
        #        coordinate_x - an integer, the x coordinate
        #        coordinate_y - an integer, the y coordinate
        self.__coordinate_x = coordinate_x
        self.__coordinate_y = coordinate_y
    
    @property
    def get_coordinate_x(self):
        # Getter for the 'coordinate_x' instance
        # Input: self - the current object
        # Output: the x coordinate of the current object
        return self.__coordinate_x
    
    @property
    def get_coordinate_y(self):
        # Getter for the 'coordinate_y' instance
        # Input: self - the current object
        # Output: the y coordinate of the current object
        return self.__coordinate_y
