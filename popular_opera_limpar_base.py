import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.sqlite3"


OPERAS = [
    (1001, 3.5, 12.0, 2.0, 1.5, 19.0),
    (1002, 2.5, 8.5, 1.5, 1.0, 13.5),
    (1003, 4.0, 10.0, 2.2, 1.8, 18.0),
    (1004, 3.0, 9.0, 1.7, 1.2, 14.9),
    (1005, 4.5, 11.5, 2.4, 1.6, 20.0),
]


def popular_opera_e_limpar_base():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM BASE")

        conn.executemany(
            """
            INSERT INTO OPERA (
                categoria, log_opera, Mark_opera, tributo_opera,
                promotor_opera, total_opera
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(categoria) DO UPDATE SET
                log_opera = excluded.log_opera,
                Mark_opera = excluded.Mark_opera,
                tributo_opera = excluded.tributo_opera,
                promotor_opera = excluded.promotor_opera,
                total_opera = excluded.total_opera
            """,
            OPERAS,
        )

        conn.commit()


if __name__ == "__main__":
    popular_opera_e_limpar_base()
    print("Tabela BASE limpa e OPERA preenchida com dados de demonstracao.")
