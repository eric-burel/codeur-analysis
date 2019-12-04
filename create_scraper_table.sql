DROP TABLE scraper_codeurproject;
CREATE TABLE scraper_codeurproject
(
    "id" character varying(300) NOT NULL,
    "title" "text" NOT NULL,
    "url" character varying(200),
    "description" "text" NOT NULL,
    "published_at" timestamp with time zone,
    "premium" boolean NOT NULL,
    "full_description" "text"
);