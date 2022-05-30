-- SELECT title, rating  FROM movies WHERE year = 2010 ORDER BY year DESC; ^아니고^
SELECT title, rating  FROM movies JOIN ratings ON id = movie_id WHERE year = 2010 ORDER BY rating DESC, title;