-- SQLite

CREATE TABLE Emr (
    memberID INTEGER PRIMARY KEY,
    memberName VARCHAR(100),
    memberSex TEXT,
    memberDOB DATE,
    payor VARCHAR(100),
    clinicalNotes TEXT,
    ICDCode VARCHAR(20),
    procedureCode VARCHAR(20),
    priorAuthStatus VARCHAR(20)
);
select * from User;
select * from Emr;
INSERT INTO Emr (MemberID, MemberName, MemberSex, MemberDOB, Payor, ClinicalNotes)
VALUES (1, 'John Doe', 'Male', '1990-01-01', 'Aetna', 'Patient requires MRI'),
       (2, 'Jane Smith', 'Female', '1985-05-15', 'Blue Cross', 'Patient has allergies'),
       (3, 'Michael Johnson', 'Male', '1978-09-20', 'UnitedHealthcare', 'Patient needs Knee Surgery');

ALTER TABLE Emr ADD COLUMN ICDCode VARCHAR(20);

select * from Emr;

select * from User;

UPDATE Emr
SET ICDCode = '';
UPDATE Emr
SET procedureCode = '';

UPDATE Emr
SET priorAuthStatus = '';

UPDATE Emr
SET ClinicalNotes = 'Patient requires brain MRI'
WHERE memberID=1;

UPDATE Emr
SET ClinicalNotes = 'Patient has peanut allergies'
WHERE memberID=2;

UPDATE Emr
SET ClinicalNotes = 'Patient needs Knee Surgery due to Osteoporosis'
WHERE memberID=3;


UPDATE Emr
SET ICDCode = 'T78.0'
WHERE memberID=2;
'T78.0' - peanut allergy

UPDATE Emr
SET ICDCode = 'M17.1'
WHERE memberID=3;


UPDATE Emr
SET ICDCode = 'C71.9'
WHERE memberID=1;

'C71.9' - brain surgery

UPDATE Emr
SET ICDCode = 'T78.0'
WHERE memberID=2;
'T78.0' - peanut allergy

UPDATE Emr
SET ICDCode = 'M17.1'
WHERE memberID=3;

UPDATE Emr
SET procedureCode = 'T0150'
WHERE memberID=1;

M17.1 - due to osteoporosis


