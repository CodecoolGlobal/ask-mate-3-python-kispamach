--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

-- Started on 2021-02-18 15:31:09

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 200 (class 1259 OID 16598)
-- Name: answer; Type: TABLE; Schema: public; Owner: haku9104
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


ALTER TABLE public.answer OWNER TO haku9104;

--
-- TOC entry 201 (class 1259 OID 16604)
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: haku9104
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answer_id_seq OWNER TO haku9104;

--
-- TOC entry 3054 (class 0 OID 0)
-- Dependencies: 201
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: haku9104
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- TOC entry 202 (class 1259 OID 16606)
-- Name: comment; Type: TABLE; Schema: public; Owner: haku9104
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


ALTER TABLE public.comment OWNER TO haku9104;

--
-- TOC entry 203 (class 1259 OID 16612)
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: haku9104
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_id_seq OWNER TO haku9104;

--
-- TOC entry 3055 (class 0 OID 0)
-- Dependencies: 203
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: haku9104
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- TOC entry 204 (class 1259 OID 16614)
-- Name: question; Type: TABLE; Schema: public; Owner: haku9104
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


ALTER TABLE public.question OWNER TO haku9104;

--
-- TOC entry 205 (class 1259 OID 16620)
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: haku9104
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_id_seq OWNER TO haku9104;

--
-- TOC entry 3056 (class 0 OID 0)
-- Dependencies: 205
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: haku9104
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- TOC entry 206 (class 1259 OID 16622)
-- Name: question_tag; Type: TABLE; Schema: public; Owner: haku9104
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.question_tag OWNER TO haku9104;

--
-- TOC entry 207 (class 1259 OID 16625)
-- Name: tag; Type: TABLE; Schema: public; Owner: haku9104
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


ALTER TABLE public.tag OWNER TO haku9104;

--
-- TOC entry 208 (class 1259 OID 16631)
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: haku9104
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO haku9104;

--
-- TOC entry 3057 (class 0 OID 0)
-- Dependencies: 208
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: haku9104
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- TOC entry 209 (class 1259 OID 16633)
-- Name: users; Type: TABLE; Schema: public; Owner: haku9104
--

CREATE TABLE public.users (
    userid integer NOT NULL,
    email text,
    password text,
    registration_time timestamp without time zone,
    reputation integer
);


ALTER TABLE public.users OWNER TO haku9104;

--
-- TOC entry 210 (class 1259 OID 16639)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: haku9104
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO haku9104;

--
-- TOC entry 3058 (class 0 OID 0)
-- Dependencies: 210
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: haku9104
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.userid;


--
-- TOC entry 2883 (class 2604 OID 16641)
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- TOC entry 2884 (class 2604 OID 16642)
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- TOC entry 2885 (class 2604 OID 16643)
-- Name: question id; Type: DEFAULT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- TOC entry 2886 (class 2604 OID 16644)
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- TOC entry 2887 (class 2604 OID 16645)
-- Name: users userid; Type: DEFAULT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.users ALTER COLUMN userid SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3038 (class 0 OID 16598)
-- Dependencies: 200
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: haku9104
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image, user_id, is_accepted) FROM stdin;
13	2021-02-17 11:08:49	1	6	dasdasdas	\N	10	f
12	2021-02-17 10:23:45	0	6	test answer	\N	8	f
14	2021-02-17 12:24:25	0	7	dsadasdas	\N	10	f
\.


--
-- TOC entry 3040 (class 0 OID 16606)
-- Dependencies: 202
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: haku9104
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) FROM stdin;
11	6	\N	dasdas	2021-02-16 15:16:12	\N	10
15	7	\N	jó lenne ha lenne	2021-02-18 08:47:49	2	8
\.


