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

# globals
_debug = 0
_log = ModuleLogger(globals())
pro_application = None
object_list = list()


@bacpypes_debugging
class ProApplication(BIPSimpleApplication, ReadWritePropertyMultipleServices, ChangeOfValueServices):
    pass


########################################################################################################################
# This task saves all writeable properties to database
#
# When a property is designated as writable or W, this shall mean that the property is required to be present in all
# BACnet standard objects of that type and that the value of the property can be changed through the use of one or more
# of the WriteProperty services defined in this standard. The value of W properties may be examined through the use of
# one or more of the ReadProperty services defined in this standard.
#
# NOTE: THIS TASK WILL PERSISTENT THE FOLLOWING OBJECT'S PROPERTIES,
#       THEY SHOULD BE UPDATED BY WRITE PROPERTY SERVICE.
# Analog Output Object      | Present_Value
# Binary Output Object      | Present_Value
# Multi-state Output Object | Present_Value
#
########################################################################################################################
@bacpypes_debugging
class Persistence(RecurringTask):

    def __init__(self, interval):
        if _debug:
            Persistence._debug("__init__ %r", interval)
        RecurringTask.__init__(self, interval * 1000)

        # save the interval
        self.interval = interval

        # connect to database
        self.cursor = None
        self.cnx = None
        try:
            self.cnx = mysql.connector.connect(**settings.xbacnet)
            self.cursor = self.cnx.cursor(dictionary=True)
        except Exception as e:
            _log.error("Error in WriteablePropertiesPersistence init " + str(e))
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
        global object_list
        if _debug:
            Persistence._debug("process_task")

        ################################################################################################################
        # STEP 1: Check database connectivity
        ################################################################################################################
        if not self.cursor or not self.cnx.is_connected():
            try:
                self.cnx = mysql.connector.connect(**settings.xbacnet)
                self.cursor = self.cnx.cursor(dictionary=True)
            except Exception as e:
                _log.error("Error in WriteablePropertiesPersistence process_task " + str(e))
                if self.cursor:
                    self.cursor.close()
                if self.cnx:
                    self.cnx.close()

        ################################################################################################################
        # STEP 2: Read writable properties of objects
        ################################################################################################################
        if _debug:
            Persistence._debug("STEP 2: Read writable properties of objects: " + str(object_list))
        analog_output_object_dict = dict()
        binary_output_object_dict = dict()
        multi_state_output_object_dict = dict()

        for i in range(len(object_list)):
            if object_list[i].objectType == 'analogOutput':
                analog_output_object_dict[object_list[i].objectIdentifier[1]] = object_list[i].presentValue
            elif object_list[i].objectType == 'binaryOutput':
                binary_output_object_dict[object_list[i].objectIdentifier[1]] = object_list[i].presentValue
            elif object_list[i].objectType == 'multiStateOutput':
                multi_state_output_object_dict[object_list[i].objectIdentifier[1]] = object_list[i].presentValue
            else:
                pass

        ################################################################################################################
        # STEP 3: Update properties to database
        ################################################################################################################

        if _debug:
            Persistence._debug("STEP 3: Update properties to database: " + str(object_list))

        if len(analog_output_object_dict) > 0:
            for object_identifier in analog_output_object_dict:
                try:
                    update = (" UPDATE tbl_analog_output_objects "
                              " SET present_value = %s "
                              " WHERE (object_identifier = %s ")
                    self.cursor.execute(update, (analog_output_object_dict[object_identifier],
                                                 object_identifier,))
                    self.cnx.commit()
                except Exception as e:
                    if self.cursor:
                        self.cursor.close()
                    if self.cnx:
                        self.cnx.close()

        if len(binary_output_object_dict) > 0:
            for object_identifier in binary_output_object_dict:
                try:
                    update = (" UPDATE tbl_binary_output_objects "
                              " SET present_value = %s "
                              " WHERE (object_identifier = %s ")
                    self.cursor.execute(update, (binary_output_object_dict[object_identifier],
                                                 object_identifier,))
                    self.cnx.commit()
                except Exception as e:
                    if self.cursor:
                        self.cursor.close()
                    if self.cnx:
                        self.cnx.close()

        if len(multi_state_output_object_dict) > 0:
            for object_identifier in multi_state_output_object_dict:
                try:
                    update = (" UPDATE tbl_multi_state_output_objects "
                              " SET present_value = %s "
                              " WHERE (object_identifier = %s ")
                    self.cursor.execute(update, (multi_state_output_object_dict[object_identifier],
                                                 object_identifier,))
                    self.cnx.commit()
                except Exception as e:
                    if self.cursor:
                        self.cursor.close()
                    if self.cnx:
                        self.cnx.close()

        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()

