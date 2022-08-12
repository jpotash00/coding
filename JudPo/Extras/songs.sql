create table songs (
    song_id INT NOT NULL AUTO_INCREMENT,
    title varchar(50),
    artist varchar(50), 
    genre varchar(25),
    released_year INT,
    song_key varchar(25),
    bpm INT,
    camelot varchar(3),
    Instrumental_type varchar(4),
    PRIMARY KEY (song_id)
);
