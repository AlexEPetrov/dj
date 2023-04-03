BEGIN;
--
-- Create model market_source_data_ats
--
CREATE TABLE "ats_market_source_data_ats" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "observation_date" datetime NOT NULL, "publication_date" datetime NULL, "price_zone_code" integer NOT NULL, "consumer_price" decimal NOT NULL, "consumer_volume" decimal NOT NULL, "thermal_volume" decimal NOT NULL, "hydro_volume" decimal NOT NULL, "atomic_volume" decimal NOT NULL, "renewable_volume" decimal NOT NULL);
--
-- Create index ats_market__observa_92891c_idx on field(s) observation_date of model market_source_data_ats
--
CREATE INDEX "ats_market__observa_92891c_idx" ON "ats_market_source_data_ats" ("observation_date");
--
-- Create index ats_market__price_z_f2596a_idx on field(s) price_zone_code of model market_source_data_ats
--
CREATE INDEX "ats_market__price_z_f2596a_idx" ON "ats_market_source_data_ats" ("price_zone_code");
--
-- Create constraint unique-price-per-date-zone on model market_source_data_ats
--
CREATE TABLE "new__ats_market_source_data_ats" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "observation_date" datetime NOT NULL, "publication_date" datetime NULL, "price_zone_code" integer NOT NULL, "consumer_price" decimal NOT NULL, "consumer_volume" decimal NOT NULL, "thermal_volume" decimal NOT NULL, "hydro_volume" decimal NOT NULL, "atomic_volume" decimal NOT NULL, "renewable_volume" decimal NOT NULL, CONSTRAINT "unique-price-per-date-zone" UNIQUE ("observation_date", "price_zone_code"));
INSERT INTO "new__ats_market_source_data_ats" ("id", "observation_date", "publication_date", "price_zone_code", "consumer_price", "consumer_volume", "thermal_volume", "hydro_volume", "atomic_volume", "renewable_volume") SELECT "id", "observation_date", "publication_date", "price_zone_code", "consumer_price", "consumer_volume", "thermal_volume", "hydro_volume", "atomic_volume", "renewable_volume" FROM "ats_market_source_data_ats";
DROP TABLE "ats_market_source_data_ats";
ALTER TABLE "new__ats_market_source_data_ats" RENAME TO "ats_market_source_data_ats";
CREATE INDEX "ats_market__observa_92891c_idx" ON "ats_market_source_data_ats" ("observation_date");
CREATE INDEX "ats_market__price_z_f2596a_idx" ON "ats_market_source_data_ats" ("price_zone_code");
COMMIT;