########################################################################################################################
# INTRODUCE:
# This task will refresh all readable properties from database
#
# NOTE: DO NOT REFRESH THE FOLLOWING OBJECT'S PROPERTIES.
#       THEY SHOULD BE UPDATED BY WRITE PROPERTY SERVICE.
# Analog Output Object      | Present_Value
# Binary Output Object      | Present_Value
# Multi-state Output Object | Present_Value
#
########################################################################################################################
@bacpypes_debugging
class Refreshing(RecurringTask):

    ####################################################################################################################
    # PROCEDURES:
    # STEP 1: Connect to the database
    ####################################################################################################################
    def __init__(self, interval):
        if _debug:
            Refreshing._debug("__init__ %r", interval)
        RecurringTask.__init__(self, interval * 1000)

        # save the interval
        self.interval = interval

        # connect to database
        self.cursor = None
        self.cnx = None
        try:
            self.cnx = mysql.connector.connect(**settings.xbacnet)
            self.cursor = self.cnx.cursor(dictionary=True)
        except Exception as e:
            _log.error("Error in  ReadablePropertiesRefreshing init " + str(e))
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
        global object_list
        if _debug:
            Refreshing._debug("process_task")

        if _debug:
            Refreshing._debug("before refresh object list: " + str(object_list))

        ################################################################################################################
        # STEP 1: Check database connectivity
        ################################################################################################################
        if not self.cursor or not self.cnx.is_connected():
            try:
                self.cnx = mysql.connector.connect(**settings.xbacnet)
                self.cursor = self.cnx.cursor(dictionary=True)
            except Exception as e:
                _log.error("Error in ReadablePropertiesRefreshing process_task " + str(e))
                if self.cursor:
                    self.cursor.close()
                if self.cnx:
                    self.cnx.close()

        ################################################################################################################
        # STEP 2: Read objects from database
        ################################################################################################################
        analog_input_object_dict = dict()
        analog_output_object_dict = dict()
        analog_value_object_dict = dict()
        binary_input_object_dict = dict()
        binary_output_object_dict = dict()
        binary_value_object_dict = dict()
        multi_state_input_object_dict = dict()
        multi_state_output_object_dict = dict()
        multi_state_value_object_dict = dict()

        # step 2.1
        # todo: recover once database server is available from system reboot
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
# PROCEDURES
# STEP1: Create the device and application
# STEP2: Get all objects from database
# STEP3: Create objects and append them to the application
# STEP4: Install tasks
# STEP5: Run the application
########################################################################################################################

