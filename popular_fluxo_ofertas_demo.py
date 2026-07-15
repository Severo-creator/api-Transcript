import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.sqlite3"


PRODUTOS = [
    {
        "ean": "7899706100001",
        "ncm": "3305.90.00",
        "sku_f": "SKU-F-001",
        "sku_r": "SKU-R-001",
        "descricao": "Shampoo Hidratante 12x350ml",
        "categoria": 1001,
        "industria": "Industria Alfa",
        "marca": "Marca Solaris",
        "custo": 84.00,
        "venda": 108.00,
        "embalagem": 12,
        "estoque": 120,
        "preco_rede": 128.00,
        "ultima_compra": 104.00,
        "contrato": 4.0,
    },
    {
        "ean": "7899706100002",
        "ncm": "3401.30.00",
        "sku_f": "SKU-F-002",
        "sku_r": "SKU-R-002",
        "descricao": "Sabonete Liquido 6x500ml",
        "categoria": 1001,
        "industria": "Industria Alfa",
        "marca": "Marca Solaris",
        "custo": 42.00,
        "venda": 59.40,
        "embalagem": 6,
        "estoque": 80,
        "preco_rede": 72.00,
        "ultima_compra": 55.00,
        "contrato": 3.5,
    },
    {
        "ean": "7899706100003",
        "ncm": "1905.90.90",
        "sku_f": "SKU-F-003",
        "sku_r": "SKU-R-003",
        "descricao": "Biscoito Recheado 24x90g",
        "categoria": 1002,
        "industria": "Alimentos Beta",
        "marca": "Marca Saboria",
        "custo": 36.00,
        "venda": 52.80,
        "embalagem": 24,
        "estoque": 240,
        "preco_rede": 60.00,
        "ultima_compra": 49.00,
        "contrato": 2.0,
    },
    {
        "ean": "7899706100004",
        "ncm": "2202.10.00",
        "sku_f": "SKU-F-004",
        "sku_r": "SKU-R-004",
        "descricao": "Refrigerante Cola 12x2L",
        "categoria": 1003,
        "industria": "Bebidas Delta",
        "marca": "Marca Fonte",
        "custo": 72.00,
        "venda": 96.00,
        "embalagem": 12,
        "estoque": 60,
        "preco_rede": 117.00,
        "ultima_compra": 91.00,
        "contrato": 2.8,
    },
    {
        "ean": "7899706100005",
        "ncm": "3402.20.00",
        "sku_f": "SKU-F-005",
        "sku_r": "SKU-R-005",
        "descricao": "Detergente Neutro 24x500ml",
        "categoria": 1004,
        "industria": "Limpeza Gama",
        "marca": "Marca Brilho",
        "custo": 48.00,
        "venda": 69.60,
        "embalagem": 24,
        "estoque": 180,
        "preco_rede": 82.00,
        "ultima_compra": 66.00,
        "contrato": 3.0,
    },
]


def popular_fluxo():
    with sqlite3.connect(DB_PATH) as conn:
        for produto in PRODUTOS:
            preco_unitario = produto["venda"] / produto["embalagem"]

            conn.execute(
                """
                INSERT INTO FORNECEDOR (
                    EAN, NCM, SKU_f, descricao_f, industria, marca,
                    preco_custo_embalagem_f, preco_venda_embalagem_f,
                    embalagem_f, preco_unitario_f, estoque_f
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(EAN) DO UPDATE SET
                    NCM = excluded.NCM,
                    SKU_f = excluded.SKU_f,
                    descricao_f = excluded.descricao_f,
                    industria = excluded.industria,
                    marca = excluded.marca,
                    preco_custo_embalagem_f = excluded.preco_custo_embalagem_f,
                    preco_venda_embalagem_f = excluded.preco_venda_embalagem_f,
                    embalagem_f = excluded.embalagem_f,
                    preco_unitario_f = excluded.preco_unitario_f,
                    estoque_f = excluded.estoque_f
                """,
                (
                    produto["ean"],
                    produto["ncm"],
                    produto["sku_f"],
                    produto["descricao"],
                    produto["industria"],
                    produto["marca"],
                    produto["custo"],
                    produto["venda"],
                    produto["embalagem"],
                    preco_unitario,
                    produto["estoque"],
                ),
            )

            conn.execute(
                """
                INSERT INTO BASE (
                    EAN, NCM, SKU_f, descricao_f, categoria, industria, marca,
                    preco_custo_embalagem_f, preco_venda_embalagem_f,
                    embalagem_f, preco_unitario_f, estoque_f
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(EAN) DO UPDATE SET
                    NCM = excluded.NCM,
                    SKU_f = excluded.SKU_f,
                    descricao_f = excluded.descricao_f,
                    categoria = excluded.categoria,
                    industria = excluded.industria,
                    marca = excluded.marca,
                    preco_custo_embalagem_f = excluded.preco_custo_embalagem_f,
                    preco_venda_embalagem_f = excluded.preco_venda_embalagem_f,
                    embalagem_f = excluded.embalagem_f,
                    preco_unitario_f = excluded.preco_unitario_f,
                    estoque_f = excluded.estoque_f
                """,
                (
                    produto["ean"],
                    produto["ncm"],
                    produto["sku_f"],
                    produto["descricao"],
                    produto["categoria"],
                    produto["industria"],
                    produto["marca"],
                    produto["custo"],
                    produto["venda"],
                    produto["embalagem"],
                    preco_unitario,
                    produto["estoque"],
                ),
            )

            conn.execute(
                """
                INSERT INTO REDE (
                    EAN, SKU_r, descricao_r, preco_venda_r,
                    preco_ultima_compra, contrato_r, mark_r, venda_diaria_r
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(EAN) DO UPDATE SET
                    SKU_r = excluded.SKU_r,
                    descricao_r = excluded.descricao_r,
                    preco_venda_r = excluded.preco_venda_r,
                    preco_ultima_compra = excluded.preco_ultima_compra,
                    contrato_r = excluded.contrato_r,
                    mark_r = excluded.mark_r,
                    venda_diaria_r = excluded.venda_diaria_r
                """,
                (
                    produto["ean"],
                    produto["sku_r"],
                    produto["descricao"],
                    produto["preco_rede"],
                    produto["ultima_compra"],
                    produto["contrato"],
                    10.0,
                    5.0,
                ),
            )

        conn.commit()


if __name__ == "__main__":
    popular_fluxo()
    print("FORNECEDOR, BASE e REDE preenchidas para demonstracao de ofertas.")
