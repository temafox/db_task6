CREATE TABLE IF NOT EXISTS master ( 
	login             varchar(30) PRIMARY KEY, 
	password          varchar(30) NOT NULL, 
	first_name        varchar(30) NOT NULL, 
	last_name         varchar(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS cat ( 
	cat_id            integer     PRIMARY KEY 	GENERATED ALWAYS AS IDENTITY, 
	master            varchar(30) NOT NULL    	REFERENCES master, 
	name              varchar(30) NOT NULL, 
	sex               char(7)     NOT NULL          CHECK ( (sex = 'мужской') OR (sex = 'женский') ),
	color             varchar(30), 
	birth_date        date        CHECK (birth_date <= CURRENT_DATE), 
	height            integer, 
	mass              integer 
);

CREATE TABLE IF NOT EXISTS disease (
	disease 	  varchar(30) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS cat_disease_history (
	cat_disease_id    integer     PRIMARY KEY       GENERATED ALWAYS AS IDENTITY,
	disease           varchar(30) NOT NULL          REFERENCES disease,
	cat_id            integer     NOT NULL          REFERENCES cat,
	start_date        date        NOT NULL		CHECK (start_date <= CURRENT_DATE),
	end_date          date        CHECK ( (end_date IS NULL) OR ( (end_date IS NOT NULL) AND (end_date >= start_date) ) )
);

CREATE TABLE IF NOT EXISTS vet ( 
	login             varchar(30) PRIMARY KEY, 
	password          varchar(30) NOT NULL, 
	first_name        varchar(30) NOT NULL, 
	last_name         varchar(30) NOT NULL 
);

CREATE TABLE IF NOT EXISTS specialty (
	specialty         varchar(30) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS vet_specialty (
	vet_specialty_id  integer     PRIMARY KEY 	GENERATED ALWAYS AS IDENTITY,
	vet               varchar(30) REFERENCES vet,
	specialty         varchar(30) REFERENCES specialty
);

CREATE TABLE IF NOT EXISTS disease_state (
	disease_state     varchar(30) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS prescription ( 
	prescription_id   integer     PRIMARY KEY 	GENERATED ALWAYS AS IDENTITY, 
	start_date        date        NOT NULL, 
	end_date          date        CHECK ( (end_date IS NULL) OR ( (end_date IS NOT NULL) AND (end_date >= start_date) ) ),
	directions        text
);

CREATE TABLE IF NOT EXISTS examination ( 
	date_time         timestamp   NOT NULL, 
	examination_id    integer     PRIMARY KEY 	GENERATED ALWAYS AS IDENTITY, 
	cat_id            integer     NOT NULL    	REFERENCES cat, 
	vet_specialty_id  integer     NOT NULL   	REFERENCES vet_specialty, 
	disease 	  varchar(30) REFERENCES disease,
	disease_state     varchar(30) REFERENCES disease_state,
	comments	  text,
	prescription_id   integer     UNIQUE      	REFERENCES prescription,
	CHECK ( ( (disease IS NOT NULL) AND (disease_state IS NOT NULL) ) OR ( (disease IS NULL) AND (disease_state IS NULL) ) )
); 
