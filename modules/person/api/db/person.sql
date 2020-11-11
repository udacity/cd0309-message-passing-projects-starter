create database person if not exists

CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    company_name VARCHAR NOT NULL
);

insert into public.person (id, first_name, last_name, company_name) values (5, 'Taco', 'Fargo', 'Alpha Omega Upholstery');
insert into public.person (id, first_name, last_name, company_name) values (6, 'Frank', 'Shader', 'USDA');
insert into public.person (id, first_name, last_name, company_name) values (1, 'Pam', 'Trexler', 'Hampton, Hampton and McQuill');
insert into public.person (id, first_name, last_name, company_name) values (8, 'Paul', 'Badman', 'Paul Badman & Associates');
insert into public.person (id, first_name, last_name, company_name) values (9, 'Otto', 'Spring', 'The Chicken Sisters Restaurant');

