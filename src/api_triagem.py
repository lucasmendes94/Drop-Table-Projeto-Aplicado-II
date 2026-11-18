"""API local de triagem de avaliações e servidor do Painel de Voz do Cliente.

Carrega o modelo treinado uma única vez na inicialização, disponibiliza o
endpoint ``POST /triagem`` e serve ``produto/painel_voz_cliente.html`` no
mesmo endereço local.

Uso, a partir da raiz do projeto:
    python -m src.api_triagem
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import joblib

from src.preparacao import normalizar_texto


BASE_DIR = Path(__file__).resolve().parents[1]
MODELO_PADRAO = BASE_DIR / "data" / "processed" / "modelo" / "modelo_sentimento.joblib"
PAINEL_PADRAO = BASE_DIR / "produto" / "painel_voz_cliente.html"
LIMITE_CORPO_BYTES = 1_048_576  # 1 MiB


def carregar_modelo(caminho: str | Path = MODELO_PADRAO) -> Any:
    """Carrega o pipeline de sentimento salvo em joblib."""
    caminho_modelo = Path(caminho)
    if not caminho_modelo.is_file():
        raise FileNotFoundError(f"Modelo não encontrado em: {caminho_modelo}")
    return joblib.load(caminho_modelo)


def classificar_avaliacao(texto: object, modelo: Any) -> dict[str, object]:
    """Valida, normaliza e classifica uma avaliação textual.

    Retorna ``sentimento`` (``negativo``, ``neutro`` ou ``positivo``) e
    ``encaminhar_para_revisao`` (``True`` apenas para previsão negativa).
    """
    if not isinstance(texto, str):
        raise ValueError("O campo 'texto' deve ser uma string.")

    texto_limpo = normalizar_texto(texto)
    if not texto_limpo:
        raise ValueError(
            "O campo 'texto' está vazio ou sem conteúdo válido após a normalização."
        )

    sentimento = str(modelo.predict([texto_limpo])[0])
    return {
        "sentimento": sentimento,
        "encaminhar_para_revisao": sentimento == "negativo",
    }


class ServidorTriagem(ThreadingHTTPServer):
    """Servidor HTTP com o modelo mantido em memória durante toda a execução."""

    def __init__(
        self,
        server_address: tuple[str, int],
        modelo: Any,
        caminho_painel: Path,
    ) -> None:
        self.modelo = modelo
        self.caminho_painel = caminho_painel
        super().__init__(server_address, ManipuladorTriagem)


class ManipuladorTriagem(BaseHTTPRequestHandler):
    """Manipula requisições do painel HTML e do endpoint POST /triagem."""

    server: ServidorTriagem

    def _enviar_json(self, status: int, payload: dict[str, object]) -> None:
        corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(corpo)

    def _enviar_html(self, status: int, conteudo: str) -> None:
        corpo = conteudo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        rota = self.path.split("?", 1)[0]
        if rota in {"/", "/painel_voz_cliente.html", "/produto/painel_voz_cliente.html"}:
            if not self.server.caminho_painel.is_file():
                self._enviar_json(404, {"erro": "Arquivo do painel não encontrado."})
                return
            html = self.server.caminho_painel.read_text(encoding="utf-8")
            self._enviar_html(200, html)
            return

        if rota == "/health":
            self._enviar_json(200, {"status": "ok"})
            return

        self._enviar_json(404, {"erro": "Rota não encontrada."})

    def do_POST(self) -> None:
        rota = self.path.split("?", 1)[0]
        if rota != "/triagem":
            self._enviar_json(404, {"erro": "Rota não encontrada."})
            return

        cabecalho_tamanho = self.headers.get("Content-Length")
        if cabecalho_tamanho is None:
            self._enviar_json(400, {"erro": "Cabeçalho Content-Length ausente."})
            return

        try:
            tamanho = int(cabecalho_tamanho)
        except ValueError:
            self._enviar_json(400, {"erro": "Cabeçalho Content-Length inválido."})
            return

        if tamanho <= 0 or tamanho > LIMITE_CORPO_BYTES:
            self._enviar_json(400, {"erro": "Corpo da requisição vazio ou acima do limite."})
            return

        bruto = self.rfile.read(tamanho)
        try:
            dados = json.loads(bruto.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._enviar_json(400, {"erro": "JSON inválido."})
            return

        if not isinstance(dados, dict) or "texto" not in dados:
            self._enviar_json(400, {"erro": "Informe um JSON com o campo 'texto'."})
            return

        try:
            resultado = classificar_avaliacao(dados["texto"], self.server.modelo)
        except ValueError as exc:
            self._enviar_json(400, {"erro": str(exc)})
            return

        self._enviar_json(200, resultado)


def criar_servidor(
    host: str = "127.0.0.1",
    porta: int = 8000,
    caminho_modelo: str | Path = MODELO_PADRAO,
    caminho_painel: str | Path = PAINEL_PADRAO,
) -> ServidorTriagem:
    """Inicializa o servidor carregando o modelo uma única vez."""
    modelo = carregar_modelo(caminho_modelo)
    painel = Path(caminho_painel)
    return ServidorTriagem((host, porta), modelo=modelo, caminho_painel=painel)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inicia a API de triagem e o Painel de Voz do Cliente."
    )
    parser.add_argument("--host", default="127.0.0.1", help="Endereço de escuta.")
    parser.add_argument("--port", type=int, default=8000, help="Porta HTTP local.")
    parser.add_argument(
        "--modelo",
        default=str(MODELO_PADRAO),
        help="Caminho do modelo .joblib.",
    )
    parser.add_argument(
        "--painel",
        default=str(PAINEL_PADRAO),
        help="Caminho do arquivo HTML do painel.",
    )
    argumentos = parser.parse_args()

    servidor = criar_servidor(
        host=argumentos.host,
        porta=argumentos.port,
        caminho_modelo=argumentos.modelo,
        caminho_painel=argumentos.painel,
    )
    host_real, porta_real = servidor.server_address
    print(f"Painel disponível em: http://{host_real}:{porta_real}/")
    print(f"Endpoint de triagem:  POST http://{host_real}:{porta_real}/triagem")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
