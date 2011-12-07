

/************************ REBUILD DATABASE ***************************************/

PRINT '*** Beginning Database Creation ***'

USE [MASTER]
GO

CREATE DATABASE [TheDW]  ON
   (NAME = N'TheDW_Data', 
    FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL10.mssqlserver\mssql\data\TheDW.MDF', 
    SIZE = 3MB, 
    FILEGROWTH = 10%) 
  LOG ON 
    (NAME = N'TheDW_Log', 
     FILENAME = N'C:\Program Files\Microsoft SQL Server\mssql10.mssqlserver\MSSQL\data\TheDW.LDF', 
     SIZE = 1MB, 
     FILEGROWTH = 10%)
 COLLATE SQL_Latin1_General_CP1_CI_AS
GO 

PRINT '*** Completed Database Creation ***'


PRINT '*** Beginning Table Creation ***'

USE [TheDW]
GO


CREATE TABLE [Employee_Table]
  (
    [Soc_Sec_Num]            [nchar]    (11) NOT NULL ,
    [First_Name]             [nvarchar] (25) NULL ,
    [Middle_Initial]         [nchar]    (1)  NULL ,
    [Last_Name]              [nvarchar] (25) NULL ,
    [Address1]               [nvarchar] (50) NULL ,
    [Address2]               [nvarchar] (50) NULL ,
    [City]                   [nvarchar] (25) NULL ,
    [State]                  [nchar]    (2)  NULL ,
    [ZipCode]                [nvarchar] (10) NULL ,
    [Home_Phone_Number]      [nchar]    (14) NULL ,
    [Sex]                    [nchar]    (1)  NULL ,
    [Date_Of_Birth]          [datetime]      NULL ,
    [Employment_Type]        [nchar]    (3)  NULL ,
    [Original_Hire_Date]     [datetime]      NULL ,
    [Final_Termination_Date] [datetime]      NULL ,
    [Import_TUID]            [nvarchar] (20) NULL ,
       
    CONSTRAINT [PK_Employee_Table] PRIMARY KEY CLUSTERED
      ( [Soc_Sec_Num] )

  ) ON [PRIMARY]
GO


CREATE TABLE [Subsidiary_Table] 
  (
    [Subsidiary_Number]    [nchar]    (3)  NOT NULL ,
    [Subsidiary_Name]      [nvarchar] (25) NULL     ,

    CONSTRAINT [PK_Subsidiary_Table] PRIMARY KEY CLUSTERED
      ( [Subsidiary_Number] ) ,

  ) ON [PRIMARY]
GO


CREATE TABLE [Department_Code_Table] 
  (
    [Department_Code]      [nchar]    (3)  NOT NULL ,
    [Subsidiary_Number]    [nchar]    (3)   NOT NULL ,
    [Department_Name]      [nvarchar] (25)  NULL ,     
    [Manager_Soc_Sec_Num]  [nchar]    (11)  NULL ,

    CONSTRAINT [PK_Department_Code_Table] PRIMARY KEY CLUSTERED
      ( [Department_Code], [Subsidiary_Number] ),
      
    CONSTRAINT [FK_Department_Code_Table_Subsidiary_Number] 
      FOREIGN KEY ( [Subsidiary_Number] )
        REFERENCES [Subsidiary_Table] ( [Subsidiary_Number] ) 
		ON DELETE CASCADE
                ON UPDATE CASCADE ,

    CONSTRAINT [FK_Department_Code_Table_Manager_Soc_Sec_Num]
      FOREIGN KEY ( [Manager_Soc_Sec_Num] )
         REFERENCES [Employee_Table] ( [Soc_Sec_Num] )
                 ON DELETE CASCADE
                 ON UPDATE CASCADE


  ) ON [PRIMARY]
GO




CREATE TABLE [Job_Class_Code_Table] 
  (
    [Job_Class_Code]       [nchar]    (3)  NOT NULL ,
    [Subsidiary_Number]    [nchar]    (3)   NOT NULL ,
    [Department_Code]      [nchar]    (3)  NOT NULL ,     
    [Job_Title]            [nchar]    (25)  NULL ,

    CONSTRAINT [PK_Job_Class_Code_Table] PRIMARY KEY CLUSTERED
      ( [Job_Class_Code], [Subsidiary_Number] ) ,
                     

    CONSTRAINT [FK_Job_Class_Code_Table_Subsidiary_Number] 
      FOREIGN KEY ( [Subsidiary_Number] )
        REFERENCES [Subsidiary_Table] ( [Subsidiary_Number] ) ,
		

    CONSTRAINT [FK_Job_Class_Code_Table_Department_Code]
      FOREIGN KEY ( [Department_Code],[Subsidiary_Number] )
         REFERENCES [Department_Code_Table] ( [Department_Code], [Subsidiary_Number] )
                
  ) ON [PRIMARY]
GO


