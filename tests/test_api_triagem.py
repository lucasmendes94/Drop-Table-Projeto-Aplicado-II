"""Testes de integração locais para a API de triagem e o painel HTML."""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request

import pytest

from src.api_triagem import criar_servidor


@pytest.fixture(scope="module")
def url_base() -> str:
    servidor = criar_servidor(host="127.0.0.1", porta=0)
    _, porta = servidor.server_address
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{porta}"
    finally:
        servidor.shutdown()
        servidor.server_close()


def _post_triagem(url_base: str, corpo: bytes) -> tuple[int, dict[str, object]]:
    req = urllib.request.Request(
        f"{url_base}/triagem",
        data=corpo,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


def test_health_retorna_ok(url_base: str) -> None:
    with urllib.request.urlopen(f"{url_base}/health", timeout=5) as resp:
        assert resp.status == 200
        dados = json.loads(resp.read().decode("utf-8"))

    assert dados == {"status": "ok"}


def test_painel_servido_com_graficos_e_formulario(url_base: str) -> None:
    with urllib.request.urlopen(f"{url_base}/", timeout=5) as resp:
        assert resp.status == 200
        html = resp.read().decode("utf-8")

    assert "Painel de Voz do Cliente - ConectaShop" in html
    assert "Temas recorrentes nas avaliações negativas de treino" in html
    assert 'id="form-triagem"' in html
    assert "POST /triagem" in html


def test_triagem_negativa_sugere_revisao(url_base: str) -> None:
    corpo = json.dumps(
        {"texto": "Produto chegou muito atrasado, com defeito e caixa rasgada."}
    ).encode("utf-8")
    status, dados = _post_triagem(url_base, corpo)

    assert status == 200
    assert dados["sentimento"] == "negativo"
    assert dados["encaminhar_para_revisao"] is True


def test_triagem_positiva_sem_alerta(url_base: str) -> None:
    corpo = json.dumps(
        {"texto": "Excelente produto, chegou antes do prazo e muito bem embalado!"}
    ).encode("utf-8")
    status, dados = _post_triagem(url_base, corpo)

    assert status == 200
    assert dados["sentimento"] in {"positivo", "neutro"}
    assert dados["sentimento"] == "positivo"
    assert dados["encaminhar_para_revisao"] is False


def test_caso_ambiguo_previsto_neutro_sem_alerta(url_base: str) -> None:
    corpo = json.dumps(
        {"texto": "Produto demorou muito para chegar"}
    ).encode("utf-8")
    status, dados = _post_triagem(url_base, corpo)

    assert status == 200
    assert dados["sentimento"] == "neutro"
    assert dados["encaminhar_para_revisao"] is False


def test_triagem_avaliacoes_sucessivas(url_base: str) -> None:
    casos = [
        ("Nao recebi meu pedido e ninguem responde no atendimento.", "negativo", True),
        ("Tudo certo, entrega rapida e produto otimo.", "positivo", False),
        ("Veio quebrado, pessima qualidade.", "negativo", True),
    ]
    for texto, sentimento_esperado, revisao_esperada in casos:
        corpo = json.dumps({"texto": texto}).encode("utf-8")
        status, dados = _post_triagem(url_base, corpo)
        assert status == 200
        assert dados["sentimento"] == sentimento_esperado
        assert dados["encaminhar_para_revisao"] is revisao_esperada


@pytest.mark.parametrize(
    "payload",
    [
        {"texto": ""},
        {"texto": "   "},
        {"texto": "!!! ??? --- ..."},
        {},
        {"texto": 123},
        {"texto": None},
    ],
)
def test_triagem_rejeita_entradas_invalidas_ou_vazias(
    url_base: str, payload: dict[str, object]
) -> None:
    corpo = json.dumps(payload).encode("utf-8")
    status, dados = _post_triagem(url_base, corpo)

    assert status == 400
    assert "erro" in dados


def test_triagem_rejeita_json_malformado(url_base: str) -> None:
    status, dados = _post_triagem(url_base, b"{texto: invalido")

    assert status == 400
    assert "erro" in dados
