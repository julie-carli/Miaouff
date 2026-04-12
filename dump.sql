--
-- PostgreSQL database dump
--

-- Dumped from database version 17.9 (Debian 17.9-1.pgdg13+1)
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: animals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.animals (
    animal_id integer NOT NULL,
    species character varying(100) NOT NULL,
    breed character varying(100) NOT NULL,
    lifespan character varying(50),
    diet text,
    specifics text,
    image character varying(200)
);


ALTER TABLE public.animals OWNER TO postgres;

--
-- Name: animals_animal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.animals_animal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.animals_animal_id_seq OWNER TO postgres;

--
-- Name: animals_animal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.animals_animal_id_seq OWNED BY public.animals.animal_id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    category_id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_category_id_seq OWNER TO postgres;

--
-- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories.category_id;


--
-- Name: order_products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_products (
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer NOT NULL,
    unit_price_excl_tax numeric(10,2) NOT NULL,
    unit_price_incl_tax numeric(10,2) NOT NULL
);


ALTER TABLE public.order_products OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    order_id integer NOT NULL,
    user_id integer,
    order_date timestamp without time zone NOT NULL,
    status character varying(50) NOT NULL,
    total_price_excl_tax numeric(10,2) NOT NULL,
    total_price_incl_tax numeric(10,2) NOT NULL,
    shipping_fee numeric(10,2) NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_order_id_seq OWNER TO postgres;

--
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    payment_id integer NOT NULL,
    payment_method character varying(50),
    payment_status character varying(50),
    payment_date timestamp without time zone NOT NULL,
    payment_total double precision NOT NULL,
    order_id integer
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- Name: payments_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payments_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_payment_id_seq OWNER TO postgres;

--
-- Name: payments_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payments_payment_id_seq OWNED BY public.payments.payment_id;


--
-- Name: pets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pets (
    pet_id integer NOT NULL,
    name character varying(255) NOT NULL,
    age integer NOT NULL,
    gender character varying(10) NOT NULL,
    description text,
    adoption_date date,
    image character varying(200),
    shelter_id integer,
    animal_id integer
);


ALTER TABLE public.pets OWNER TO postgres;

--
-- Name: pets_pet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pets_pet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pets_pet_id_seq OWNER TO postgres;

--
-- Name: pets_pet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pets_pet_id_seq OWNED BY public.pets.pet_id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    product_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    price_excl_tax numeric(10,2) NOT NULL,
    price_incl_tax numeric(10,2) NOT NULL,
    stock integer NOT NULL,
    weight numeric(10,2) NOT NULL,
    image character varying(200),
    category_id integer
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_product_id_seq OWNER TO postgres;

--
-- Name: products_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;


--
-- Name: shelters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shelters (
    shelter_id integer NOT NULL,
    name character varying(255) NOT NULL,
    address text NOT NULL,
    phone character varying(20) NOT NULL,
    email character varying(255) NOT NULL,
    description text,
    image character varying(200)
);


ALTER TABLE public.shelters OWNER TO postgres;

--
-- Name: shelters_shelter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shelters_shelter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shelters_shelter_id_seq OWNER TO postgres;

--
-- Name: shelters_shelter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shelters_shelter_id_seq OWNED BY public.shelters.shelter_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    email character varying(255) NOT NULL,
    password text NOT NULL,
    address_number character varying(10),
    street_name character varying(255),
    address_complement character varying(255),
    postal_code character varying(10),
    city character varying(100),
    country character varying(100),
    phone character varying(20),
    role character varying(50) NOT NULL,
    birth_date date
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: animals animal_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animals ALTER COLUMN animal_id SET DEFAULT nextval('public.animals_animal_id_seq'::regclass);


--
-- Name: categories category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN category_id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);


--
-- Name: orders order_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);


--
-- Name: payments payment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments ALTER COLUMN payment_id SET DEFAULT nextval('public.payments_payment_id_seq'::regclass);


--
-- Name: pets pet_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets ALTER COLUMN pet_id SET DEFAULT nextval('public.pets_pet_id_seq'::regclass);


--
-- Name: products product_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);


--
-- Name: shelters shelter_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shelters ALTER COLUMN shelter_id SET DEFAULT nextval('public.shelters_shelter_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: animals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.animals (animal_id, species, breed, lifespan, diet, specifics, image) FROM stdin;
1	Chien	Labrador	10-14 ans	Croquettes, pâtée, alimentation équilibrée.	Chien intelligent, affectueux et joueur, idéal pour les familles.	images/labrador.png
2	Chien	Chihuahua	12-20 ans	Croquettes adaptées aux petites races, parfois complémentée de nourriture humide.	Petit chien vif et attachant, très fidèle à son maître.	images/chihuahua.png
3	Chien	Husky	12-15 ans	Alimentation riche en protéines, adaptée aux chiens très actifs.	Chien énergique, intelligent et sociable, nécessite beaucoup d'exercice.	images/husky.png
4	Chat	Maine Coon	12-15 ans	Croquettes premium, viande et poisson occasionnellement.	Grand chat affectueux, joueur et très sociable, aime l'eau.	images/maine_coon.png
5	Chat	Chat Européen	12-18 ans	Croquettes équilibrées, alimentation variée.	Chat robuste et adaptable, sociable et indépendant.	images/chat_europeen.png
6	Chat	Angora	12-16 ans	Alimentation équilibrée avec des compléments pour le pelage.	Chat élégant, joueur et très attaché à son humain.	images/angora.png
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (category_id, name) FROM stdin;
2	Jouets
3	Hygiène
4	Autres
6	Alimentation
\.


--
-- Data for Name: order_products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_products (order_id, product_id, quantity, unit_price_excl_tax, unit_price_incl_tax) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (order_id, user_id, order_date, status, total_price_excl_tax, total_price_incl_tax, shipping_fee) FROM stdin;
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (payment_id, payment_method, payment_status, payment_date, payment_total, order_id) FROM stdin;
\.


--
-- Data for Name: pets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pets (pet_id, name, age, gender, description, adoption_date, image, shelter_id, animal_id) FROM stdin;
1	Mew	2	Mâle	Un adorable chat joueur et curieux qui adore les câlins.	\N	images/mew.png	1	5
2	Minou	4	Mâle	Un chat doux et calme qui aime se prélasser au soleil.	\N	images/minou.png	1	5
3	Chippie	1	Femelle	Petite boule d'énergie, Chippie adore jouer et grimper partout.	\N	images/chippie.png	1	5
4	Max	3	Mâle	Max est un chien affectueux et protecteur, idéal pour une famille.	\N	images/max.png	2	1
5	Tonnerre	5	Mâle	Un chien énergique et joueur qui adore courir et se dépenser.	\N	images/tonnerre.png	2	3
6	Daisy	2	Femelle	Daisy est une chienne douce et sociable qui adore les enfants.	\N	images/daisy.png	2	2
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (product_id, name, description, price_excl_tax, price_incl_tax, stock, weight, image, category_id) FROM stdin;
4	Savon Douceur Animale	Un savon doux pour nettoyer et hydrater la peau de votre compagnon.	6.66	7.99	50	0.20	images/savon.png	3
5	Gant Attrape-Poils	Un gant pratique pour enlever les poils morts de votre animal.	10.83	12.99	120	0.30	images/gant.png	3
6	Litière Confort+	Litière absorbante et anti-odeurs pour le bien-être de votre chat.	13.33	15.99	60	10.00	images/litiere.png	3
7	Haltère Bleu Musclé	Un haltère en caoutchouc robuste pour muscler et divertir votre chien.	7.49	8.99	90	0.70	images/haltere.png	2
8	Poisson Sautillant	Un jouet en forme de poisson qui bouge pour stimuler votre chat.	5.83	6.99	100	0.20	images/poisson-jouet.png	2
9	Tour de Jeu Féli'Fun	Un jouet avec trois étages et une balle par niveau pour divertir votre chat.	12.49	14.99	75	0.90	images/roulette.png	2
10	Don pour le Refuge	Faites un don pour soutenir les animaux en refuge.	5.00	5.00	9999	0.00	images/don.png	4
1	Croquettes Énergie+	Des croquettes riches en nutriments pour une vitalité optimale.	24.99	29.99	100	5.00	images/croquettes.png	6
3	Os à Ronger Saveur Bœuf	Un os savoureux qui aide à l’hygiène dentaire de votre chien.	4.58	5.49	80	0.60	images/os.png	6
2	Délice Gourmet Félin	Une pâtée savoureuse et équilibrée pour chats exigeants.	2.49	2.99	200	0.30	images/patee.png	6
\.


--
-- Data for Name: shelters; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shelters (shelter_id, name, address, phone, email, description, image) FROM stdin;
1	Le Havre des Ronronnements	12 Rue des Chats Heureux, 28000 Chartres, France	+33 2 37 00 00 00	havre-ronronnements@miaouff.fr	Un refuge chaleureux dédié aux chats en attente d'une famille aimante.	the_haven_of_purrs.png
2	Le Refuge des Câlins Canins	25 Avenue des Amis Fidèles, 28100 Dreux, France	+33 2 37 11 11 11	refuge-calins-canins@miaouff.fr	Un havre de paix pour chiens abandonnés, en quête d'un nouveau foyer.	the_canine_cuddle_shelter.png
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, first_name, last_name, email, password, address_number, street_name, address_complement, postal_code, city, country, phone, role, birth_date) FROM stdin;
1	\N	\N	julie@miaouff.fr	pbkdf2:sha256:600000$ve7iiFzEFhPc6zqj$140c2c49dc0577489eff267aaf2be4079a6b72b7e34af80521d248848645e5d7	\N	\N	\N	\N	\N	\N	\N	admin	\N
2	\N	\N	juju@juju.fr	pbkdf2:sha256:600000$n3Y8m0uLFQ52LanK$1efc1babd10013a36d81f80f52e7f4959fc01d98d77e980d126b8f602e830ef5	\N	\N	\N	\N	\N	\N	\N	user	\N
3	\N	\N	i@i.com	pbkdf2:sha256:600000$hc0Qts7UbExPb5bL$b58a8c888aa55d6e6eacceb553fa526733d4a34f7b580972a3b3fb9e68ce80f7	\N	\N	\N	\N	\N	\N	\N	user	\N
4	\N	\N	z@z.fr	pbkdf2:sha256:600000$oFOp2xZjQpvkHeba$c698d35df4d218ee855ddfdd15b9d911791605e138013f4efc5791dd9103fb18	\N	\N	\N	\N	\N	\N	\N	user	\N
5	\N	\N	m@m.com	pbkdf2:sha256:600000$fKuEivlKhQornYDJ$3afd0744b562bc2deb90b3962617c6bf10712d9bf9fa04c0f3907d3b54bac07b	\N	\N	\N	\N	\N	\N	\N	user	\N
6	\N	\N	l@l.com	pbkdf2:sha256:600000$bmLqg6Du6WZUFHXS$fc02d1bf8ed6bf29e48e713cf60b94a5fd3c9708af1ccff2de3abc29b92770e6	\N	\N	\N	\N	\N	\N	\N	user	\N
7	\N	\N	s@s.com	pbkdf2:sha256:600000$Q6fuboxSEujx3muc$4db6ef50369cee76ab74cbb13269fe03b59e013ca268a78c6fedf80a74655bee	\N	\N	\N	\N	\N	\N	\N	user	\N
8	\N	\N	b@b.com	pbkdf2:sha256:600000$uS8M9AfeVhsvKsJ9$7121b56d03c1a2ff5471fc59770ad4ec1dc66f40836299dc14a576b30494b3e2	\N	\N	\N	\N	\N	\N	\N	user	\N
9	\N	\N	v@v.com	pbkdf2:sha256:600000$fiozuvT44UTa9Fx4$922f34fdc0f685ca2c41bc0a59ffbf102884e347b216bf424e476369eb0d7156	\N	\N	\N	\N	\N	\N	\N	user	\N
10	\N	\N	va@va.com	pbkdf2:sha256:600000$j53VmXlCcDyJrfA8$d600c81558879480db2eb312e615a542d8a91721de097d24e3d20a50b07d1627	\N	\N	\N	\N	\N	\N	\N	user	\N
13	\N	\N	cd@cd.com	pbkdf2:sha256:600000$d5XEy2b59FKWSMiV$1e799b38044efe62debe0ade0ad93a048a65e46f78296ba8c383ec90483ff199	\N	\N	\N	\N	\N	\N	\N	user	\N
14	\N	\N	nd@nd.com	pbkdf2:sha256:600000$YwxQI30ZIvY1laSD$bbae5888222fff2894e7065aa3660173d3bd90b62ebe3debdb68229389aff1e7	\N	\N	\N	\N	\N	\N	\N	user	\N
12	Pauline	Bernard	pltest@pltest.com	pbkdf2:sha256:600000$VVI4woyv7fVymwJR$0061bb14fdc66b79c0341b1946c55406930b08dc2643e35c40ce4d21d07cdb9b	2	Rue des Acacias	Tour B	28000	Chartres	France	0798572639	user	1986-06-12
16	\N	\N	test@example.com	pbkdf2:sha256:600000$WAZ8orqtbvtsCAQs$0f94cd24bcc5c63fd2b4a9463195d19c56a0d0101f8fc11f932185bd2d98288b	\N	\N	\N	\N	\N	\N	\N	user	\N
17	\N	\N	nono@nono.com	pbkdf2:sha256:600000$3GsOPGlQZBz4rrKK$0f6b4defa20290e31f45d6be29211b3b48d6513f5e07354fb8801a09fc331ee1	\N	\N	\N	\N	\N	\N	\N	user	\N
18	\N	\N	lpm@lpm.com	pbkdf2:sha256:600000$14fJQiaTto9JDq7b$76574345465548264c14b8c24b3e79426e6ba356b48cf641cb1e87a5493bee44	\N	\N	\N	\N	\N	\N	\N	user	\N
19	\N	\N	koko@koko.com	pbkdf2:sha256:600000$3KiBkm57lBpL8cqM$54b57444e6f50809e7e3f85a66998b87ca38b5b38163f3172ef9b551cc057c37	\N	\N	\N	\N	\N	\N	\N	user	\N
20	\N	\N	hoho@hoho.com	pbkdf2:sha256:600000$xb8jlSVDfeKkzONE$db2e2e10e4cc3763eaeb387531cfbc9594441f7d59ef8245feaf58d0805081e7	\N	\N	\N	\N	\N	\N	\N	user	\N
21	\N	\N	olol@olol.com	pbkdf2:sha256:600000$RogDDhK0PcwkHxRO$d5ea1c3c5345601fbfd6bd3de162a3a7b425b9f346a45593a6d1570d93a2aabb	\N	\N	\N	\N	\N	\N	\N	user	\N
\.