CREATE TABLE [Job_Assignment_Table]
  (
    [Soc_Sec_Num]             [nchar]   (11)   NOT NULL ,
    [Subsidiary_Number]       [nchar]   (3)    NOT NULL ,
    [Company_Employee_Number] [nchar]   (9)    NULL ,
    [FT_PT_Code]              [nchar]   (3)    NULL ,
    [Status_Code]             [nchar]   (10)   NULL ,
    [Hired_Date]              [datetime]       NULL ,
    [Termination_Date]        [datetime]       NULL ,
    [Termination_Code]        [nchar]   (2)    NULL ,
    [Hourly_Base_Pay]         [numeric] (18,5) NULL ,
    [Budgeted_Hours_Per_Pay]  [numeric] (18,5) NULL ,
    [Job_Class_Code]          [nchar]   (3)    NOT NULL ,
    [Import_TUID]             [nvarchar](20)   NULL ,

    CONSTRAINT [PK_Job_Assignment_Table] PRIMARY KEY CLUSTERED
      ( [Soc_Sec_Num], [Subsidiary_Number] ) ,

    CONSTRAINT [FK_Job_Assignment_Table_Soc_Sec_Num] 
      FOREIGN KEY ( [Soc_Sec_Num] )
        REFERENCES [Employee_Table] ( [Soc_Sec_Num] ) 
		ON DELETE CASCADE
                ON UPDATE CASCADE ,

    CONSTRAINT [FK_Job_Assignment_Table_Subsidiary_Number] 
      FOREIGN KEY ( [Subsidiary_Number] )
        REFERENCES [Subsidiary_Table] ( [Subsidiary_Number] ) 
		ON DELETE CASCADE
                ON UPDATE CASCADE ,

    CONSTRAINT [FK_Job_Assignment_Table_Job_Class_Code] 
      FOREIGN KEY ( [Job_Class_Code], [Subsidiary_Number] )
        REFERENCES [Job_Class_Code_Table] ( [Job_Class_Code], [Subsidiary_Number] ) 
		ON DELETE CASCADE
                ON UPDATE CASCADE 



) ON [PRIMARY]
GO


CREATE TABLE [Tables_Table]
  (
     [Table_Name]  [nchar]    (50)  NOT NULL ,
     [Keys]        [nvarchar] (250) NOT NULL ,
     [Is_Shadowed] [nchar]    (1)   NOT NULL ,
     [Load_Order]  [nchar]    (5)   NOT NULL ,
     
     CONSTRAINT [PK_Tables_Table] PRIMARY KEY CLUSTERED
	( [Table_Name] )

  ) ON [PRIMARY]
GO

CREATE TABLE [Extract_File_Translation_Table]
  (
     [Subsidiary_Number]  [nchar]    (3)   NOT NULL ,
     [Legacy_FieldName] [nvarchar] (250) NOT NULL ,
     [DW_Fieldname]     [nvarchar] (250) NOT NULL ,
     [DW_Tablename]     [nvarchar] (250) NOT NULL ,
  ) ON [PRIMARY]
GO

CREATE TABLE [Business_Rules_Table]
  (
     [Subsidiary_Number] [nchar]    (3)   NOT NULL ,
     [DW_Fieldname]    [nvarchar] (250) NOT NULL ,
     [Legacy_Value]    [nvarchar] (250) NOT NULL ,
     [DW_Value]        [nvarchar] (250) NOT NULL ,
   ) ON [PRIMARY]
GO

CREATE TABLE [Import_Table]
  (
     [Import_TUID]     [nchar]    (18)  NOT NULL ,
     [Filename]        [nvarchar] (250) NOT NULL ,
     [Import_Datetime] [datetime]       NOT NULL ,
     [Subsidiary_Number] [nchar]    (3)   NOT NULL ,

     CONSTRAINT [PK_Import_Table] PRIMARY KEY CLUSTERED
	( [Import_TUID] )

   ) ON [PRIMARY]
GO





CREATE TABLE [Employee_Shadows_Table]
  (
    [Soc_Sec_Num]            [nchar]    (11) NULL ,
    [First_Name]             [nvarchar] (25) NULL ,
    [Middle_Initial]         [nchar]    (1)  NULL ,
    [Last_Name]              [nvarchar] (25) NULL ,
    [Address1]               [nvarchar] (50) NULL ,
    [Address2]               [nvarchar] (50) NULL ,
    [City]                   [nvarchar] (25) NULL ,
    [State]                  [nchar]    (2)  NULL ,
    [ZipCode]                [nvarchar] (10) NULL ,
    [Home_Phone_Number]      [nchar]    (14) NULL ,
    [Sex]                    [nchar]    (1)  NULL ,
    [Date_Of_Birth]          [datetime]      NULL ,
    [Employment_Type]        [nchar]    (3)  NULL ,
    [Original_Hire_Date]     [datetime]      NULL ,
    [Final_Termination_Date] [datetime]      NULL ,
    [Import_TUID]            [nvarchar] (20) NULL 

  ) ON [PRIMARY]
GO


CREATE TABLE [Job_Assignment_Shadows_Table]
  (
    [Soc_Sec_Num]             [nchar]   (11)   NULL ,
    [Subsidiary_Number]       [nchar]   (3)    NULL ,
    [Company_Employee_Number] [nchar]   (9)    NULL ,
    [FT_PT_Code]              [nchar]   (3)    NULL ,
    [Status_Code]             [nchar]   (10)   NULL ,
    [Hired_Date]              [datetime]       NULL ,
    [Termination_Date]        [datetime]       NULL ,
    [Termination_Code]        [nchar]   (2)    NULL ,
    [Hourly_Base_Pay]         [numeric] (18,5) NULL ,
    [Budgeted_Hours_Per_Pay]  [numeric] (18,5) NULL ,
    [Job_Class_Code]          [nchar]   (3)    NULL ,
    [Import_TUID]             [nvarchar](20)   NULL 

) ON [PRIMARY]
GO


PRINT '*** Ending Table Creation ***'


PRINT '*** Script Execution Completed ***'