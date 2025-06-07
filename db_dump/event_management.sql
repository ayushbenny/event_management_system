-- Adminer 4.8.1 PostgreSQL 17.2 (Debian 17.2-1.pgdg120+1) dump

\connect "event_management";

DROP TABLE IF EXISTS "alembic_version";
CREATE TABLE "public"."alembic_version" (
    "version_num" character varying(32) NOT NULL,
    CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num")
) WITH (oids = false);

INSERT INTO "alembic_version" ("version_num") VALUES
('f3d9bd065732');

DROP TABLE IF EXISTS "attendees";
DROP SEQUENCE IF EXISTS attendees_id_seq;
CREATE SEQUENCE attendees_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 20 CACHE 1;

CREATE TABLE "public"."attendees" (
    "id" integer DEFAULT nextval('attendees_id_seq') NOT NULL,
    "name" character varying(255) NOT NULL,
    "email" character varying(255) NOT NULL,
    "event_id" integer NOT NULL,
    "registered_at" timestamptz,
    CONSTRAINT "attendees_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "unique_email_per_event" UNIQUE ("email", "event_id")
) WITH (oids = false);

CREATE INDEX "ix_attendees_email" ON "public"."attendees" USING btree ("email");

CREATE INDEX "ix_attendees_id" ON "public"."attendees" USING btree ("id");

INSERT INTO "attendees" ("id", "name", "email", "event_id", "registered_at") VALUES
(1,	'John Doe',	'john.doe@example.com',	2,	'2025-06-05 17:56:51.938192+00'),
(2,	'John Doe',	'john.doe@example.com',	1,	'2025-06-05 17:57:34.730238+00'),
(3,	'John Doe',	'john.doe@example.com',	3,	'2025-06-05 17:58:58.465527+00'),
(4,	'John Sammy',	'john.sammy@example.com',	3,	'2025-06-05 17:59:10.410253+00'),
(5,	'John Doe',	'john@example.com',	8,	'2025-06-06 14:13:34.528581+00'),
(6,	'Alice',	'alice@example.com',	9,	'2025-06-06 14:13:34.58007+00'),
(7,	'Bob',	'bob@example.com',	10,	'2025-06-06 14:13:34.625905+00'),
(8,	'Sam',	'sam@example.com',	11,	'2025-06-06 14:13:34.676848+00'),
(9,	'Tom',	'tom@example.com',	11,	'2025-06-06 14:13:34.681342+00'),
(10,	'John Doe',	'john@example.com',	13,	'2025-06-06 14:14:16.663874+00'),
(11,	'Alice',	'alice@example.com',	14,	'2025-06-06 14:14:16.713715+00'),
(12,	'Bob',	'bob@example.com',	15,	'2025-06-06 14:14:16.767378+00'),
(13,	'Sam',	'sam@example.com',	16,	'2025-06-06 14:14:16.816343+00'),
(14,	'Tom',	'tom@example.com',	16,	'2025-06-06 14:14:16.821042+00'),
(15,	'John Doe',	'john@example.com',	19,	'2025-06-06 14:15:08.243152+00'),
(16,	'Alice',	'alice@example.com',	20,	'2025-06-06 14:15:08.287502+00'),
(17,	'Bob',	'bob@example.com',	21,	'2025-06-06 14:15:08.331519+00'),
(18,	'Sam',	'sam@example.com',	22,	'2025-06-06 14:15:08.372431+00'),
(19,	'Tom',	'tom@example.com',	22,	'2025-06-06 14:15:08.378511+00'),
(20,	'John Dcruz',	'john.dcruz@example.com',	25,	'2025-06-07 06:32:32.979206+00');

DROP TABLE IF EXISTS "events";
DROP SEQUENCE IF EXISTS events_id_seq;
CREATE SEQUENCE events_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 25 CACHE 1;

