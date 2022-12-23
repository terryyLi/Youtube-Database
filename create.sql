-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-12-02 01:27:51.061

-- tables
-- Table: Advertisement
CREATE TABLE Advertisement (
    advertisement_id int  NOT NULL,
    link text  NOT NULL,
    productname text  NOT NULL,
    advertiser_id int  NOT NULL,
    CONSTRAINT Advertisement_pk PRIMARY KEY (advertisement_id)
);

-- Table: Advertiser
CREATE TABLE Advertiser (
    advertiser_id int  NOT NULL,
    name text  NOT NULL,
    CONSTRAINT Advertiser_pk PRIMARY KEY (advertiser_id)
);

-- Table: Channel
CREATE TABLE Channel (
    channel_id int  NOT NULL,
    name text  NOT NULL,
    user_id int  NOT NULL,
    CONSTRAINT Channel_pk PRIMARY KEY (channel_id)
);

-- Table: Comment
CREATE TABLE Comment (
    comment_id int  NOT NULL,
    content text  NOT NULL,
    user_id int  NOT NULL,
    video_id int  NOT NULL,
    CONSTRAINT Comment_pk PRIMARY KEY (comment_id)
);

-- Table: Creator
CREATE TABLE Creator (
    user_id int  NOT NULL,
    name text  NOT NULL,
    gender text  NOT NULL,
    age int  NOT NULL,
    isVerified boolean  NOT NULL,
    CONSTRAINT Creator_pk PRIMARY KEY (user_id)
);

-- Table: Subscribing
CREATE TABLE Subscribing (
    user_id int  NOT NULL,
    channel_id int  NOT NULL,
    CONSTRAINT Subscribing_pk PRIMARY KEY (channel_id,user_id)
);

-- Table: Video
CREATE TABLE Video (
    video_id int  NOT NULL,
    name text  NOT NULL,
    views int  NOT NULL,
    genre text  NOT NULL,
    channel_id int  NOT NULL,
    advertisement_id int  NOT NULL,
    user_id int  NOT NULL,
    CONSTRAINT Video_pk PRIMARY KEY (video_id)
);

-- Table: Viewer
CREATE TABLE Viewer (
    user_id int  NOT NULL,
    name text  NOT NULL,
    gender text  NOT NULL,
    age int  NOT NULL,
    CONSTRAINT Viewer_pk PRIMARY KEY (user_id)
);

-- Table: Viewing
CREATE TABLE Viewing (
    user_id int  NOT NULL,
    video_id int  NOT NULL,
    CONSTRAINT Viewing_pk PRIMARY KEY (user_id,video_id)
);

-- foreign keys
-- Reference: Advertisment_Advertiser (table: Advertisement)
ALTER TABLE Advertisement ADD CONSTRAINT Advertisment_Advertiser
    FOREIGN KEY (advertiser_id)
    REFERENCES Advertiser (advertiser_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Channel_Creator (table: Channel)
ALTER TABLE Channel ADD CONSTRAINT Channel_Creator
    FOREIGN KEY (user_id)
    REFERENCES Creator (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Comment_Video (table: Comment)
ALTER TABLE Comment ADD CONSTRAINT Comment_Video
    FOREIGN KEY (video_id)
    REFERENCES Video (video_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Comment_Viewer (table: Comment)
ALTER TABLE Comment ADD CONSTRAINT Comment_Viewer
    FOREIGN KEY (user_id)
    REFERENCES Viewer (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Subscribing_Channel (table: Subscribing)
ALTER TABLE Subscribing ADD CONSTRAINT Subscribing_Channel
    FOREIGN KEY (channel_id)
    REFERENCES Channel (channel_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Subscribing_Viewer (table: Subscribing)
ALTER TABLE Subscribing ADD CONSTRAINT Subscribing_Viewer
    FOREIGN KEY (user_id)
    REFERENCES Viewer (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Video_Advertisement (table: Video)
ALTER TABLE Video ADD CONSTRAINT Video_Advertisement
    FOREIGN KEY (advertisement_id)
    REFERENCES Advertisement (advertisement_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Video_Channel (table: Video)
ALTER TABLE Video ADD CONSTRAINT Video_Channel
    FOREIGN KEY (channel_id)
    REFERENCES Channel (channel_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Video_Creator (table: Video)
ALTER TABLE Video ADD CONSTRAINT Video_Creator
    FOREIGN KEY (user_id)
    REFERENCES Creator (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Viewing_Video (table: Viewing)
ALTER TABLE Viewing ADD CONSTRAINT Viewing_Video
    FOREIGN KEY (video_id)
    REFERENCES Video (video_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Viewing_Viewer (table: Viewing)
ALTER TABLE Viewing ADD CONSTRAINT Viewing_Viewer
    FOREIGN KEY (user_id)
    REFERENCES Viewer (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