--
-- TOC entry 3042 (class 0 OID 16614)
-- Dependencies: 204
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: haku9104
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image, user_id) FROM stdin;
6	2021-02-16 14:48:22	20	8	Meddig leszünk ma?	Remélem nem sokáig, meccs előtt jól jönne egy kis szundi.	\N	10
7	2021-02-16 15:20:50	49	14	Kép van a gépen?	Van a kép ezen a gépen?	\N	9
13	2021-02-18 09:35:37	1	6	Sql Update Query	I have a table T1 which contains three columns: Id, Name, Address\r\n\r\nThere is another table T2 which contains 2 columns Id, New_Address. Id column of T2 is same as of T1.\r\n\r\nI need a query which will update Address column of T1 with New_Address of T2.\r\n\r\nI can do it through a loop by checking ID and executing update statement. How can it has to be done with a query?	images/uploaded_images/13.png	8
12	2021-02-18 09:34:17	1	36	Best and/or fastest way to create lists in python?	 I don't think there would be any performance difference given that the lists have only 50 elements, but what if I need a list of a million elements? Would the use of xrange make any improvement? Which is the preferred/fastest way to create and initialize lists in python?	images/uploaded_images/12.jpeg	8
14	2021-02-18 09:38:06	1	23	 How do I take my Python skills to the next level?	How do I improve my python coding skills? I feel like i could do better	images/uploaded_images/14.jpeg	10
19	2021-02-18 09:45:32	9	-6	What does the “yield” keyword do?	What is the use of the yield keyword in Python, and what does it do?\r\n\r\nFor example, I'm trying to understand this code1:\r\n\r\ndef _get_child_candidates(self, distance, min_dist, max_dist):\r\n    if self._leftchild and distance - max_dist < self._median:\r\n        yield self._leftchild\r\n    if self._rightchild and distance + max_dist >= self._median:\r\n        yield self._rightchild  \r\nAnd this is the caller:\r\n\r\nresult, candidates = [], [self]\r\nwhile candidates:\r\n    node = candidates.pop()\r\n    distance = node._get_dist(obj)\r\n    if distance <= max_dist and distance >= min_dist:\r\n        result.extend(node._values)\r\n    candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))\r\nreturn result\r\nWhat happens when the method _get_child_candidates is called? Is a list returned? A single element? Is it called again? When will subsequent calls stop?	\N	7
16	2021-02-18 09:41:55	6	1	How are the new tf.contrib.summary summaries in TensorFlow evaluated?	I'm having a bit of trouble understanding the new tf.contrib.summary API. In the old one, it seemed that all one was supposed to do was to run tf.summary.merge_all() and run that as an op.\r\n\r\nBut now we have things like tf.contrib.summary.record_summaries_every_n_global_steps, which can be used like this:\r\n\r\nimport tensorflow.contrib.summary as tfsum\r\n\r\nsummary_writer = tfsum.create_file_writer(logdir, flush_millis=3000)\r\nsummaries = []\r\n\r\n# First we create one summary which runs every n global steps\r\nwith summary_writer.as_default(), tfsum.record_summaries_every_n_global_steps(30):\r\n    summaries.append(tfsum.scalar("train/loss", loss))\r\n\r\n# And then one that runs every single time?\r\nwith summary_writer.as_default(), tfsum.always_record_summaries():\r\n    summaries.append(tfsum.scalar("train/accuracy", accuracy))\r\n\r\n# Then create an optimizer which uses a global step\r\nstep = tf.create_global_step()\r\ntrain = tf.train.AdamOptimizer().minimize(loss, global_step=step)\r\nAnd now come a few questions:\r\n\r\nIf we just run session.run(summaries) in a loop, I assume that the accuracy summary would get written every single time, while the loss one wouldn't, because it only gets written if the global step is divisible by 30?\r\nAssuming the summaries automatically evaluate their dependencies, I never need to run session.run([accuracy, summaries]) but can just run, session.run(summaries) since they have a dependency in the graph, right?\r\nIf 2) is true, can't I just add a control dependency to the training step so that the summaries are written on every train run? Or is this a bad practice?\r\nIs there any downside to using control dependencies in general for things which are going to be evaluated at the same time anyway?\r\nWhy does tf.contrib.summary.scalar (and others) take in a step parameter?\r\nBy adding a control dependency in 3) I mean doing this:\r\n\r\ntf.control_dependencies(summaries):\r\n    train = tf.train.AdamOptimizer().minimize(loss, global_step=step)	images/uploaded_images/16.png	9
17	2021-02-18 09:43:21	7	5	Google App Engine Remote API does not work from local client	This is using the Python SDK version 1.8.0.\r\n\r\nMy remote API works fine using remote_api_shell.py, but doesn't work when trying to accessing from within a python script. I'm using the sample code from google:\r\n\r\nfrom google.appengine.ext.remote_api import remote_api_stub\r\nimport getpass\r\n\r\ndef auth_func():\r\n  return (raw_input('Username:'), getpass.getpass('Password:'))\r\n\r\nremote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', auth_func,\r\n                               'localhost:8080')\r\nand I'm also importing the fix_sys_path() from dev_appserver.py to set my sys.path correctly for the google app engine SDK:\r\n\r\nimport dev_appserver\r\ndev_appserver.fix_sys_path()\r\nthat adds, among other paths, the following line to my sys.path:\r\n\r\n'/google_appengine_1.8.0/lib/fancy_urllib'\r\nHowever, the following error is thrown when the above call to remote_api_stub.ConfigureRemoteApi() is called:\r\n\r\nopener.add_handler(fancy_urllib.FancyProxyHandler())\r\nAttributeError: 'module' object has no attribute 'FancyProxyHandler'	\N	9
18	2021-02-18 09:44:16	6	14	Mayavi colorbar in TraitsUI creating blank window	I'm trying to create a GUI in TraitsUI that includes two Mayavi figures. I have implemented these figures as per the multiple engines example in the Mayavi documentation.\r\n\r\nHowever, when I add a colorbar to one of the figures and run the GUI script it sometimes opens a blank Mayavi Scene Editor window in addition to the desired TraitsUI window. This blank window doesn't always appear, never on the first run after restarting the python kernel, and sometimes only after running the script a few times in succession and closing the windows that appear each time.\r\n\r\nRunning the much-reduced code below produces the same behaviour, and removing the mlab.colorbar(s) line stops the problem. How can I get a colorbar without opening blank windows? There doesn't seem to be an obvious way to assign a colorbar to a specific figure as for the surface plot. I am running Python 3.5 on Windows 7 (but get the same issues on Ubuntu).\r\n\r\nfrom traits.api import HasTraits, Instance, on_trait_change\r\nfrom traitsui.api import View, Item\r\nimport numpy as np\r\n\r\nfrom mayavi.core.api import Engine\r\nfrom mayavi.core.ui.api import SceneEditor, MlabSceneModel\r\nfrom mayavi import mlab\r\n\r\n#Generate a test surface to display\r\ndef test_surf():\r\n    x, y = np.mgrid[-7.:7.05:0.1, -5.:5.05:0.05]\r\n    z = np.sin(x + y) + np.sin(2 * x - y) + np.cos(3 * x + 4 * y)\r\n    return x, y, z        \r\n\r\nclass MyApp(HasTraits):\r\n\r\n    #Create a mayavi scene with a specified engine\r\n    engine = Instance(Engine, ())\r\n    scene = Instance(MlabSceneModel)\r\n    def _scene_default(self):\r\n        self.engine.start()\r\n        return MlabSceneModel(engine=self.engine)         \r\n\r\n    #Plot the surface when the scene is activated\r\n    @on_trait_change('scene.activated')\r\n    def populate_scene(self):\r\n        s = mlab.surf(*test_surf(), figure=self.scene.mayavi_scene)\r\n        mlab.colorbar(s)\r\n\r\n    view = View(Item('scene', editor=SceneEditor()))\r\n\r\nif __name__ == '__main__':\r\n    MyApp().configure_traits()	images/uploaded_images/18.jpeg	9
15	2021-02-18 09:39:23	15	11	How to use pygame module?	import pygame\r\nimport time\r\nimport datetime\r\ncup=int(input("please enter how many cups you want to drink in a day: "))\r\ninterval=int(input("please enter after how many minutes we should remind you: "))\r\nwaterat=time.time() #gives some random time which will help we know the duration\r\nintervalsec=interval*60\r\nif (cup>0):\r\n    if (time.time()-waterat)>intervalsec:\r\n        print("DRINK WATER!!!!!!")\r\n        while (true):\r\n            pygame.mixer.music.load('water.mp3')\r\n            pygame.mixer.music.play(-1)\r\n            #plays infinite time\r\n            word=input("enter done if you done drinking water: ")\r\n            if (word.lower=="done"):\r\n                cup=cup-1\r\n                waterat=time.time()\r\n                f=open("drinktime.txt","a")\r\n                f.write(datetime.datetime.now())\r\n                #datetime function is inside datetime module\r\n                break\r\ntime.sleep(60)\r\n#program sleep for 60 sec\r\nthe error I get is-\r\n\r\nTraceback (most recent call last):\r\n  File "C:/Users/Nishant/Desktop/practice/water reminder/drink.py", line 1, in <module>\r\n    import pygame\r\n  File "C:\\Users\\Nishant\\AppData\\Roaming\\Python\\Python37\\site-packages\\pygame\\__init__.py", line 120, in <module>\r\n    from pygame.base import *\r\nModuleNotFoundError: No module named 'pygame.base'	images/uploaded_images/15.jpeg	10
\.


