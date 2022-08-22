CREATE TABLE "aicte" (
  "email" varchar PRIMARY KEY,
  "password" varchar,
  "phone" varchar,
  "gender" varchar,
  "user_type" varchar,
  "aadhar" varchar,
  "aadhar_remark" varchar,
  "seeded_bank_acc" varchar,
  "seeded_remark" varchar,
  "pan" varchar,
  "pan_remark" varchar,
  "name" varchar,
  "college" varchar,
  "address" varchar,
  "dob" varchar,
  "admission_year" varchar,
  "last_updated" date,
  "otp" varchar
);

CREATE TABLE "uid" (
  "aadhar" varchar PRIMARY KEY,
  "name" varchar,
  "gender" varchar,
  "address" varchar,
  "dob" date,
  "phone" varchar
);

CREATE TABLE "npci" (
  "aadhar" varchar PRIMARY KEY,
  "seeded_bank_acc" varchar
);

CREATE TABLE "pan" (
  "pan" varchar PRIMARY KEY,
  "name" varchar,
  "address" varchar,
  "dob" date
);

/*

inserting in UID table:
INSERT INTO uid("aadhar","name","gender","address","dob") VALUES ('220945152786','Atharva Kinikar','M','Pune','2001-05-09');
SELECT * FROM uid;

inserting into users table:
INSERT INTO users("email","password","college","name","user_type","phone") VALUES ('aryan@gmail.com','123','PICT','Aryan Agrawal','Student','1234567890')
SELECT * FROM users;

inserting in aicte table:
INSERT INTO aicte("aadhar","seeded_bank_acc","pan","name","college","gender") VALUES ('220945152786','111111','PAN123','Atharva Kinikar','Pune Institute of Computer Technology','M');
SELECT * FROM aicte;

inserting in npci table :
INSERT INTO npci("aadhar","seeded_bank_acc") VALUES ('220945152786','111111');
SELECT * FROM npci;

*/