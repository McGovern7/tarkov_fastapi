DROP DATABASE IF EXISTS `Tarkov_Project`;
CREATE DATABASE `Tarkov_Project`;
USE `Tarkov_Project`;

CREATE TABLE `tarkov_ammo` (
  ammo_name VARCHAR(25),
  calibre VARCHAR(25),
  penetration INT,
  damage INT,
  velocity INT,
  frag_pct INT,
  PRIMARY KEY (ammo_name, calibre)
);

#CREATE TABLE `tarkov_quests` (
#  quest_name VARCHAR(25),
#  trader_name VARCHAR(15),
#  location VARCHAR(25),
#  req_lvl INT,
#  rep_gained FLOAT,
#  xp_gained INT,
#  PRIMARY KEY (quest_name)
#);

INSERT INTO `tarkov_ammo` (
`ammo_name`,
`calibre`,
`penetration`,
`damage`,
`velocity`,
`frag_pct`)
VALUES
('5.2MM BUCKSHOT','12 Gauge Shot',1,296,330,0),
('8.5MM MAGNUM BUCKSHOT','12 Gauge Shot',2,400,385,0),
('6.5MM EXPRESS BUCKSHOT','12 Gauge Shot',3,315,430,0),
('7MM BUCKSHOT','12 Gauge Shot',3,280,415,0),
('PIRANHA','12 Gauge Shot',24,250,310,0),
('FLECHETTE','12 Gauge Shot',31,200,320,0),

('RIP','12 Gauge Slugs',2,265,410,100),
('SUPERPERFORMANCE HP SLUG','12 Gauge Slugs',5,220,594,39),
('GRIZZLY 40 SLUG','12 Gauge Slugs',12,190,390,12),
('COPPER SABOT HP SLUG','12 Gauge Slugs',14,206,442,38),
('LEAD SLUG','12 Gauge Slugs',15,167,370,20),
('DUAL SABOT SLUG','12 Gauge Slugs',17,170,415,10),
('POLEVA-3 SLUG','12 Gauge Slugs',17,140,410,20),
('FTX CUSTOM LITE SLUG','12 Gauge Slugs',20,183,480,10),
('POLEVA-6U SLUG','12 Gauge Slugs',20,150,430,15),
('MAKESHIFT .50 BMG SLUG','12 Gauge Slugs',26,197,410,5),
('AP-20 ARMOR PIERCING SLUG','12 Gauge Slugs',37,164,510,3),

('5.6MM BUCKSHOT','20 Gauge',1,208,340,0),
('6.2MM BUCKSHOT','20 Gauge',2,176,410,0),
('7.5MM BUCKSHOT','20 Gauge',3,200,475,0),
('7.3MM BUCKSHOT','20 Gauge',3,207,430,0),
('DEVASTATOR SLUG','20 Gauge',5,198,405,100),
('POLEVA-3 SLUG','20 Gauge',14,120,425,20),
('STAR SLUG','20 Gauge',16,154,415,10),
('POLEVA-6U','20 Gauge',17,135,445,15),

('ZVEZDA FLASHBANG ROUND','23x75mm',NULL,NULL,NULL,20),
('SHRAPNEL-25 BUCKSHOT','23x75mm',10,624,375,0),
('SHRAPNEL-10 BUCKSHOT','23x75mm',11,696,270,0),
('BARRIKADA SLUG','23x75mm',39,192,420,20),

('PM SP8 GZH','9x18mm',1,67,250,60),
('PM SP7 GZH','9x18mm',2,77,420,2),
('PM PSV','9x18mm',3,69,280,40),
('PM P GZH','9x18mm',5,50,302,25),
('PM PSO GZH','9x18mm',5,54,315,35),
('PM PS GS PPO','9x18mm',6,55,330,25),
('PM PRS GS','9x18mm',6,58,302,30),
('PM PPE GZH','9x18mm',7,61,297,35),
('PM PPT GZH','9x18mm',8,59,301,17),
('PM PST GZH','9x18mm',12,50,298,20),
('PM RG028 GZH','9x18mm',13,65,330,2),
('PM BZHT GZH','9x18mm',18,53,325,17),
('PMM PSTM GZH','9x18mm',24,58,420,17),
('PM PBM GZH','9x18mm',28,40,519,16),

('TT LRNPC','7.62x25mm',7,66,385,35),
('TT LRN','7.62x25mm',8,64,375,35),
('TT FMJ43','7.62x25mm',11,60,427,25),
('TT AKBS','7.62x25mm',12,58,425,25),
('TT P GL','7.62x25mm',14,58,430,25),
('TT PT GZH','7.62x25mm',18,55,415,17),
('TT PST GZH','7.62x25mm',25,50,430,20),

('RIP','9x19mm',2,102,381,100),
('QUAKEMAKER','9x19mm',8,85,290,10),
('PSO GZH','9x19mm',10,59,340,25),
('LUGER CGI','9x19mm',10,70,420,25),
('T GZH','9x19mm',14,58,365,15),
('M882','9x19mm',18,56,385,20),
('PST GZH','9x19mm',20,54,457,15),
('AP.6.3','9x19mm',30,52,392,5),
('PBP GZH','9x19mm',39,52,560,5),

('ACP RIP','.45',3,130,293,100),
('ACP HYDRA-SHOK','.45',13,100,274,50),
('ACP LASERMATCH FMJ','.45',19,76,290,1),
('ACP MATCH FMJ','.45',25,72,340,1),
('ACP AP','.45',38,66,299,1),

('PE GZH','9x21mm',15,80,415,35),
('P GZH','9x21mm',18,65,413,30),
('PS GZH','9x21mm',22,54,410,20),
('7U4','9x21mm',27,47,300,25),
('BT GZH','9x21mm',32,49,410,20),
('7N42','9x21mm',38,45,400,10),

