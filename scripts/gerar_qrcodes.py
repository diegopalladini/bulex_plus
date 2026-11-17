"""Gera os QR Codes de cada medicamento em docs/qrcodes/.

Cada QR Code aponta para a tela do medicamento no app publicado,
simulando o código impresso na embalagem.

Uso (dependência apenas de desenvolvimento, não usada pelo app):
    pip install "qrcode[pil]"
    python scripts/gerar_qrcodes.py
"""
import os
import sqlite3
import sys

import qrcode

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from database import DB_PATH, iniciar_banco  # noqa: E402

URL_APP = "https://bulex-mvp.onrender.com"
PASTA_SAIDA = os.path.join(BASE_DIR, "docs", "qrcodes")


def main():
    iniciar_banco()
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        medicamentos = conn.execute("SELECT id, nome FROM medicamentos ORDER BY id").fetchall()

    for id_med, nome in medicamentos:
        url = f"{URL_APP}/medicamento/{id_med}"
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        imagem = qr.make_image(fill_color="#9b1b30", back_color="white")

        caminho = os.path.join(PASTA_SAIDA, f"medicamento-{id_med}.png")
        imagem.save(caminho)
        print(f"{id_med:>2} {nome:<22} -> {url}")


if __name__ == "__main__":
    main()
