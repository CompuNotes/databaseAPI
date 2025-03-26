create table TAG
(
    name varchar(255) charset utf8mb4 not null,
    id   int auto_increment
        primary key
);

create table USER
(
    id       int auto_increment
        primary key,
    username varchar(255) charset utf8mb4 not null,
    email    varchar(255) charset utf8mb4 not null,
    password varchar(255) charset utf8mb4 not null,
    constraint users_pk
        unique (username),
    constraint users_pk_2
        unique (email)
);

create table FILE
(
    path    varchar(255) charset utf8mb3 not null,
    user_id int                          null,
    id      int auto_increment
        primary key,
    constraint FILE_pk_2
        unique (id),
    constraint FILE_USER_id_fk
        foreign key (user_id) references USER (id)
            on update cascade on delete set null
);

create table FILE_TAG
(
    tag_id  int not null,
    file_id int not null,
    primary key (tag_id, file_id),
    constraint FILE_TAG_FILE_id_fk
        foreign key (file_id) references FILE (id),
    constraint FILE_TAG_TAG_id_fk
        foreign key (tag_id) references TAG (id)
            on update cascade on delete cascade
);

create table RATING
(
    rating  tinyint unsigned not null,
    user_id int              not null,
    file_id int              not null,
    primary key (user_id, file_id),
    constraint RATING_FILE_id_fk
        foreign key (file_id) references FILE (id)
            on update cascade on delete cascade,
    constraint RATING_USER_id_fk
        foreign key (user_id) references USER (id)
            on update cascade on delete cascade
);