--
-- TOC entry 3044 (class 0 OID 16622)
-- Dependencies: 206
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: haku9104
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
6	5
7	6
15	8
15	10
15	11
15	12
15	13
15	14
15	15
\.


--
-- TOC entry 3045 (class 0 OID 16625)
-- Dependencies: 207
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: haku9104
--

COPY public.tag (id, name) FROM stdin;
4	#liverpoollipcse
5	das
6	picture
7	kecske
8	mario
9	a
10	python
11	css
12	pyGame
13	sql
14	error
15	frontend
\.


--
-- TOC entry 3047 (class 0 OID 16633)
-- Dependencies: 209
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: haku9104
--

COPY public.users (userid, email, password, registration_time, reputation) FROM stdin;
6	smartin96@citromail.hu	$2b$12$RjCASCOGvJVLrqpYOrcGWuDVPIYQlShhRHUhE8Db6gwMm42O8iFSm	2021-02-16 14:46:13	0
8	balazs@citromail.hu	$2b$12$MoZPLt46FqY7B42CkXBFCeX.SGms3aEw5qLcQL9OPwPE28yH3iJHi	2021-02-16 14:47:05	210
10	martin@hotmail.hu	$2b$12$pb8BYswIkq7agnAC.fPGl.eTq.PzJwb9icvHiAtoi6V9wdESEgNjO	2021-02-16 14:47:46	318
7	gergo@gmail.com	$2b$12$AKGzo7FiD31zjx5YHdge9uDNjdUon2GEdaQcwv1k92oWHpXTexgvi	2021-02-16 14:46:47	24
9	david@freemail.hu	$2b$12$aRRwkYY69cbtt4dC.PuLeOEklsydKdY5UzuCpOK1oh.hJwELmV7Va	2021-02-16 14:47:21	172
\.