def main():
    ####################################################################################################################
    # STEP1: Create the device and application
    ####################################################################################################################
    global pro_application, object_list
    # make a parser
    parser = ConfigArgumentParser(description=__doc__)

    # parse the command line arguments
    args = parser.parse_args()

    if _debug:
        _log.debug("initialization")
    if _debug:
        _log.debug("    - args: %r", args)

    # make a device object
    this_device = LocalDeviceObject(ini=args.ini)
    if _debug:
        _log.debug("    - this_device: %r", this_device)

    # make an application
    pro_application = ProApplication(this_device, args.ini.address)

    ####################################################################################################################
    # STEP2: Get all objects from database
    ####################################################################################################################
    analog_input_object_list = list()
    analog_output_object_list = list()
    analog_value_object_list = list()
    binary_input_object_list = list()
    binary_output_object_list = list()
    binary_value_object_list = list()
    multi_state_input_object_list = list()
    multi_state_output_object_list = list()
    multi_state_value_object_list = list()
    cursor = None
    cnx = None
    try:
        cnx = mysql.connector.connect(**settings.xbacnet)
        cursor = cnx.cursor(dictionary=True)
        # step 2.1
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, units, cov_increment "
                 " FROM tbl_analog_input_objects ")
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
                analog_input_object_list.append(result)
        if _debug:
            _log.debug(str(analog_input_object_list))

        # step 2.2
        query = (" SELECT id, object_identifier, object_name, present_value, description, status_flags, event_state, "
                 "        out_of_service, units, relinquish_default, current_command_priority, cov_increment "
                 " FROM tbl_analog_output_objects ")
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
        _log.error("Error in  main procedure " + str(e))
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    ####################################################################################################################
    # STEP3: Create objects and append them to the application
    ####################################################################################################################

    # step 3.1
    for result in analog_input_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])
        pro_object = AnalogInputObject(
            objectIdentifier=("analogInput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),
                         int(result['status_flags'][1]),
                         int(result['status_flags'][2]),
                         int(result['status_flags'][3])],
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            units=result['units'],
            covIncrement=result['cov_increment'],
        )
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # step 3.2
    for result in analog_output_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])
        # priority_array = PriorityArray()
        # for i in range(16):
        #     priority_array.append(PriorityValue(Integer(i)))
        pro_object = AnalogOutputObject(
            objectIdentifier=("analogOutput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),
                         int(result['status_flags'][1]),
                         int(result['status_flags'][2]),
                         int(result['status_flags'][3])],
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            units=result['units'],
            # priorityArray=priority_array,
            relinquishDefault=result['relinquish_default'],
            # currentCommandPriority=PriorityValue(Integer(8)),
            covIncrement=result['cov_increment'],
        )
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # step 3.3
    for result in analog_value_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])
        pro_object = AnalogValueObject(
            objectIdentifier=("analogValue", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),
                         int(result['status_flags'][1]),
                         int(result['status_flags'][2]),
                         int(result['status_flags'][3])],
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            units=result['units'],
            covIncrement=result['cov_increment'],
        )
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # step 3.4
    for result in binary_input_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])
        pro_object = BinaryInputObject(
            objectIdentifier=("binaryInput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),
                         int(result['status_flags'][1]),
                         int(result['status_flags'][2]),
                         int(result['status_flags'][3])],
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            polarity=result['polarity'],
        )
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # step 3.5
    for result in binary_output_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])
        pro_object = BinaryOutputObject(
            objectIdentifier=("binaryOutput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),
                         int(result['status_flags'][1]),
                         int(result['status_flags'][2]),
                         int(result['status_flags'][3])],
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            polarity=result['polarity'],
            relinquishDefault=result['relinquish_default'],
            # currentCommandPriority=result['current_command_priority'],
        )
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # step 3.6
    for result in binary_value_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])
        pro_object = BinaryValueObject(
            objectIdentifier=("binaryValue", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),
                         int(result['status_flags'][1]),
                         int(result['status_flags'][2]),
                         int(result['status_flags'][3])],
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
        )
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # step 3.7
    for result in multi_state_input_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])
        pro_object = MultiStateInputObject(
            objectIdentifier=("multiStateInput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),
                         int(result['status_flags'][1]),
                         int(result['status_flags'][2]),
                         int(result['status_flags'][3])],
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            numberOfStates=result['number_of_states'],
            stateText=result['state_text'],
        )
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # step 3.8
    for result in multi_state_output_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])
        pro_object = MultiStateOutputObject(
            objectIdentifier=("multiStateOutput", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),
                         int(result['status_flags'][1]),
                         int(result['status_flags'][2]),
                         int(result['status_flags'][3])],
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            numberOfStates=result['number_of_states'],
            stateText=result['state_text'],
            relinquishDefault=result['relinquish_default'],
            # currentCommandPriority=result['current_command_priority'],
        )
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    # step 3.9
    for result in multi_state_value_object_list:
        if _debug:
            _log.debug("    - creating: %r", result['object_name'])
        pro_object = MultiStateValueObject(
            objectIdentifier=("multiStateValue", result['object_identifier']),
            objectName=result['object_name'],
            presentValue=result['present_value'],
            description=result['description'],
            statusFlags=[int(result['status_flags'][0]),
                         int(result['status_flags'][1]),
                         int(result['status_flags'][2]),
                         int(result['status_flags'][3])],
            eventState=result['event_state'],
            outOfService=result['out_of_service'],
            numberOfStates=result['number_of_states'],
            stateText=result['state_text'],
        )
        pro_application.add_object(pro_object)
        object_list.append(pro_object)
        if _debug:
            _log.debug("    - created: %r", result['object_name'])

    if _debug:
        _log.debug("    - object list: %r", this_device.objectList)

    ####################################################################################################################
    # STEP4: Install tasks
    ####################################################################################################################
    Persistence(settings.PERSISTENCE_INTERVAL).install_task()
    Refreshing(settings.REFRESHING_INTERVAL).install_task()

    ####################################################################################################################
    # STEP5: Run the application
    ####################################################################################################################

    if _debug:
        _log.debug("running")

    run()

    if _debug:
        _log.debug("finish")


if __name__ == "__main__":
    main()
