"""
XBACnet Server - BACnet Protocol Implementation

This module implements a BACnet server that provides BACnet objects and services
for building automation and control systems. It supports various BACnet object types
including analog inputs/outputs, binary inputs/outputs, and multi-state objects.

The server integrates with a MySQL database for persistent storage of object properties
and provides automatic synchronization between the BACnet objects and database records.

Key Features:
- BACnet/IP communication protocol
- Multiple object type support (Analog, Binary, Multi-state)
- Database persistence for object properties
- Automatic property refresh from database
- Change of Value (COV) notifications
- Read/Write property services

Author: XBACnet Team
Date: 2024
"""

from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser
from bacpypes.core import run
from bacpypes.task import RecurringTask
from bacpypes.object import AnalogInputObject
from bacpypes.object import AnalogOutputObject
from bacpypes.object import AnalogValueObject
from bacpypes.object import BinaryInputObject
from bacpypes.object import BinaryOutputObject
from bacpypes.object import BinaryValueObject
from bacpypes.object import MultiStateInputObject
from bacpypes.object import MultiStateOutputObject
from bacpypes.object import MultiStateValueObject
from bacpypes.local.device import LocalDeviceObject
from bacpypes.app import BIPSimpleApplication
from bacpypes.service.cov import ChangeOfValueServices
from bacpypes.service.object import ReadWritePropertyMultipleServices
from bacpypes.basetypes import PriorityArray, PriorityValue
from bacpypes.primitivedata import Integer
import mysql.connector
import settings

# Global variables for debugging and application state
_debug = 0  # Debug level (0 = off, higher values = more verbose)
_log = ModuleLogger(globals())  # Logger for debugging and error messages
pro_application = None  # Main BACnet application instance
object_list = list()  # List of all BACnet objects managed by this server


@bacpypes_debugging
class ProApplication(BIPSimpleApplication, ReadWritePropertyMultipleServices, ChangeOfValueServices):
    """
    Main BACnet application class that combines multiple BACnet services.

    This class inherits from:
    - BIPSimpleApplication: Basic BACnet/IP application functionality
    - ReadWritePropertyMultipleServices: Support for reading/writing multiple properties
    - ChangeOfValueServices: Support for COV (Change of Value) notifications

    The application handles BACnet communication, property access, and value change notifications.
    """
    pass


