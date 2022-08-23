CREATE TABLE IF NOT EXISTS public.example_app_a
(
    id bigint NOT NULL DEFAULT nextval('example_app_a_id_seq'::regclass),

    uuid uuid NOT NULL,

    name character varying(64) COLLATE pg_catalog."default" NOT NULL,
    nickname character varying(64) COLLATE pg_catalog."default" NOT NULL,
    sex character varying(8) COLLATE pg_catalog."default" NOT NULL,
    sex2 character varying(8) COLLATE pg_catalog."default" NOT NULL,

    age smallint,
    balance numeric(8,2) NOT NULL,
    score integer NOT NULL,

    is_active boolean NOT NULL,
    created_time timestamp with time zone NOT NULL,
    updated_time timestamp with time zone NOT NULL,

    CONSTRAINT example_app_a_pkey PRIMARY KEY (id),
    CONSTRAINT example_app_a_uuid_key UNIQUE (uuid),
    CONSTRAINT example_app_a_age_check CHECK (age >= 0),
    CONSTRAINT example_app_a_score_check CHECK (score >= 0)
);


CREATE TABLE IF NOT EXISTS public.example_app_b
(
    id bigint NOT NULL DEFAULT nextval('example_app_b_id_seq'::regclass),
    a_id bigint NOT NULL,
    CONSTRAINT example_app_b_pkey PRIMARY KEY (id),
    CONSTRAINT example_app_b_a_id_9a9a6b60_fk_example_app_a_id FOREIGN KEY (a_id)
        REFERENCES public.example_app_a (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX IF NOT EXISTS example_app_b_a_id_9a9a6b60
    ON public.example_app_b USING btree
    (a_id ASC NULLS LAST)
    TABLESPACE pg_default;
