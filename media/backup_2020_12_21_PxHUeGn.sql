-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: bd_pagos
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alquiler`
--

DROP TABLE IF EXISTS `alquiler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alquiler` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_salida` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `estado` int NOT NULL,
  `transaccion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `alquiler_transaccion_id_7b7f9332_fk_transaccion_id` (`transaccion_id`),
  CONSTRAINT `alquiler_transaccion_id_7b7f9332_fk_transaccion_id` FOREIGN KEY (`transaccion_id`) REFERENCES `transaccion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alquiler`
--

LOCK TABLES `alquiler` WRITE;
/*!40000 ALTER TABLE `alquiler` DISABLE KEYS */;
/*!40000 ALTER TABLE `alquiler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asig_recurso`
--

DROP TABLE IF EXISTS `asig_recurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asig_recurso` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_asig` date NOT NULL,
  `lote` varchar(100) NOT NULL,
  `estado` int NOT NULL,
  `inventariado` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lote` (`lote`),
  KEY `asig_recurso_user_id_d322153c_fk_usuario_id` (`user_id`),
  CONSTRAINT `asig_recurso_user_id_d322153c_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asig_recurso`
--

LOCK TABLES `asig_recurso` WRITE;
/*!40000 ALTER TABLE `asig_recurso` DISABLE KEYS */;
INSERT INTO `asig_recurso` VALUES (1,'2020-12-10','1',2,1,1),(3,'2020-12-12','2',2,1,1);
/*!40000 ALTER TABLE `asig_recurso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (3,'admin'),(2,'Clientes');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=180 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (178,2,44),(21,2,81),(179,2,84),(22,3,1),(23,3,2),(24,3,3),(25,3,4),(26,3,5),(27,3,6),(28,3,7),(29,3,8),(30,3,9),(31,3,10),(32,3,11),(33,3,12),(34,3,13),(35,3,14),(36,3,15),(37,3,16),(38,3,17),(39,3,18),(40,3,19),(41,3,20),(42,3,21),(43,3,22),(44,3,23),(45,3,24),(46,3,25),(47,3,26),(48,3,27),(49,3,28),(50,3,29),(51,3,30),(52,3,31),(53,3,32),(54,3,33),(55,3,34),(56,3,35),(57,3,36),(58,3,37),(59,3,38),(60,3,39),(61,3,40),(62,3,41),(63,3,42),(64,3,43),(65,3,44),(66,3,45),(67,3,46),(68,3,47),(69,3,48),(70,3,49),(71,3,50),(72,3,51),(73,3,52),(74,3,53),(75,3,54),(76,3,55),(77,3,56),(78,3,57),(79,3,58),(80,3,59),(81,3,60),(82,3,61),(83,3,62),(84,3,63),(85,3,64),(86,3,65),(87,3,66),(88,3,67),(89,3,68),(90,3,69),(91,3,70),(92,3,71),(93,3,72),(94,3,73),(95,3,74),(96,3,75),(97,3,76),(98,3,77),(99,3,78),(100,3,79),(101,3,80),(102,3,81),(103,3,82),(104,3,83),(105,3,84),(106,3,85),(107,3,86),(108,3,87),(109,3,88),(110,3,89),(111,3,90),(112,3,91),(113,3,92),(114,3,93),(115,3,94),(116,3,95),(117,3,96),(118,3,97),(119,3,98),(120,3,99),(121,3,100),(122,3,101),(123,3,102),(124,3,103),(125,3,104),(126,3,105),(127,3,106),(128,3,107),(129,3,108),(130,3,109),(131,3,110),(132,3,111),(133,3,112),(134,3,113),(135,3,114),(136,3,115),(137,3,116),(138,3,117),(139,3,118),(140,3,119),(141,3,120),(142,3,121),(143,3,122),(144,3,123),(145,3,124),(146,3,125),(147,3,126),(148,3,127),(149,3,128),(150,3,129),(151,3,130),(152,3,131),(153,3,132),(154,3,133),(155,3,134),(156,3,135),(157,3,136),(158,3,137),(159,3,138),(160,3,139),(161,3,140),(162,3,141),(163,3,142),(164,3,143),(165,3,144),(166,3,145),(167,3,146),(168,3,147),(169,3,148),(170,3,149),(171,3,150),(172,3,151),(173,3,152),(174,3,153),(175,3,154),(176,3,155),(177,3,156);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add categoria',6,'add_categoria'),(22,'Can change categoria',6,'change_categoria'),(23,'Can delete categoria',6,'delete_categoria'),(24,'Can view categoria',6,'view_categoria'),(25,'Can add cliente',7,'add_cliente'),(26,'Can change cliente',7,'change_cliente'),(27,'Can delete cliente',7,'delete_cliente'),(28,'Can view cliente',7,'view_cliente'),(29,'Can add empresa',8,'add_empresa'),(30,'Can change empresa',8,'change_empresa'),(31,'Can delete empresa',8,'delete_empresa'),(32,'Can view empresa',8,'view_empresa'),(33,'Can add gasto',9,'add_gasto'),(34,'Can change gasto',9,'change_gasto'),(35,'Can delete gasto',9,'delete_gasto'),(36,'Can view gasto',9,'view_gasto'),(37,'Can add presentacion',10,'add_presentacion'),(38,'Can change presentacion',10,'change_presentacion'),(39,'Can delete presentacion',10,'delete_presentacion'),(40,'Can view presentacion',10,'view_presentacion'),(41,'Can add producto',11,'add_producto'),(42,'Can change producto',11,'change_producto'),(43,'Can delete producto',11,'delete_producto'),(44,'Can view producto',11,'view_producto'),(45,'Can add proveedor',12,'add_proveedor'),(46,'Can change proveedor',12,'change_proveedor'),(47,'Can delete proveedor',12,'delete_proveedor'),(48,'Can view proveedor',12,'view_proveedor'),(49,'Can add tipo_gasto',13,'add_tipo_gasto'),(50,'Can change tipo_gasto',13,'change_tipo_gasto'),(51,'Can delete tipo_gasto',13,'delete_tipo_gasto'),(52,'Can view tipo_gasto',13,'view_tipo_gasto'),(53,'Can add devolucion',14,'add_devolucion'),(54,'Can change devolucion',14,'change_devolucion'),(55,'Can delete devolucion',14,'delete_devolucion'),(56,'Can view devolucion',14,'view_devolucion'),(57,'Can add usuario',15,'add_user'),(58,'Can change usuario',15,'change_user'),(59,'Can delete usuario',15,'delete_user'),(60,'Can view usuario',15,'view_user'),(61,'Can add Tipo_maquina',16,'add_tipo_maquina'),(62,'Can change Tipo_maquina',16,'change_tipo_maquina'),(63,'Can delete Tipo_maquina',16,'delete_tipo_maquina'),(64,'Can view Tipo_maquina',16,'view_tipo_maquina'),(65,'Can add maquina',17,'add_maquina'),(66,'Can change maquina',17,'change_maquina'),(67,'Can delete maquina',17,'delete_maquina'),(68,'Can view maquina',17,'view_maquina'),(69,'Can add detalle_reparcion',18,'add_detalle_reparacion'),(70,'Can change detalle_reparcion',18,'change_detalle_reparacion'),(71,'Can delete detalle_reparcion',18,'delete_detalle_reparacion'),(72,'Can view detalle_reparcion',18,'view_detalle_reparacion'),(73,'Can add reparacion',19,'add_reparacion'),(74,'Can change reparacion',19,'change_reparacion'),(75,'Can delete reparacion',19,'delete_reparacion'),(76,'Can view reparacion',19,'view_reparacion'),(77,'Can add transaccion',20,'add_transaccion'),(78,'Can change transaccion',20,'change_transaccion'),(79,'Can delete transaccion',20,'delete_transaccion'),(80,'Can view transaccion',20,'view_transaccion'),(81,'Can add venta',21,'add_venta'),(82,'Can change venta',21,'change_venta'),(83,'Can delete venta',21,'delete_venta'),(84,'Can view venta',21,'view_venta'),(85,'Can add detalle_venta',22,'add_detalle_venta'),(86,'Can change detalle_venta',22,'change_detalle_venta'),(87,'Can delete detalle_venta',22,'delete_detalle_venta'),(88,'Can view detalle_venta',22,'view_detalle_venta'),(89,'Can add compra',23,'add_compra'),(90,'Can change compra',23,'change_compra'),(91,'Can delete compra',23,'delete_compra'),(92,'Can view compra',23,'view_compra'),(93,'Can add detalle_compra',24,'add_detalle_compra'),(94,'Can change detalle_compra',24,'change_detalle_compra'),(95,'Can delete detalle_compra',24,'delete_detalle_compra'),(96,'Can view detalle_compra',24,'view_detalle_compra'),(97,'Can add inventario_producto',25,'add_inventario_producto'),(98,'Can change inventario_producto',25,'change_inventario_producto'),(99,'Can delete inventario_producto',25,'delete_inventario_producto'),(100,'Can view inventario_producto',25,'view_inventario_producto'),(101,'Can add inventario_material',26,'add_inventario_material'),(102,'Can change inventario_material',26,'change_inventario_material'),(103,'Can delete inventario_material',26,'delete_inventario_material'),(104,'Can view inventario_material',26,'view_inventario_material'),(105,'Can add confeccion',27,'add_confeccion'),(106,'Can change confeccion',27,'change_confeccion'),(107,'Can delete confeccion',27,'delete_confeccion'),(108,'Can view confeccion',27,'view_confeccion'),(109,'Can add detalle_confeccion',28,'add_detalle_confeccion'),(110,'Can change detalle_confeccion',28,'change_detalle_confeccion'),(111,'Can delete detalle_confeccion',28,'delete_detalle_confeccion'),(112,'Can view detalle_confeccion',28,'view_detalle_confeccion'),(113,'Can add alquiler',29,'add_alquiler'),(114,'Can change alquiler',29,'change_alquiler'),(115,'Can delete alquiler',29,'delete_alquiler'),(116,'Can view alquiler',29,'view_alquiler'),(117,'Can add detalle_alquiler',30,'add_detalle_alquiler'),(118,'Can change detalle_alquiler',30,'change_detalle_alquiler'),(119,'Can delete detalle_alquiler',30,'delete_detalle_alquiler'),(120,'Can view detalle_alquiler',30,'view_detalle_alquiler'),(121,'Can add material',31,'add_material'),(122,'Can change material',31,'change_material'),(123,'Can delete material',31,'delete_material'),(124,'Can view material',31,'view_material'),(125,'Can add asig_recurso',32,'add_asig_recurso'),(126,'Can change asig_recurso',32,'change_asig_recurso'),(127,'Can delete asig_recurso',32,'delete_asig_recurso'),(128,'Can view asig_recurso',32,'view_asig_recurso'),(129,'Can add detalle_asig_maquina',33,'add_detalle_asig_maquina'),(130,'Can change detalle_asig_maquina',33,'change_detalle_asig_maquina'),(131,'Can delete detalle_asig_maquina',33,'delete_detalle_asig_maquina'),(132,'Can view detalle_asig_maquina',33,'view_detalle_asig_maquina'),(133,'Can add detalle_asig_recurso',34,'add_detalle_asig_recurso'),(134,'Can change detalle_asig_recurso',34,'change_detalle_asig_recurso'),(135,'Can delete detalle_asig_recurso',34,'delete_detalle_asig_recurso'),(136,'Can view detalle_asig_recurso',34,'view_detalle_asig_recurso'),(137,'Can add producto_base',35,'add_producto_base'),(138,'Can change producto_base',35,'change_producto_base'),(139,'Can delete producto_base',35,'delete_producto_base'),(140,'Can view producto_base',35,'view_producto_base'),(141,'Can add sitio',36,'add_sitioweb'),(142,'Can change sitio',36,'change_sitioweb'),(143,'Can delete sitio',36,'delete_sitioweb'),(144,'Can view sitio',36,'view_sitioweb'),(145,'Can add produccion',37,'add_produccion'),(146,'Can change produccion',37,'change_produccion'),(147,'Can delete produccion',37,'delete_produccion'),(148,'Can view produccion',37,'view_produccion'),(149,'Can add detalle_perdidas_producto',38,'add_detalle_perdidas_productos'),(150,'Can change detalle_perdidas_producto',38,'change_detalle_perdidas_productos'),(151,'Can delete detalle_perdidas_producto',38,'delete_detalle_perdidas_productos'),(152,'Can view detalle_perdidas_producto',38,'view_detalle_perdidas_productos'),(153,'Can add detalle_perdidas_material',39,'add_detalle_perdidas_materiales'),(154,'Can change detalle_perdidas_material',39,'change_detalle_perdidas_materiales'),(155,'Can delete detalle_perdidas_material',39,'delete_detalle_perdidas_materiales'),(156,'Can view detalle_perdidas_material',39,'view_detalle_perdidas_materiales'),(157,'Can add databasebackups',40,'add_databasebackups'),(158,'Can change databasebackups',40,'change_databasebackups'),(159,'Can delete databasebackups',40,'delete_databasebackups'),(160,'Can view databasebackups',40,'view_databasebackups');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(25) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Ropa para Hombre','Ropa para Hombre'),(2,'Ropa para Mujer','Ropa para Mujer'),(3,'Telas','Telas para produccion'),(4,'Ropa de Niño','Ropa para Niños');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombres` varchar(50) NOT NULL,
  `apellidos` varchar(20) DEFAULT NULL,
  `cedula` varchar(10) NOT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `sexo` int NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cedula` (`cedula`),
  UNIQUE KEY `telefono` (`telefono`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'Diana Carolina','Gomez Moran','0910978329','gmez@gmail.com',0,'0994547884','MIlagro','2020-12-10'),(4,'Angie Isabel','Gomez Moran','1204222895','chrisstianandres@gmail.com',0,'042710122','Sin direccion','2020-12-16'),(41,'Dayanna Lisbeth','Ochoa Ramirez','1102294509','dayana15@gmail.com',0,'097868644','Sin direccion','2020-12-19');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compra`
--

DROP TABLE IF EXISTS `compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_compra` date NOT NULL,
  `subtotal` decimal(9,2) NOT NULL,
  `iva` decimal(9,2) NOT NULL,
  `total` decimal(9,2) NOT NULL,
  `estado` int NOT NULL,
  `proveedor_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `compra_proveedor_id_11336635_fk_proveedor_id` (`proveedor_id`),
  KEY `compra_user_id_04314f70_fk_usuario_id` (`user_id`),
  CONSTRAINT `compra_proveedor_id_11336635_fk_proveedor_id` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id`),
  CONSTRAINT `compra_user_id_04314f70_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compra`
--

LOCK TABLES `compra` WRITE;
/*!40000 ALTER TABLE `compra` DISABLE KEYS */;
INSERT INTO `compra` VALUES (1,'2020-12-12',1116.10,133.93,1250.03,1,1,1);
/*!40000 ALTER TABLE `compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `confeccion`
--

