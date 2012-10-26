#
# Encoding: Unicode (UTF-8)
#


DROP TABLE IF EXISTS `Business_Rules_Table`;
DROP TABLE IF EXISTS `Department_Code_Table`;
DROP TABLE IF EXISTS `Employee_Shadows_Table`;
DROP TABLE IF EXISTS `Employee_Table`;
DROP TABLE IF EXISTS `Extract_File_Translation_Table`;
DROP TABLE IF EXISTS `Import_Table`;
DROP TABLE IF EXISTS `Job_Assignment_Shadows_Table`;
DROP TABLE IF EXISTS `Job_Assignment_Table`;
DROP TABLE IF EXISTS `Job_Class_Code_Table`;
DROP TABLE IF EXISTS `Subsidiary_Table`;
DROP TABLE IF EXISTS `Tables_Table`;


CREATE TABLE `Business_Rules_Table` (
  `Subsidiary_Number` char(3) NOT NULL,
  `DW_Fieldname` varchar(250) NOT NULL,
  `Legacy_Value` varchar(250) NOT NULL,
  `DW_Value` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Department_Code_Table` (
  `Department_Code` char(3) NOT NULL,
  `Subsidiary_Number` char(3) NOT NULL,
  `Department_Name` varchar(25) DEFAULT NULL,
  `Manager_Soc_Sec_Num` char(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Employee_Shadows_Table` (
  `Soc_Sec_Num` char(11) DEFAULT NULL,
  `First_Name` varchar(25) DEFAULT NULL,
  `Middle_Initial` char(1) DEFAULT NULL,
  `Last_Name` varchar(25) DEFAULT NULL,
  `Address1` varchar(50) DEFAULT NULL,
  `Address2` varchar(50) DEFAULT NULL,
  `City` varchar(25) DEFAULT NULL,
  `State` char(2) DEFAULT NULL,
  `ZipCode` varchar(10) DEFAULT NULL,
  `Home_Phone_Number` char(14) DEFAULT NULL,
  `Sex` char(1) DEFAULT NULL,
  `Date_Of_Birth` datetime DEFAULT NULL,
  `Employment_Type` char(3) DEFAULT NULL,
  `Original_Hire_Date` datetime DEFAULT NULL,
  `Final_Termination_Date` datetime DEFAULT NULL,
  `Import_TUID` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Employee_Table` (
  `Soc_Sec_Num` char(11) NOT NULL,
  `First_Name` varchar(25) DEFAULT NULL,
  `Middle_Initial` char(1) DEFAULT NULL,
  `Last_Name` varchar(25) DEFAULT NULL,
  `Address1` varchar(50) DEFAULT NULL,
  `Address2` varchar(50) DEFAULT NULL,
  `City` varchar(25) DEFAULT NULL,
  `State` char(2) DEFAULT NULL,
  `ZipCode` varchar(10) DEFAULT NULL,
  `Home_Phone_Number` char(14) DEFAULT NULL,
  `Sex` char(1) DEFAULT NULL,
  `Date_Of_Birth` datetime DEFAULT NULL,
  `Employment_Type` char(3) DEFAULT NULL,
  `Original_Hire_Date` datetime DEFAULT NULL,
  `Final_Termination_Date` datetime DEFAULT NULL,
  `Import_TUID` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Extract_File_Translation_Table` (
  `Subsidiary_Number` char(3) NOT NULL,
  `Legacy_FieldName` varchar(250) NOT NULL,
  `DW_Fieldname` varchar(250) NOT NULL,
  `DW_Tablename` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Import_Table` (
  `Import_TUID` char(18) NOT NULL,
  `Filename` varchar(250) NOT NULL,
  `Import_Datetime` datetime NOT NULL,
  `Subsidiary_Number` char(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Job_Assignment_Shadows_Table` (
  `Soc_Sec_Num` char(11) DEFAULT NULL,
  `Subsidiary_Number` char(3) DEFAULT NULL,
  `Company_Employee_Number` char(9) DEFAULT NULL,
  `FT_PT_Code` char(3) DEFAULT NULL,
  `Status_Code` char(10) DEFAULT NULL,
  `Hired_Date` datetime DEFAULT NULL,
  `Termination_Date` datetime DEFAULT NULL,
  `Termination_Code` char(2) DEFAULT NULL,
  `Hourly_Base_Pay` decimal(18,5) DEFAULT NULL,
  `Budgeted_Hours_Per_Pay` decimal(18,5) DEFAULT NULL,
  `Job_Class_Code` char(3) DEFAULT NULL,
  `Import_TUID` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Job_Assignment_Table` (
  `Soc_Sec_Num` char(11) NOT NULL,
  `Subsidiary_Number` char(3) NOT NULL,
  `Company_Employee_Number` char(9) DEFAULT NULL,
  `FT_PT_Code` char(3) DEFAULT NULL,
  `Status_Code` char(10) DEFAULT NULL,
  `Hired_Date` datetime DEFAULT NULL,
  `Termination_Date` datetime DEFAULT NULL,
  `Termination_Code` char(2) DEFAULT NULL,
  `Hourly_Base_Pay` decimal(18,5) DEFAULT NULL,
  `Budgeted_Hours_Per_Pay` decimal(18,5) DEFAULT NULL,
  `Job_Class_Code` char(3) NOT NULL,
  `Import_TUID` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Job_Class_Code_Table` (
  `Job_Class_Code` char(3) NOT NULL,
  `Subsidiary_Number` char(3) NOT NULL,
  `Department_Code` char(3) NOT NULL,
  `Job_Title` char(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Subsidiary_Table` (
  `Subsidiary_Number` char(3) DEFAULT NULL,
  `Subsidiary_Name` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Tables_Table` (
  `Table_Name` char(50) NOT NULL,
  `Keys` varchar(250) NOT NULL,
  `Is_Shadowed` char(1) NOT NULL,
  `Load_Order` char(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




SET FOREIGN_KEY_CHECKS = 0;


LOCK TABLES `Business_Rules_Table` WRITE;
INSERT INTO `Business_Rules_Table` (`Subsidiary_Number`, `DW_Fieldname`, `Legacy_Value`, `DW_Value`) VALUES ('001', 'Subsidiary_Number', '001', '001'), ('002', 'Subsidiary_Number', '2', '002'), ('003', 'Subsidiary_Number', '003', '003'), ('001', 'Subsidiary_Number', 'NULL', 'VRFY Subsidiary_Table.Subsidiary_Number'), ('002', 'Subsidiary_Number', 'NULL', 'VRFY Subsidiary_Table.Subsidiary_Number'), ('003', 'Subsidiary_Number', 'NULL', 'VRFY Subsidiary_Table.Subsidiary_Number'), ('001', 'Job_Class_Code', 'NULL', 'VRFY Job_Class_Code_Table.Job_Class_Code'), ('002', 'Job_Class_Code', 'NULL', 'VRFY Job_Class_Code_Table.Job_Class_Code'), ('003', 'Job_Class_Code', 'NULL', 'VRFY Job_Class_Code_Table.Job_Class_Code'), ('001', 'Soc_Sec_Num', 'NULL', 'MASK 000-00-0000'), ('002', 'Soc_Sec_Num', 'NULL', 'MASK 000-00-0000'), ('003', 'Soc_Sec_Num', 'NULL', 'MASK 000-00-0000'), ('001', 'Home_Phone_Number', 'NULL', 'MASK (000) 000-0000'), ('002', 'Home_Phone_Number', 'NULL', 'MASK (000) 000-0000'), ('003', 'Home_Phone_Number', 'NULL', 'MASK (000) 000-0000'), ('001', 'ORIGINAL_HIRE_DATE', 'NULL', 'MASK mm/dd/yyyy'), ('002', 'ORIGINAL_HIRE_DATE', 'NULL', 'MASK mm/dd/yyyy'), ('003', 'ORIGINAL_HIRE_DATE', 'NULL', 'MASK mm/dd/yyyy'), ('001', 'Sex', 'M', 'M'), ('001', 'Sex', 'F', 'F'), ('002', 'Sex', '1', 'M'), ('002', 'Sex', '2', 'F'), ('003', 'Sex', 'male', 'M'), ('003', 'Sex', 'female', 'F'), ('001', 'Date_Of_Birth', 'NULL', 'MASK mm/dd/yyyy'), ('002', 'Date_Of_Birth', 'NULL', 'MASK mm/dd/yyyy'), ('003', 'Date_Of_Birth', 'NULL', 'MASK mm/dd/yyyy'), ('001', 'FT_PT_Code', 'NULL', 'TRUL 1'), ('002', 'FT_PT_Code', 'NULL', 'TRUL 1'), ('003', 'FT_PT_Code', 'NULL', 'TRUL 1'), ('001', 'Status_Code', 'NULL', 'TRUL 1'), ('002', 'Status_Code', 'NULL', 'TRUL 1'), ('003', 'Status_Code', 'NULL', 'TRUL 1'), ('001', 'Termination_Date', 'NULL', 'MASK mm/dd/yyyy'), ('002', 'Termination_Date', 'NULL', 'MASK mm/dd/yyyy'), ('003', 'Termination_Date', 'NULL', 'MASK mm/dd/yyyy'), ('001', 'Final_Termination_Date', 'NULL', 'MASK mm/dd/yyyy'), ('002', 'Final_Termination_Date', 'NULL', 'MASK mm/dd/yyyy'), ('003', 'Final_Termination_Date', 'NULL', 'MASK mm/dd/yyyy'), ('002', 'Termination_Code', 'R', 'R'), ('002', 'Termination_Code', 'F', 'F'), ('003', 'Termination_Code', '1', 'F'), ('003', 'Termination_Code', '2', 'R'), ('003', 'Termination_Code', '3', 'F'), ('003', 'Termination_Code', '4', 'F'), ('003', 'Termination_Code', '5', 'R');
UNLOCK TABLES;


LOCK TABLES `Department_Code_Table` WRITE;
INSERT INTO `Department_Code_Table` (`Department_Code`, `Subsidiary_Number`, `Department_Name`, `Manager_Soc_Sec_Num`) VALUES ('100', '001', 'Development', NULL), ('100', '002', 'Production', NULL), ('100', '003', 'Engineering', NULL), ('200', '002', 'Food Services', NULL), ('200', '003', 'Maintenance', NULL), ('300', '002', 'Facilities', NULL), ('300', '003', 'Physical Plant', NULL), ('400', '003', 'Employee Services', NULL), ('500', '001', 'Facilities', NULL);
UNLOCK TABLES;


LOCK TABLES `Employee_Shadows_Table` WRITE;
UNLOCK TABLES;


LOCK TABLES `Employee_Table` WRITE;
UNLOCK TABLES;


LOCK TABLES `Extract_File_Translation_Table` WRITE;
INSERT INTO `Extract_File_Translation_Table` (`Subsidiary_Number`, `Legacy_FieldName`, `DW_Fieldname`, `DW_Tablename`) VALUES ('001', 'SUBSIDIARY_NUMBER', 'Subsidiary_Number', 'Job_Assignment_Table'), ('001', 'SOCIAL_SECURITY_NUMBER', 'Soc_Sec_Num', 'Job_Assignment_Table'), ('001', 'ORIGINAL_HIRE_DATE', 'Hired_Date', 'Job_Assignment_Table'), ('001', 'EMPLOYEE_NUMBER', 'Company_Employee_Number', 'Job_Assignment_Table'), ('001', 'FT_PT_CODE', 'FT_PT_Code', 'Job_Assignment_Table'), ('001', 'STATUS_CODE', 'Status_Code', 'Job_Assignment_Table'), ('001', 'TERMINATION_DATE', 'Termination_Date', 'Job_Assignment_Table'), ('001', 'TERMINATION_CODE', 'Termination_Code', 'Job_Assignment_Table'), ('001', 'HOURLY_BASE_PAY', 'Hourly_Base_Pay', 'Job_Assignment_Table'), ('001', 'BUDGETED_HOURS_PER_PAY', 'Budgeted_Hours_Per_Pay', 'Job_Assignment_Table'), ('001', 'JOB_CLASS_CODE', 'Job_Class_Code', 'Job_Assignment_Table'), ('001', 'SOCIAL_SECURITY_NUMBER', 'Soc_Sec_Num', 'Employee_Table'), ('001', 'FIRST_NAME', 'First_Name', 'Employee_Table'), ('001', 'MIDDLE_INITIAL', 'Middle_Initial', 'Employee_Table'), ('001', 'LAST_NAME', 'Last_Name', 'Employee_Table'), ('001', 'ADDRESS_LINE_1', 'Address1', 'Employee_Table'), ('001', 'ADDRESS_LINE_2', 'Address2', 'Employee_Table'), ('001', 'CITY', 'City', 'Employee_Table'), ('001', 'STATE', 'State', 'Employee_Table'), ('001', 'ZIP_CODE', 'ZipCode', 'Employee_Table'), ('001', 'HOME_PHONE_NUMBER', 'Home_Phone_Number', 'Employee_Table'), ('001', 'ORIGINAL_HIRE_DATE', 'Original_Hire_Date', 'Employee_Table'), ('001', 'SEX', 'Sex', 'Employee_Table'), ('001', 'DATE_OF_BIRTH', 'Date_Of_Birth', 'Employee_Table'), ('001', 'FT_PT_CODE', 'Employment_Type', 'Employee_Table'), ('001', 'TERMINATION_DATE', 'Final_Termination_Date', 'Employee_Table'), ('002', 'EpSubNum', 'Subsidiary_Number', 'Job_Assignment_Table'), ('002', 'EpSocSecNum', 'Soc_Sec_Num', 'Job_Assignment_Table'), ('002', 'jbHireDate', 'Hired_Date', 'Job_Assignment_Table'), ('002', 'jbEmpNum', 'Company_Employee_Number', 'Job_Assignment_Table'), ('002', 'jbEmpCode', 'FT_PT_Code', 'Job_Assignment_Table'), ('002', 'jbStatCode', 'Status_Code', 'Job_Assignment_Table'), ('002', 'jbTermDate', 'Termination_Date', 'Job_Assignment_Table'), ('002', 'jbTermReason', 'Termination_Code', 'Job_Assignment_Table'), ('002', 'jbHourPay', 'Hourly_Base_Pay', 'Job_Assignment_Table'), ('002', 'jbBudgetedHrs', 'Budgeted_Hours_Per_Pay', 'Job_Assignment_Table'), ('002', 'jbClassification', 'Job_Class_Code', 'Job_Assignment_Table'), ('002', 'EpSocSecNum', 'Soc_Sec_Num', 'Employee_Table'), ('002', 'EpFname', 'First_Name', 'Employee_Table'), ('002', 'EpMInit', 'Middle_Initial', 'Employee_Table'), ('002', 'EpLname', 'Last_Name', 'Employee_Table'), ('002', 'EpAdd1', 'Address1', 'Employee_Table'), ('002', 'EpAdd2', 'Address2', 'Employee_Table'), ('002', 'EpCity', 'City', 'Employee_Table'), ('002', 'EpState', 'State', 'Employee_Table'), ('002', 'EpZip', 'ZipCode', 'Employee_Table'), ('002', 'EpHomePhone', 'Home_Phone_Number', 'Employee_Table'), ('002', 'jbHireDate', 'Original_Hire_Date', 'Employee_Table'), ('002', 'EpGender', 'Sex', 'Employee_Table'), ('002', 'EpDateOfBith', 'Date_Of_Birth', 'Employee_Table'), ('002', 'jbEmpCode', 'Employment_Type', 'Employee_Table'), ('002', 'jbTermDate', 'Final_Termination_Date', 'Employee_Table'), ('003', 'CompanyCode', 'Subsidiary_Number', 'Job_Assignment_Table'), ('003', 'SSN', 'Soc_Sec_Num', 'Job_Assignment_Table'), ('003', 'HireDate', 'Hired_Date', 'Job_Assignment_Table'), ('003', 'EmpNum', 'Company_Employee_Number', 'Job_Assignment_Table'), ('003', 'EmpCode', 'FT_PT_Code', 'Job_Assignment_Table'), ('003', 'EmpCode', 'Status_Code', 'Job_Assignment_Table'), ('003', 'TermDate', 'Termination_Date', 'Job_Assignment_Table'), ('003', 'TermCode', 'Termination_Code', 'Job_Assignment_Table'), ('003', 'BasePay', 'Hourly_Base_Pay', 'Job_Assignment_Table'), ('003', 'HrsPerPay', 'Budgeted_Hours_Per_Pay', 'Job_Assignment_Table'), ('003', 'JobCode', 'Job_Class_Code', 'Job_Assignment_Table'), ('003', 'SSN', 'Soc_Sec_Num', 'Employee_Table'), ('003', 'Fname', 'First_Name', 'Employee_Table'), ('003', 'Minit', 'Middle_Initial', 'Employee_Table'), ('003', 'Lname', 'Last_Name', 'Employee_Table'), ('003', 'Addr1', 'Address1', 'Employee_Table'), ('003', 'Addr2', 'Address2', 'Employee_Table'), ('003', 'City', 'City', 'Employee_Table'), ('003', 'State', 'State', 'Employee_Table'), ('003', 'Zip', 'ZipCode', 'Employee_Table'), ('003', 'HomePhone', 'Home_Phone_Number', 'Employee_Table'), ('003', 'HireDate', 'Original_Hire_Date', 'Employee_Table'), ('003', 'Sex', 'Sex', 'Employee_Table'), ('003', 'BirthDate', 'Date_Of_Birth', 'Employee_Table'), ('003', 'EmpCode', 'Employment_Type', 'Employee_Table'), ('003', 'TermDate', 'Final_Termination_Date', 'Employee_Table');
UNLOCK TABLES;


LOCK TABLES `Import_Table` WRITE;
UNLOCK TABLES;


LOCK TABLES `Job_Assignment_Shadows_Table` WRITE;
UNLOCK TABLES;


LOCK TABLES `Job_Assignment_Table` WRITE;
UNLOCK TABLES;


LOCK TABLES `Job_Class_Code_Table` WRITE;
INSERT INTO `Job_Class_Code_Table` (`Job_Class_Code`, `Subsidiary_Number`, `Department_Code`, `Job_Title`) VALUES ('104', '001', '100', 'Nuclear Physics'), ('104', '003', '100', 'Manufacturing'), ('105', '001', '100', 'Quantum Chemistry'), ('105', '003', '100', 'Production Planning'), ('109', '002', '100', 'Waffleball Division'), ('115', '001', '100', 'Radical CS Research'), ('115', '002', '100', 'Volleyball Division'), ('115', '003', '100', 'Packaging'), ('203', '001', '500', 'Janitorial'), ('203', '003', '200', 'Telecom'), ('207', '001', '500', 'Kitchen'), ('207', '003', '300', 'Plumbing'), ('212', '001', '500', 'Outdoor Maintenance'), ('212', '003', '200', 'Electrical'), ('213', '001', '500', 'Machine Repair'), ('213', '003', '400', 'Kitchen'), ('214', '001', '500', 'Telecom'), ('214', '003', '400', 'Laundry'), ('304', '002', '200', 'Kitchen'), ('307', '002', '300', 'Telecom'), ('309', '002', '300', 'Janitorial');
UNLOCK TABLES;


LOCK TABLES `Subsidiary_Table` WRITE;
INSERT INTO `Subsidiary_Table` (`Subsidiary_Number`, `Subsidiary_Name`) VALUES ('001', 'Jones Excavating Services'), ('002', 'Brown Time Systems'), ('003', 'Yoyodyne Propulsion'), ('004', 'Venkmann & Stansz'), ('005', 'Nova Robotics');
UNLOCK TABLES;


LOCK TABLES `Tables_Table` WRITE;
INSERT INTO `Tables_Table` (`Table_Name`, `Keys`, `Is_Shadowed`, `Load_Order`) VALUES ('Employee_Table', 'Soc_Sec_Num', 'Y', '1'), ('Job_Assignment_Table', 'Soc_Sec_Num+Subsidiary_Number', 'Y', '2');
UNLOCK TABLES;




SET FOREIGN_KEY_CHECKS = 1;