--
-- Name: animals_animal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.animals_animal_id_seq', 6, true);


--
-- Name: categories_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_category_id_seq', 7, true);


--
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_order_id_seq', 1, false);


--
-- Name: payments_payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payments_payment_id_seq', 1, false);


--
-- Name: pets_pet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pets_pet_id_seq', 6, true);


--
-- Name: products_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_product_id_seq', 10, true);


--
-- Name: shelters_shelter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shelters_shelter_id_seq', 19, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 21, true);


--
-- Name: animals animals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animals
    ADD CONSTRAINT animals_pkey PRIMARY KEY (animal_id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- Name: order_products order_products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_products
    ADD CONSTRAINT order_products_pkey PRIMARY KEY (order_id, product_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_id);


--
-- Name: pets pets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_pkey PRIMARY KEY (pet_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: shelters shelters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shelters
    ADD CONSTRAINT shelters_pkey PRIMARY KEY (shelter_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: order_products order_products_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_products
    ADD CONSTRAINT order_products_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- Name: order_products order_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_products
    ADD CONSTRAINT order_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: payments payments_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- Name: pets pets_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animals(animal_id);


--
-- Name: pets pets_shelter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_shelter_id_fkey FOREIGN KEY (shelter_id) REFERENCES public.shelters(shelter_id);


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO postgres;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO postgres;


--
-- PostgreSQL database dump complete
--

