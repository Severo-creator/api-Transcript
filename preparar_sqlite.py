import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.sqlite3"


SCHEMA = """
CREATE TABLE IF NOT EXISTS FORNECEDOR (
    EAN varchar(255) PRIMARY KEY,
    NCM varchar(255),
    SKU_f varchar(255),
    descricao_f varchar(255),
    industria varchar(255),
    marca varchar(255),
    preco_custo_embalagem_f real,
    preco_venda_embalagem_f real,
    embalagem_f integer,
    preco_unitario_f real,
    estoque_f integer
);

CREATE TABLE IF NOT EXISTS CATEGORIA (
    categoria integer PRIMARY KEY,
    desc_categoria varchar(255),
    mark_categoria real,
    prioridade varchar(255)
);

CREATE TABLE IF NOT EXISTS NCM (
    NCM varchar(255) PRIMARY KEY,
    descricao_n varchar(255),
    tributo_n real
);

CREATE TABLE IF NOT EXISTS BASE (
    EAN varchar(255) PRIMARY KEY,
    NCM varchar(255),
    SKU_f varchar(255),
    descricao_f varchar(255),
    categoria integer,
    industria varchar(255),
    marca varchar(255),
    preco_custo_embalagem_f real,
    preco_venda_embalagem_f real,
    embalagem_f integer,
    preco_unitario_f real,
    estoque_f integer
);

CREATE TABLE IF NOT EXISTS REDE (
    EAN varchar(255) PRIMARY KEY,
    SKU_r varchar(255),
    descricao_r varchar(255),
    preco_venda_r real,
    preco_ultima_compra real,
    contrato_r real,
    mark_r real,
    venda_diaria_r real
);

CREATE TABLE IF NOT EXISTS OPERA (
    categoria integer PRIMARY KEY,
    log_opera real,
    Mark_opera real,
    tributo_opera real,
    promotor_opera real,
    total_opera real
);

CREATE TABLE IF NOT EXISTS OFERTA (
    ID integer PRIMARY KEY AUTOINCREMENT,
    EAN varchar(255) UNIQUE,
    sku_f varchar(255),
    sku_r varchar(255),
    descricao_r varchar(255),
    preco_embalagem_oferta real,
    preco_unitario_oferta real,
    embalagem_f integer,
    data_tab datetime
);

CREATE TABLE IF NOT EXISTS PEDIDO (
    num_ped integer PRIMARY KEY AUTOINCREMENT,
    data_ped datetime,
    EAN varchar(255),
    sku_r varchar(255),
    sku_f varchar(255),
    descricao_r varchar(255),
    preco_tab real,
    qnt_ped integer,
    subtotal_ped real,
    valortotal_ped real,
    qntt_ped integer
);
"""


def criar_tabelas():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)
        conn.commit()


if __name__ == "__main__":
    criar_tabelas()
    print(f"Banco SQLite preparado em: {DB_PATH}")
