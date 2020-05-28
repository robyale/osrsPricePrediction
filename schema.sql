CREATE TABLE public.items
(
    id integer NOT NULL,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    high_volume bit(1),
    high_volatility bit(1),
    CONSTRAINT items_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.items
    OWNER to postgres;

CREATE TABLE public.prices
(
    id bigint NOT NULL DEFAULT nextval('prices_id_seq'::regclass),
    item_id integer NOT NULL,
    day bigint NOT NULL,
    price integer NOT NULL,
    CONSTRAINT prices_pkey PRIMARY KEY (id),
    CONSTRAINT item_id_to_id FOREIGN KEY (item_id)
        REFERENCES public.items (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.prices
    OWNER to postgres;

CREATE TABLE public.volume
(
    id bigint NOT NULL DEFAULT nextval('volume_id_seq'::regclass),
    item_id integer NOT NULL,
    day bigint NOT NULL,
    volume bigint NOT NULL,
    CONSTRAINT volume_pkey PRIMARY KEY (id),
    CONSTRAINT item_id_to_id FOREIGN KEY (item_id)
        REFERENCES public.items (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.volume
    OWNER to postgres;