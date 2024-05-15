Для запуска нужно создать файл .env в папке проекта со следующими полями:

BOT_TOKEN=<...> – токен бота
DBNAME=<...> – название БД
USER=<...> – имя пользователя БД
HOST=<...> – IP-адрес ус–ва, на котором развернута БД
PASSWORD=<...> – пароль

Для создания таблицы 'tasks':

CREATE TABLE IF NOT EXISTS public.tasks
(
    task_id integer NOT NULL DEFAULT nextval('tasks_task_id_seq'::regclass),
    user_id bigint,
    name character varying COLLATE pg_catalog."default",
    CONSTRAINT tasks_pkey PRIMARY KEY (task_id)
)

Видео взаимодействия с чат-ботом – screencast.mov