CREATE TABLE "public"."events" (
    "id" integer DEFAULT nextval('events_id_seq') NOT NULL,
    "name" character varying(255) NOT NULL,
    "location" character varying(500) NOT NULL,
    "start_time" timestamptz NOT NULL,
    "end_time" timestamptz NOT NULL,
    "max_capacity" integer NOT NULL,
    "created_at" timestamptz,
    "updated_at" timestamptz,
    CONSTRAINT "events_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE INDEX "ix_events_id" ON "public"."events" USING btree ("id");

CREATE INDEX "ix_events_name" ON "public"."events" USING btree ("name");

CREATE INDEX "ix_events_start_time" ON "public"."events" USING btree ("start_time");

INSERT INTO "events" ("id", "name", "location", "start_time", "end_time", "max_capacity", "created_at", "updated_at") VALUES
(1,	'Tech Conference 2025',	'Bangalore International Exhibition Centre',	'2025-07-01 04:30:00+00',	'2025-07-01 11:30:00+00',	500,	'2025-06-05 17:52:25.259101+00',	'2025-06-05 17:52:25.259108+00'),
(2,	'Tech Conference 2025',	'Bangalore International Exhibition Centre',	'2025-07-01 04:30:00+00',	'2025-07-01 11:30:00+00',	500,	'2025-06-05 17:52:25.924644+00',	'2025-06-05 17:52:25.924649+00'),
(3,	'Tech Conference 2025',	'Bangalore International Exhibition Centre',	'2025-07-01 04:30:00+00',	'2025-07-01 11:30:00+00',	2,	'2025-06-05 17:52:26.48863+00',	'2025-06-05 17:52:26.488635+00'),
(4,	'Tech Conference 2025',	'Bangalore International Exhibition Centre',	'2025-07-01 04:30:00+00',	'2025-07-01 11:30:00+00',	500,	'2025-06-05 18:05:30.988576+00',	'2025-06-05 18:05:30.988584+00'),
(5,	'Tech Conference 2025',	'Bangalore International Exhibition Centre',	'2025-07-01 03:30:00+00',	'2025-07-02 12:30:00+00',	500,	'2025-06-05 18:25:58.042177+00',	'2025-06-05 18:25:58.042187+00'),
(6,	'Tech Conference 2025',	'Bangalore International Exhibition Centre',	'2025-07-01 03:30:00+00',	'2025-07-02 12:30:00+00',	500,	'2025-06-05 18:26:25.705771+00',	'2025-06-05 18:26:25.705777+00'),
(7,	'Upcoming Event',	'Delhi',	'2025-06-06 15:13:34.456166+00',	'2025-06-06 16:13:34.456177+00',	10,	'2025-06-06 14:13:34.466093+00',	'2025-06-06 14:13:34.466098+00'),
(8,	'Register Test Event',	'Mumbai',	'2025-06-06 16:13:34.518609+00',	'2025-06-06 17:13:34.518615+00',	1,	'2025-06-06 14:13:34.520121+00',	'2025-06-06 14:13:34.520125+00'),
(9,	'Duplicate Email Event',	'Bangalore',	'2025-06-06 17:13:34.572222+00',	'2025-06-06 18:13:34.572229+00',	2,	'2025-06-06 14:13:34.573071+00',	'2025-06-06 14:13:34.573074+00'),
(10,	'Full Capacity Event',	'Chennai',	'2025-06-06 17:13:34.617939+00',	'2025-06-06 18:13:34.617946+00',	1,	'2025-06-06 14:13:34.618686+00',	'2025-06-06 14:13:34.61869+00'),
(11,	'Attendee List Event',	'Hyderabad',	'2025-06-06 19:13:34.667367+00',	'2025-06-06 20:13:34.667376+00',	10,	'2025-06-06 14:13:34.66872+00',	'2025-06-06 14:13:34.668726+00'),
(12,	'Upcoming Event',	'Delhi',	'2025-06-06 15:14:16.589359+00',	'2025-06-06 16:14:16.589366+00',	10,	'2025-06-06 14:14:16.598072+00',	'2025-06-06 14:14:16.59808+00'),
(13,	'Register Test Event',	'Mumbai',	'2025-06-06 16:14:16.644131+00',	'2025-06-06 17:14:16.644141+00',	1,	'2025-06-06 14:14:16.646879+00',	'2025-06-06 14:14:16.646889+00'),
(14,	'Duplicate Email Event',	'Bangalore',	'2025-06-06 17:14:16.702302+00',	'2025-06-06 18:14:16.70231+00',	2,	'2025-06-06 14:14:16.703455+00',	'2025-06-06 14:14:16.70346+00'),
(15,	'Full Capacity Event',	'Chennai',	'2025-06-06 17:14:16.757729+00',	'2025-06-06 18:14:16.757738+00',	1,	'2025-06-06 14:14:16.758815+00',	'2025-06-06 14:14:16.75882+00'),
(16,	'Attendee List Event',	'Hyderabad',	'2025-06-06 19:14:16.805941+00',	'2025-06-06 20:14:16.805949+00',	10,	'2025-06-06 14:14:16.806982+00',	'2025-06-06 14:14:16.806988+00'),
(17,	'Test Event',	'Test Location',	'2025-06-06 15:15:08.134011+00',	'2025-06-06 16:15:08.134017+00',	100,	'2025-06-06 14:15:08.143093+00',	'2025-06-06 14:15:08.143098+00'),
(18,	'Upcoming Event',	'Delhi',	'2025-06-06 15:15:08.175302+00',	'2025-06-06 16:15:08.175311+00',	10,	'2025-06-06 14:15:08.17663+00',	'2025-06-06 14:15:08.176636+00'),
(19,	'Register Test Event',	'Mumbai',	'2025-06-06 16:15:08.23034+00',	'2025-06-06 17:15:08.230349+00',	1,	'2025-06-06 14:15:08.231464+00',	'2025-06-06 14:15:08.23147+00'),
(20,	'Duplicate Email Event',	'Bangalore',	'2025-06-06 17:15:08.278061+00',	'2025-06-06 18:15:08.278071+00',	2,	'2025-06-06 14:15:08.279563+00',	'2025-06-06 14:15:08.27957+00'),
(21,	'Full Capacity Event',	'Chennai',	'2025-06-06 17:15:08.321561+00',	'2025-06-06 18:15:08.32157+00',	1,	'2025-06-06 14:15:08.322686+00',	'2025-06-06 14:15:08.322692+00'),
(22,	'Attendee List Event',	'Hyderabad',	'2025-06-06 19:15:08.363454+00',	'2025-06-06 20:15:08.363462+00',	10,	'2025-06-06 14:15:08.364282+00',	'2025-06-06 14:15:08.364288+00'),
(23,	'Tech Conference 2025',	'Bangalore International Exhibition Centre',	'2025-07-01 03:30:00+00',	'2025-07-02 12:30:00+00',	500,	'2025-06-07 06:21:49.41474+00',	'2025-06-07 06:21:49.414744+00'),
(24,	'Tech Conference 2025',	'Bangalore International Exhibition Centre',	'2025-07-01 03:30:00+00',	'2025-07-02 12:30:00+00',	500,	'2025-06-07 06:29:21.949741+00',	'2025-06-07 06:29:21.949745+00'),
(25,	'Tech Conference 2025',	'Bangalore International Exhibition Centre',	'2025-07-01 03:30:00+00',	'2025-07-02 12:30:00+00',	500,	'2025-06-07 06:29:49.648497+00',	'2025-06-07 06:29:49.648503+00');

ALTER TABLE ONLY "public"."attendees" ADD CONSTRAINT "attendees_event_id_fkey" FOREIGN KEY (event_id) REFERENCES events(id) NOT DEFERRABLE;

-- 2025-06-07 06:36:44.150883+00