--
-- TOC entry 3059 (class 0 OID 0)
-- Dependencies: 201
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: haku9104
--

SELECT pg_catalog.setval('public.answer_id_seq', 14, true);


--
-- TOC entry 3060 (class 0 OID 0)
-- Dependencies: 203
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: haku9104
--

SELECT pg_catalog.setval('public.comment_id_seq', 22, true);


--
-- TOC entry 3061 (class 0 OID 0)
-- Dependencies: 205
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: haku9104
--

SELECT pg_catalog.setval('public.question_id_seq', 19, true);


--
-- TOC entry 3062 (class 0 OID 0)
-- Dependencies: 208
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: haku9104
--

SELECT pg_catalog.setval('public.tag_id_seq', 15, true);


--
-- TOC entry 3063 (class 0 OID 0)
-- Dependencies: 210
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: haku9104
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- TOC entry 2889 (class 2606 OID 16647)
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- TOC entry 2891 (class 2606 OID 16649)
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- TOC entry 2899 (class 2606 OID 16651)
-- Name: users pk_id; Type: CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_id PRIMARY KEY (userid);


--
-- TOC entry 2893 (class 2606 OID 16653)
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- TOC entry 2895 (class 2606 OID 16655)
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- TOC entry 2897 (class 2606 OID 16657)
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- TOC entry 2902 (class 2606 OID 16658)
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- TOC entry 2900 (class 2606 OID 16663)
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- TOC entry 2906 (class 2606 OID 16668)
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- TOC entry 2903 (class 2606 OID 16673)
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- TOC entry 2907 (class 2606 OID 16678)
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- TOC entry 2905 (class 2606 OID 16683)
-- Name: question fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(userid);


--
-- TOC entry 2904 (class 2606 OID 16688)
-- Name: comment fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(userid);


--
-- TOC entry 2901 (class 2606 OID 16693)
-- Name: answer fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: haku9104
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(userid);


-- Completed on 2021-02-18 15:31:09

--
-- PostgreSQL database dump complete
--

