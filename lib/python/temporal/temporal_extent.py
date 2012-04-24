"""!@package grass.temporal

@brief GRASS Python scripting module (temporal GIS functions)

Temporal GIS related temporal extent functions to be used in Python scripts and tgis packages.

Usage:

@code
import grass.temporal as tgis

tgis.raster_temporal_extent()
...
@endcode

(C) 2008-2011 by the GRASS Development Team
This program is free software under the GNU General Public
License (>=v2). Read the file COPYING that comes with GRASS
for details.

@author Soeren Gebbert
"""
from base import *

###############################################################################

class abstract_temporal_extent(sql_database_interface):
    """!This is the abstract time base class for relative and absolute time objects"""
    def __init__(self, table=None, ident=None, start_time=None, end_time=None):

	sql_database_interface.__init__(self, table, ident)

	self.set_id(ident)
	self.set_start_time(start_time)
	self.set_end_time(end_time)

    def starts(self, extent):
	"""!Return True if this time object starts at the start of the provided time object and finishes within it
	   A  |-----|
	   B  |---------|
	"""
        if  self.D["end_time"] == None or extent.D["end_time"] == None :
            return False
            
	if self.D["start_time"] == extent.D["start_time"] and self.D["end_time"] < extent.D["end_time"]:
	    return True
        else:
	    return False

    def started(self, extent):
	"""!Return True if this time object is started at the start of the provided time object
	   A  |---------|
	   B  |-----|
	"""
        if  self.D["end_time"] == None or extent.D["end_time"] == None :
            return False

	if self.D["start_time"] == extent.D["start_time"] and self.D["end_time"] > extent.D["end_time"]:
	    return True
        else:
	    return False

    def finishes(self, extent):
	"""!Return True if this time object finishes at the end and within of the provided time object
	   A      |-----|
	   B  |---------|
	"""
        if  self.D["end_time"] == None or extent.D["end_time"] == None :
            return False

	if self.D["end_time"] == extent.D["end_time"] and  self.D["start_time"] > extent.D["start_time"] :
	    return True
        else:
	    return False

    def finished(self, extent):
	"""!Return True if this time object finished at the end of the provided time object
	   A  |---------|
	   B      |-----|
	"""
        if  self.D["end_time"] == None or extent.D["end_time"] == None :
            return False

	if self.D["end_time"] == extent.D["end_time"] and  self.D["start_time"] < extent.D["start_time"] :
	    return True
        else:
	    return False

    def after(self, extent):
	"""!Return True if this time object is temporal located after the provided time object
	   A             |---------|
	   B  |---------|
	"""
        if extent.D["end_time"] == None:
            if self.D["start_time"] > extent.D["start_time"]:
                return True
            else:
                return False

	if self.D["start_time"] > extent.D["end_time"]:
	    return True
        else:
	    return False

    def before(self, extent):
	"""!Return True if this time object is temporal located before the provided time object
	   A  |---------|
	   B             |---------|
	"""
        if self.D["end_time"] == None:
            if self.D["start_time"] < extent.D["start_time"]:
                return True
            else:
                return False

	if self.D["end_time"] < extent.D["start_time"]:
	    return True
        else:
	    return False

    def adjacent(self, extent):
	"""!Return True if this time object is a meeting neighbour the provided time object
	   A            |---------|
	   B  |---------|
	   A  |---------|
	   B            |---------|
	"""
        if  self.D["end_time"] == None and extent.D["end_time"] == None :
            return False
        
	if (self.D["start_time"] == extent.D["end_time"]) or (self.D["end_time"] == extent.D["start_time"]):
	    return True
        else:
	    return False

    def follows(self, extent):
	"""!Return True if this time object temporally follows the provided time object
	   A            |---------|
	   B  |---------|
	"""
        if  extent.D["end_time"] == None :
            return False

	if self.D["start_time"] == extent.D["end_time"]:
	    return True
        else:
	    return False

    def precedes(self, extent):
	"""!Return True if this time object is temporal precedes the provided time object
	   A  |---------|
	   B            |---------|
	"""
        if  self.D["end_time"] == None:
            return False

	if self.D["end_time"] == extent.D["start_time"]:
	    return True
        else:
	    return False

    def during(self, extent):
	"""!Return True if this time object is temporal located during the provided time object
	   A   |-------|
	   B  |---------|
	"""
        # Check single point of time in interval
        if  extent.D["end_time"] == None:
                return False

        # Check single point of time in interval
        if  self.D["end_time"] == None:
            if self.D["start_time"] > extent.D["start_time"] and self.D["start_time"] < extent.D["end_time"]:
                return True
            else:
                return False

	if self.D["start_time"] > extent.D["start_time"] and self.D["end_time"] < extent.D["end_time"]:
	    return True
        else:
	    return False

    def contains(self, extent):
	"""!Return True if this time object contains the provided time object
	   A  |---------|
	   B   |-------|
	"""
        # Check single point of time in interval
        if  self.D["end_time"] == None:
                return False

        # Check single point of time in interval
        if  extent.D["end_time"] == None:
            if self.D["start_time"] < extent.D["start_time"] and self.D["end_time"] > extent.D["start_time"]:
                return True
            else:
                return False

	if self.D["start_time"] < extent.D["start_time"] and self.D["end_time"] > extent.D["end_time"]:
	    return True
        else:
	    return False

    def equivalent(self, extent):
	"""!Return True if this time object is temporal located equivalent the provided time object
	   A  |---------|
	   B  |---------|
	"""
        if  self.D["end_time"] == None and extent.D["end_time"] == None :
            if self.D["start_time"] == extent.D["start_time"]:
                return True
            else:
                return False

        if  self.D["end_time"] == None or extent.D["end_time"] == None :
            return False

	if self.D["start_time"] == extent.D["start_time"] and self.D["end_time"] == extent.D["end_time"]:
	    return True
        else:
	    return False

    def overlapped(self, extent):
	"""!Return True if this time object temporally overlapped the provided time object
           A  |---------|
	   B    |---------|
	"""
        if  self.D["end_time"] == None or extent.D["end_time"] == None :
            return False

	if self.D["start_time"] < extent.D["start_time"] and self.D["end_time"] < extent.D["end_time"] and\
	   self.D["end_time"] > extent.D["start_time"]:
	    return True
        else:
	    return False

    def overlaps(self, extent):
	"""!Return True if this time object temporally overlaps the provided time object
	   A    |---------|
           B  |---------|
	"""
        if  self.D["end_time"] == None or extent.D["end_time"] == None :
            return False
            
	if self.D["start_time"] > extent.D["start_time"] and self.D["end_time"] > extent.D["end_time"] and\
	   self.D["start_time"] < extent.D["end_time"]:
	    return True
        else:
	    return False

    def temporal_relation(self, extent):
	"""!Returns the temporal relation between temporal objects
	   Temporal relationships are implemented after [Allen and Ferguson 1994 Actions and Events in Interval Temporal Logic]
	"""
        
        # First check for correct time
        if not self.D.has_key("start_time"):
            return None
        if not self.D.has_key("end_time"):
            return None
        if not extent.D.has_key("start_time"):
            return None
        if not extent.D.has_key("end_time"):
            return None

        if self.D["start_time"] == None or extent.D["start_time"] == None:
            return None

	if self.equivalent(extent):
	    return "equivalent"
	if self.during(extent):
	    return "during"
	if self.contains(extent):
	    return "contains"
	if self.overlaps(extent):
	    return "overlaps"
	if self.overlapped(extent):
	    return "overlapped"
	if self.after(extent):
	    return "after"
	if self.before(extent):
	    return "before"
	if self.starts(extent):
	    return "starts"
	if self.finishes(extent):
	    return "finishes"
	if self.started(extent):
	    return "started"
	if self.finished(extent):
	    return "finished"
	if self.follows(extent):
	    return "follows"
	if self.precedes(extent):
	    return "precedes"
        return None

    def set_id(self, ident):
	"""!Convenient method to set the unique identifier (primary key)"""
	self.ident = ident
	self.D["id"] = ident

    def set_start_time(self, start_time):
	"""!Set the valid start time of the extent"""
	self.D["start_time"] = start_time

    def set_end_time(self, end_time):
	"""!Set the valid end time of the extent"""
	self.D["end_time"] = end_time

    def get_id(self):
	"""!Convenient method to get the unique identifier (primary key)
	   @return None if not found
	"""
	if self.D.has_key("id"):
	    return self.D["id"]
        else:
	    return None

    def get_start_time(self):
	"""!Get the valid start time of the extent
	   @return None if not found"""
	if self.D.has_key("start_time"):
	    return self.D["start_time"]
        else:
	    return None

    def get_end_time(self):
	"""!Get the valid end time of the extent
	   @return None if not found"""
	if self.D.has_key("end_time"):
	    return self.D["end_time"]
        else:
	    return None

    def print_info(self):
        """!Print information about this class in human readable style"""
        #      0123456789012345678901234567890
        print " | Start time:................. " + str(self.get_start_time())
        print " | End time:................... " + str(self.get_end_time())

    def print_shell_info(self):
        """!Print information about this class in shell style"""
        print "start_time=" + str(self.get_start_time())
        print "end_time=" + str(self.get_end_time())

