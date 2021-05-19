CREATE TABLE `company` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text,
  `ogrn` bigint DEFAULT NULL,
  `okpo` bigint DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `date_reg` varchar(45) DEFAULT NULL,
  `us_capital` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=517 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci