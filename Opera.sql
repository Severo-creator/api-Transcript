CREATE TABLE `FORNECEDOR` (
  `EAN` varchar(255) PRIMARY KEY,
  `NCM` varchar(255),
  `SKU_f` varchar(255),
  `descricao_f` varchar(255),
  `industria` varchar(255),
  `marca` varchar(255),
  `preco_custo_embalagem_f` float,
  `preco_venda_embalagem_f` float,
  `embalagem_f` integer,
  `preco_unitario_f` float,
  `estoque_f` integer
);

CREATE TABLE `CATEGORIA` (
  `categoria` int PRIMARY KEY,
  `desc_categoria` varchar(255),
  `mark_categoria` float,
  `prioridade` varchar(255)
);

CREATE TABLE `REDE` (
  `EAN` varchar(255) PRIMARY KEY,
  `SKU_r` varchar(255),
  `descricao_r` varchar(255),
  `preco_venda_r` float,
  `preco_ultima_compra` float,
  `contrato_r` float COMMENT 'valores % de vantagens do Fornecedor',
  `mark_r` float,
  `venda_diaria_r` float
);

CREATE TABLE `OPERA` (
  `categoria` int PRIMARY KEY,
  `log_opera` float,
  `Mark_opera` float,
  `tributo_opera` float,
  `promotor_opera` float,
  `total_opera` float
);

CREATE TABLE `OFERTA` (
  `ID` varchar(255) PRIMARY KEY,
  `EAN` varchar(255) UNIQUE,
  `sku_f` varchar(255),
  `sku_r` varchar(255),
  `descricao_r` varchar(255),
  `preco_embalagem_oferta` float,
  `preco_unitario_oferta` float,
  `embalagem_f` integer,
  `data_tab` datetime
);

CREATE TABLE `PEDIDO` (
  `num_ped` integer PRIMARY KEY AUTO_INCREMENT,
  `data_ped` datetime,
  `EAN` varchar(255),
  `sku_r` varchar(255),
  `sku_f` varchar(255),
  `descricao_r` varchar(255),
  `preco_tab` float,
  `qnt_ped` integer,
  `subtotal_ped` float,
  `valortotal_ped` float,
  `qntt_ped` integer
);

CREATE TABLE `BASE` (
  `ID` integer PRIMARY KEY AUTO_INCREMENT,
  `EAN` varchar(255) UNIQUE,
  `NCM` varchar(255),
  `SKU_f` varchar(255),
  `descricao_f` varchar(255),
  `categoria` int,
  `industria` varchar(255),
  `marca` varchar(255),
  `preco_custo_embalagem_f` float,
  `preco_venda_embalagem_f` float,
  `embalagem_f` integer,
  `preco_unitario_f` float,
  `estoque_f` integer
);

ALTER TABLE `REDE` ADD FOREIGN KEY (`EAN`) REFERENCES `OFERTA` (`EAN`);

ALTER TABLE `OPERA` ADD FOREIGN KEY (`categoria`) REFERENCES `CATEGORIA` (`categoria`);

ALTER TABLE `OFERTA` ADD FOREIGN KEY (`EAN`) REFERENCES `BASE` (`EAN`);

ALTER TABLE `PEDIDO` ADD FOREIGN KEY (`EAN`) REFERENCES `REDE` (`EAN`);

ALTER TABLE `BASE` ADD FOREIGN KEY (`EAN`) REFERENCES `FORNECEDOR` (`EAN`);

ALTER TABLE `BASE` ADD FOREIGN KEY (`categoria`) REFERENCES `CATEGORIA` (`categoria`);