########################################################################################################################
# Persistence Task - Saves Writable Properties to Database
#
# This task periodically saves all writable properties from BACnet objects to the database.
# According to BACnet standards, writable properties (marked as 'W') are required to be present
# in all BACnet standard objects of that type and can be changed through WriteProperty services.
#
# The task specifically handles the following writable object properties:
# - Analog Output Object: Present_Value
# - Binary Output Object: Present_Value
# - Multi-state Output Object: Present_Value
#
# These properties are updated when BACnet clients use WriteProperty services to change values.
# The persistence task ensures that these changes are saved to the database for reliability.
#
########################################################################################################################
@bacpypes_debugging
class Persistence(RecurringTask):

    def __init__(self, interval):
        """
        Initialize the persistence task with specified interval.

        Args:
            interval (int): Interval in seconds between persistence operations
        """
        if _debug:
            Persistence._debug("__init__ %r", interval)
        RecurringTask.__init__(self, interval * 1000)  # Convert seconds to milliseconds

        # Save the interval for reference
        self.interval = interval

        # Initialize database connection variables
        self.cursor = None
        self.cnx = None
        try:
            # Connect to MySQL database using settings configuration
            self.cnx = mysql.connector.connect(**settings.xbacnet)
            self.cursor = self.cnx.cursor(dictionary=True)  # Use dictionary cursor for named columns
        except Exception as e:
            _log.error("Error in WriteablePropertiesPersistence init " + str(e))
            # Clean up database connections on error
            if self.cursor:
                self.cursor.close()
            if self.cnx:
                self.cnx.close()

    ####################################################################################################################
    # PROCEDURES:
    # STEP 1: Check database connectivity
    # STEP 2: Read writable properties of objects
    # STEP 3: Update properties to database
    ####################################################################################################################
    def process_task(self):
        """
        Main task execution method that runs periodically.

        This method:
        1. Checks database connectivity and reconnects if necessary
        2. Reads current values of writable properties from BACnet objects
        3. Updates the database with the current property values
        """
        global object_list
        if _debug:
            Persistence._debug("process_task")

        ################################################################################################################
        # STEP 1: Check database connectivity
        ################################################################################################################
        # Verify database connection is still active, reconnect if needed
        if not self.cursor or not self.cnx.is_connected():
            try:
                # Reconnect to database
                self.cnx = mysql.connector.connect(**settings.xbacnet)
                self.cursor = self.cnx.cursor(dictionary=True)
            except Exception as e:
                _log.error("Error in WriteablePropertiesPersistence process_task " + str(e))
                # Clean up connections on error
                if self.cursor:
                    self.cursor.close()
                if self.cnx:
                    self.cnx.close()

        ################################################################################################################
        # STEP 2: Read writable properties of objects
        ################################################################################################################
        if _debug:
            Persistence._debug("STEP 2: Read writable properties of objects: " + str(object_list))

        # Initialize dictionaries to store current values of writable properties
        analog_output_object_dict = dict()      # Store analog output present values
        binary_output_object_dict = dict()      # Store binary output present values
        multi_state_output_object_dict = dict() # Store multi-state output present values

        # Iterate through all BACnet objects and extract writable properties
        for i in range(len(object_list)):
            if object_list[i].objectType == 'analogOutput':
                # Store analog output present value with object identifier as key
                analog_output_object_dict[object_list[i].objectIdentifier[1]] = object_list[i].presentValue
            elif object_list[i].objectType == 'binaryOutput':
                # Store binary output present value with object identifier as key
                binary_output_object_dict[object_list[i].objectIdentifier[1]] = object_list[i].presentValue
            elif object_list[i].objectType == 'multiStateOutput':
                # Store multi-state output present value with object identifier as key
                multi_state_output_object_dict[object_list[i].objectIdentifier[1]] = object_list[i].presentValue
            else:
                # Skip non-writable object types
                pass

        ################################################################################################################
        # STEP 3: Update properties to database
        ################################################################################################################

        if _debug:
            Persistence._debug("STEP 3: Update properties to database: " + str(object_list))

        # Update analog output objects in database
        if len(analog_output_object_dict) > 0:
            for object_identifier in analog_output_object_dict:
                try:
                    # Update present_value for analog output object
                    update = (" UPDATE tbl_analog_output_objects "
                              " SET present_value = %s "
                              " WHERE (object_identifier = %s ")
                    self.cursor.execute(update, (analog_output_object_dict[object_identifier],
                                                 object_identifier,))
                    self.cnx.commit()  # Commit the transaction
                except Exception as e:
                    # Handle database errors and clean up connections
                    if self.cursor:
                        self.cursor.close()
                    if self.cnx:
                        self.cnx.close()

        # Update binary output objects in database
        if len(binary_output_object_dict) > 0:
            for object_identifier in binary_output_object_dict:
                try:
                    # Update present_value for binary output object
                    update = (" UPDATE tbl_binary_output_objects "
                              " SET present_value = %s "
                              " WHERE (object_identifier = %s ")
                    self.cursor.execute(update, (binary_output_object_dict[object_identifier],
                                                 object_identifier,))
                    self.cnx.commit()  # Commit the transaction
                except Exception as e:
                    # Handle database errors and clean up connections
                    if self.cursor:
                        self.cursor.close()
                    if self.cnx:
                        self.cnx.close()

        # Update multi-state output objects in database
        if len(multi_state_output_object_dict) > 0:
            for object_identifier in multi_state_output_object_dict:
                try:
                    # Update present_value for multi-state output object
                    update = (" UPDATE tbl_multi_state_output_objects "
                              " SET present_value = %s "
                              " WHERE (object_identifier = %s ")
                    self.cursor.execute(update, (multi_state_output_object_dict[object_identifier],
                                                 object_identifier,))
                    self.cnx.commit()  # Commit the transaction
                except Exception as e:
                    # Handle database errors and clean up connections
                    if self.cursor:
                        self.cursor.close()
                    if self.cnx:
                        self.cnx.close()

        # Clean up database connections
        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()

