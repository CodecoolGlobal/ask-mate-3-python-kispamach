--
-- PostgreSQL database dump
--

-- Dumped from database version 12.6 (Ubuntu 12.6-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.6 (Ubuntu 12.6-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: martin
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer,
    is_accepted boolean
);


ALTER TABLE public.answer OWNER TO martin;

--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: martin
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answer_id_seq OWNER TO martin;

--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: martin
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: martin
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer
);


ALTER TABLE public.comment OWNER TO martin;

--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: martin
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_id_seq OWNER TO martin;

--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: martin
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: martin
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);


ALTER TABLE public.question OWNER TO martin;

--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: martin
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_id_seq OWNER TO martin;

--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: martin
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: question_tag; Type: TABLE; Schema: public; Owner: martin
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.question_tag OWNER TO martin;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: martin
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


ALTER TABLE public.tag OWNER TO martin;

--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: martin
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO martin;

--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: martin
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: martin
--

CREATE TABLE public.users (
    userid integer NOT NULL,
    email text,
    password text,
    registration_time timestamp without time zone,
    reputation integer
);


ALTER TABLE public.users OWNER TO martin;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: martin
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO martin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: martin
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.userid;


--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Name: users userid; Type: DEFAULT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.users ALTER COLUMN userid SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: martin
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image, user_id, is_accepted) FROM stdin;
13	2021-02-17 11:08:49	1	6	dasdasdas	\N	10	f
12	2021-02-17 10:23:45	0	6	test answer	\N	8	f
14	2021-02-17 12:24:25	0	7	dsadasdas	\N	10	f
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: martin
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) FROM stdin;
11	6	\N	dasdas	2021-02-16 15:16:12	\N	10
15	7	\N	jó lenne ha lenne	2021-02-18 08:47:49	2	8
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: martin
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image, user_id) FROM stdin;
6	2021-02-16 14:48:22	20	8	Meddig leszünk ma?	Remélem nem sokáig, meccs előtt jól jönne egy kis szundi.	\N	10
7	2021-02-16 15:20:50	49	14	Kép van a gépen?	Van a kép ezen a gépen?	\N	9
\.


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: martin
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
6	5
7	6
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: martin
--

COPY public.tag (id, name) FROM stdin;
4	#liverpoollipcse
5	das
6	picture
7	kecske
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: martin
--

COPY public.users (userid, email, password, registration_time, reputation) FROM stdin;
6	smartin96@citromail.hu	$2b$12$RjCASCOGvJVLrqpYOrcGWuDVPIYQlShhRHUhE8Db6gwMm42O8iFSm	2021-02-16 14:46:13	0
8	balazs@citromail.hu	$2b$12$MoZPLt46FqY7B42CkXBFCeX.SGms3aEw5qLcQL9OPwPE28yH3iJHi	2021-02-16 14:47:05	0
7	gergo@gmail.com	$2b$12$AKGzo7FiD31zjx5YHdge9uDNjdUon2GEdaQcwv1k92oWHpXTexgvi	2021-02-16 14:46:47	36
10	martin@hotmail.hu	$2b$12$pb8BYswIkq7agnAC.fPGl.eTq.PzJwb9icvHiAtoi6V9wdESEgNjO	2021-02-16 14:47:46	148
9	david@freemail.hu	$2b$12$aRRwkYY69cbtt4dC.PuLeOEklsydKdY5UzuCpOK1oh.hJwELmV7Va	2021-02-16 14:47:21	72
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: martin
--

SELECT pg_catalog.setval('public.answer_id_seq', 14, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: martin
--

SELECT pg_catalog.setval('public.comment_id_seq', 21, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: martin
--

SELECT pg_catalog.setval('public.question_id_seq', 11, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: martin
--

SELECT pg_catalog.setval('public.tag_id_seq', 7, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: martin
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- Name: users pk_id; Type: CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_id PRIMARY KEY (userid);


--
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- Name: question fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(userid);


--
-- Name: comment fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(userid);


--
-- Name: answer fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: martin
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(userid);


--
-- PostgreSQL database dump complete
--

