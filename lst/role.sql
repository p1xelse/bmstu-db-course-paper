-- Администратор
CREATE ROLE administrator;
GRANT ALL PRIVILEGES ON SCHEMA public TO administrator;
GRANT ALL PRIVILEGES ON DATABASE postgres TO administrator;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO administrator;
CREATE USER admin with
	CREATEDB
	CREATEROLE
    ENCRYPTED PASSWORD 'admin'
    IN ROLE administrator LOGIN;

-- Разработчик
CREATE ROLE developer;
GRANT SELECT, INSERT, UPDATE, DELETE
    ON users, project, entry, tag, tag_entry, goal, friend_relation
    TO developer;
GRANT USAGE ON SCHEMA public TO developer;

CREATE USER dev
    WITH ENCRYPTED PASSWORD 'dev'
    IN ROLE developer LOGIN;

-- Гость
CREATE ROLE guest;
GRANT SELECT
    ON project, entry, tag, tag_entry, goal, friend_relation
    TO guest;
GRANT USAGE ON SCHEMA public TO guest;

CREATE USER visitor
    WITH ENCRYPTED PASSWORD 'guest'
    IN ROLE guest LOGIN;