########################################################################################################################
# Refreshing Task - Updates Readable Properties from Database
#
# This task periodically refreshes all readable properties of BACnet objects from the database.
# It ensures that the BACnet objects reflect the current state stored in the database.
#
# IMPORTANT: This task does NOT refresh the following writable properties:
# - Analog Output Object: Present_Value
# - Binary Output Object: Present_Value
# - Multi-state Output Object: Present_Value
#
# These properties should only be updated through BACnet WriteProperty services to maintain
# proper BACnet protocol compliance and avoid conflicts with client write operations.
#
########################################################################################################################
@bacpypes_debugging
class Refreshing(RecurringTask):

    ####################################################################################################################
    # PROCEDURES:
    # STEP 1: Connect to the database
    ####################################################################################################################
    def __init__(self, interval):
        """
        Initialize the refreshing task with specified interval.

        Args:
            interval (int): Interval in seconds between refresh operations
        """
        if _debug:
            Refreshing._debug("__init__ %r", interval)
        RecurringTask.__init__(self, interval * 1000)  # Convert seconds to milliseconds

        # Save the interval for reference
        self.interval = interval

        # Initialize database connection variables
        self.cursor = None
        self.cnx = None
        try:
            # Connect to MySQL database using settings configuration
            self.cnx = mysql.connector.connect(**settings.xbacnet)
            self.cursor = self.cnx.cursor(dictionary=True)  # Use dictionary cursor for named columns
        except Exception as e:
            _log.error("Error in  ReadablePropertiesRefreshing init " + str(e))
            # Clean up database connections on error
            if self.cursor:
                self.cursor.close()
            if self.cnx:
                self.cnx.close()

    ####################################################################################################################
    # PROCEDURES:
    # STEP 1: Check database connectivity
    # STEP 2: Read objects from database
    # STEP 3: Update properties of objects
    ####################################################################################################################
    def process_task(self):
        """
        Main task execution method that runs periodically.

        This method:
        1. Checks database connectivity and reconnects if necessary
        2. Reads all object properties from the database
        3. Updates the corresponding BACnet object properties
        """
        global object_list
        if _debug:
            Refreshing._debug("process_task")

        if _debug:
            Refreshing._debug("before refresh object list: " + str(object_list))

        ################################################################################################################
        # STEP 1: Check database connectivity
        ################################################################################################################
        # Verify database connection is still active, reconnect if needed
        if not self.cursor or not self.cnx.is_connected():
            try:
                # Reconnect to database
                self.cnx = mysql.connector.connect(**settings.xbacnet)
                self.cursor = self.cnx.cursor(dictionary=True)
            except Exception as e:
                _log.error("Error in ReadablePropertiesRefreshing process_task " + str(e))
                # Clean up connections on error
                if self.cursor:
                    self.cursor.close()
                if self.cnx:
                    self.cnx.close()

        ################################################################################################################
        # STEP 2: Read objects from database
        ################################################################################################################
        # Initialize dictionaries to store object properties from database
        analog_input_object_dict = dict()      # Analog input objects
        analog_output_object_dict = dict()     # Analog output objects
        analog_value_object_dict = dict()      # Analog value objects
        binary_input_object_dict = dict()      # Binary input objects
        binary_output_object_dict = dict()     # Binary output objects
        binary_value_object_dict = dict()      # Binary value objects
        multi_state_input_object_dict = dict() # Multi-state input objects
        multi_state_output_object_dict = dict() # Multi-state output objects
        multi_state_value_object_dict = dict() # Multi-state value objects

        # Step 2.1: Read analog input objects from database
        # TODO: Add recovery mechanism for database server availability after system reboot
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, units, cov_increment "
                 " FROM tbl_analog_input_objects ")
        self.cursor.execute(query)
        rows_objects = self.cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = float(row['present_value'])
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['units'] = row['units']
                result['cov_increment'] = float(row['cov_increment'])
                analog_input_object_dict[result['object_identifier']] = result

        if _debug:
            _log.debug(str(analog_input_object_dict))

        # step 2.2
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, units, relinquish_default, current_command_priority, cov_increment "
                 " FROM tbl_analog_output_objects ")
        self.cursor.execute(query)
        rows_objects = self.cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = float(row['present_value'])
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['units'] = row['units']
                result['relinquish_default'] = row['relinquish_default']
                result['current_command_priority'] = row['current_command_priority']
                result['cov_increment'] = float(row['cov_increment'])
                analog_output_object_dict[result['object_identifier']] = result
        if _debug:
            _log.debug(str(analog_output_object_dict))

        # step 2.3
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, units, cov_increment "
                 " FROM tbl_analog_value_objects ")
        self.cursor.execute(query)
        rows_objects = self.cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = float(row['present_value'])
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['units'] = row['units']
                result['cov_increment'] = float(row['cov_increment'])
                analog_value_object_dict[result['object_identifier']] = result
        if _debug:
            _log.debug(str(analog_value_object_dict))

        # step 2.4
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, polarity "
                 " FROM tbl_binary_input_objects ")
        self.cursor.execute(query)
        rows_objects = self.cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['polarity'] = row['polarity']
                binary_input_object_dict[result['object_identifier']] = result
        if _debug:
            _log.debug(str(binary_input_object_dict))

        # step 2.5
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, polarity, relinquish_default, current_command_priority  "
                 " FROM tbl_binary_output_objects ")
        self.cursor.execute(query)
        rows_objects = self.cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['polarity'] = row['polarity']
                result['relinquish_default'] = row['relinquish_default']
                result['current_command_priority'] = row['current_command_priority']
                binary_output_object_dict[result['object_identifier']] = result
        if _debug:
            _log.debug(str(binary_output_object_dict))

        # step 2.6
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service "
                 " FROM tbl_binary_value_objects ")
        self.cursor.execute(query)
        rows_objects = self.cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                binary_value_object_dict[result['object_identifier']] = result
        if _debug:
            _log.debug(str(binary_value_object_dict))

        # step 2.7
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, number_of_states, state_text "
                 " FROM tbl_multi_state_input_objects ")
        self.cursor.execute(query)
        rows_objects = self.cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['number_of_states'] = row['number_of_states']
                if (row['state_text'] is not None and
                        isinstance(row['state_text'], str) and
                        len(row['state_text']) > 0):
                    result['state_text'] = str(row['state_text']).split(";")
                else:
                    result['state_text'] = None
                multi_state_input_object_dict[result['object_identifier']] = result
        if _debug:
            _log.debug(str(multi_state_input_object_dict))

        # step 2.8
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, number_of_states, state_text, relinquish_default, current_command_priority "
                 " FROM tbl_multi_state_output_objects ")
        self.cursor.execute(query)
        rows_objects = self.cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['number_of_states'] = row['number_of_states']
                if (row['state_text'] is not None and
                        isinstance(row['state_text'], str) and
                        len(row['state_text']) > 0):
                    result['state_text'] = str(row['state_text']).split(";")
                else:
                    result['state_text'] = None
                result['relinquish_default'] = row['relinquish_default']
                result['current_command_priority'] = row['current_command_priority']
                multi_state_output_object_dict[result['object_identifier']] = result
        if _debug:
            _log.debug(str(multi_state_output_object_dict))

        # step 2.9
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, number_of_states, state_text "
                 " FROM tbl_multi_state_value_objects ")
        self.cursor.execute(query)
        rows_objects = self.cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['number_of_states'] = row['number_of_states']
                if (row['state_text'] is not None and
                        isinstance(row['state_text'], str) and
                        len(row['state_text']) > 0):
                    result['state_text'] = str(row['state_text']).split(";")
                else:
                    result['state_text'] = None
                multi_state_value_object_dict[result['object_identifier']] = result
        if _debug:
            _log.debug(str(multi_state_value_object_dict))

        ################################################################################################################
        # STEP 3: Update properties of objects
        ################################################################################################################
        for i in range(len(object_list)):

            if object_list[i].objectType == 'analogInput':
                # step 3.1
                result = analog_input_object_dict.get(object_list[i].objectIdentifier[1], None)
                if result is not None:
                    object_list[i].objectName = result['object_name']
                    object_list[i].presentValue = result['present_value']
                    object_list[i].description = result['description']
                    object_list[i].statusFlags = [int(result['status_flags'][0]),
                                                      int(result['status_flags'][1]),
                                                      int(result['status_flags'][2]),
                                                      int(result['status_flags'][3])]
                    object_list[i].eventState = result['event_state']
                    object_list[i].outOfService = result['out_of_service']
                    object_list[i].units = result['units']
                    object_list[i].covIncrement = result['cov_increment']
            elif object_list[i].objectType == 'analogOutput':
                # step 3.2
                result = analog_output_object_dict.get(object_list[i].objectIdentifier[1], None)
                if result is not None:
                    object_list[i].objectName = result['object_name']
                    # NOTE: DO NOT REFRESH PRESENT VALUE OF ANALOG OUTPUT OBJECT
                    object_list[i].description = result['description']
                    object_list[i].statusFlags = [int(result['status_flags'][0]),
                                                  int(result['status_flags'][1]),
                                                  int(result['status_flags'][2]),
                                                  int(result['status_flags'][3])]
                    object_list[i].eventState = result['event_state']
                    object_list[i].outOfService = result['out_of_service']
                    object_list[i].units = result['units']
                    object_list[i].relinquishDefault = result['relinquish_default']
                    # object_list[i].currentCommandPriority = result['current_command_priority']
                    object_list[i].covIncrement = result['cov_increment']
            elif object_list[i].objectType == 'analogValue':
                # step 3.3
                result = analog_value_object_dict.get(object_list[i].objectIdentifier[1], None)
                if result is not None:
                    object_list[i].objectName = result['object_name']
                    object_list[i].presentValue = result['present_value']
                    object_list[i].description = result['description']
                    object_list[i].statusFlags = [int(result['status_flags'][0]),
                                                  int(result['status_flags'][1]),
                                                  int(result['status_flags'][2]),
                                                  int(result['status_flags'][3])]
                    object_list[i].eventState = result['event_state']
                    object_list[i].outOfService = result['out_of_service']
                    object_list[i].units = result['units']
                    object_list[i].covIncrement = result['cov_increment']
            elif object_list[i].objectType == 'binaryInput':
                # step 3.4
                result = binary_input_object_dict.get(object_list[i].objectIdentifier[1], None)
                if result is not None:
                    object_list[i].objectName = result['object_name']
                    object_list[i].presentValue = result['present_value']
                    object_list[i].description = result['description']
                    object_list[i].statusFlags = [int(result['status_flags'][0]),
                                                  int(result['status_flags'][1]),
                                                  int(result['status_flags'][2]),
                                                  int(result['status_flags'][3])]
                    object_list[i].eventState = result['event_state']
                    object_list[i].outOfService = result['out_of_service']
                    object_list[i].polarity = result['polarity']
            elif object_list[i].objectType == 'binaryOutput':
                # step 3.5
                result = binary_output_object_dict.get(object_list[i].objectIdentifier[1], None)
                if result is not None:
                    object_list[i].objectName = result['object_name']
                    # NOTE: DO NOT REFRESH PRESENT VALUE OF BINARY OUTPUT OBJECT
                    object_list[i].description = result['description']
                    object_list[i].statusFlags = [int(result['status_flags'][0]),
                                                  int(result['status_flags'][1]),
                                                  int(result['status_flags'][2]),
                                                  int(result['status_flags'][3])]
                    object_list[i].eventState = result['event_state']
                    object_list[i].outOfService = result['out_of_service']
                    object_list[i].polarity = result['polarity']
                    object_list[i].relinquishDefault = result['relinquish_default']
                    # object_list[i].currentCommandPriority = result['current_command_priority']
            elif object_list[i].objectType == 'binaryValue':
                # step 3.6
                result = binary_value_object_dict.get(object_list[i].objectIdentifier[1], None)
                if result is not None:
                    object_list[i].objectName = result['object_name']
                    object_list[i].presentValue = result['present_value']
                    object_list[i].description = result['description']
                    object_list[i].statusFlags = [int(result['status_flags'][0]),
                                                  int(result['status_flags'][1]),
                                                  int(result['status_flags'][2]),
                                                  int(result['status_flags'][3])]
                    object_list[i].eventState = result['event_state']
                    object_list[i].outOfService = result['out_of_service']
            elif object_list[i].objectType == 'multiStateInput':
                # step 3.7
                result = multi_state_input_object_dict.get(object_list[i].objectIdentifier[1], None)
                if result is not None:
                    object_list[i].objectName = result['object_name']
                    object_list[i].presentValue = result['present_value']
                    object_list[i].description = result['description']
                    object_list[i].statusFlags = [int(result['status_flags'][0]),
                                                  int(result['status_flags'][1]),
                                                  int(result['status_flags'][2]),
                                                  int(result['status_flags'][3])]
                    object_list[i].eventState = result['event_state']
                    object_list[i].outOfService = result['out_of_service']
                    object_list[i].numberOfStates = result['number_of_states']
                    object_list[i].stateText = result['state_text']
            elif object_list[i].objectType == 'multiStateOutput':
                # step 3.8
                result = multi_state_output_object_dict.get(object_list[i].objectIdentifier[1], None)
                if result is not None:
                    object_list[i].objectName = result['object_name']
                    # NOTE: DO NOT REFRESH PRESENT VALUE OF MULTI STATE OUTPUT OBJECT
                    object_list[i].description = result['description']
                    object_list[i].statusFlags = [int(result['status_flags'][0]),
                                                  int(result['status_flags'][1]),
                                                  int(result['status_flags'][2]),
                                                  int(result['status_flags'][3])]
                    object_list[i].eventState = result['event_state']
                    object_list[i].outOfService = result['out_of_service']
                    object_list[i].numberOfStates = result['number_of_states']
                    object_list[i].stateText = result['state_text']
                    object_list[i].relinquishDefault = result['relinquish_default']
                    # object_list[i].currentCommandPriority = result['current_command_priority']
            elif object_list[i].objectType == 'multiStateValue':
                # step 3.9
                result = multi_state_value_object_dict.get(object_list[i].objectIdentifier[1], None)
                if result is not None:
                    object_list[i].objectName = result['object_name']
                    object_list[i].presentValue = result['present_value']
                    object_list[i].description = result['description']
                    object_list[i].statusFlags = [int(result['status_flags'][0]),
                                                  int(result['status_flags'][1]),
                                                  int(result['status_flags'][2]),
                                                  int(result['status_flags'][3])]
                    object_list[i].eventState = result['event_state']
                    object_list[i].outOfService = result['out_of_service']
                    object_list[i].numberOfStates = result['number_of_states']
                    object_list[i].stateText = result['state_text']
            else:
                pass

        if _debug:
            Refreshing._debug("after refresh object list: " + str(object_list))

        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()


