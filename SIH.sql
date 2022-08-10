CREATE TABLE "users" (
  "email" varchar PRIMARY KEY,
  "password" varchar,
  "college" varchar,
  "name" varchar,
  "user_type" smallint,
  "phone" varchar,
  "aadhar" varchar,
  "pan" varchar,
  "seeded_bank_acc" varchar
);

CREATE TABLE "aicte" (
  "aadhar" varchar PRIMARY KEY,
  "seeded_bank_acc" varchar,
  "pan" varchar,
  "name" varchar,
  "college" varchar,
  "gender" varchar
);

CREATE TABLE "uid" (
  "aadhar" varchar PRIMARY KEY,
  "name" varchar,
  "gender" varchar,
  "address" varchar,
  "dob" date
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

inserting into users table:
INSERT INTO users("email","password","college","name","user_type","phone") VALUES ('aryan@gmail.com','123','PICT','Aryan Agrawal','Student','1234567890')

inserting in aicte table:
INSERT INTO aicte("aadhar","seeded_bank_acc","pan","name","college","gender") VALUES ('220945152786','111111','PAN123','Atharva Kinikar','Pune Institute of Computer Technology','M');

inserting in npci table :
INSERT INTO npci("aadhar","seeded_bank_acc") VALUES ('220945152786','111111');

*/