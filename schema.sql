SET SESSION storage_engine = 'InnoDB';
SET SESSION time_zone = '+0:00';
ALTER DATABASE CHARACTER SET 'utf8';

DROP TABLE IF EXISTS settings;
CREATE TABLE settings (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  first_block_text VARCHAR(100),
  second_block_text VARCHAR(100),
  insta_link VARCHAR(100),
  youtube_link VARCHAR(100),
  facebook_link VARCHAR(100),
  tel_num VARCHAR(100),
  email VARCHAR(100)
);

insert into settings
    (first_block_text, second_block_text, insta_link, youtube_link, facebook_link, tel_num, email)
values
    ('first_block_text', 'second_block_text', 'insta_link', 'youtube_link', 'facebook_link', '777', 'email@email.email');