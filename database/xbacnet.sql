-- XBACnet Database

-- ---------------------------------------------------------------------------------------------------------------------
-- Schema xbacnet
-- ---------------------------------------------------------------------------------------------------------------------
DROP DATABASE IF EXISTS `xbacnet` ;
CREATE DATABASE IF NOT EXISTS `xbacnet` ;
USE `xbacnet` ;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_logs`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_logs` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_logs` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `utc_date_time` DATETIME NOT NULL,
  `activity` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_analog_input_objects`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_analog_input_objects` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_analog_input_objects` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `object_identifier` BIGINT NOT NULL,
  `object_name` VARCHAR(255) NOT NULL,
  `present_value` DECIMAL(18, 3) NOT NULL,
  `description` VARCHAR(255),
  `status_flags` CHAR(4) NOT NULL COMMENT 'The four flags are {IN_ALARM, FAULT,
  OVERRIDDEN, OUT_OF_SERVICE} ',
  `event_state` VARCHAR(32)  NOT NULL,
  `out_of_service` BOOLEAN NOT NULL,
  `units` VARCHAR(255)  NOT NULL,
  `cov_increment` DECIMAL(18, 3),
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_analog_input_objects`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;
INSERT INTO `xbacnet`.`tbl_analog_input_objects`(`id`, `object_identifier`, `object_name`,
  `present_value`, `description`,`status_flags`, `event_state`, `out_of_service`, `units`,
  `cov_increment` )
VALUES
  (1, 10001,'Sample_1_AI',0, null, '0000',  'normal', false, 'kilowattHours',1.00);
COMMIT;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_analog_output_objects`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_analog_output_objects` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_analog_output_objects` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `object_identifier` BIGINT NOT NULL,
  `object_name` VARCHAR(255) NOT NULL,
  `present_value` DECIMAL(18, 3) NOT NULL COMMENT 'Commandable, W',
  `description` VARCHAR(255),
  `status_flags` CHAR(4) NOT NULL COMMENT 'The four flags are {IN_ALARM, FAULT,
  OVERRIDDEN, OUT_OF_SERVICE} ',
  `event_state` VARCHAR(32)  NOT NULL,
  `out_of_service` BOOLEAN NOT NULL,
  `units` VARCHAR(255)  NOT NULL,
  `relinquish_default` DECIMAL(18, 3) NOT NULL COMMENT 'This property is the default value
  to be used for the Present_Value property when all command priority values in the Priority_Array
  property have a NULL value',
  `current_command_priority` INT COMMENT 'The value of this property shall be equal to the
  index of the entry in the Priority_Array from which the Present_Value\'s value has been taken.
  If Present_Value has taken on the value of Relinquish_Default, this property shall have the value
  Null.',
  `cov_increment` DECIMAL(18, 3),
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_analog_output_objects`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;
INSERT INTO `xbacnet`.`tbl_analog_output_objects`(`id`, `object_identifier`, `object_name`,
  `present_value`, `description`,`status_flags`, `event_state`, `out_of_service`, `units`,
  `relinquish_default`, `current_command_priority`, `cov_increment` )
VALUES
  (1, 20001, 'Sample_2_AO', 0, null, '0000',  'normal', false, 'kilowattHours', 0, null, 1.00);
COMMIT;


-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_analog_value_objects`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_analog_value_objects` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_analog_value_objects` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `object_identifier` BIGINT NOT NULL,
  `object_name` VARCHAR(255) NOT NULL,
  `present_value` DECIMAL(18, 3) NOT NULL,
  `description` VARCHAR(255),
  `status_flags` CHAR(4) NOT NULL COMMENT 'The four flags are {IN_ALARM, FAULT,
  OVERRIDDEN, OUT_OF_SERVICE} ',
  `event_state` VARCHAR(32)  NOT NULL,
  `out_of_service` BOOLEAN NOT NULL,
  `units` VARCHAR(255)  NOT NULL,
  `cov_increment` DECIMAL(18, 3),
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_analog_value_objects`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;
INSERT INTO `xbacnet`.`tbl_analog_value_objects`(`id`, `object_identifier`, `object_name`,
  `present_value`, `description`,`status_flags`, `event_state`, `out_of_service`, `units`,
  `cov_increment` )
VALUES
  (1, 30001, 'Sample_3_AV', 0, null, '0000',  'normal', false, 'kilowattHours',1.00);
COMMIT;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_binary_input_objects`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_binary_input_objects` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_binary_input_objects` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `object_identifier` BIGINT NOT NULL,
  `object_name` VARCHAR(255) NOT NULL,
  `present_value` VARCHAR(8) NOT NULL COMMENT 'The logical state of the Input shall be
  either INACTIVE or ACTIVE. The relationship between the Present_Value and the physical state
  of the Input is determined by the Polarity property.',
  `description` VARCHAR(255),
  `status_flags` CHAR(4) NOT NULL COMMENT 'The four flags are {IN_ALARM, FAULT,
  OVERRIDDEN, OUT_OF_SERVICE} ',
  `event_state` VARCHAR(32)  NOT NULL,
  `out_of_service` BOOLEAN NOT NULL COMMENT 'This property is an indication whether
  (TRUE) or not (FALSE) the physical input that the object represents is not in service.',
  `polarity` VARCHAR(8) NOT NULL COMMENT 'This property indicates the relationship
  between the physical state of the Input and the logical state represented by the Present_Value
  property. If the Polarity property is NORMAL, then the ACTIVE state of the Present_Value
  property is also the ACTIVE or ON state of the physical Input as long as Out_Of_Service is
  FALSE. If the Polarity property is REVERSE, then the ACTIVE state of the Present_Value
  property is the INACTIVE or OFF state of the physical Input as long as Out_Of_Service is
  FALSE.',
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_binary_input_objects`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;
INSERT INTO `xbacnet`.`tbl_binary_input_objects`(`id`, `object_identifier`, `object_name`,
  `present_value`, `description`,`status_flags`, `event_state`, `out_of_service`, `polarity` )
VALUES
  (1, 40001, 'Sample_4_BI', 'active', null, '0000',  'normal', false, 'normal');
COMMIT;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_binary_output_objects`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_binary_output_objects` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_binary_output_objects` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `object_identifier` BIGINT NOT NULL,
  `object_name` VARCHAR(255) NOT NULL,
  `present_value` VARCHAR(8) NOT NULL COMMENT 'The logical state of the Input shall be
  either INACTIVE or ACTIVE. The relationship between the Present_Value and the physical state
  of the output is determined by the Polarity property.',
  `description` VARCHAR(255),
  `status_flags` CHAR(4) NOT NULL COMMENT 'The four flags are {IN_ALARM, FAULT,
  OVERRIDDEN, OUT_OF_SERVICE} ',
  `event_state` VARCHAR(32)  NOT NULL,
  `out_of_service` BOOLEAN NOT NULL COMMENT 'This property is an indication whether
  (TRUE) or not (FALSE) the physical input that the object represents is not in service.',
  `polarity` VARCHAR(8) NOT NULL COMMENT 'This property indicates the relationship
  between the physical state of the output and the logical state represented by the Present_Value
  property. If the Polarity property is NORMAL, then the ACTIVE state of the Present_Value
  property is also the ACTIVE or ON state of the physical output as long as Out_Of_Service is
  FALSE. If the Polarity property is REVERSE, then the ACTIVE state of the Present_Value
  property is the INACTIVE or OFF state of the physical output as long as Out_Of_Service is
  FALSE.',
  `relinquish_default` VARCHAR(8) NOT NULL COMMENT 'This property is the default value
  to be used for the Present_Value property when all command priority values in the Priority_Array
  property have a NULL value',
  `current_command_priority` INT COMMENT 'The value of this property shall be equal to the
  index of the entry in the Priority_Array from which the Present_Value\'s value has been taken.
  If Present_Value has taken on the value of Relinquish_Default, this property shall have the value
  Null.',
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_binary_output_objects`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;
INSERT INTO `xbacnet`.`tbl_binary_output_objects`(`id`, `object_identifier`, `object_name`,
  `present_value`, `description`,`status_flags`, `event_state`, `out_of_service`, `polarity`,
  `relinquish_default`, `current_command_priority`)
VALUES
  (1, 50001, 'Sample_5_BO', 'active', null, '0000', 'normal', false, 'normal', 'active', null);
COMMIT;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_binary_value_objects`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_binary_value_objects` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_binary_value_objects` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `object_identifier` BIGINT NOT NULL,
  `object_name` VARCHAR(255) NOT NULL,
  `present_value` VARCHAR(8) NOT NULL COMMENT 'The logical state of the Input shall be
  either INACTIVE or ACTIVE. The relationship between the Present_Value and the physical state
  of the Input is determined by the Polarity property.',
  `description` VARCHAR(255),
  `status_flags` CHAR(4) NOT NULL COMMENT 'The four flags are {IN_ALARM, FAULT,
  OVERRIDDEN, OUT_OF_SERVICE} ',
  `event_state` VARCHAR(32)  NOT NULL,
  `out_of_service` BOOLEAN NOT NULL COMMENT 'This property is an indication whether
  (TRUE) or not (FALSE) the physical input that the object represents is not in service.',
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_binary_value_objects`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;
INSERT INTO `xbacnet`.`tbl_binary_value_objects`(`id`, `object_identifier`, `object_name`,
  `present_value`, `description`,`status_flags`, `event_state`, `out_of_service` )
VALUES
  (1, 60001, 'Sample_6_BV', 'active', null, '0000',  'normal', false);
COMMIT;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_multi_state_input_objects`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_multi_state_input_objects` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_multi_state_input_objects` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `object_identifier` BIGINT NOT NULL,
  `object_name` VARCHAR(255) NOT NULL,
  `present_value` INT NOT NULL COMMENT 'This property, of type Unsigned, reflects the
  logical state of the input. The logical state of the input shall be one of \'n\' states, where \'n\' is the
  number of states defined in the Number_Of_States property. The means used to determine the
  current state is a local matter. The Present_Value property shall always have a value greater than
  zero. The Present_Value property shall be writable when Out_Of_Service is TRUE. Any local
  modification of the value of the Present_Value when the Number_Of_States property is changed is
   a local matter.',
  `description` VARCHAR(255),
  `status_flags` CHAR(4) NOT NULL COMMENT 'The four flags are {IN_ALARM, FAULT,
  OVERRIDDEN, OUT_OF_SERVICE} ',
  `event_state` VARCHAR(32)  NOT NULL,
  `out_of_service` BOOLEAN NOT NULL,
  `number_of_states` INT NOT NULL COMMENT 'This property defines the number of states the
  Present_Value may have. The Number_Of_States property shall always have a value greater than
  zero. If the value of this property is changed, the size of the State_Text array, if present, shall also
  be changed to the same value. If the Number_of_States property value becomes less than the value
   of the Present_Value, the object shall have a Reliability of MULTI_STATE_OUT_OF_RANGE
   as long as this situation remains, unless the object is out of service. It is a local matter whether
   Present_Value is modified when the Number_of_States property value becomes less than its
   current value.',
  `state_text` VARCHAR(1024) COMMENT 'This property contains strings
  representing descriptions of all possible states of the Present_Value. The number of descriptions
  matches the number of states defined in the Number_Of_States property. The Present_Value,
  interpreted as an integer, serves as an index into the array. If the size of this array is changed, the
  Number_Of_States property shall also be changed to the same value.
  NOTE: USE SEMICOLON ; TO SPLIT STRING OR LEFT IT NULL',
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_multi_state_input_objects`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;
INSERT INTO `xbacnet`.`tbl_multi_state_input_objects`(`id`, `object_identifier`, `object_name`,
  `present_value`, `description`,`status_flags`, `event_state`, `out_of_service`, `number_of_states`, `state_text`)
VALUES
  (1, 70001,'Sample_7_MSI',1, null, '0000',  'normal', false, 3, 'Normal;Warmup;Cooldown');
COMMIT;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_multi_state_output_objects`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_multi_state_output_objects` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_multi_state_output_objects` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `object_identifier` BIGINT NOT NULL,
  `object_name` VARCHAR(255) NOT NULL,
  `present_value` INT NOT NULL COMMENT '(Commandable) This property reflects the logical
  state of an output. The logical state of the output shall be one of \'n\' states, where \'n\' is the
  number of states defined in the Number_Of_States property. How the Present_Value is used is a
  local matter. Any local modification of the value of the Present_Value when the
  Number_Of_States property is changed is a local matter. The Present_Value property shall always
  have a value greater than zero.',
  `description` VARCHAR(255),
  `status_flags` CHAR(4) NOT NULL COMMENT 'The four flags are {IN_ALARM, FAULT,
  OVERRIDDEN, OUT_OF_SERVICE} ',
  `event_state` VARCHAR(32)  NOT NULL,
  `out_of_service` BOOLEAN NOT NULL,
  `number_of_states` INT NOT NULL COMMENT 'This property defines the number of states the
  Present_Value may have. The Number_Of_States property shall always have a value greater than
  zero. If the value of this property is changed, the size of the State_Text array, if present, shall also
  be changed to the same value. If the Number_of_States property value becomes less than the value
   of the Present_Value, the object shall have a Reliability of MULTI_STATE_OUT_OF_RANGE
   as long as this situation remains, unless the object is out of service. It is a local matter whether
   Present_Value is modified when the Number_of_States property value becomes less than its
   current value.',
  `state_text` VARCHAR(1024) COMMENT 'This property contains strings
  representing descriptions of all possible states of the Present_Value. The number of descriptions
  matches the number of states defined in the Number_Of_States property. The Present_Value,
  interpreted as an integer, serves as an index into the array. If the size of this array is changed, the
  Number_Of_States property shall also be changed to the same value.
  NOTE: USE SEMICOLON ; TO SPLIT STRING OR LEFT IT NULL ',
  `relinquish_default` INT NOT NULL COMMENT 'This property is the default value to be used
  for the Present_Value property when all command priority values in the Priority_Array property
  have a NULL value.',
  `current_command_priority` INT COMMENT 'The value of this property shall be equal to the
  index of the entry in the Priority_Array from which the Present_Value\'s value has been taken.
  If Present_Value has taken on the value of Relinquish_Default, this property shall have the value
  Null.',
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_multi_state_output_objects`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;
INSERT INTO `xbacnet`.`tbl_multi_state_output_objects`(`id`, `object_identifier`, `object_name`,
  `present_value`, `description`,`status_flags`, `event_state`, `out_of_service`, `number_of_states`,
  `state_text`, `relinquish_default`,  `current_command_priority`)
VALUES
  (1, 80001,'Sample_8_MSO',1, null, '0000',  'normal', false, 3, 'Normal;Warmup;Cooldown', 0, null);
COMMIT;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_multi_state_value_objects`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_multi_state_value_objects` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_multi_state_value_objects` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `object_identifier` BIGINT NOT NULL,
  `object_name` VARCHAR(255) NOT NULL,
  `present_value` INT NOT NULL COMMENT 'This property, of type Unsigned, reflects the logical
  state of the multi-state value. The logical state of the multi-state value shall be one of \'n\' states,
  where \'n\' is the number of states defined in the Number_Of_States property. How the
  Present_Value is used is a local matter. The Present_Value property shall always have a value
  greater than zero. Present_Value shall be optionally commandable. If Present_Value is
  commandable for a given object instance, then the Priority_Array and Relinquish_Default
  properties shall also be present for that instance. The Present_Value property shall be writable
  when Out_Of_Service is TRUE. Any local modification of the value of the Present_Value when
  the Number_Of_States property is changed is a local matter.',
  `description` VARCHAR(255),
  `status_flags` CHAR(4) NOT NULL COMMENT 'The four flags are {IN_ALARM, FAULT,
  OVERRIDDEN, OUT_OF_SERVICE} ',
  `event_state` VARCHAR(32)  NOT NULL,
  `out_of_service` BOOLEAN NOT NULL,
  `number_of_states` INT NOT NULL COMMENT 'This property defines the number of states the
  Present_Value may have. The Number_Of_States property shall always have a value greater than
  zero. If the value of this property is changed, the size of the State_Text array, if present, shall also
  be changed to the same value. If the Number_of_States property value becomes less than the value
   of the Present_Value, the object shall have a Reliability of MULTI_STATE_OUT_OF_RANGE
   as long as this situation remains, unless the object is out of service. It is a local matter whether
   Present_Value is modified when the Number_of_States property value becomes less than its
   current value.',
  `state_text` VARCHAR(1024) COMMENT 'This property contains strings
  representing descriptions of all possible states of the Present_Value. The number of descriptions
  matches the number of states defined in the Number_Of_States property. The Present_Value,
  interpreted as an integer, serves as an index into the array. If the size of this array is changed, the
  Number_Of_States property shall also be changed to the same value.
  NOTE: USE SEMICOLON ; TO SPLIT STRING OR LEFT IT NULL ',
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_multi_state_value_objects`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;
INSERT INTO `xbacnet`.`tbl_multi_state_value_objects`(`id`, `object_identifier`, `object_name`,
  `present_value`, `description`,`status_flags`, `event_state`, `out_of_service`, `number_of_states`, `state_text`)
VALUES
  (1, 90001,'Sample_9_MSV',1, null, '0000',  'normal', false, 3, 'Normal;Warmup;Cooldown');
COMMIT;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_sessions`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_sessions` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_sessions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_uuid` CHAR(36) NOT NULL,
  `token` VARCHAR(128) NOT NULL,
  `utc_expires` DATETIME NOT NULL,
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_users`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_users` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_users` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `uuid` CHAR(36) NOT NULL,
  `display_name` VARCHAR(128) NOT NULL,
  `email` VARCHAR(128) NOT NULL,
  `salt` VARCHAR(128) NOT NULL,
  `password` VARCHAR(256) NOT NULL,
  `is_admin` BOOL NOT NULL ,
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_users`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;
-- default username: administrator
-- default password: !BACnetPro1
INSERT INTO `xbacnet`.`tbl_users`(`id`, `name`, `uuid`, `display_name`, `email`, `salt`,
  `password`, `is_admin`)
