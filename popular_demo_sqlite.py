import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.sqlite3"


CATEGORIAS = [
    (1001, "Higiene e Beleza", 12.0, "Alta"),
    (1002, "Alimentos Basicos", 8.5, "Alta"),
    (1003, "Bebidas", 10.0, "Media"),
    (1004, "Limpeza", 9.0, "Media"),
    (1005, "Pet Shop", 11.5, "Baixa"),
]

NCMS = [
    ("3305.90.00", "Produtos capilares", 2.5),
    ("3401.30.00", "Sabonetes e preparacoes de limpeza", 3.0),
    ("1905.90.90", "Produtos de panificacao", 1.8),
    ("2202.10.00", "Bebidas nao alcoolicas", 2.2),
    ("3402.20.00", "Preparacoes para limpeza", 2.7),
    ("2309.10.00", "Alimentos para animais", 1.5),
]

BASES = [
    (
        "7899706100001",
        "3305.90.00",
        "SKU-F-001",
        "Shampoo Hidratante 12x350ml",
        1001,
        "Industria Alfa",
        "Marca Solaris",
        84.00,
        108.00,
        12,
        9.00,
        120,
    ),
    (
        "7899706100002",
        "3401.30.00",
        "SKU-F-002",
        "Sabonete Liquido 6x500ml",
        1001,
        "Industria Alfa",
        "Marca Solaris",
        42.00,
        59.40,
        6,
        9.90,
        80,
    ),
    (
        "7899706100003",
        "1905.90.90",
        "SKU-F-003",
        "Biscoito Recheado 24x90g",
        1002,
        "Alimentos Beta",
        "Marca Saboria",
        36.00,
        52.80,
        24,
        2.20,
        240,
    ),
    (
        "7899706100004",
        "2202.10.00",
        "SKU-F-004",
        "Refrigerante Cola 12x2L",
        1003,
        "Bebidas Delta",
        "Marca Fonte",
        72.00,
        96.00,
        12,
        8.00,
        60,
    ),
    (
        "7899706100005",
        "3402.20.00",
        "SKU-F-005",
        "Detergente Neutro 24x500ml",
        1004,
        "Limpeza Gama",
        "Marca Brilho",
        48.00,
        69.60,
        24,
        2.90,
        180,
    ),
    (
        "7899706100006",
        "2309.10.00",
        "SKU-F-006",
        "Racao Caes Adultos 6x3kg",
        1005,
        "Pet Omega",
        "Marca Companheiro",
        150.00,
        210.00,
        6,
        35.00,
        45,
    ),
]


def popular():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            """
            INSERT INTO CATEGORIA (categoria, desc_categoria, mark_categoria, prioridade)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(categoria) DO UPDATE SET
                desc_categoria = excluded.desc_categoria,
                mark_categoria = excluded.mark_categoria,
                prioridade = excluded.prioridade
            """,
            CATEGORIAS,
        )

        conn.executemany(
            """
            INSERT INTO NCM (NCM, descricao_n, tributo_n)
            VALUES (?, ?, ?)
            ON CONFLICT(NCM) DO UPDATE SET
                descricao_n = excluded.descricao_n,
                tributo_n = excluded.tributo_n
            """,
            NCMS,
        )

        conn.executemany(
            """
            INSERT INTO BASE (
                EAN, NCM, SKU_f, descricao_f, categoria, industria, marca,
                preco_custo_embalagem_f, preco_venda_embalagem_f, embalagem_f,
                preco_unitario_f, estoque_f
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
            BASES,
        )

        conn.commit()


if __name__ == "__main__":
    popular()
    print("Dados de demonstracao inseridos em NCM, CATEGORIA e BASE.")
