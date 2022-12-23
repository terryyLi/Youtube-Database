-- Setup the database for a very simple 'social network'.
-- Friends - Users - Messages 

\c postgres
DROP DATABASE IF EXISTS youtube;

CREATE database youtube;
\c youtube

\i create.SQL

-- Users.csv
-- Friends.csv
-- Messages.csv

-- In this lab, as preparation for the project, you need to create the
-- three csv files Users.csv, Friends.csv and Messages.csv.  Create at
-- least 6 entries in each of these files.  
--
-- Look previous lab CSV files to guide your effort.

-- Modeling the structure of the 'Users' table,
-- read data from a csv file Users.csv
--
-- insert at least 6 users

\copy Advertiser(advertiser_id, name) FROM advertiser.csv csv header;

\copy Advertisement(advertisement_id, link, productname, advertiser_id) FROM advertisements.csv csv header;

\copy Creator(user_id, name, gender, age, isVerified) FROM creator.csv csv header;

\copy Channel(channel_id, name, user_id) FROM channel.csv csv header;

\copy Video(video_id, name, views, genre, channel_id, advertisement_id, user_id) FROM video.csv csv header;

\copy Viewer(user_id, name, gender, age) FROM viewer.csv csv header;

\copy Comment(comment_id, content, user_id, video_id) FROM comment.csv csv header;

\copy Subscribing(user_id,channel_id) FROM subscribing.csv csv header;

\copy Viewing(user_id, video_id) FROM viewing.csv csv header;

-- Similarly load the table 'Friends'
-- 
-- In our model we view friendship is a symmetrical relationship.
-- Hence when ever (i,j) is inserted we also explicitly insert (j,i)
-- 
-- insert at least 6 friendship links


-- ============================================================
  
