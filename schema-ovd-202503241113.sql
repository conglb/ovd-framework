--
-- PostgreSQL database cluster dump
--

-- Started on 2025-03-24 11:13:07 CET

SET default_transaction_read_only = off;

SET client_encoding = 'BIG5';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE admin;
ALTER ROLE admin WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS;

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.6
-- Dumped by pg_dump version 16.4

-- Started on 2025-03-24 11:13:07 CET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'BIG5';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 17111)
-- Name: timescaledb; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS timescaledb WITH SCHEMA public;


--
-- TOC entry 4007 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION timescaledb; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION timescaledb IS 'Enables scalable inserts and complex queries for time-series data (Community Edition)';


--
-- TOC entry 3716 (class 0 OID 17132)
-- Dependencies: 225
-- Data for Name: hypertable; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.hypertable (id, schema_name, table_name, associated_schema_name, associated_table_prefix, num_dimensions, chunk_sizing_func_schema, chunk_sizing_func_name, chunk_target_size, compression_state, compressed_hypertable_id, status) FROM stdin;
\.


--
-- TOC entry 3722 (class 0 OID 17202)
-- Dependencies: 233
-- Data for Name: chunk; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.chunk (id, hypertable_id, schema_name, table_name, compressed_chunk_id, dropped, status, osm_chunk, creation_time) FROM stdin;
\.


--
-- TOC entry 3727 (class 0 OID 17261)
-- Dependencies: 238
-- Data for Name: chunk_column_stats; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.chunk_column_stats (id, hypertable_id, chunk_id, column_name, range_start, range_end, valid) FROM stdin;
\.


--
-- TOC entry 3718 (class 0 OID 17168)
-- Dependencies: 229
-- Data for Name: dimension; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.dimension (id, hypertable_id, column_name, column_type, aligned, num_slices, partitioning_func_schema, partitioning_func, interval_length, compress_interval_length, integer_now_func_schema, integer_now_func) FROM stdin;
\.


--
-- TOC entry 3720 (class 0 OID 17187)
-- Dependencies: 231
-- Data for Name: dimension_slice; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.dimension_slice (id, dimension_id, range_start, range_end) FROM stdin;
\.


--
-- TOC entry 3724 (class 0 OID 17227)
-- Dependencies: 234
-- Data for Name: chunk_constraint; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.chunk_constraint (chunk_id, dimension_slice_id, constraint_name, hypertable_constraint_name) FROM stdin;
\.


--
-- TOC entry 3726 (class 0 OID 17244)
-- Dependencies: 236
-- Data for Name: chunk_index; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.chunk_index (chunk_id, index_name, hypertable_id, hypertable_index_name) FROM stdin;
\.


--
-- TOC entry 3739 (class 0 OID 17440)
-- Dependencies: 255
-- Data for Name: compression_chunk_size; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.compression_chunk_size (chunk_id, compressed_chunk_id, uncompressed_heap_size, uncompressed_toast_size, uncompressed_index_size, compressed_heap_size, compressed_toast_size, compressed_index_size, numrows_pre_compression, numrows_post_compression, numrows_frozen_immediately) FROM stdin;
\.


--
-- TOC entry 3738 (class 0 OID 17430)
-- Dependencies: 254
-- Data for Name: compression_settings; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.compression_settings (relid, segmentby, orderby, orderby_desc, orderby_nullsfirst) FROM stdin;
\.


--
-- TOC entry 3732 (class 0 OID 17350)
-- Dependencies: 247
-- Data for Name: continuous_agg; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_agg (mat_hypertable_id, raw_hypertable_id, parent_mat_hypertable_id, user_view_schema, user_view_name, partial_view_schema, partial_view_name, direct_view_schema, direct_view_name, materialized_only, finalized) FROM stdin;
\.


--
-- TOC entry 3740 (class 0 OID 17456)
-- Dependencies: 256
-- Data for Name: continuous_agg_migrate_plan; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_agg_migrate_plan (mat_hypertable_id, start_ts, end_ts, user_view_definition) FROM stdin;
\.


--
-- TOC entry 3741 (class 0 OID 17465)
-- Dependencies: 258
-- Data for Name: continuous_agg_migrate_plan_step; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_agg_migrate_plan_step (mat_hypertable_id, step_id, status, start_ts, end_ts, type, config) FROM stdin;
\.


--
-- TOC entry 3733 (class 0 OID 17377)
-- Dependencies: 248
-- Data for Name: continuous_aggs_bucket_function; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_aggs_bucket_function (mat_hypertable_id, bucket_func, bucket_width, bucket_origin, bucket_offset, bucket_timezone, bucket_fixed_width) FROM stdin;
\.


