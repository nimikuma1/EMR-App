-- SQLite
select * from Emr;

INSERT INTO Emr (MemberID, MemberName, MemberSex, MemberDOB, Payor, ClinicalNotes)
VALUES (1, 'John Doe', 'Male', '1990-01-01', 'Aetna', 'Patient requires MRI due to neurological disorders'),
       (2, 'Jane Smith', 'Female', '1985-05-15', 'Blue Cross', 'Patient has allergies'),
       (3, 'Michael Johnson', 'Male', '1978-09-20', 'UnitedHealthcare', 'Patient needs Knee Surgery');

ALTER TABLE Emr
ADD COLUMN procedureCode TEXT;

ALTER TABLE Emr
ADD COLUMN priorAuthStatus TEXT;

ALTER TABLE Emr
ADD COLUMN priorAuthStatus TEXT;

UPDATE Emr
SET ICDCode = '';
UPDATE Emr
SET procedureCode = '';

UPDATE Emr
SET priorAuthSubmitted = '';
UPDATE Emr
SET priorAuthStatus = '';

UPDATE Emr
SET clinicalNotes = 'Patient requires brain MRI due to Neurological disorders' 
where memberId =1;

DROP TABLE Emr;

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