###############################################################################

class absolute_temporal_extent(abstract_temporal_extent):
    """!This is the absolute time class for all maps and spacetime datasets

       start_time and end_time must be of type datetime
    """
    def __init__(self, table=None, ident=None, start_time=None, end_time=None, timezone=None):

	abstract_temporal_extent.__init__(self, table, ident, start_time, end_time)

	self.set_timezone(timezone)

    def set_timezone(self, timezone):
	"""!Set the timezone of the map, the timezone is of type string.
           Timezones are not supported yet, instead the timezone is set in the datetime string as offset in minutes.
        """
	self.D["timezone"] = timezone

    def get_timezone(self):
	"""!Get the timezone of the map
           Timezones are not supported yet, instead the timezone is set in the datetime string as offset in minutes.
	   @return None if not found"""
	if self.D.has_key("timezone"):
	    return self.D["timezone"]
        else:
	    return None

    def print_info(self):
        """!Print information about this class in human readable style"""
        #      0123456789012345678901234567890
        print " +-------------------- Absolute time -----------------------------------------+"
        abstract_temporal_extent.print_info(self)
        #print " | Timezone:................... " + str(self.get_timezone())

    def print_shell_info(self):
        """!Print information about this class in shell style"""
        abstract_temporal_extent.print_shell_info(self)
        #print "timezone=" + str(self.get_timezone())