DROP TABLE IF EXISTS `confeccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `confeccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_entrega` date DEFAULT NULL,
  `estado` int NOT NULL,
  `transaccion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `confeccion_transaccion_id_3f45c1d4_fk_transaccion_id` (`transaccion_id`),
  CONSTRAINT `confeccion_transaccion_id_3f45c1d4_fk_transaccion_id` FOREIGN KEY (`transaccion_id`) REFERENCES `transaccion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `confeccion`
--

LOCK TABLES `confeccion` WRITE;
/*!40000 ALTER TABLE `confeccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `confeccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `databasebackups`
--

DROP TABLE IF EXISTS `databasebackups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `databasebackups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `archive` varchar(100) NOT NULL,
  `fecha` date NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `databasebackups_user_id_486fa5c8_fk_usuario_id` (`user_id`),
  CONSTRAINT `databasebackups_user_id_486fa5c8_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `databasebackups`
--

LOCK TABLES `databasebackups` WRITE;
/*!40000 ALTER TABLE `databasebackups` DISABLE KEYS */;
/*!40000 ALTER TABLE `databasebackups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_alquiler`
--

DROP TABLE IF EXISTS `detalle_alquiler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_alquiler` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pvp_by_alquiler` decimal(9,2) DEFAULT NULL,
  `cantidad` int NOT NULL,
  `subtotal` decimal(9,2) NOT NULL,
  `alquiler_id` int NOT NULL,
  `inventario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `detalle_alquiler_alquiler_id_a0ef59fd_fk_alquiler_id` (`alquiler_id`),
  KEY `detalle_alquiler_inventario_id_a1854606_fk_inventari` (`inventario_id`),
  CONSTRAINT `detalle_alquiler_alquiler_id_a0ef59fd_fk_alquiler_id` FOREIGN KEY (`alquiler_id`) REFERENCES `alquiler` (`id`),
  CONSTRAINT `detalle_alquiler_inventario_id_a1854606_fk_inventari` FOREIGN KEY (`inventario_id`) REFERENCES `inventario_producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_alquiler`
--

LOCK TABLES `detalle_alquiler` WRITE;
/*!40000 ALTER TABLE `detalle_alquiler` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_alquiler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_asig_maquina`
--

DROP TABLE IF EXISTS `detalle_asig_maquina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_asig_maquina` (
  `id` int NOT NULL AUTO_INCREMENT,
  `asig_recurso_id` int NOT NULL,
  `maquina_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `detalle_asig_maquina_asig_recurso_id_01b924c9_fk_asig_recurso_id` (`asig_recurso_id`),
  KEY `detalle_asig_maquina_maquina_id_a930c5f4_fk_maquina_id` (`maquina_id`),
  CONSTRAINT `detalle_asig_maquina_asig_recurso_id_01b924c9_fk_asig_recurso_id` FOREIGN KEY (`asig_recurso_id`) REFERENCES `asig_recurso` (`id`),
  CONSTRAINT `detalle_asig_maquina_maquina_id_a930c5f4_fk_maquina_id` FOREIGN KEY (`maquina_id`) REFERENCES `maquina` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_asig_maquina`
--

LOCK TABLES `detalle_asig_maquina` WRITE;
/*!40000 ALTER TABLE `detalle_asig_maquina` DISABLE KEYS */;
INSERT INTO `detalle_asig_maquina` VALUES (1,3,1);
/*!40000 ALTER TABLE `detalle_asig_maquina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_asig_recurso`
--

DROP TABLE IF EXISTS `detalle_asig_recurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_asig_recurso` (
  `id` int NOT NULL AUTO_INCREMENT,
  `asig_recurso_id` int NOT NULL,
  `inventario_material_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `detalle_asig_recurso_asig_recurso_id_2a0ee2d4_fk_asig_recurso_id` (`asig_recurso_id`),
  KEY `detalle_asig_recurso_inventario_material__3c0fad06_fk_inventari` (`inventario_material_id`),
  CONSTRAINT `detalle_asig_recurso_asig_recurso_id_2a0ee2d4_fk_asig_recurso_id` FOREIGN KEY (`asig_recurso_id`) REFERENCES `asig_recurso` (`id`),
  CONSTRAINT `detalle_asig_recurso_inventario_material__3c0fad06_fk_inventari` FOREIGN KEY (`inventario_material_id`) REFERENCES `inventario_material` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_asig_recurso`
--

LOCK TABLES `detalle_asig_recurso` WRITE;
/*!40000 ALTER TABLE `detalle_asig_recurso` DISABLE KEYS */;
INSERT INTO `detalle_asig_recurso` VALUES (1,3,10),(2,3,9);
/*!40000 ALTER TABLE `detalle_asig_recurso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_compra`
--

DROP TABLE IF EXISTS `detalle_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `p_compra_actual` decimal(9,2) DEFAULT NULL,
  `cantidad` int NOT NULL,
  `subtotal` decimal(9,2) NOT NULL,
  `compra_id` int NOT NULL,
  `material_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `detalle_compra_compra_id_4fc61e57_fk_compra_id` (`compra_id`),
  KEY `detalle_compra_material_id_83834732_fk_material_id` (`material_id`),
  CONSTRAINT `detalle_compra_compra_id_4fc61e57_fk_compra_id` FOREIGN KEY (`compra_id`) REFERENCES `compra` (`id`),
  CONSTRAINT `detalle_compra_material_id_83834732_fk_material_id` FOREIGN KEY (`material_id`) REFERENCES `material` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_compra`
--

LOCK TABLES `detalle_compra` WRITE;
/*!40000 ALTER TABLE `detalle_compra` DISABLE KEYS */;
INSERT INTO `detalle_compra` VALUES (1,125.00,10,1116.10,1,1);
/*!40000 ALTER TABLE `detalle_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_confeccion`
--

DROP TABLE IF EXISTS `detalle_confeccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_confeccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pvp_by_confec` decimal(9,2) DEFAULT NULL,
  `cantidad` int NOT NULL,
  `subtotal` decimal(9,2) NOT NULL,
  `confeccion_id` int NOT NULL,
  `producto_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `detalle_confeccion_confeccion_id_2d725600_fk_confeccion_id` (`confeccion_id`),
  KEY `detalle_confeccion_producto_id_2dfc949f_fk_producto_id` (`producto_id`),
  CONSTRAINT `detalle_confeccion_confeccion_id_2d725600_fk_confeccion_id` FOREIGN KEY (`confeccion_id`) REFERENCES `confeccion` (`id`),
  CONSTRAINT `detalle_confeccion_producto_id_2dfc949f_fk_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_confeccion`
--

LOCK TABLES `detalle_confeccion` WRITE;
/*!40000 ALTER TABLE `detalle_confeccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_confeccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_perdidas_material`
--

DROP TABLE IF EXISTS `detalle_perdidas_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_perdidas_material` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL,
  `material_id` int NOT NULL,
  `produccion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `detalle_perdidas_material_material_id_650bd574_fk_material_id` (`material_id`),
  KEY `detalle_perdidas_mat_produccion_id_792ba5f6_fk_produccio` (`produccion_id`),
  CONSTRAINT `detalle_perdidas_mat_produccion_id_792ba5f6_fk_produccio` FOREIGN KEY (`produccion_id`) REFERENCES `produccion` (`id`),
  CONSTRAINT `detalle_perdidas_material_material_id_650bd574_fk_material_id` FOREIGN KEY (`material_id`) REFERENCES `material` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_perdidas_material`
--

LOCK TABLES `detalle_perdidas_material` WRITE;
/*!40000 ALTER TABLE `detalle_perdidas_material` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_perdidas_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_perdidas_producto`
--

DROP TABLE IF EXISTS `detalle_perdidas_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_perdidas_producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL,
  `produccion_id` int NOT NULL,
  `producto_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `detalle_perdidas_pro_produccion_id_27e49db3_fk_produccio` (`produccion_id`),
  KEY `detalle_perdidas_producto_producto_id_cf8e7b76_fk_producto_id` (`producto_id`),
  CONSTRAINT `detalle_perdidas_pro_produccion_id_27e49db3_fk_produccio` FOREIGN KEY (`produccion_id`) REFERENCES `produccion` (`id`),
  CONSTRAINT `detalle_perdidas_producto_producto_id_cf8e7b76_fk_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_perdidas_producto`
--

LOCK TABLES `detalle_perdidas_producto` WRITE;
/*!40000 ALTER TABLE `detalle_perdidas_producto` DISABLE KEYS */;
INSERT INTO `detalle_perdidas_producto` VALUES (1,1,1,1);
/*!40000 ALTER TABLE `detalle_perdidas_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_reparcion`
--

DROP TABLE IF EXISTS `detalle_reparcion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_reparcion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pvp_rep_by_prod` decimal(9,2) DEFAULT NULL,
  `cantidad` int NOT NULL,
  `subtotal` decimal(9,2) NOT NULL,
  `producto_id` int DEFAULT NULL,
  `reparacion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `detalle_reparcion_producto_id_73356f93_fk_producto_id` (`producto_id`),
  KEY `detalle_reparcion_reparacion_id_70ee6c2a_fk_reparacion_id` (`reparacion_id`),
  CONSTRAINT `detalle_reparcion_producto_id_73356f93_fk_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`),
  CONSTRAINT `detalle_reparcion_reparacion_id_70ee6c2a_fk_reparacion_id` FOREIGN KEY (`reparacion_id`) REFERENCES `reparacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_reparcion`
--

LOCK TABLES `detalle_reparcion` WRITE;
/*!40000 ALTER TABLE `detalle_reparcion` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_reparcion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_venta`
--

DROP TABLE IF EXISTS `detalle_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pvp_actual` decimal(9,2) NOT NULL,
  `cantidad` int NOT NULL,
  `subtotal` decimal(9,2) NOT NULL,
  `inventario_id` int NOT NULL,
  `venta_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `detalle_venta_inventario_id_b5461a4a_fk_inventario_producto_id` (`inventario_id`),
  KEY `detalle_venta_venta_id_ecf1a1a3_fk_venta_id` (`venta_id`),
  CONSTRAINT `detalle_venta_inventario_id_b5461a4a_fk_inventario_producto_id` FOREIGN KEY (`inventario_id`) REFERENCES `inventario_producto` (`id`),
  CONSTRAINT `detalle_venta_venta_id_ecf1a1a3_fk_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `venta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_venta`
--

LOCK TABLES `detalle_venta` WRITE;
/*!40000 ALTER TABLE `detalle_venta` DISABLE KEYS */;
INSERT INTO `detalle_venta` VALUES (1,10.00,1,10.00,1,1),(2,10.00,12,10.00,1,2),(3,12.00,3,36.00,300,4),(4,12.00,3,36.00,301,4),(5,12.00,3,36.00,302,4),(6,10.00,5,50.00,350,4),(7,10.00,5,50.00,351,4),(8,10.00,5,50.00,352,4),(9,10.00,5,50.00,353,4),(10,10.00,5,50.00,354,4),(11,15.00,5,75.00,410,4),(12,15.00,5,75.00,411,4),(13,15.00,5,75.00,412,4),(14,15.00,5,75.00,413,4),(15,15.00,5,75.00,414,4),(16,10.00,2,20.00,355,5),(17,10.00,2,20.00,356,5),(18,15.00,1,15.00,415,5),(19,10.00,2,20.00,357,6),(20,10.00,2,20.00,358,6),(21,15.00,1,15.00,416,6),(22,10.00,2,20.00,359,7),(23,10.00,2,20.00,360,7),(24,15.00,1,15.00,417,7),(25,12.00,3,36.00,303,8),(26,12.00,3,36.00,304,8),(27,12.00,3,36.00,305,8),(28,15.00,3,45.00,418,8),(29,15.00,3,45.00,419,8),(30,15.00,3,45.00,420,8),(31,12.00,1,12.00,306,9),(32,15.00,2,30.00,421,10),(33,15.00,2,30.00,422,10),(34,15.00,1,15.00,423,11),(35,12.00,1,12.00,307,11),(36,15.00,1,15.00,424,12),(37,12.00,1,12.00,308,12),(38,15.00,1,15.00,425,13),(39,12.00,1,12.00,309,13),(40,15.00,1,15.00,426,14),(41,12.00,1,12.00,310,14),(42,15.00,1,15.00,427,15),(43,12.00,1,12.00,311,15),(44,15.00,1,15.00,428,16),(45,12.00,1,12.00,312,16),(46,15.00,1,15.00,429,17),(47,12.00,1,12.00,313,17),(48,15.00,1,15.00,430,18),(49,12.00,1,12.00,314,18),(50,15.00,1,15.00,431,19),(51,12.00,1,12.00,315,19),(52,15.00,1,15.00,432,20),(53,12.00,1,12.00,316,20),(54,15.00,1,15.00,433,21),(55,12.00,1,12.00,317,21);
/*!40000 ALTER TABLE `detalle_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devolucion`
--

DROP TABLE IF EXISTS `devolucion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devolucion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `venta_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `devolucion_venta_id_ff12d98e_fk_venta_id` (`venta_id`),
  CONSTRAINT `devolucion_venta_id_ff12d98e_fk_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `venta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devolucion`
--

LOCK TABLES `devolucion` WRITE;
/*!40000 ALTER TABLE `devolucion` DISABLE KEYS */;
INSERT INTO `devolucion` VALUES (1,'2020-12-13',3);
/*!40000 ALTER TABLE `devolucion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_usuario_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2020-12-07 20:00:52.917807','1','admin Christian Andres',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Cedula\", \"Celular\", \"Telefono\", \"Direccion\", \"Estado\"]}}]',15,1),(2,'2020-12-07 20:01:46.228953','1','Confecciones IJEI 0978765652001',1,'[{\"added\": {}}]',8,1),(3,'2020-12-10 14:02:28.630552','1','Confecciones \"IJEI\"',1,'[{\"added\": {}}]',36,1),(4,'2020-12-11 00:35:43.545633','1','Camisa XL',2,'[{\"changed\": {\"fields\": [\"Stock\"]}}]',35,1),(5,'2020-12-11 00:35:54.492849','1','Camisa XL',2,'[{\"changed\": {\"fields\": [\"Stock\"]}}]',35,1),(6,'2020-12-11 00:37:27.004082','1','2020-12-10',1,'[{\"added\": {}}]',32,1),(7,'2020-12-11 00:37:45.684744','1','2020-12-10 1',1,'[{\"added\": {}}, {\"added\": {\"name\": \"detalle_perdidas_producto\", \"object\": \"2020-12-10 1 Camisa XL\"}}, {\"added\": {\"name\": \"detalle_perdidas_producto\", \"object\": \"2020-12-10 1 Camisa XL\"}}, {\"added\": {\"name\": \"detalle_perdidas_producto\", \"object\": \"2020-12-10 1 Camisa XL\"}}]',37,1),(8,'2020-12-11 00:37:50.760361','1','Camisa XL',1,'[{\"added\": {}}]',25,1),(9,'2020-12-12 18:45:32.667587','2','Diana Carolina 2020-12-10 11.20',1,'[{\"added\": {}}, {\"added\": {\"name\": \"detalle_venta\", \"object\": \"Diana Carolina 2020-12-10 11.20\"}}]',21,1),(10,'2020-12-13 19:14:13.250270','1','Camisa XL',2,'[{\"changed\": {\"fields\": [\"Stock\"]}}]',35,1),(11,'2020-12-13 19:14:17.131435','1','Camisa XL',2,'[]',11,1),(12,'2020-12-13 19:14:32.302654','2','Camisa SM',2,'[{\"changed\": {\"fields\": [\"Stock\"]}}]',35,1),(13,'2020-12-13 19:14:34.023840','2','Camisa SM',2,'[]',11,1),(14,'2020-12-13 19:14:51.486856','3','Blusa SM',2,'[{\"changed\": {\"fields\": [\"Stock\"]}}]',35,1),(15,'2020-12-13 19:14:52.664702','3','Blusa SM',2,'[]',11,1),(16,'2020-12-13 19:27:33.995654','1','Camisa XL',2,'[{\"changed\": {\"fields\": [\"Stock\"]}}]',35,1),(17,'2020-12-13 19:33:15.080693','1','Camisa XL',2,'[]',35,1),(18,'2020-12-13 19:33:16.482208','1','Camisa XL',2,'[]',11,1),(19,'2020-12-13 19:33:54.397779','2','Camisa SM',2,'[]',11,1),(20,'2020-12-13 19:34:00.843149','3','Blusa SM',2,'[]',35,1),(21,'2020-12-16 17:43:10.955831','1','Clientes',1,'[{\"added\": {}}]',3,1),(22,'2020-12-16 18:04:27.535800','2','cgomez Christian Andres',1,'[{\"added\": {}}]',15,1),(23,'2020-12-16 18:04:40.523888','2','cgomez Christian Andres',2,'[]',15,1),(24,'2020-12-16 18:04:51.397391','2','cgomez Christian Andres',2,'[]',15,1),(25,'2020-12-16 18:09:35.006311','2','cgomez Christian Andres',2,'[{\"changed\": {\"fields\": [\"Last login\"]}}]',15,1),(26,'2020-12-16 18:12:36.236297','1','Clientes',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(27,'2020-12-16 18:14:39.027933','1','Clientes',3,'',3,1),(28,'2020-12-16 18:17:12.068061','1','admin Christian Andres',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',15,1),(29,'2020-12-17 01:48:13.116883','2','Clientes',2,'[]',3,1),(30,'2020-12-17 01:48:30.038591','30','Aoleas20 Angie Isabel',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',15,1),(31,'2020-12-17 01:48:34.821676','30','Aoleas20 Angie Isabel',2,'[]',15,1),(32,'2020-12-17 21:41:44.003319','3','admin',1,'[{\"added\": {}}]',3,1),(33,'2020-12-17 21:41:57.108010','1','admin Christian Andres',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',15,1),(34,'2020-12-17 21:42:13.143594','1','admin Christian Andres',2,'[]',15,1),(35,'2020-12-19 16:20:31.692042','2','Clientes',2,'[]',3,1),(36,'2020-12-19 16:20:51.103020','2','Clientes',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(37,'2020-12-19 22:50:39.967902','2','Clientes',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(29,'alquiler','alquiler'),(30,'alquiler','detalle_alquiler'),(32,'asignar_recursos','asig_recurso'),(33,'asignar_recursos','detalle_asig_maquina'),(34,'asignar_recursos','detalle_asig_recurso'),(3,'auth','group'),(2,'auth','permission'),(6,'categoria','categoria'),(7,'cliente','cliente'),(23,'compra','compra'),(24,'compra','detalle_compra'),(27,'confeccion','confeccion'),(28,'confeccion','detalle_confeccion'),(4,'contenttypes','contenttype'),(40,'DatabaseBackups','databasebackups'),(14,'delvoluciones_venta','devolucion'),(8,'empresa','empresa'),(9,'gasto','gasto'),(26,'inventario_material','inventario_material'),(25,'inventario_productos','inventario_producto'),(17,'maquina','maquina'),(16,'maquina','tipo_maquina'),(31,'material','material'),(10,'presentacion','presentacion'),(39,'produccion','detalle_perdidas_materiales'),(38,'produccion','detalle_perdidas_productos'),(37,'produccion','produccion'),(11,'producto','producto'),(35,'producto_base','producto_base'),(12,'proveedor','proveedor'),(18,'reparacion','detalle_reparacion'),(19,'reparacion','reparacion'),(5,'sessions','session'),(36,'sitioweb','sitioweb'),(13,'tipogasto','tipo_gasto'),(20,'transaccion','transaccion'),(15,'user','user'),(22,'venta','detalle_venta'),(21,'venta','venta');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-12-07 16:24:26.576695'),(2,'contenttypes','0002_remove_content_type_name','2020-12-07 16:24:28.948772'),(3,'auth','0001_initial','2020-12-07 16:24:30.881465'),(4,'auth','0002_alter_permission_name_max_length','2020-12-07 16:24:41.916042'),(5,'auth','0003_alter_user_email_max_length','2020-12-07 16:24:42.005493'),(6,'auth','0004_alter_user_username_opts','2020-12-07 16:24:42.114249'),(7,'auth','0005_alter_user_last_login_null','2020-12-07 16:24:42.191518'),(8,'auth','0006_require_contenttypes_0002','2020-12-07 16:24:42.264830'),(9,'auth','0007_alter_validators_add_error_messages','2020-12-07 16:24:42.317457'),(10,'auth','0008_alter_user_username_max_length','2020-12-07 16:24:42.368660'),(11,'auth','0009_alter_user_last_name_max_length','2020-12-07 16:24:42.455734'),(12,'auth','0010_alter_group_name_max_length','2020-12-07 16:24:42.759517'),(13,'auth','0011_update_proxy_permissions','2020-12-07 16:24:42.825759'),(14,'auth','0012_alter_user_first_name_max_length','2020-12-07 16:24:42.872286'),(15,'user','0001_initial','2020-12-07 16:24:44.266808'),(16,'admin','0001_initial','2020-12-07 16:24:55.357978'),(17,'admin','0002_logentry_remove_auto_add','2020-12-07 16:25:01.854247'),(18,'admin','0003_logentry_add_action_flag_choices','2020-12-07 16:25:02.122063'),(19,'cliente','0001_initial','2020-12-07 16:25:03.473924'),(20,'transaccion','0001_initial','2020-12-07 16:25:04.310915'),(21,'presentacion','0001_initial','2020-12-07 16:25:06.886816'),(22,'categoria','0001_initial','2020-12-07 16:25:07.391735'),(23,'producto_base','0001_initial','2020-12-07 16:25:08.041181'),(24,'producto','0001_initial','2020-12-07 16:25:14.128585'),(25,'material','0001_initial','2020-12-07 16:25:15.761054'),(26,'asignar_recursos','0001_initial','2020-12-07 16:25:18.451155'),(27,'produccion','0001_initial','2020-12-07 16:25:23.227258'),(28,'inventario_productos','0001_initial','2020-12-07 16:25:35.427557'),(29,'alquiler','0001_initial','2020-12-07 16:25:40.130245'),(30,'alquiler','0002_detalle_alquiler_inventario','2020-12-07 16:25:46.492547'),(31,'alquiler','0003_alquiler_transaccion','2020-12-07 16:25:48.219608'),(32,'maquina','0001_initial','2020-12-07 16:25:49.286646'),(33,'proveedor','0001_initial','2020-12-07 16:25:53.635515'),(34,'compra','0001_initial','2020-12-07 16:25:55.518523'),(35,'inventario_material','0001_initial','2020-12-07 16:26:01.821414'),(36,'asignar_recursos','0002_auto_20201207_1124','2020-12-07 16:26:15.064140'),(37,'asignar_recursos','0003_asig_recurso_user','2020-12-07 16:26:17.383798'),(38,'compra','0002_compra_user','2020-12-07 16:26:19.352068'),(39,'confeccion','0001_initial','2020-12-07 16:26:20.479927'),(40,'confeccion','0002_confeccion_transaccion','2020-12-07 16:26:28.302781'),(41,'venta','0001_initial','2020-12-07 16:26:29.600661'),(42,'delvoluciones_venta','0001_initial','2020-12-07 16:26:37.740087'),(43,'delvoluciones_venta','0002_devolucion_venta','2020-12-07 16:26:39.703856'),(44,'empresa','0001_initial','2020-12-07 16:26:40.933992'),(45,'tipogasto','0001_initial','2020-12-07 16:26:41.587676'),(46,'gasto','0001_initial','2020-12-07 16:26:42.478775'),(47,'reparacion','0001_initial','2020-12-07 16:26:50.094483'),(48,'reparacion','0002_auto_20201207_1124','2020-12-07 16:26:54.188755'),(49,'sessions','0001_initial','2020-12-07 16:26:56.157572'),(50,'sitioweb','0001_initial','2020-12-07 16:26:58.536219'),(51,'transaccion','0002_transaccion_user','2020-12-07 16:27:00.751435'),(52,'producto','0002_producto_imagen','2020-12-10 23:46:38.595585'),(53,'producto','0003_auto_20201212_1658','2020-12-12 21:58:25.527028'),(54,'produccion','0002_produccion_estado','2020-12-13 22:18:06.140822'),(55,'user','0002_auto_20201216_1822','2020-12-16 23:23:37.696882'),(56,'venta','0002_auto_20201217_1430','2020-12-17 19:30:13.205167'),(57,'user','0003_user_tipo','2020-12-17 22:06:19.320155'),(58,'alquiler','0004_auto_20201220_1851','2020-12-20 23:51:51.398709'),(59,'DatabaseBackups','0001_initial','2020-12-21 01:39:12.035857'),(60,'confeccion','0003_auto_20201220_2038','2020-12-21 01:39:18.514826'),(61,'reparacion','0003_auto_20201220_2038','2020-12-21 01:39:18.608454');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('jy9c9vzrqgtb1ag3f7fcb493bo2fai08','.eJxVjMsOwiAUBf-FtSFSkEtduvcbCNyHVA0kpV0Z_12bdKHbMzPnpWJalxLXznOcSJ2VUYffLSd8cN0A3VO9NY2tLvOU9abonXZ9bcTPy-7-HZTUy7e2HLIPBnEQcCdAAkyAgwcCDiyUDVk8omFjaRQxAsSS84jkxLFH9f4AEM85xQ:1kr1HX:nqg2DoY5O4cYq0S1axRTK_craSgNgmb4jPXNY_1dMsM','2021-01-03 16:10:03.285464'),('ogiopibjk1oegnw4karpu77f7pr0mz55','.eJxVjMsOwiAUBf-FtSFSkEtduvcbCNyHVA0kpV0Z_12bdKHbMzPnpWJalxLXznOcSJ2VUYffLSd8cN0A3VO9NY2tLvOU9abonXZ9bcTPy-7-HZTUy7e2HLIPBnEQcCdAAkyAgwcCDiyUDVk8omFjaRQxAsSS84jkxLFH9f4AEM85xQ:1kqewn:OfR3pVTRlzyu9fvY0st5MyTwM40wTAo6zclA3Sn0pvE','2021-01-02 16:19:09.540237'),('rqsr7vnd00seybsrtzb53ut13osncb11','.eJxVjMsOwiAUBf-FtSFSkEtduvcbCNyHVA0kpV0Z_12bdKHbMzPnpWJalxLXznOcSJ2VUYffLSd8cN0A3VO9NY2tLvOU9abonXZ9bcTPy-7-HZTUy7e2HLIPBnEQcCdAAkyAgwcCDiyUDVk8omFjaRQxAsSS84jkxLFH9f4AEM85xQ:1kpJ9w:UX7Qa2zNL3wQCu1dpDSPifBhhktNeO_0XPjeZ5os82Y','2020-12-29 22:51:08.553160'),('sgdtkm8cvwlrpyrz4iqpwss4fd7pdfcv','.eJxVjMsOwiAUBf-FtSFSkEtduvcbCNyHVA0kpV0Z_12bdKHbMzPnpWJalxLXznOcSJ2VUYffLSd8cN0A3VO9NY2tLvOU9abonXZ9bcTPy-7-HZTUy7e2HLIPBnEQcCdAAkyAgwcCDiyUDVk8omFjaRQxAsSS84jkxLFH9f4AEM85xQ:1kpJEE:yeNZwqE-YmsPFe0ZeM56_uR541Fzlq5_h9xbbayaf90','2020-12-29 22:55:34.709174'),('sktfjhsxzetifodtfhd0bvarx96mvzbi','.eJxVjMsOwiAUBf-FtSFSkEtduvcbCNyHVA0kpV0Z_12bdKHbMzPnpWJalxLXznOcSJ2VUYffLSd8cN0A3VO9NY2tLvOU9abonXZ9bcTPy-7-HZTUy7e2HLIPBnEQcCdAAkyAgwcCDiyUDVk8omFjaRQxAsSS84jkxLFH9f4AEM85xQ:1kpJLo:engGv1aHUNSdNadm9us5cAUGXHy1giftWIO1ZjLoMdw','2020-12-29 23:03:24.422630'),('tn9yfjne44yws07j7r1sio96q5fr55dw','.eJxVjMsOwiAUBf-FtSFSkEtduvcbCNyHVA0kpV0Z_12bdKHbMzPnpWJalxLXznOcSJ2VUYffLSd8cN0A3VO9NY2tLvOU9abonXZ9bcTPy-7-HZTUy7e2HLIPBnEQcCdAAkyAgwcCDiyUDVk8omFjaRQxAsSS84jkxLFH9f4AEM85xQ:1kpJBJ:0VhgLhr5DeTADd1ziRi3Uz20N6qpXGddZjFQgVOt_9M','2020-12-29 22:52:33.892939'),('u63afw2hevm0xeq0cohh71xie65krh68','.eJxVjMsOwiAUBf-FtSFSkEtduvcbCNyHVA0kpV0Z_12bdKHbMzPnpWJalxLXznOcSJ2VUYffLSd8cN0A3VO9NY2tLvOU9abonXZ9bcTPy-7-HZTUy7e2HLIPBnEQcCdAAkyAgwcCDiyUDVk8omFjaRQxAsSS84jkxLFH9f4AEM85xQ:1kmJYz:63m8SMC9GCxZjmx9jtrDtqilqBz6Jp92PlxpzhA5VfQ','2020-12-21 16:40:37.816461'),('xtd4igg1cr9q1uxs78csofynzz8w5nkq','.eJxVjMsOwiAUBf-FtSFSkEtduvcbCNyHVA0kpV0Z_12bdKHbMzPnpWJalxLXznOcSJ2VUYffLSd8cN0A3VO9NY2tLvOU9abonXZ9bcTPy-7-HZTUy7e2HLIPBnEQcCdAAkyAgwcCDiyUDVk8omFjaRQxAsSS84jkxLFH9f4AEM85xQ:1kpJAO:NcGl_qESNWjwBGZiRxUwO2eQ9CZZvWwK6EEI-qxQxeE','2020-12-29 22:51:36.424621');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empresa`
--

DROP TABLE IF EXISTS `empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empresa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  `ciudad` varchar(25) NOT NULL,
  `ruc` varchar(13) NOT NULL,
  `direccion` varchar(25) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `iva` int DEFAULT NULL,
  `indice` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ruc` (`ruc`),
  UNIQUE KEY `telefono` (`telefono`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresa`
--

LOCK TABLES `empresa` WRITE;
/*!40000 ALTER TABLE `empresa` DISABLE KEYS */;
INSERT INTO `empresa` VALUES (1,'Confecciones IJEI','Milagro','0978765652001','Milagro','0994695413','gmez@gmail.com',12,25);
/*!40000 ALTER TABLE `empresa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gasto`
--

DROP TABLE IF EXISTS `gasto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gasto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_pago` date NOT NULL,
  `valor` decimal(9,2) NOT NULL,
  `detalle` varchar(50) NOT NULL,
  `empresa_id` int NOT NULL,
  `tipo_gasto_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gasto_empresa_id_f4c127b0_fk_empresa_id` (`empresa_id`),
  KEY `gasto_tipo_gasto_id_25d252dd_fk_tipo_gasto_id` (`tipo_gasto_id`),
  CONSTRAINT `gasto_empresa_id_f4c127b0_fk_empresa_id` FOREIGN KEY (`empresa_id`) REFERENCES `empresa` (`id`),
  CONSTRAINT `gasto_tipo_gasto_id_25d252dd_fk_tipo_gasto_id` FOREIGN KEY (`tipo_gasto_id`) REFERENCES `tipo_gasto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gasto`
--

LOCK TABLES `gasto` WRITE;
/*!40000 ALTER TABLE `gasto` DISABLE KEYS */;
/*!40000 ALTER TABLE `gasto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_material`
--

DROP TABLE IF EXISTS `inventario_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_material` (
  `id` int NOT NULL AUTO_INCREMENT,
  `estado` int NOT NULL,
  `compra_id` int NOT NULL,
  `material_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventario_material_compra_id_cb8576f2_fk_compra_id` (`compra_id`),
  KEY `inventario_material_material_id_3954fe62_fk_material_id` (`material_id`),
  CONSTRAINT `inventario_material_compra_id_cb8576f2_fk_compra_id` FOREIGN KEY (`compra_id`) REFERENCES `compra` (`id`),
  CONSTRAINT `inventario_material_material_id_3954fe62_fk_material_id` FOREIGN KEY (`material_id`) REFERENCES `material` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_material`
--

LOCK TABLES `inventario_material` WRITE;
/*!40000 ALTER TABLE `inventario_material` DISABLE KEYS */;
INSERT INTO `inventario_material` VALUES (1,1,1,1),(2,1,1,1),(3,1,1,1),(4,1,1,1),(5,1,1,1),(6,1,1,1),(7,1,1,1),(8,1,1,1),(9,0,1,1),(10,0,1,1);
/*!40000 ALTER TABLE `inventario_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_producto`
--

DROP TABLE IF EXISTS `inventario_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `estado` int NOT NULL,
  `produccion_id` int NOT NULL,
  `producto_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventario_producto_produccion_id_260e35c0_fk_produccion_id` (`produccion_id`),
  KEY `inventario_producto_producto_id_d2962083_fk_producto_id` (`producto_id`),
  CONSTRAINT `inventario_producto_produccion_id_260e35c0_fk_produccion_id` FOREIGN KEY (`produccion_id`) REFERENCES `produccion` (`id`),
  CONSTRAINT `inventario_producto_producto_id_d2962083_fk_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=485 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_producto`
--

LOCK TABLES `inventario_producto` WRITE;
/*!40000 ALTER TABLE `inventario_producto` DISABLE KEYS */;
INSERT INTO `inventario_producto` VALUES (1,0,1,1),(300,0,7,2),(301,0,7,2),(302,0,7,2),(303,0,7,2),(304,0,7,2),(305,0,7,2),(306,0,7,2),(307,0,7,2),(308,0,7,2),(309,0,7,2),(310,0,7,2),(311,0,7,2),(312,0,7,2),(313,0,7,2),(314,0,7,2),(315,0,7,2),(316,0,7,2),(317,0,7,2),(318,1,7,2),(319,1,7,2),(320,1,7,2),(321,1,7,2),(322,1,7,2),(323,1,7,2),(324,1,7,2),(325,1,7,2),(326,1,7,2),(327,1,7,2),(328,1,7,2),(329,1,7,2),(330,1,7,2),(331,1,7,2),(332,1,7,2),(333,1,7,2),(334,1,7,2),(335,1,7,2),(336,1,7,2),(337,1,7,2),(338,1,7,2),(339,1,7,2),(340,1,7,2),(341,1,7,2),(342,1,7,2),(343,1,7,2),(344,1,7,2),(345,1,7,2),(346,1,7,2),(347,1,7,2),(348,1,7,2),(349,1,7,2),(350,0,7,1),(351,0,7,1),(352,0,7,1),(353,0,7,1),(354,0,7,1),(355,0,7,1),(356,0,7,1),(357,0,7,1),(358,0,7,1),(359,0,7,1),(360,0,7,1),(361,1,7,1),(362,1,7,1),(363,1,7,1),(364,1,7,1),(365,1,7,1),(366,1,7,1),(367,1,7,1),(368,1,7,1),(369,1,7,1),(370,1,7,1),(371,1,7,1),(372,1,7,1),(373,1,7,1),(374,1,7,1),(375,1,7,1),(376,1,7,1),(377,1,7,1),(378,1,7,1),(379,1,7,1),(380,1,7,1),(381,1,7,1),(382,1,7,1),(383,1,7,1),(384,1,7,1),(385,1,7,1),(386,1,7,1),(387,1,7,1),(388,1,7,1),(389,1,7,1),(390,1,7,1),(391,1,7,1),(392,1,7,1),(393,1,7,1),(394,1,7,1),(395,1,7,1),(396,1,7,1),(397,1,7,1),(398,1,7,1),(399,1,7,1),(400,1,7,1),(401,1,7,1),(402,1,7,1),(403,1,7,1),(404,1,7,1),(405,1,7,1),(406,1,7,1),(407,1,7,1),(408,1,7,1),(409,1,7,1),(410,0,7,3),(411,0,7,3),(412,0,7,3),(413,0,7,3),(414,0,7,3),(415,0,7,3),(416,0,7,3),(417,0,7,3),(418,0,7,3),(419,0,7,3),(420,0,7,3),(421,0,7,3),(422,0,7,3),(423,0,7,3),(424,0,7,3),(425,0,7,3),(426,0,7,3),(427,0,7,3),(428,0,7,3),(429,0,7,3),(430,0,7,3),(431,0,7,3),(432,0,7,3),(433,0,7,3),(434,1,7,3),(435,1,7,3),(436,1,7,3),(437,1,7,3),(438,1,7,3),(439,1,7,3),(440,1,7,3),(441,1,7,3),(442,1,7,3),(443,1,7,3),(444,1,7,3),(445,1,7,3),(446,1,7,3),(447,1,7,3),(448,1,7,3),(449,1,7,3),(450,1,7,3),(451,1,7,3),(452,1,7,3),(453,1,7,3),(454,1,7,3),(455,1,7,3),(456,1,7,3),(457,1,7,3),(458,1,7,3),(459,1,7,3),(460,1,7,3),(461,1,7,3),(462,1,7,3),(463,1,7,3),(464,1,7,3),(465,1,7,3),(466,1,7,3),(467,1,7,3),(468,1,7,3),(469,1,7,3),(470,1,7,3),(471,1,7,3),(472,1,7,3),(473,1,7,3),(474,1,7,3),(475,1,7,3),(476,1,7,3),(477,1,7,3),(478,1,7,3),(479,1,7,3),(480,1,7,3),(481,1,7,3),(482,1,7,3),(483,1,7,3),(484,1,7,3);
/*!40000 ALTER TABLE `inventario_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maquina`
--

DROP TABLE IF EXISTS `maquina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maquina` (
  `id` int NOT NULL AUTO_INCREMENT,
  `estado` int NOT NULL,
  `serie` varchar(50) NOT NULL,
  `tipo_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `maquina_tipo_id_09a0d527_fk_Tipo_maquina_id` (`tipo_id`),
  CONSTRAINT `maquina_tipo_id_09a0d527_fk_Tipo_maquina_id` FOREIGN KEY (`tipo_id`) REFERENCES `tipo_maquina` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maquina`
--

LOCK TABLES `maquina` WRITE;
/*!40000 ALTER TABLE `maquina` DISABLE KEYS */;
INSERT INTO `maquina` VALUES (1,0,'45212154',1);
/*!40000 ALTER TABLE `maquina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `material`
--

DROP TABLE IF EXISTS `material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `material` (
  `id` int NOT NULL AUTO_INCREMENT,
  `p_compra` decimal(9,2) DEFAULT NULL,
  `producto_base_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `material_producto_base_id_8ea29333_fk_producto_base_id` (`producto_base_id`),
  CONSTRAINT `material_producto_base_id_8ea29333_fk_producto_base_id` FOREIGN KEY (`producto_base_id`) REFERENCES `producto_base` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `material`
--

LOCK TABLES `material` WRITE;
/*!40000 ALTER TABLE `material` DISABLE KEYS */;
INSERT INTO `material` VALUES (1,125.00,4);
/*!40000 ALTER TABLE `material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presentacion`
--

DROP TABLE IF EXISTS `presentacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presentacion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `abreviatura` varchar(10) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presentacion`
--

LOCK TABLES `presentacion` WRITE;
/*!40000 ALTER TABLE `presentacion` DISABLE KEYS */;
INSERT INTO `presentacion` VALUES (1,'Unidad','ud','Unidad de producto'),(2,'Rollo mediano','rmd','Rollo mediano de producto');
/*!40000 ALTER TABLE `presentacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccion`
--

DROP TABLE IF EXISTS `produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_ingreso` date NOT NULL,
  `novedades` varchar(100) NOT NULL,
  `asignacion_id` int NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `produccion_asignacion_id_cc01393b_fk_asig_recurso_id` (`asignacion_id`),
  CONSTRAINT `produccion_asignacion_id_cc01393b_fk_asig_recurso_id` FOREIGN KEY (`asignacion_id`) REFERENCES `asig_recurso` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion`
--

LOCK TABLES `produccion` WRITE;
/*!40000 ALTER TABLE `produccion` DISABLE KEYS */;
INSERT INTO `produccion` VALUES (1,'2020-12-10','Sin novedad',1,0),(6,'2020-12-13','Perdidas de productos materiales',3,1),(7,'2020-12-13','Sin novedad',3,0);
/*!40000 ALTER TABLE `produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pvp` decimal(9,2) DEFAULT NULL,
  `pvp_alq` decimal(9,2) DEFAULT NULL,
  `pvp_confec` decimal(9,2) DEFAULT NULL,
  `producto_base_id` int NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `producto_producto_base_id_0f2b6bb5_fk_producto_base_id` (`producto_base_id`),
  CONSTRAINT `producto_producto_base_id_0f2b6bb5_fk_producto_base_id` FOREIGN KEY (`producto_base_id`) REFERENCES `producto_base` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,10.00,5.00,7.00,1,'/producto/imagen/item-3.png'),(2,12.00,8.00,5.00,2,'producto/imagen/item-4.png'),(3,15.00,9.00,12.00,3,'/producto/imagen/item-5.png'),(4,15.05,5.00,10.00,7,'producto/imagen/lookbook-men.png');
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_base`
--

DROP TABLE IF EXISTS `producto_base`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_base` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `stock` int NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `categoria_id` int NOT NULL,
  `presentacion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `producto_base_categoria_id_87d8a24f_fk_categoria_id` (`categoria_id`),
  KEY `producto_base_presentacion_id_50b14b48_fk_presentacion_id` (`presentacion_id`),
  CONSTRAINT `producto_base_categoria_id_87d8a24f_fk_categoria_id` FOREIGN KEY (`categoria_id`) REFERENCES `categoria` (`id`),
  CONSTRAINT `producto_base_presentacion_id_50b14b48_fk_presentacion_id` FOREIGN KEY (`presentacion_id`) REFERENCES `presentacion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_base`
--

LOCK TABLES `producto_base` WRITE;
/*!40000 ALTER TABLE `producto_base` DISABLE KEYS */;
INSERT INTO `producto_base` VALUES (1,'Camisa XL',49,'Camisa XL 100% Algodon',1,1),(2,'Camisa SM',32,'Camisa SM',1,1),(3,'Blusa SM',51,'Blusa SM de algodon',2,1),(4,'Tela de seda blanca',8,'Tela de seda blanca para producción',3,2),(5,'Pantalón S',0,'Pantalón',4,1),(6,'Pantalón L',0,'Pantalón L',4,1),(7,'Pantalón SM',0,'Pantalón SM',4,1);
/*!40000 ALTER TABLE `producto_base` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `tipo` int NOT NULL,
  `num_doc` varchar(13) NOT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `telefono` varchar(10) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `num_doc` (`num_doc`),
  UNIQUE KEY `telefono` (`telefono`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'Textiles del Ecuador',0,'0919995373','textilesec@gmail.com','0959447885','MIlagro','2020-12-12');
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reparacion`
--

DROP TABLE IF EXISTS `reparacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reparacion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_ingreso` date DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `estado` int NOT NULL,
  `transaccion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reparacion_transaccion_id_a159f94f_fk_transaccion_id` (`transaccion_id`),
  CONSTRAINT `reparacion_transaccion_id_a159f94f_fk_transaccion_id` FOREIGN KEY (`transaccion_id`) REFERENCES `transaccion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reparacion`
--

LOCK TABLES `reparacion` WRITE;
/*!40000 ALTER TABLE `reparacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `reparacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sitio`
--

DROP TABLE IF EXISTS `sitio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sitio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(50) NOT NULL,
  `mision` varchar(500) NOT NULL,
  `vision` varchar(500) NOT NULL,
  `mapa` varchar(10000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sitio`
--

LOCK TABLES `sitio` WRITE;
/*!40000 ALTER TABLE `sitio` DISABLE KEYS */;
INSERT INTO `sitio` VALUES (1,'Confecciones \"IJEI\"','Nuestra Mision es larga','Nuestra Vision tambien','<iframe src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d31896.41200310224!2d-79.61713942433664!3d-2.1339125643377264!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x902d47b9b02facc9%3A0xc4f916f01d2842fe!2sCASA%20GUADUA!5e0!3m2!1ses!2sec!4v1607001784903!5m2!1ses!2sec\" width=\"600\" height=\"450\" frameborder=\"0\" style=\"border:0;\" allowfullscreen=\"\" aria-hidden=\"false\" tabindex=\"0\"></iframe>');
/*!40000 ALTER TABLE `sitio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_gasto`
--

DROP TABLE IF EXISTS `tipo_gasto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_gasto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_gasto`
--

LOCK TABLES `tipo_gasto` WRITE;
/*!40000 ALTER TABLE `tipo_gasto` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipo_gasto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_maquina`
--

DROP TABLE IF EXISTS `tipo_maquina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_maquina` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_maquina`
--

LOCK TABLES `tipo_maquina` WRITE;
/*!40000 ALTER TABLE `tipo_maquina` DISABLE KEYS */;
INSERT INTO `tipo_maquina` VALUES (1,'Maquina de Coser H124','Maquina de Coser H124 2017');
/*!40000 ALTER TABLE `tipo_maquina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaccion`
--

DROP TABLE IF EXISTS `transaccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` int NOT NULL,
  `fecha_trans` date NOT NULL,
  `subtotal` decimal(9,2) NOT NULL,
  `iva` decimal(9,2) NOT NULL,
  `total` decimal(9,2) NOT NULL,
  `cliente_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transaccion_cliente_id_c37454fc_fk_cliente_id` (`cliente_id`),
  KEY `transaccion_user_id_7f5b7161_fk_usuario_id` (`user_id`),
  CONSTRAINT `transaccion_cliente_id_c37454fc_fk_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`),
  CONSTRAINT `transaccion_user_id_7f5b7161_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaccion`
--

LOCK TABLES `transaccion` WRITE;
/*!40000 ALTER TABLE `transaccion` DISABLE KEYS */;
INSERT INTO `transaccion` VALUES (1,0,'2020-12-10',10.00,1.20,11.20,1,1),(2,0,'2020-12-13',74.00,8.88,82.88,1,1),(3,0,'2020-12-13',161.00,19.32,180.32,1,1),(4,0,'2020-12-16',35.00,4.20,39.20,1,1),(5,0,'2020-12-16',35.00,4.20,39.20,1,1),(6,0,'2020-12-16',35.00,4.20,39.20,1,30),(7,0,'2020-12-17',81.00,9.72,90.72,1,1),(8,0,'2020-12-19',12.00,1.44,13.44,41,36),(9,0,'2020-12-19',30.00,3.60,33.60,41,36),(10,0,'2020-12-19',27.00,3.24,30.24,41,36),(11,0,'2020-12-19',27.00,3.24,30.24,41,36),(12,0,'2020-12-19',27.00,3.24,30.24,41,36),(13,0,'2020-12-19',27.00,3.24,30.24,41,36),(14,0,'2020-12-19',27.00,3.24,30.24,41,36),(15,0,'2020-12-19',27.00,3.24,30.24,41,36),(16,0,'2020-12-19',27.00,3.24,30.24,41,36),(17,0,'2020-12-19',27.00,3.24,30.24,41,36),(18,0,'2020-12-19',27.00,3.24,30.24,41,36),(19,0,'2020-12-19',27.00,3.24,30.24,41,36),(20,0,'2020-12-19',27.00,3.24,30.24,41,36);
/*!40000 ALTER TABLE `transaccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `cedula` varchar(10) NOT NULL,
  `celular` varchar(10) DEFAULT NULL,
  `telefono` varchar(9) DEFAULT NULL,
  `direccion` varchar(500) DEFAULT NULL,
  `sexo` int NOT NULL,
  `estado` int NOT NULL,
  `tipo` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `cedula` (`cedula`),
  UNIQUE KEY `telefono` (`telefono`),
  UNIQUE KEY `celular` (`celular`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'pbkdf2_sha256$216000$EiaRGVoDNTNu$NSbKeonb7yp/m+EznFW9G2K/swOF9nFmEQUyr0Waxsk=','2020-12-20 16:10:03.098436',1,'admin','Christian Andres','Gomez Moran','chrisstianandres@gmail.com',1,1,'2020-12-07 16:39:16.000000','','0604551580','0994695413','032954259','Milagro',1,1,1),(2,'pbkdf2_sha256$216000$69HM2vh2x0s2$giXsrZMuNrVr8dJy6FZmH/r2NaIuAdKRqQvv+/FhoBM=','2020-12-16 18:09:32.000000',0,'cgomez','Christian Andres','Gomez Moran','chrisstianandres@gmail.com',0,1,'2020-12-16 17:42:48.000000','','0910473248','0994695414','099454788','Milagro',1,1,1),(30,'pbkdf2_sha256$216000$94nZDqlnPa2f$tg2NY2k5sZgYupEOAYJsKpRAHQ5OJSxlVNrELgyLxeM=','2020-12-17 01:49:04.909881',0,'Aoleas20','Angie Isabel','Gomez Moran','chrisstianandres@gmail.com',0,1,'2020-12-17 01:14:12.000000','','1204222895','0994675845','042710122','Milagro',0,1,1),(36,'pbkdf2_sha256$216000$uwzSCX09d8ca$P0wMo84GPxSQRvbl7LDYsDq1zvuUVJeKQP2C5eduoLU=','2020-12-19 16:13:04.622027',0,'dayana124','Dayanna Lisbeth','Ochoa Ramirez','dayana15@gmail.com',0,1,'2020-12-19 16:01:24.721906','','1102294509','0994675843','097868644',NULL,0,1,0);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario_groups`
--

DROP TABLE IF EXISTS `usuario_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_groups_user_id_group_id_a743d7e7_uniq` (`user_id`,`group_id`),
  KEY `usuario_groups_group_id_c67c8651_fk_auth_group_id` (`group_id`),
  CONSTRAINT `usuario_groups_group_id_c67c8651_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `usuario_groups_user_id_bf125d45_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_groups`
--

LOCK TABLES `usuario_groups` WRITE;
/*!40000 ALTER TABLE `usuario_groups` DISABLE KEYS */;
INSERT INTO `usuario_groups` VALUES (4,1,3),(3,30,2),(6,36,2);
/*!40000 ALTER TABLE `usuario_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario_user_permissions`
--

DROP TABLE IF EXISTS `usuario_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_user_permissions_user_id_permission_id_30490d1f_uniq` (`user_id`,`permission_id`),
  KEY `usuario_user_permiss_permission_id_a8893ce7_fk_auth_perm` (`permission_id`),
  CONSTRAINT `usuario_user_permiss_permission_id_a8893ce7_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `usuario_user_permissions_user_id_96a81eab_fk_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_user_permissions`
--

LOCK TABLES `usuario_user_permissions` WRITE;
/*!40000 ALTER TABLE `usuario_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `estado` int NOT NULL,
  `transaccion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `venta_transaccion_id_3f45921d_fk_transaccion_id` (`transaccion_id`),
  CONSTRAINT `venta_transaccion_id_3f45921d_fk_transaccion_id` FOREIGN KEY (`transaccion_id`) REFERENCES `transaccion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (1,1,1),(2,1,1),(3,0,2),(4,1,3),(5,1,4),(6,1,5),(7,1,6),(8,2,7),(9,1,8),(10,1,9),(11,1,10),(12,1,11),(13,1,12),(14,1,13),(15,1,14),(16,1,15),(17,1,16),(18,1,17),(19,1,18),(20,1,19),(21,1,20);
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-21 13:30:37
