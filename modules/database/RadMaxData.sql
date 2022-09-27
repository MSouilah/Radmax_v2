BEGIN TRANSACTION;
DROP TABLE IF EXISTS "RadMaxData";
CREATE TABLE IF NOT EXISTS "RadMaxData" (
	"id"	INTEGER NOT NULL,
	"date"	VARCHAR,
	"exp_name"	VARCHAR,
	"crys_name"	VARCHAR,
	"fit_algo"	VARCHAR,
	"fit_success"	VARCHAR,
	"residual"	FLOAT,
	"geometry"	VARCHAR,
	"model"	VARCHAR,
	"alldata"	BLOB,
	"spdata"	BLOB,
	"dwpdata"	BLOB,
	"pathDict"	BLOB,
	"xrd_data"	BLOB,
	PRIMARY KEY("id")
);
COMMIT;