###############################################################################

class raster_absolute_time(absolute_temporal_extent):
    def __init__(self, ident=None, start_time=None, end_time=None, timezone=None):
        absolute_temporal_extent.__init__(self, "raster_absolute_time", ident, start_time, end_time, timezone)

class raster3d_absolute_time(absolute_temporal_extent):
    def __init__(self, ident=None, start_time=None, end_time=None, timezone=None):
        absolute_temporal_extent.__init__(self, "raster3d_absolute_time", ident, start_time, end_time, timezone)

class vector_absolute_time(absolute_temporal_extent):
    def __init__(self, ident=None, start_time=None, end_time=None, timezone=None):
        absolute_temporal_extent.__init__(self, "vector_absolute_time", ident, start_time, end_time, timezone)

###############################################################################

class stds_absolute_time(absolute_temporal_extent):
    def __init__(self, table=None, ident=None, start_time=None, end_time=None, granularity=None, timezone=None, map_time=None):
        absolute_temporal_extent.__init__(self, table, ident, start_time, end_time, timezone)

	self.set_granularity(granularity)
        self.set_map_time(map_time)

    def set_granularity(self, granularity):
	"""!Set the granularity of the space time dataset"""
	self.D["granularity"] = granularity

    def set_map_time(self, map_time):
	"""!Set the type of the map time

           Registered maps may have different types of time:
           Single point of time "point"
           Time intervals "interval"
           Or single point and interval time "mixed"

           This variable will be set automatically when maps are registered.
        """
	self.D["map_time"] = map_time

    def get_granularity(self):
	"""!Get the granularity of the space time dataset
	   @return None if not found"""
	if self.D.has_key("granularity"):
	    return self.D["granularity"]
        else:
	    return None

    def get_map_time(self):
	"""!Get the type of the map time

           Registered maps may have different types of time:
           Single point of time "point"
           Time intervals "interval"
           Or single point and interval time "mixed"

           This variable will be set automatically when maps are registered.
        """
	if self.D.has_key("map_time"):
	    return self.D["map_time"]
        else:
	    return None

    def print_info(self):
        """!Print information about this class in human readable style"""
        absolute_temporal_extent.print_info(self)
        #      0123456789012345678901234567890
        print " | Granularity:................ " + str(self.get_granularity())
        print " | Temporal type of maps:...... " + str(self.get_map_time())

    def print_shell_info(self):
        """!Print information about this class in shell style"""
        absolute_temporal_extent.print_shell_info(self)
        print "granularity=" + str(self.get_granularity())
        print "map_time=" + str(self.get_map_time())

###############################################################################

class strds_absolute_time(stds_absolute_time):
    def __init__(self, ident=None, start_time=None, end_time=None, granularity=None, timezone=None):
        stds_absolute_time.__init__(self, "strds_absolute_time", ident, start_time, end_time, granularity, timezone)

class str3ds_absolute_time(stds_absolute_time):
    def __init__(self, ident=None, start_time=None, end_time=None, granularity=None, timezone=None):
        stds_absolute_time.__init__(self, "str3ds_absolute_time", ident, start_time, end_time, granularity, timezone)

class stvds_absolute_time(stds_absolute_time):
    def __init__(self, ident=None, start_time=None, end_time=None, granularity=None, timezone=None):
        stds_absolute_time.__init__(self, "stvds_absolute_time", ident, start_time, end_time, granularity, timezone)

###############################################################################