VALUES
(1, 'administrator', '19957e99-e5ae-445b-bfbb-d3f8219a8715', 'Administrator',
   'administrator@xbacnet.com', 'a3ee9aa8519e4f3ab756d68ee0cdd76e',
   'aabba725223e87c33bea01e98a9b0d47f916abb82c714b089dc410aa612ce97bb5ee6cca5514b12ea7db152e7be5b1328a730e94f3975d11f899b7e3e3e34799', 1);
COMMIT;

-- ---------------------------------------------------------------------------------------------------------------------
-- Table `xbacnet`.`tbl_versions`
-- ---------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `xbacnet`.`tbl_versions` ;

CREATE TABLE IF NOT EXISTS `xbacnet`.`tbl_versions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `version` VARCHAR(256) NOT NULL,
  `release_date` DATE NOT NULL,
  PRIMARY KEY (`id`));

-- ---------------------------------------------------------------------------------------------------------------------
-- Example Data for table `xbacnet`.`tbl_versions`
-- ---------------------------------------------------------------------------------------------------------------------
START TRANSACTION;
USE `xbacnet`;

INSERT INTO `xbacnet`.`tbl_versions`
(`id`, `version`, `release_date`)
VALUES
(1, '1.0.0', '2020-09-28');

COMMIT;
