-- Table: public.user_vault

-- DROP TABLE IF EXISTS public.user_vault;

CREATE TABLE IF NOT EXISTS public.user_vault
(
    id integer NOT NULL DEFAULT nextval('user_vault_id_seq'::regclass),
    content text COLLATE pg_catalog."default",
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT user_vault_pk PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_vault
    OWNER to postgres;

COMMENT ON COLUMN public.user_vault.id
    IS 'user_primary_key';