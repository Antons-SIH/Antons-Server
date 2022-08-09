CREATE TABLE "user" (
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