--
-- TOC entry 3736 (class 0 OID 17410)
-- Dependencies: 251
-- Data for Name: continuous_aggs_hypertable_invalidation_log; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_aggs_hypertable_invalidation_log (hypertable_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- TOC entry 3734 (class 0 OID 17390)
-- Dependencies: 249
-- Data for Name: continuous_aggs_invalidation_threshold; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_aggs_invalidation_threshold (hypertable_id, watermark) FROM stdin;
\.


--
-- TOC entry 3737 (class 0 OID 17414)
-- Dependencies: 252
-- Data for Name: continuous_aggs_materialization_invalidation_log; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_aggs_materialization_invalidation_log (materialization_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- TOC entry 3735 (class 0 OID 17400)
-- Dependencies: 250
-- Data for Name: continuous_aggs_watermark; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_aggs_watermark (mat_hypertable_id, watermark) FROM stdin;
\.


--
-- TOC entry 3731 (class 0 OID 17337)
-- Dependencies: 245
-- Data for Name: metadata; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.metadata (key, value, include_in_telemetry) FROM stdin;
install_timestamp	2024-10-24 19:34:42.636484+00	t
timescaledb_version	2.17.1	f
\.


--
-- TOC entry 3717 (class 0 OID 17154)
-- Dependencies: 227
-- Data for Name: tablespace; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.tablespace (id, hypertable_id, tablespace_name) FROM stdin;
\.


--
-- TOC entry 3730 (class 0 OID 17281)
-- Dependencies: 240
-- Data for Name: bgw_job; Type: TABLE DATA; Schema: _timescaledb_config; Owner: admin
--

COPY _timescaledb_config.bgw_job (id, application_name, schedule_interval, max_runtime, max_retries, retry_period, proc_schema, proc_name, owner, scheduled, fixed_schedule, initial_start, hypertable_id, config, check_schema, check_name, timezone) FROM stdin;
\.


--
-- TOC entry 4008 (class 0 OID 0)
-- Dependencies: 237
-- Name: chunk_column_stats_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_column_stats_id_seq', 1, false);


--
-- TOC entry 4009 (class 0 OID 0)
-- Dependencies: 235
-- Name: chunk_constraint_name; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_constraint_name', 1, false);


--
-- TOC entry 4010 (class 0 OID 0)
-- Dependencies: 232
-- Name: chunk_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_id_seq', 1, false);


--
-- TOC entry 4011 (class 0 OID 0)
-- Dependencies: 257
-- Name: continuous_agg_migrate_plan_step_step_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.continuous_agg_migrate_plan_step_step_id_seq', 1, false);


--
-- TOC entry 4012 (class 0 OID 0)
-- Dependencies: 228
-- Name: dimension_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.dimension_id_seq', 1, false);


--
-- TOC entry 4013 (class 0 OID 0)
-- Dependencies: 230
-- Name: dimension_slice_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.dimension_slice_id_seq', 1, false);


--
-- TOC entry 4014 (class 0 OID 0)
-- Dependencies: 224
-- Name: hypertable_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.hypertable_id_seq', 1, false);


--
-- TOC entry 4015 (class 0 OID 0)
-- Dependencies: 239
-- Name: bgw_job_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_config; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_config.bgw_job_id_seq', 1000, false);


-- Completed on 2025-03-24 11:13:07 CET

--
-- PostgreSQL database dump complete
--

--
-- Database "ovd" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.6
-- Dumped by pg_dump version 16.4

-- Started on 2025-03-24 11:13:07 CET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'BIG5';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4027 (class 1262 OID 16384)
-- Name: ovd; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE ovd WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE ovd OWNER TO admin;

\connect ovd

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'BIG5';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 17837)
-- Name: timescaledb; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS timescaledb WITH SCHEMA public;


--
-- TOC entry 4028 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION timescaledb; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION timescaledb IS 'Enables scalable inserts and complex queries for time-series data (Community Edition)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 276 (class 1259 OID 18719)
-- Name: ais_data; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.ais_data (
    "timestamp" timestamp with time zone NOT NULL,
    mmsi bigint NOT NULL,
    imo text,
    ship_type text,
    heading real,
    course real,
    speed real,
    navstatus text,
    name text,
    callsign text,
    draught real,
    destination text,
    eta timestamp without time zone,
    latitude real,
    longitude real,
    extra jsonb
);


ALTER TABLE public.ais_data OWNER TO admin;

--
-- TOC entry 279 (class 1259 OID 27186)
-- Name: engine_data; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.engine_data (
    source_id character varying,
    "timestamp" timestamp with time zone,
    source_type character varying
);


ALTER TABLE public.engine_data OWNER TO admin;

--
-- TOC entry 278 (class 1259 OID 27183)
-- Name: ship_information; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.ship_information (
);


ALTER TABLE public.ship_information OWNER TO admin;

--
-- TOC entry 277 (class 1259 OID 27180)
-- Name: weather_data; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.weather_data (
);


ALTER TABLE public.weather_data OWNER TO admin;

--
-- TOC entry 3732 (class 0 OID 17858)
-- Dependencies: 225
-- Data for Name: hypertable; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.hypertable (id, schema_name, table_name, associated_schema_name, associated_table_prefix, num_dimensions, chunk_sizing_func_schema, chunk_sizing_func_name, chunk_target_size, compression_state, compressed_hypertable_id, status) FROM stdin;
\.


--
-- TOC entry 3738 (class 0 OID 17928)
-- Dependencies: 233
-- Data for Name: chunk; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.chunk (id, hypertable_id, schema_name, table_name, compressed_chunk_id, dropped, status, osm_chunk, creation_time) FROM stdin;
\.


--
-- TOC entry 3743 (class 0 OID 17987)
-- Dependencies: 238
-- Data for Name: chunk_column_stats; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.chunk_column_stats (id, hypertable_id, chunk_id, column_name, range_start, range_end, valid) FROM stdin;
\.


--
-- TOC entry 3734 (class 0 OID 17894)
-- Dependencies: 229
-- Data for Name: dimension; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.dimension (id, hypertable_id, column_name, column_type, aligned, num_slices, partitioning_func_schema, partitioning_func, interval_length, compress_interval_length, integer_now_func_schema, integer_now_func) FROM stdin;
\.


--
-- TOC entry 3736 (class 0 OID 17913)
-- Dependencies: 231
-- Data for Name: dimension_slice; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.dimension_slice (id, dimension_id, range_start, range_end) FROM stdin;
\.


--
-- TOC entry 3740 (class 0 OID 17953)
-- Dependencies: 234
-- Data for Name: chunk_constraint; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.chunk_constraint (chunk_id, dimension_slice_id, constraint_name, hypertable_constraint_name) FROM stdin;
\.


--
-- TOC entry 3742 (class 0 OID 17970)
-- Dependencies: 236
-- Data for Name: chunk_index; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.chunk_index (chunk_id, index_name, hypertable_id, hypertable_index_name) FROM stdin;
\.


--
-- TOC entry 3755 (class 0 OID 18166)
-- Dependencies: 255
-- Data for Name: compression_chunk_size; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.compression_chunk_size (chunk_id, compressed_chunk_id, uncompressed_heap_size, uncompressed_toast_size, uncompressed_index_size, compressed_heap_size, compressed_toast_size, compressed_index_size, numrows_pre_compression, numrows_post_compression, numrows_frozen_immediately) FROM stdin;
\.


--
-- TOC entry 3754 (class 0 OID 18156)
-- Dependencies: 254
-- Data for Name: compression_settings; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.compression_settings (relid, segmentby, orderby, orderby_desc, orderby_nullsfirst) FROM stdin;
\.


--
-- TOC entry 3748 (class 0 OID 18076)
-- Dependencies: 247
-- Data for Name: continuous_agg; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_agg (mat_hypertable_id, raw_hypertable_id, parent_mat_hypertable_id, user_view_schema, user_view_name, partial_view_schema, partial_view_name, direct_view_schema, direct_view_name, materialized_only, finalized) FROM stdin;
\.


--
-- TOC entry 3756 (class 0 OID 18182)
-- Dependencies: 256
-- Data for Name: continuous_agg_migrate_plan; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_agg_migrate_plan (mat_hypertable_id, start_ts, end_ts, user_view_definition) FROM stdin;
\.


--
-- TOC entry 3757 (class 0 OID 18191)
-- Dependencies: 258
-- Data for Name: continuous_agg_migrate_plan_step; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_agg_migrate_plan_step (mat_hypertable_id, step_id, status, start_ts, end_ts, type, config) FROM stdin;
\.


--
-- TOC entry 3749 (class 0 OID 18103)
-- Dependencies: 248
-- Data for Name: continuous_aggs_bucket_function; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_aggs_bucket_function (mat_hypertable_id, bucket_func, bucket_width, bucket_origin, bucket_offset, bucket_timezone, bucket_fixed_width) FROM stdin;
\.


--
-- TOC entry 3752 (class 0 OID 18136)
-- Dependencies: 251
-- Data for Name: continuous_aggs_hypertable_invalidation_log; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_aggs_hypertable_invalidation_log (hypertable_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- TOC entry 3750 (class 0 OID 18116)
-- Dependencies: 249
-- Data for Name: continuous_aggs_invalidation_threshold; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_aggs_invalidation_threshold (hypertable_id, watermark) FROM stdin;
\.


--
-- TOC entry 3753 (class 0 OID 18140)
-- Dependencies: 252
-- Data for Name: continuous_aggs_materialization_invalidation_log; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_aggs_materialization_invalidation_log (materialization_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- TOC entry 3751 (class 0 OID 18126)
-- Dependencies: 250
-- Data for Name: continuous_aggs_watermark; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.continuous_aggs_watermark (mat_hypertable_id, watermark) FROM stdin;
\.


--
-- TOC entry 3747 (class 0 OID 18063)
-- Dependencies: 245
-- Data for Name: metadata; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.metadata (key, value, include_in_telemetry) FROM stdin;
install_timestamp	2024-10-24 19:34:42.827566+00	t
timescaledb_version	2.17.1	f
exported_uuid	f9561b24-35bc-4dd3-a664-b6513508abf8	t
\.


--
-- TOC entry 3733 (class 0 OID 17880)
-- Dependencies: 227
-- Data for Name: tablespace; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: admin
--

COPY _timescaledb_catalog.tablespace (id, hypertable_id, tablespace_name) FROM stdin;
\.


--
-- TOC entry 3746 (class 0 OID 18007)
-- Dependencies: 240
-- Data for Name: bgw_job; Type: TABLE DATA; Schema: _timescaledb_config; Owner: admin
--

COPY _timescaledb_config.bgw_job (id, application_name, schedule_interval, max_runtime, max_retries, retry_period, proc_schema, proc_name, owner, scheduled, fixed_schedule, initial_start, hypertable_id, config, check_schema, check_name, timezone) FROM stdin;
\.


--
-- TOC entry 4018 (class 0 OID 18719)
-- Dependencies: 276
-- Data for Name: ais_data; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.ais_data ("timestamp", mmsi, imo, ship_type, heading, course, speed, navstatus, name, callsign, draught, destination, eta, latitude, longitude, extra) FROM stdin;
\.


--
-- TOC entry 4021 (class 0 OID 27186)
-- Dependencies: 279
-- Data for Name: engine_data; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.engine_data (source_id, "timestamp", source_type) FROM stdin;
\.


--
-- TOC entry 4020 (class 0 OID 27183)
-- Dependencies: 278
-- Data for Name: ship_information; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.ship_information  FROM stdin;
\.


--
-- TOC entry 4019 (class 0 OID 27180)
-- Dependencies: 277
-- Data for Name: weather_data; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.weather_data  FROM stdin;
\.


--
-- TOC entry 4029 (class 0 OID 0)
-- Dependencies: 237
-- Name: chunk_column_stats_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_column_stats_id_seq', 1, false);


--
-- TOC entry 4030 (class 0 OID 0)
-- Dependencies: 235
-- Name: chunk_constraint_name; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_constraint_name', 1, false);


--
-- TOC entry 4031 (class 0 OID 0)
-- Dependencies: 232
-- Name: chunk_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_id_seq', 1, false);


--
-- TOC entry 4032 (class 0 OID 0)
-- Dependencies: 257
-- Name: continuous_agg_migrate_plan_step_step_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.continuous_agg_migrate_plan_step_step_id_seq', 1, false);


--
-- TOC entry 4033 (class 0 OID 0)
-- Dependencies: 228
-- Name: dimension_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.dimension_id_seq', 1, false);


--
-- TOC entry 4034 (class 0 OID 0)
-- Dependencies: 230
-- Name: dimension_slice_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.dimension_slice_id_seq', 1, false);


--
-- TOC entry 4035 (class 0 OID 0)
-- Dependencies: 224
-- Name: hypertable_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_catalog.hypertable_id_seq', 1, false);


--
-- TOC entry 4036 (class 0 OID 0)
-- Dependencies: 239
-- Name: bgw_job_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_config; Owner: admin
--

SELECT pg_catalog.setval('_timescaledb_config.bgw_job_id_seq', 1000, false);


-- Completed on 2025-03-24 11:13:07 CET

--
-- PostgreSQL database dump complete
--

-- Completed on 2025-03-24 11:13:07 CET

--
-- PostgreSQL database cluster dump complete
--

