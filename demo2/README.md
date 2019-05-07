# face_rec
reconocimiento facial conectado a una base de datos postgresql 
tabla know_users
campos (ci(text), id(integer), nombre(text), img_src(text))


UPDATE know_users SET nombre = 'ximena', img_src='ximena.png' WHERE id =4;
INSERT INTO know_users (nombre, img_src) VALUES ('face-8', 'face-.png');

create table deteccion(
  name text,
  fecha date,
  hora time,
  id serial,
  primary key (id)
 );

 INSERT INTO deteccion (name, fecha, hora) VALUES ('reddy', '2019/04/12', '20:14:40');