########################################################################################################################
# Main Application Procedures
# STEP1: Create the device and application
# STEP2: Get all objects from database
# STEP3: Create objects and append them to the application
# STEP4: Install tasks
# STEP5: Run the application
########################################################################################################################

def main():
    """
    Main function that initializes and runs the BACnet server.

    This function:
    1. Creates the BACnet device and application
    2. Loads all objects from the database
    3. Creates BACnet objects and adds them to the application
    4. Installs background tasks for persistence and refreshing
    5. Starts the BACnet server
    """
    ####################################################################################################################
    # STEP1: Create the device and application
    ####################################################################################################################
    global pro_application, object_list

    # Create command line argument parser
    parser = ConfigArgumentParser(description=__doc__)

    # Parse the command line arguments
    args = parser.parse_args()

    if _debug:
        _log.debug("initialization")
    if _debug:
        _log.debug("    - args: %r", args)

    # Create the local BACnet device object
    this_device = LocalDeviceObject(ini=args.ini)
    if _debug:
        _log.debug("    - this_device: %r", this_device)

    # Create the main BACnet application
    pro_application = ProApplication(this_device, args.ini.address)

    ####################################################################################################################
    # STEP2: Get all objects from database
    ####################################################################################################################
    # Initialize lists to store object data from database
    analog_input_object_list = list()      # Analog input objects
    analog_output_object_list = list()     # Analog output objects
    analog_value_object_list = list()      # Analog value objects
    binary_input_object_list = list()      # Binary input objects
    binary_output_object_list = list()     # Binary output objects
    binary_value_object_list = list()      # Binary value objects
    multi_state_input_object_list = list() # Multi-state input objects
    multi_state_output_object_list = list() # Multi-state output objects
    multi_state_value_object_list = list() # Multi-state value objects

    # Initialize database connection variables
    cursor = None
    cnx = None
    try:
        # Connect to MySQL database
        cnx = mysql.connector.connect(**settings.xbacnet)
        cursor = cnx.cursor(dictionary=True)  # Use dictionary cursor for named columns
        # Step 2.1: Query analog input objects from database
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, units, cov_increment "
                 " FROM tbl_analog_input_objects ")
        cursor.execute(query)
        rows_objects = cursor.fetchall()

        # Process analog input objects if any exist
        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))

                # Create dictionary with object properties
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = float(row['present_value'])
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['units'] = row['units']
                result['cov_increment'] = float(row['cov_increment'])
                analog_input_object_list.append(result)
        if _debug:
            _log.debug(str(analog_input_object_list))

        # Step 2.2: Query analog output objects from database
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, units, relinquish_default, current_command_priority, cov_increment "
                 " FROM tbl_analog_output_objects ")
        cursor.execute(query)
        rows_objects = cursor.fetchall()

        # Process analog output objects if any exist
        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))

                # Create dictionary with object properties
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = float(row['present_value'])
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['units'] = row['units']
                result['relinquish_default'] = row['relinquish_default']
                result['current_command_priority'] = row['current_command_priority']
                result['cov_increment'] = float(row['cov_increment'])
                analog_output_object_list.append(result)
        if _debug:
            _log.debug(str(analog_output_object_list))

        # step 2.3
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, units, cov_increment "
                 " FROM tbl_analog_value_objects ")
        cursor.execute(query)
        rows_objects = cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = float(row['present_value'])
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['units'] = row['units']
                result['cov_increment'] = float(row['cov_increment'])
                analog_value_object_list.append(result)
        if _debug:
            _log.debug(str(analog_value_object_list))

        # step 2.4
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, polarity "
                 " FROM tbl_binary_input_objects ")
        cursor.execute(query)
        rows_objects = cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['polarity'] = row['polarity']
                binary_input_object_list.append(result)
        if _debug:
            _log.debug(str(binary_input_object_list))

        # step 2.5
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, polarity, relinquish_default, current_command_priority  "
                 " FROM tbl_binary_output_objects ")
        cursor.execute(query)
        rows_objects = cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['polarity'] = row['polarity']
                result['relinquish_default'] = row['relinquish_default']
                result['current_command_priority'] = row['current_command_priority']
                binary_output_object_list.append(result)
        if _debug:
            _log.debug(str(binary_output_object_list))

        # step 2.6
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service "
                 " FROM tbl_binary_value_objects ")
        cursor.execute(query)
        rows_objects = cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                binary_value_object_list.append(result)
        if _debug:
            _log.debug(str(binary_value_object_list))

        # step 2.7
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, number_of_states, state_text "
                 " FROM tbl_multi_state_input_objects ")
        cursor.execute(query)
        rows_objects = cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['number_of_states'] = row['number_of_states']
                if (row['state_text'] is not None and
                        isinstance(row['state_text'], str) and
                        len(row['state_text']) > 0):
                    result['state_text'] = str(row['state_text']).split(";")
                else:
                    result['state_text'] = None
                multi_state_input_object_list.append(result)
        if _debug:
            _log.debug(str(multi_state_input_object_list))

        # step 2.8
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, number_of_states, state_text, relinquish_default, current_command_priority "
                 " FROM tbl_multi_state_output_objects ")
        cursor.execute(query)
        rows_objects = cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['number_of_states'] = row['number_of_states']
                if (row['state_text'] is not None and
                        isinstance(row['state_text'], str) and
                        len(row['state_text']) > 0):
                    result['state_text'] = str(row['state_text']).split(";")
                else:
                    result['state_text'] = None
                result['relinquish_default'] = row['relinquish_default']
                result['current_command_priority'] = row['current_command_priority']
                multi_state_output_object_list.append(result)
        if _debug:
            _log.debug(str(multi_state_output_object_list))

        # step 2.9
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, number_of_states, state_text "
                 " FROM tbl_multi_state_value_objects ")
        cursor.execute(query)
        rows_objects = cursor.fetchall()

        if rows_objects is not None and len(rows_objects) > 0:
            for row in rows_objects:
                if _debug:
                    _log.debug(str(row))
                result = dict()
                result['id'] = row['id']
                result['object_identifier'] = int(row['object_identifier'])
                result['object_name'] = row['object_name']
                result['present_value'] = row['present_value']
                result['description'] = row['description']
                result['status_flags'] = row['status_flags']
                result['event_state'] = row['event_state']
                result['out_of_service'] = bool(row['out_of_service'])
                result['number_of_states'] = row['number_of_states']
                if (row['state_text'] is not None and
                        isinstance(row['state_text'], str) and
                        len(row['state_text']) > 0):
                    result['state_text'] = str(row['state_text']).split(";")
                else:
                    result['state_text'] = None
                multi_state_value_object_list.append(result)
        if _debug:
            _log.debug(str(multi_state_value_object_list))
    except Exception as e:
        # Handle database connection errors
        _log.error("Error in  main procedure " + str(e))
    finally:
        # Always clean up database connections
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    ####################################################################################################################
    # STEP3: Create objects and append them to the application
    ####################################################################################################################

    # Step 3.1: Create analog input objects
    for result in analog_input_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])

        # Create analog input BACnet object with properties from database
        pro_object = AnalogInputObject(
            objectIdentifier=("analogInput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),  # In Alarm
                         int(result['status_flags'][1]),  # Fault
                         int(result['status_flags'][2]),  # Overridden
                         int(result['status_flags'][3])], # Out of Service
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            units=result['units'],
            covIncrement=result['cov_increment'],
        )
        # Add object to BACnet application and global object list
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # Step 3.2: Create analog output objects
    for result in analog_output_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])

        # Note: Priority array functionality is commented out but available for future use
        # priority_array = PriorityArray()
        # for i in range(16):
        #     priority_array.append(PriorityValue(Integer(i)))

        # Create analog output BACnet object with properties from database
        pro_object = AnalogOutputObject(
            objectIdentifier=("analogOutput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),  # In Alarm
                         int(result['status_flags'][1]),  # Fault
                         int(result['status_flags'][2]),  # Overridden
                         int(result['status_flags'][3])], # Out of Service
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            units=result['units'],
            # priorityArray=priority_array,  # Priority array for command priority
            relinquishDefault=result['relinquish_default'],
            # currentCommandPriority=PriorityValue(Integer(8)),  # Current command priority
            covIncrement=result['cov_increment'],
        )
        # Add object to BACnet application and global object list
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # Step 3.3: Create analog value objects
    for result in analog_value_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])

        # Create analog value BACnet object with properties from database
        pro_object = AnalogValueObject(
            objectIdentifier=("analogValue", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),  # In Alarm
                         int(result['status_flags'][1]),  # Fault
                         int(result['status_flags'][2]),  # Overridden
                         int(result['status_flags'][3])], # Out of Service
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            units=result['units'],
            covIncrement=result['cov_increment'],
        )
        # Add object to BACnet application and global object list
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # Step 3.4: Create binary input objects
    for result in binary_input_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])

        # Create binary input BACnet object with properties from database
        pro_object = BinaryInputObject(
            objectIdentifier=("binaryInput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),  # In Alarm
                         int(result['status_flags'][1]),  # Fault
                         int(result['status_flags'][2]),  # Overridden
                         int(result['status_flags'][3])], # Out of Service
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            polarity=result['polarity'],  # Normal or Reverse polarity
        )
        # Add object to BACnet application and global object list
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # Step 3.5: Create binary output objects
    for result in binary_output_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])

        # Create binary output BACnet object with properties from database
        pro_object = BinaryOutputObject(
            objectIdentifier=("binaryOutput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),  # In Alarm
                         int(result['status_flags'][1]),  # Fault
                         int(result['status_flags'][2]),  # Overridden
                         int(result['status_flags'][3])], # Out of Service
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            polarity=result['polarity'],  # Normal or Reverse polarity
            relinquishDefault=result['relinquish_default'],
            # currentCommandPriority=result['current_command_priority'],  # Command priority
        )
        # Add object to BACnet application and global object list
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # Step 3.6: Create binary value objects
    for result in binary_value_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])

        # Create binary value BACnet object with properties from database
        pro_object = BinaryValueObject(
            objectIdentifier=("binaryValue", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),  # In Alarm
                         int(result['status_flags'][1]),  # Fault
                         int(result['status_flags'][2]),  # Overridden
                         int(result['status_flags'][3])], # Out of Service
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
        )
        # Add object to BACnet application and global object list
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # Step 3.7: Create multi-state input objects
    for result in multi_state_input_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])

        # Create multi-state input BACnet object with properties from database
        pro_object = MultiStateInputObject(
            objectIdentifier=("multiStateInput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),  # In Alarm
                         int(result['status_flags'][1]),  # Fault
                         int(result['status_flags'][2]),  # Overridden
                         int(result['status_flags'][3])], # Out of Service
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            numberOfStates=result['number_of_states'],
            stateText=result['state_text'],  # Array of state text descriptions
        )
        # Add object to BACnet application and global object list
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # Step 3.8: Create multi-state output objects
    for result in multi_state_output_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])

        # Create multi-state output BACnet object with properties from database
        pro_object = MultiStateOutputObject(
            objectIdentifier=("multiStateOutput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),  # In Alarm
                         int(result['status_flags'][1]),  # Fault
                         int(result['status_flags'][2]),  # Overridden
                         int(result['status_flags'][3])], # Out of Service
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            numberOfStates=result['number_of_states'],
            stateText=result['state_text'],  # Array of state text descriptions
            relinquishDefault=result['relinquish_default'],
            # currentCommandPriority=result['current_command_priority'],  # Command priority
        )
        # Add object to BACnet application and global object list
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # Step 3.9: Create multi-state value objects
    for result in multi_state_value_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])

        # Create multi-state value BACnet object with properties from database
        pro_object = MultiStateValueObject(
            objectIdentifier=("multiStateValue", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),  # In Alarm
                         int(result['status_flags'][1]),  # Fault
                         int(result['status_flags'][2]),  # Overridden
                         int(result['status_flags'][3])], # Out of Service
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            numberOfStates=result['number_of_states'],
            stateText=result['state_text'],  # Array of state text descriptions
        )
        # Add object to BACnet application and global object list
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    if _debug:
        _log.debug("    - object list: %r", this_device.objectList)

    ####################################################################################################################
    # STEP4: Install tasks
    ####################################################################################################################
    # Install persistence task to save writable properties to database
    Persistence(settings.PERSISTENCE_INTERVAL).install_task()

    # Install refreshing task to update readable properties from database
    Refreshing(settings.REFRESHING_INTERVAL).install_task()

    ####################################################################################################################
    # STEP5: Run the application
    ####################################################################################################################

    if _debug:
        _log.debug("running")

    # Start the BACnet server - this blocks until the server is stopped
    run()

    if _debug:
        _log.debug("finish")


if __name__ == "__main__":
    # Entry point - run the main function when script is executed directly
    main()