('SOFT POINT','.357 MAGNUM',12,108,455,20),
('HP','.357 MAGNUM',18,99,481,60),
('JHP','.357 MAGNUM',24,88,425,60),
('FMJ','.357 MAGNUM',35,70,385,1),

('R37.F','5.7x28mm',8,98,729,100),
('SS198LF','5.7x28mm',17,70,792,80),
('R37.X','5.7x28mm',11,81,724,70),
('SS197R','5.7x28mm',25,62,594,50),
('L191 (TRACER)','5.7x28mm',33,53,715,20),
('SB193','5.7x28mm',27,59,299,20),
('SS190','5.7x28mm',37,49,715,20),

('ACTION SX','4.6x30mm',18,65,690,50),
('SUBSONIC SX','4.6x30mm',23,52,290,20),
('JSP SX','4.6x30mm',32,46,579,30),
('FMJ SX','4.6x30mm',40,43,620,20),
('AP SX','4.6x30mm',53,35,680,10),

('FMJ','9x39mm',17,75,330,30),
('SP-5 GS','9x39mm',28,71,290,20),
('SPP GS','9x39mm',35,68,310,20),
('PAB-9 GS','9x39mm',43,62,320,10),
('SP-6 GS','9x39mm',48,60,305,10),
('BP GS','9x39mm',54,48,295,10),

('TKM GEKSA','.366',14,110,550,45),
('TKM FMJ','.366',23,98,580,25),
('TKM EKO','.366',30,73,770,20),
('TKM AP-M','.366',42,90,602,1),

('HP','5.45x39mm',9,76,884,35),
('PRS GS','5.45x39mm',13,70,866,30),
('SP','5.45x39mm',15,65,873,45),
('US GS','5.45x39mm',17,63,303,10),
('T GS','5.45x39mm',20,57,883,16),
('FMJ','5.45x39mm',24,55,884,25),
('PS GS','5.45x39mm',28,53,890,40),
('PP GS','5.45x39mm',34,50,886,17),
('BT GS','5.45x39mm',37,48,880,16),
('7N40','5.45x39mm',42,52,915,2),
('BP GS','5.45x39mm',45,46,890,16),
('BS GS','5.45x39mm',54,43,830,17),
('PPBS GS IGOLNIK','5.45x39mm',62,37,905,2),

('WARMAGEDDON','5.56x45mm',3,88,936,90),
('HP','5.56x45mm',7,79,947,70),
('MK 255 MOD 0 (RRLP)','5.56x45mm',11,72,936,3),
('M856','5.56x45mm',18,64,874,33),
('FMJ','5.56x45mm',23,59,957,50),
('M855','5.56x45mm',31,57,922,40),
('MK 318 MOD 0 (SOST)','5.56x45mm',33,55,902,35),
('M856A1','5.56x45mm',38,52,940,42),
('M855A1','5.56x45mm',44,49,945,44),
('M995','5.56x45mm',53,42,1013,42),
('SSA AP','5.56x45mm',57,38,1013,20),

('HP','7.62x39mm',15,87,754,40),
('SP','7.62x39mm',20,68,772,35),
('FMJ','7.62x39mm',26,63,775,30),
('US GZH','7.62x39mm',29,56,300,8),
('T-45M1 GZH','7.62x39mm',30,64,720,12),
('PS GZH','7.62x39mm',35,57,700,20),
('PP','7.62x39mm',41,55,732,15),
('BP GZH','7.62x39mm',47,58,730,12),
('MAI AP','7.62x39mm',58,47,730,5),

('BLACKOUT WHISPER','.300 blk',14,90,853,35),
('BLACKOUT V-MAX','.300 blk',20,72,723,25),
('BLACKOUT BCP FMJ','.300 blk',30,60,605,30),
('BLACKOUT M62 TRACER','.300 blk',36,54,442,20),
('BLACKOUT CBJ','.300 blk',43,58,725,15),
('BLACKOUT AP','.300 blk',48,51,635,30),

('SIG FMJ','6.8x51mm',36,80,899,18),
('SIG HYBRID','6.8x51mm',47,72,914,12),

('ULTRA NOSLER','7.62x51mm',15,107,822,70),
('TCW SP','7.62x51mm',30,87,808,35),
('BCP FMJ','7.62x51mm',35,83,840,20),
('M80','7.62x51mm',41,80,833,17),
('M62 TRACER','7.62x51mm',44,79,816,14),
('M61','7.62x51mm',64,70,849,13),
('M993','7.62x51mm',70,67,910,12),

('HP BT (TRACER)','7.62x54R',23,102,807,40),
('SP BT (TRACER)','7.62x54R',27,92,703,24),
('FMJ','7.62x54R',33,84,760,20),
('T-46M GZH','7.62x54R',41,82,800,18),
('LPS GZH','7.62x54R',42,81,865,18),
('PS GZH','7.62x54R',45,84,875,8),
('BT GZH','7.62x54R',55,78,875,8),
('SNB GZH','7.62x54R',62,75,875,8),
('BS GS','7.62x54R',70,72,785,8),

('PS12A','12.7x55mm',10,165,290,70),
('PS12','12.7x55mm',28,115,285,30),
('PS12B','12.7x55mm',46,102,300,30),

('TAC-X','.338 Lapua Magnum',18,196,880,50),
('UCW','.338 Lapua Magnum',32,142,849,60),
('FMJ','.338 Lapua Magnum',47,122,900,20),
('AP','.338 Lapua Magnum',79,115,849,13)
; 

#ALTER TABLE `tarkov_ammo`
#ADD class_one INT, # value 6 if penetration > 20
#ADD class_two INT,
#ADD class_three INT,
#ADD class_four INT,
#ADD class_five INT,
#ADD class_six INT;