class relative_temporal_extent(abstract_temporal_extent):
    """!This is the relative time class for all maps and spacetime datasets

       start_time and end_time must be of type integer
    """
    def __init__(self, table=None, ident=None, start_time=None, end_time=None, unit=None):

	abstract_temporal_extent.__init__(self, table, ident, start_time, end_time)
	self.D["unit"] = unit

    def set_unit(self, unit):
        """!Set the unit of the relative time. Valid units are:
           * years
           * months
           * days
           * hours
           * minutes
           * seconds
        """
	self.D["unit"] = unit

    def get_unit(self):
	"""!Get the unit of the relative time
	   @return None if not found"""
	if self.D.has_key("unit"):
	    return self.D["unit"]
        else:
	    return None

    def temporal_relation(self, map):
	"""!Returns the temporal relation between temporal objects
	   Temporal relationships are implemented after [Allen and Ferguson 1994 Actions and Events in Interval Temporal Logic]
	"""
        
        # Check units for relative time
        if not self.D.has_key("unit"):
            return None
        if not map.D.has_key("unit"):
            return None

        # Units must be equal
        if self.D["unit"] != map.D["unit"]:
            return None

	return abstract_temporal_extent.temporal_relation(self, map)

    def print_info(self):
        """!Print information about this class in human readable style"""
        #      0123456789012345678901234567890
        print " +-------------------- Relative time -----------------------------------------+"
        abstract_temporal_extent.print_info(self)
        print " | Relative time unit:......... " + str(self.get_unit())

    def print_shell_info(self):
        """!Print information about this class in shell style"""
        abstract_temporal_extent.print_shell_info(self)
        print "unit=" + str(self.get_unit())

###############################################################################

class raster_relative_time(relative_temporal_extent):
    def __init__(self, ident=None, start_time=None, end_time=None):
        relative_temporal_extent.__init__(self, "raster_relative_time", ident, start_time, end_time)

class raster3d_relative_time(relative_temporal_extent):
    def __init__(self, ident=None, start_time=None, end_time=None):
        relative_temporal_extent.__init__(self, "raster3d_relative_time", ident, start_time, end_time)

class vector_relative_time(relative_temporal_extent):
    def __init__(self, ident=None, start_time=None, end_time=None):
        relative_temporal_extent.__init__(self, "vector_relative_time", ident, start_time, end_time)
        
###############################################################################

class stds_relative_time(relative_temporal_extent):
    def __init__(self, table=None, ident=None, start_time=None, end_time=None, granularity=None, map_time=None):
        relative_temporal_extent.__init__(self, table, ident, start_time, end_time)

	self.set_granularity(granularity)
        self.set_map_time(map_time)

    def set_granularity(self, granularity):
	"""!Set the granularity of the space time dataset"""
	self.D["granularity"] = granularity

    def set_map_time(self, map_time):
	"""!Set the type of the map time

           Registered maps may have different types of time:
           Single point of time "point"
           Time intervals "interval"
           Or single point and interval time "mixed"

           This variable will be set automatically when maps are registered.
        """
	self.D["map_time"] = map_time

    def get_granularity(self):
	"""!Get the granularity of the space time dataset
	   @return None if not found"""
	if self.D.has_key("granularity"):
	    return self.D["granularity"]
        else:
	    return None

    def get_map_time(self):
	"""!Get the type of the map time

           Registered maps may have different types of time:
           Single point of time "point"
           Time intervals "interval"
           Or single point and interval time "mixed"

           This variable will be set automatically when maps are registered.
        """
	if self.D.has_key("map_time"):
	    return self.D["map_time"]
        else:
	    return None

    def print_info(self):
        """!Print information about this class in human readable style"""
        relative_temporal_extent.print_info(self)
        #      0123456789012345678901234567890
        print " | Granularity:................ " + str(self.get_granularity())
        print " | Temporal type of maps:...... " + str(self.get_map_time())

    def print_shell_info(self):
        """!Print information about this class in shell style"""
        relative_temporal_extent.print_shell_info(self)
        print "granularity=" + str(self.get_granularity())
        print "map_time=" + str(self.get_map_time())

###############################################################################

class strds_relative_time(stds_relative_time):
    def __init__(self, ident=None, start_time=None, end_time=None, granularity=None):
        stds_relative_time.__init__(self, "strds_relative_time", ident, start_time, end_time, granularity)

class str3ds_relative_time(stds_relative_time):
    def __init__(self, ident=None, start_time=None, end_time=None, granularity=None):
        stds_relative_time.__init__(self, "str3ds_relative_time", ident, start_time, end_time, granularity)

class stvds_relative_time(stds_relative_time):
    def __init__(self, ident=None, start_time=None, end_time=None, granularity=None):
        stds_relative_time.__init__(self, "stvds_relative_time", ident, start_time, end_time, granularity)
