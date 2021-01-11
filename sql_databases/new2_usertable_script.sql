PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE cars(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brand varchar NOT NULL CHECK (length(brand) <= 45),
  type varchar NOT NULL CHECK (length(type) <= 45),
  year smallint NOT NULL CHECK (length(year) = 4),
  batteryCapacity float DEFAULT 0,
  verified tinyint DEFAULT 0 CHECK (length(verified) = 1),
  edition varchar DEFAULT NULL,
  imageURL varchar DEFAULT '' 
  );
INSERT INTO cars VALUES(404,'-','-',2000,0.0,0,NULL,'');
INSERT INTO cars VALUES(1,'Nissan','Leaf',2018,40.0,1,NULL,'https://ev-database.nl/img/auto/Nissan_Leaf_2018/Nissan_Leaf_2018-01.jpg');
INSERT INTO cars VALUES(2,'Tesla','Model S',2016,85.0,1,NULL,'https://ev-database.nl/img/auto/Tesla_Model_S_2016/Tesla_Model_S_2016-01.jpg');
INSERT INTO cars VALUES(3,'Tesla','Model S',2015,85.0,1,NULL,'https://hips.hearstapps.com/amv-prod-cad-assets.s3.amazonaws.com/images/15q2/657948/2015-tesla-model-s-70d-instrumented-test-review-car-and-driver-photo-658384-s-original.jpg');
INSERT INTO cars VALUES(4,'Toyota','Prius',2015,85.0,1,NULL,'https://hips.hearstapps.com/amv-prod-cad-assets.s3.amazonaws.com/images/15q2/657948/2015-toyota-prius-review-car-and-driver-photo-660322-s-original.jpg');
INSERT INTO cars VALUES(5,'Renault','Zoe',2017,40.999999999999996447,1,'R90','https://car-images.bauersecure.com/pagefiles/68546/1040x585/zoeweb-001.jpg');
INSERT INTO cars VALUES(6,'Volvo ','V60',2013,85.0,1,NULL,'https://media2.autokopen.nl/afbeeldingen/volvo-v60-2013-257500-800.jpg');
INSERT INTO cars VALUES(7,'Ford','C-max energi',2015,85.0,1,NULL,'https://icdn2.digitaltrends.com/image/2013-ford-cmax-plugin-front-left-angle-640x640.jpg?ver=1');
INSERT INTO cars VALUES(8,'Audi','A3',2013,85.0,1,NULL,'https://parkers-images.bauersecure.com/pagefiles/202042/cut-out/331x220/audi-a3-sb-01.jpg\r\n');
INSERT INTO cars VALUES(9,'Ford','C-max energi',2015,85.0,1,NULL,'https://icdn2.digitaltrends.com/image/2013-ford-cmax-plugin-front-left-angle-640x640.jpg?ver=1');
INSERT INTO cars VALUES(10,'Chevrolet','Volt',2012,85.0,1,NULL,'https://file.kbb.com/kbb/vehicleimage/housenew/480x360/2012/2012-chevrolet-volt-frontside_chvolt121.jpg');
INSERT INTO cars VALUES(11,'Volvo','XC-60',2018,10.400000000000000355,1,'T8 Twin-Engine','https://ev-database.nl/img/auto/Volvo_XC-60/Volvo_XC-60-01.jpg');
INSERT INTO cars VALUES(12,'Chevrolet','volt',2013,85.0,1,NULL,'https://cars.usnews.com/static/images/Auto/custom/12098/2013-Chevrolet-Volt-005-medium.jpg');
INSERT INTO cars VALUES(13,'Volkswagen','Egolf',2013,85.0,1,NULL,'https://media.treehugger.com/assets/images/2012/03/volkswagen-golf-blue-e-motion_1_bkEwC_69.jpeg');
INSERT INTO cars VALUES(116,'BMW','330e',2015,7.5999999999999996447,1,NULL,'https://media.autoweek.nl/m/8mqy7a0bxrg9_800.jpg');
INSERT INTO cars VALUES(117,'BMW','X5',2016,9.0,1,'xDrive40e','https://www.autocar.co.uk/sites/autocar.co.uk/files/styles/gallery_slide/public/images/car-reviews/first-drives/legacy/bmw-x40e-ac-003.jpg?itok=tMdX72RY');
INSERT INTO cars VALUES(118,'Mercedes','GLE 500e Plug-In',2015,8.8000000000000007105,1,NULL,'https://ev-database.nl/img/auto/Mercedes_GLE_500e_Plug-In/Mercedes_GLE_500e_Plug-In-01.jpg');
INSERT INTO cars VALUES(119,'Volkswagen','Passat GTE',2015,9.9000000000000003552,1,NULL,'https://images.autowereld.com/high/108861-volkswagen-passat-gte-2015-10.jpg');
INSERT INTO cars VALUES(120,'Volkswagen','Passat GTE',2015,9.9000000000000003552,1,'Variant','https://static.autoblog.nl/images/wp2014/volkswagen-passat-gte-variant-550.jpg');
INSERT INTO cars VALUES(121,'Volvo','XC-90',2014,10.400000000000000355,1,'T8 Twin-Engine','https://car-images.bauersecure.com/pagefiles/20706/1040x585/volvoxc90_t8_1.jpg');
INSERT INTO cars VALUES(122,'Opel','Ampera-e',2017,60.0,1,NULL,'https://www.carblogger.nl/wp-content/uploads/2017/02/opel-ampera-e-2017-1200x700.jpg');
INSERT INTO cars VALUES(123,'Tesla','Model X',2016,75.0,1,'75D','https://ev-database.nl/img/auto/Tesla_Model_X/Tesla_Model_X-01.jpg');
INSERT INTO cars VALUES(124,'Hyundai','IONIQ',2018,8.9000000000000003552,1,'Plug-in','https://cdn.motor1.com/images/mgl/k0rPB/s1/2018-hyundai-ioniq-plug-in-hybrid-why-buy.jpg');
INSERT INTO cars VALUES(125,'Hyundai','IONIQ',2017,30.499999999999998223,1,'Electric','https://icdn2.digitaltrends.com/image/2017-hyundai-ioniq-ev-side-angle-640x640.jpg?ver=1');
INSERT INTO cars VALUES(126,'Kia','Optima',2016,9.8000000000000007105,1,'Plug-in Hybrid','https://ev-database.nl/img/auto/Kia_Optima_Plug-in_Hybrid/Kia_Optima_Plug-in_Hybrid-01.jpg');
INSERT INTO cars VALUES(127,'Toyota','Prius',2016,8.8000000000000007105,1,'Plug-in Hybrid','https://static.autoblog.nl/images/wp2016/toyota-prius-phev-2016-voor.jpg');
INSERT INTO cars VALUES(128,'Tesla','Model S',2016,75.0,1,'75D','https://ev-database.nl/img/auto/Tesla_Model_S_2016/Tesla_Model_S_2016-01.jpg');
INSERT INTO cars VALUES(129,'Tesla','Model S',2016,100.0,1,'P100D','https://www.dagelijksauto.nl/wp-content/gallery/tesla-model-s-model-x-p100d-ludicrous-2016-nieuwsbericht/Tesla-Model-S-2016-1.jpg');
INSERT INTO cars VALUES(130,'Tesla','Model X',2017,100.0,1,'P100D','https://autoweek.com/sites/default/files/styles/gen-1200-675/public/2120x920_mx-city.png');
INSERT INTO cars VALUES(131,'Audi','A3',2016,8.8000000000000007105,1,'Sportback E-Tron','https://ev-database.nl/img/auto/Audi_A3_Sportback_E-Tron-2016/Audi_A3_Sportback_E-Tron-2016-01.jpg');
INSERT INTO cars VALUES(132,'Volkswagen','e-Up!',2014,18.699999999999999289,1,NULL,'https://media.autoweek.nl/m/m1my6qhbavyh_800.jpg');
INSERT INTO cars VALUES(133,'BMW','740e',2016,9.1999999999999992894,1,NULL,'https://cdn1.autoexpress.co.uk/sites/autoexpressuk/files/styles/article_main_image/public/2016/07/_bl72029_01.jpg?itok=aCx2RqWC');
INSERT INTO cars VALUES(134,'Porsche','Panamera 4 E-Hybrid',2017,14.099999999999999644,1,NULL,'https://car-images.bauersecure.com/pagefiles/69207/panamera_hybrid_01.jpg');
INSERT INTO cars VALUES(135,'Volkswagen','e-Golf',2017,35.799999999999996269,1,NULL,'https://topgear.nl/thumbs/hd/2017/08/Volkswagen-e-Golf-1.jpg');
INSERT INTO cars VALUES(136,'Tesla','Model S',2017,100.0,1,'100D','https://www.groen7.nl/files/2017/tesla-model-s-100d-rood.jpg');
INSERT INTO cars VALUES(137,'Tesla','Model X',2017,100.0,1,'100D','https://www.leasecosts.ca/sites/default/files/styles/car_thumb_big/public/2017-09/tesla_canada_model_x_0.jpg?itok=wR0YCWwR');
INSERT INTO cars VALUES(138,'Citroen','C-Zero',2016,16.000000000000000888,1,NULL,'https://elektrischeauto.com/wp-content/uploads/2016/11/Citroen-C-zero-1080x640.jpg');
INSERT INTO cars VALUES(139,'Peugeot','iOn',2017,16.000000000000000888,1,NULL,'https://i.ytimg.com/vi/Bx4fBdXG-_o/maxresdefault.jpg');
INSERT INTO cars VALUES(140,'Jaguar','I-Pace',2018,90.0,1,NULL,'https://topgear.nl/thumbs/hd/2018/03/jaguar-i-pace-2018-5.jpg');
INSERT INTO cars VALUES(141,'Renault','Kangoo',2017,32.999999999999998223,1,'Maxi ZE 33','https://ev-database.nl/img/auto/Renault_Kangoo_Maxi_ZE33/Renault_Kangoo_Maxi_ZE33-01.jpg');
INSERT INTO cars VALUES(142,'Citroen','E-Berlingo',2017,22.5,1,'Multispace','https://media.autoweek.nl/m/0fsywiqbkkul_800.jpg');
INSERT INTO cars VALUES(143,'Peugeot','Partner',2017,22.5,1,'Tepee Electric','https://www.groen7.nl/files/2017/partner-tepee-10000.jpg');
INSERT INTO cars VALUES(145,'Volkswagen','Golf GTE',2017,8.6999999999999992894,1,NULL,'https://cdn2.autoexpress.co.uk/sites/autoexpressuk/files/2017/03/dsc_3724.jpg');
INSERT INTO cars VALUES(146,'Mini','Countryman',2017,7.5999999999999996447,1,'Cooper S E ALL4','https://i.ytimg.com/vi/zIv4H46tKzw/maxresdefault.jpg');
INSERT INTO cars VALUES(147,'BMW','530e',2017,9.1999999999999992894,1,'iPerformance','https://topgear.nl/thumbs/hd/2017/06/bmw-530e-iperformance-3.jpg');
INSERT INTO cars VALUES(148,'Kia','Optima',2017,11.300000000000001154,1,'Sportswagon PHEV','https://d2t6ms4cjod3h9.cloudfront.net/wp-content/uploads/2017/12/OPTIMA_01.jpg');
INSERT INTO cars VALUES(149,'Kia','Niro',2018,8.9000000000000003552,1,'PHEV','https://hips.hearstapps.com/amv-prod-cad-assets.s3.amazonaws.com/images/18q1/699327/2018-kia-niro-plug-in-hybrid-test-review-car-and-driver-photo-701589-s-original.jpg?crop=1xw:1xh;center,center&resize=900:*');
INSERT INTO cars VALUES(150,'Nissan','e-NV200 Evalia',2018,40.0,1,NULL,'https://i.ytimg.com/vi/99kpJm03XbI/maxresdefault.jpg');
INSERT INTO cars VALUES(151,'Kia','Soul EV',2015,32.999999999999998223,1,NULL,'https://car-images.bauersecure.com/pagefiles/11330/k_5023.jpg');
INSERT INTO cars VALUES(152,'Hyundai','Kona',2018,67.000000000000001776,1,'Electric 64 kWh','https://zerauto.nl/wp-content/uploads/sites/2/2018/06/hyundai-kona-electric-prijs-2018-04-640x480.jpg');
INSERT INTO cars VALUES(153,'Renault','Zoe',2018,40.999999999999996447,1,'R110','https://media.renault.nl/wp-content/uploads/2018/02/01-Nieuwe-elektromotor-voor-Renault-ZOE-1170x780.jpg');
INSERT INTO cars VALUES(154,'Mitsubishi','Outlander PHEV',2016,13.800000000000001065,1,NULL,'https://www.driving.co.uk/s3/st-driving-prod/uploads/2015/12/Mitsu.jpg');
INSERT INTO cars VALUES(155,'Smart','EQ fortwo',2018,17.600000000000004973,1,'coupe','https://evcompare.io/upload/resize_cache/iblock/a20/1200_800_2/a2045c898c3c371b8d32bcafe74f44a7.jpg');
INSERT INTO cars VALUES(156,'Smart','EQ fortwo',2018,17.600000000000004973,1,'cabrio','https://ev-database.nl/img/auto/Smart_cabrio/Smart_cabrio-01.jpg');
INSERT INTO cars VALUES(157,'Smart','EQ forfour',2018,17.600000000000004973,1,NULL,'https://c.slashgear.com/wp-content/uploads/2018/03/smart-eq-forfour-1.jpg');
INSERT INTO cars VALUES(158,'Volvo','S90',2018,10.400000000000000355,1,'T8 Twin-Engine','https://ev-database.nl/img/auto/Volvo_S90/Volvo_S90-01.jpg');
INSERT INTO cars VALUES(159,'Volvo','V90',2018,10.400000000000000355,1,'T8 Twin-Engine','https://car-images.bauersecure.com/pagefiles/77375/1040x585/volvo_v90_t8_01.jpg');
INSERT INTO cars VALUES(161,'Volvo','V60',2018,10.400000000000000355,1,'T8 Twin-Engine','https://d2t6ms4cjod3h9.cloudfront.net/wp-content/uploads/2018/03/IMG_0896.jpg');
INSERT INTO cars VALUES(162,'BMW','i3',2018,42.200000000000006394,1,'120 Ah','https://www.elektrischeauto.nl/wp-content/uploads/2018/10/BMW_i3_2019-01@2x-1024x576.jpg');
INSERT INTO cars VALUES(163,'BMW','225xe',2017,7.5999999999999996447,1,'iPerformance','https://www.carbuyer.com.sg/cb-content/uploads/2017/10/bmw-225xe-singapore-price-20174.jpg');
INSERT INTO cars VALUES(164,'BMW','i3s',2018,42.200000000000006394,1,'120 Ah','https://ev-database.nl/img/auto/BMW_i3_2019/BMW_i3_2019-01.jpg');
INSERT INTO cars VALUES(184,'Peugeot','E-Legend',2019,100.0,1,'','https://www.wsupercars.com/wallpapers/Peugeot/2018-Peugeot-e-Legend-Concept-V3-1080.jpg');
CREATE TABLE car_of_user (
  carId int NOT NULL,
  userId int NOT NULL,
  batteryPercentage int DEFAULT 0, 
  PRIMARY KEY (carId, userId), 
  FOREIGN KEY (carId)
  REFERENCES cars (id) 
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY (userId)
  REFERENCES users (id) 
    ON UPDATE CASCADE
    ON DELETE CASCADE
);
INSERT INTO car_of_user VALUES(404,31,0);
INSERT INTO car_of_user VALUES(1,1,0);
INSERT INTO car_of_user VALUES(2,2,0);
INSERT INTO car_of_user VALUES(3,3,0);
INSERT INTO car_of_user VALUES(4,4,0);
INSERT INTO car_of_user VALUES(5,27,0);
INSERT INTO car_of_user VALUES(6,6,0);
INSERT INTO car_of_user VALUES(6,28,0);
INSERT INTO car_of_user VALUES(7,7,0);
INSERT INTO car_of_user VALUES(8,8,0);
INSERT INTO car_of_user VALUES(9,9,0);
INSERT INTO car_of_user VALUES(10,10,0);
INSERT INTO car_of_user VALUES(12,11,0);
INSERT INTO car_of_user VALUES(12,12,0);
INSERT INTO car_of_user VALUES(13,13,0);
INSERT INTO car_of_user VALUES(118,18,0);
INSERT INTO car_of_user VALUES(125,18,0);
INSERT INTO car_of_user VALUES(126,17,0);
INSERT INTO car_of_user VALUES(127,5,0);
INSERT INTO car_of_user VALUES(129,18,0);
INSERT INTO car_of_user VALUES(134,18,0);
INSERT INTO car_of_user VALUES(138,18,0);
INSERT INTO car_of_user VALUES(140,18,0);
INSERT INTO car_of_user VALUES(184,15,0);
INSERT INTO car_of_user VALUES(184,18,0);
INSERT INTO car_of_user VALUES(184,20,0);
CREATE TABLE charging_stations (
  id int PRIMARY KEY,
  particleDeviceId varchar NOT NULL UNIQUE CHECK (length(particleDeviceId) <= 45)
);
INSERT INTO charging_stations VALUES(1,'340021000c47343233323032');
INSERT INTO charging_stations VALUES(2,'3f0024001047343438323536');
CREATE TABLE charging_station_sockets (
  id int PRIMARY KEY,
  chargingStationId int DEFAULT NULL,
  FOREIGN KEY (chargingStationId)
  REFERENCES charging_stations (id) 
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
);
INSERT INTO charging_station_sockets VALUES(1,1);
INSERT INTO charging_station_sockets VALUES(2,1);
INSERT INTO charging_station_sockets VALUES(3,2);
INSERT INTO charging_station_sockets VALUES(4,2);
CREATE TABLE data (
  id bigint PRIMARY KEY,
  sensorID int NOT NULL,
  dateTime datetime NOT NULL,
  unixtime int UNSIGNED NOT NULL,
  min int NOT NULL,
  avr int NOT NULL,
  max int NOT NULL
);
INSERT INTO data VALUES(275,13,'2017-08-21 11:12:04',1503306724,96923,98632,100366);
INSERT INTO data VALUES(276,13,'2017-08-21 11:22:05',1503307325,97069,98645,100293);
INSERT INTO data VALUES(277,13,'2017-08-21 11:32:06',1503307926,96776,98663,100439);
INSERT INTO data VALUES(278,13,'2017-08-21 11:42:07',1503308527,96043,98674,100146);
INSERT INTO data VALUES(279,13,'2017-08-21 11:52:08',1503309129,96923,98572,100146);
INSERT INTO data VALUES(280,13,'2017-08-21 12:02:10',1503309730,96556,98559,99633);
INSERT INTO data VALUES(281,13,'2017-08-21 12:06:09',1503309969,0,55003,75091);
INSERT INTO data VALUES(282,13,'2017-08-21 12:10:30',1503310231,81172,82996,84395);
INSERT INTO data VALUES(283,12,'2018-01-17 15:20:20',1516198820,0,184670,299926);
INSERT INTO data VALUES(284,12,'2018-01-17 15:23:34',1516199014,0,124719,299926);
INSERT INTO data VALUES(285,12,'2018-01-17 15:33:34',1516199614,0,145334,299926);
INSERT INTO data VALUES(286,12,'2018-01-17 15:43:34',1516200214,0,138384,299926);
INSERT INTO data VALUES(287,12,'2018-01-17 15:53:34',1516200814,0,118334,299926);
INSERT INTO data VALUES(288,12,'2018-01-17 16:03:34',1516201414,0,156908,299926);
INSERT INTO data VALUES(289,12,'2018-01-17 16:13:34',1516202014,0,75117,299926);
INSERT INTO data VALUES(290,12,'2018-01-17 16:23:34',1516202614,0,18090,57289);
INSERT INTO data VALUES(291,12,'2018-01-17 16:33:34',1516203214,0,19485,60293);
INSERT INTO data VALUES(292,12,'2018-01-17 16:43:34',1516203814,0,103198,299926);
INSERT INTO data VALUES(293,12,'2018-01-17 16:53:34',1516204414,0,138870,299926);
INSERT INTO data VALUES(294,12,'2018-01-17 17:03:34',1516205014,0,153023,299926);
INSERT INTO data VALUES(295,12,'2018-01-17 17:13:34',1516205614,0,141115,299926);
INSERT INTO data VALUES(296,12,'2018-01-17 17:23:34',1516206214,0,158988,299926);
CREATE TABLE error_codes (
  page varchar NOT NULL,
  error int NOT NULL,
  message varchar DEFAULT NULL,
  PRIMARY KEY (page, error)
);
INSERT INTO error_codes VALUES('battery-fill-in',202,'The batterypercentage has succesfully been logged');
INSERT INTO error_codes VALUES('battery-fill-in',401,'Your token is invalid. Please login again.');
INSERT INTO error_codes VALUES('battery-fill-in',406,'Your battery percentage could not be logged. \\n Have you selected a vehicle and entered your correct batterypercentage?');
INSERT INTO error_codes VALUES('change-user-info',401,'You are not authorized to perform this action, did you correctly enter your current password?');
INSERT INTO error_codes VALUES('homepage',400,'Could not load sockets');
INSERT INTO error_codes VALUES('homepage',408,'The sockets took too long to load. Please try again later');
INSERT INTO error_codes VALUES('login',401,'Invalid credentials');
INSERT INTO error_codes VALUES('login',403,'You have not been verified yet. Please wait till an admin verifies you');
INSERT INTO error_codes VALUES('my-cars',200,'Your car has successfully been removed');
INSERT INTO error_codes VALUES('my-cars',401,'Your token is invalid, please login again.');
INSERT INTO error_codes VALUES('new-car-form',202,'Your car has been created but not yet added to your account. Please wait until an admin verifies your car. ');
INSERT INTO error_codes VALUES('new-car-form',401,'Your token is invalid. Please login again.');
INSERT INTO error_codes VALUES('new-car-form',412,'Your car could not be created. Have you filled in all the required fields?');
INSERT INTO error_codes VALUES('registration',202,'Your account has succesfully been created, check your email.');
INSERT INTO error_codes VALUES('registration',409,'Your HanID or uidTag is already registered.');
INSERT INTO error_codes VALUES('registration',412,'Your account could not be created. Have you filled in all the required fields?');
INSERT INTO error_codes VALUES('verified-cars',202,'The car has been added to your account');
INSERT INTO error_codes VALUES('verified-cars',401,'Your token is invalid. Please login again');
CREATE TABLE measurements (
  V1 float NOT NULL,
  V2 float NOT NULL,
  V3 float NOT NULL,
  I1 float NOT NULL,
  I2 float NOT NULL,
  I3 float NOT NULL,
  P float NOT NULL,
  E float NOT NULL,
  F float NOT NULL,
  Time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  SoC float,
  socketId int NOT NULL,    
  userId varchar,
  userName varchar,
  carId int,
  carName varchar,
  FOREIGN KEY (carId)
  REFERENCES cars (id) 
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY (userId)
  REFERENCES users (uidTag) 
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY (socketId)
  REFERENCES charging_station_sockets (id) 
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
);
INSERT INTO measurements VALUES(232.79000000000000802,221.77999999999999936,0.0,5.5,5.0,2.0,0.0,0.0,50.021100000000000562,1606395726,NULL,2,'NO ID','unknown',1,'');
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name varchar NOT NULL,
  uidTag varchar NOT NULL UNIQUE CHECK (length(uidTag) <= 45),
  hanId int DEFAULT NULL,
  LastStartOrStop datetime NOT NULL DEFAULT 0,
  password varchar,
  Remark varchar,
  token varchar DEFAULT NULL CHECK (length(token) <= 45),
  verified int NOT NULL DEFAULT 0,
  email varchar NOT NULL,
  mailed tinyint DEFAULT 0 CHECK (length(mailed) <= 4),
  admin tinyint NOT NULL DEFAULT 0  CHECK (length(admin) == 1),
  socketId tinyint DEFAULT NULL UNIQUE,
  FOREIGN KEY (socketId)
  REFERENCES charging_station_sockets (id) 
    ON UPDATE CASCADE
    ON DELETE NO ACTION
	
);
INSERT INTO users VALUES(1,'Yuri van Geffen','97 2D 39 5D',567745,1552383791,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e','567745',NULL,1,'batogcristian@yahoo.com',1,0,1);
INSERT INTO users VALUES(2,'Trung Nguyen','04 4E 79 EA FA 4D 80',567744,1541761670,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e','1234567890',NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(3,'Test 1','BB 77 E3 59',0,1552305521,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e','1234567890',NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(4,'Test 2','8E FD B3 89',1,1552375671,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e',NULL,NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(5,'Trung Test','66 FB 67 D9',2,1552383791,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e','1234567890',NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(6,'Menno Merts','60 8A 8A 7C',3,1539787113,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e','1234567890',NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(7,'Dave Mateman','B6 06 DB DB',4,1552983009,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e','1234567890',NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(8,'Boes-Voet Maria','60 AD 8F 7C',5,1550765473,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e','1234567890',NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(9,'Dave Mateman','04 81 3C AA 92 31 80',6,0,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e','1234567890',NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(10,'Johan Brussen','80 41 84 7C',7,0,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e',NULL,NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(11,'Grijff Katja','B0 49 8A 7C',8,0,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e','',NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(12,'Johan Brussen','04 1F 51 12 13 3B 80',9,0,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e',NULL,NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(13,'Cornelissen Peter','90 03 8F 7C',10,1552978846,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e',NULL,NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(14,'New','67 1C B6 89',11,1548666182,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e',NULL,NULL,1,'',0,0,NULL);
INSERT INTO users VALUES(15,'admin istrator','AA BB 11 22',111111,0,'$2a$10$NDKQjK/jInEG4kOc.v.Y3OaINkeiJc/veZdaNrOlKjI73CFvzga96','Dit is de admin','623u617k1ja4',1,'oose.canterbury@gmail.com',0,1,NULL);
INSERT INTO users VALUES(17,'Joris Huinink','04 5F 26 F2 80 46 80',597240,0,'$2a$10$jwBkXER50miroKbNqQXC4uoKdXILrstTc8G/IOF2aIz61YpRgbNq6',NULL,'804z227p2qt6',1,'jorishuinink@hotmail.nl',0,1,NULL);
INSERT INTO users VALUES(18,'Wouter Noordhof','04 2C 22 52 8A 55 80',605251,0,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e',NULL,'366v228h8tu0',1,'wh.noordhof@student.han.nl',0,1,NULL);
INSERT INTO users VALUES(19,'Dennis Gommer','04 7F 79 5A 81 46 80',598695,0,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e',NULL,'846g428y7wc5',1,'Dennis.Gommer@outlook.com',0,1,NULL);
INSERT INTO users VALUES(20,'Jasmijn Bartelds','45 HJ 67 JH',602898,0,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e',NULL,'596y694a6my5',1,'jasmijn.bartelds@hotmail.nl',0,0,NULL);
INSERT INTO users VALUES(25,'Joris Huinink','BB EE RR GG EE NN 55',597241,0,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e',NULL,'366b969x8za2',1,'jowjoris@gmail.com',0,0,NULL);
INSERT INTO users VALUES(26,'Arne Brethouwer','EV DA TA BA SE',234567,0,'$2a$10$oy4.e7SQXBihoXj6teo1VuILpO4b9wcGisF3R7CUC5LFz/esEZG6e',NULL,'154w504y9km5',1,'arne@ev-database.org',0,0,NULL);
INSERT INTO users VALUES(27,'JAN VERBEEK','66 53 D9 DB',123445,0,'$2a$10$6URffL6F2RHozY5wNX2WZ.mbO1OB8g9Nva0chM6Q72oM6sGIL8lni',NULL,'741d659r8az6',1,'jan.verbeek@han.nl',0,0,NULL);
INSERT INTO users VALUES(28,'VINCENT WIEGEL ','51 08 94 B9',987654,0,'$2a$10$My5DeZVe2DuEct8C83.JYO6u7IUPN.u/K/pK12vMxshzWUfOlSgzO',NULL,'681s331k2oz8',1,'vincent.wiegel@han.nl',0,0,NULL);
INSERT INTO users VALUES(29,'RESERVE CARD','96 A9 08 FD',443159,0,'$2a$10$QE7Hqk1OH7Q2L37W5QFpyOR.snK4.tTw0xZKL7AuRtixcuboz.Jd6',NULL,NULL,1,'NguyenXuan.Trung@han.nl',0,0,NULL);
INSERT INTO users VALUES(30,'testCard','1F 7E AC 29',443199,1606314036,'$2a$10$QE7Hqk1OH7Q2L37W5QFpyOR.snK4.tTw0xZKL7AuRtixcuboz.Jd6',NULL,NULL,1,'batogc@gmail.com',1,0,3);
INSERT INTO users VALUES(31,'unknown','NO ID',0,0,'',NULL,NULL,1,'',0,0,NULL);
COMMIT;
