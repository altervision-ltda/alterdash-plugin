#!/usr/bin/env python3
"""Gera um PDF A4 na identidade visual AlterVision a partir de uma especificação JSON.

Uso:
    python3 gerar_pdf.py especificacao.json saida.pdf

O formato da especificação está em ../references/formato-json.md. Dependência: reportlab
(`pip install reportlab`). Os números chegam já formatados no padrão brasileiro: o script
desenha, não calcula.
"""
import glob
import json
import math
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(AQUI, "..", "assets", "Logo_AlterVision_branco_transparente.png")

# Cores da diretriz; nenhuma outra entra no PDF.
MARINHO = colors.HexColor("#14133B")
DEGRADE_INICIO = colors.HexColor("#3A1446")
ROSA = colors.HexColor("#96084E")
ROSA_CLARO = colors.HexColor("#F7D9E7")
CREME = colors.HexColor("#F8F5EF")
BRANCO = colors.white
BORDA = colors.HexColor("#E6E2D8")
SECUNDARIO = colors.HexColor("#5B5A74")
APAGADO = colors.HexColor("#6E6C7E")
VERDE_TEXTO = colors.HexColor("#0E6B38")
VERDE_BARRA = colors.HexColor("#1E9E57")
VERMELHO_TEXTO = colors.HexColor("#9E2A22")
VERMELHO_BARRA = colors.HexColor("#D9463B")
ATENCAO_TEXTO = colors.HexColor("#8A6100")
ATENCAO_FUNDO = colors.HexColor("#FBF0CC")

TOM_TEXTO = {"positivo": VERDE_TEXTO, "negativo": VERMELHO_TEXTO, "neutro": SECUNDARIO}
STATUS_COR = {"ok": VERDE_BARRA, "atencao": colors.HexColor("#E0A800"), "ruim": VERMELHO_BARRA}
FUNDO_CELULA = {"creme": CREME, "rosa_claro": ROSA_CLARO, "rosa": ROSA, "marinho": MARINHO}


def _registrar(nome, candidatos):
    for padrao in candidatos:
        for caminho in sorted(glob.glob(padrao, recursive=True)):
            try:
                pdfmetrics.registerFont(TTFont(nome, caminho))
                return True
            except Exception:  # OTF com contornos CFF não carrega no reportlab; tenta o próximo
                continue
    return False


def _fontes():
    """Inter/Roboto Mono quando houver TTF; senão Lato/Carlito e DejaVu Sans Mono, como manda a diretriz."""
    bases = ["/usr/share/fonts/**/", os.path.expanduser("~/.fonts/**/"),
             os.path.expanduser("~/.local/share/fonts/**/"), "/Library/Fonts/",
             os.path.expanduser("~/Library/Fonts/"), "C:/Windows/Fonts/"]

    def cand(*nomes):
        return [b + n for n in nomes for b in bases]

    texto = ("Helvetica", "Helvetica-Bold")
    for regular, negrito in [
        (("Inter-Regular.ttf", "Inter_18pt-Regular.ttf"), ("Inter-Bold.ttf", "Inter_18pt-Bold.ttf")),
        (("Lato-Regular.ttf",), ("Lato-Bold.ttf",)),
        (("Carlito-Regular.ttf",), ("Carlito-Bold.ttf",)),
    ]:
        if _registrar("AV-Texto", cand(*regular)) and _registrar("AV-Texto-Negrito", cand(*negrito)):
            pdfmetrics.registerFontFamily("AV-Texto", normal="AV-Texto", bold="AV-Texto-Negrito",
                                          italic="AV-Texto", boldItalic="AV-Texto-Negrito")
            texto = ("AV-Texto", "AV-Texto-Negrito")
            break

    mono = ("Courier", "Courier-Bold")
    for regular, negrito in [
        (("RobotoMono-Regular.ttf",), ("RobotoMono-Bold.ttf",)),
        (("DejaVuSansMono.ttf",), ("DejaVuSansMono-Bold.ttf",)),
    ]:
        if _registrar("AV-Mono", cand(*regular)) and _registrar("AV-Mono-Negrito", cand(*negrito)):
            pdfmetrics.registerFontFamily("AV-Mono", normal="AV-Mono", bold="AV-Mono-Negrito",
                                          italic="AV-Mono", boldItalic="AV-Mono-Negrito")
            mono = ("AV-Mono", "AV-Mono-Negrito")
            break
    return texto, mono


(TEXTO, TEXTO_N), (MONO, MONO_N) = _fontes()


def estilo(nome, **kw):
    # Com `parent`, herda dele; os padrões aqui só valem para estilos de raiz.
    base = {} if "parent" in kw else dict(fontName=TEXTO, fontSize=10, leading=14, textColor=MARINHO)
    base.update(kw)
    return ParagraphStyle(nome, **base)


S_TEXTO = estilo("texto")
S_TITULO_SECAO = estilo("titulo_secao", fontName=TEXTO_N, fontSize=14, leading=18, spaceAfter=4)
S_ROTULO_SECAO = estilo("rotulo_secao", fontName=MONO, fontSize=8, leading=10, textColor=ROSA)
S_NOTA = estilo("nota", fontSize=7.5, leading=10, textColor=APAGADO)
S_CAB_TABELA = estilo("cab_tabela", fontName=TEXTO_N, fontSize=8, leading=10, textColor=SECUNDARIO)
S_CAB_TABELA_D = estilo("cab_tabela_d", parent=S_CAB_TABELA, alignment=TA_RIGHT)
S_CEL = estilo("cel", fontSize=9, leading=11.5)
S_CEL_NUM = estilo("cel_num", fontName=MONO, fontSize=9, leading=11.5, alignment=TA_RIGHT)
S_META = estilo("meta", fontName=MONO, fontSize=7, leading=9, textColor=ROSA, alignment=TA_RIGHT)


def espacado(texto):
    """Rótulos de seção vão em maiúsculas; a fonte mono já dá o espaçamento."""
    return texto.upper()


class CanvasNumerado(rl_canvas.Canvas):
    """Guarda as páginas para desenhar cabeçalho e rodapé no fim, já sabendo o total de páginas."""

    def __init__(self, *args, spec=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._spec = spec
        self._paginas = []
        self.nome_pagina = ""

    def showPage(self):
        self._paginas.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._paginas)
        for estado in self._paginas:
            self.__dict__.update(estado)
            if self._pageNumber == 1:
                desenhar_capa(self, self._spec)
            else:
                desenhar_faixa_interna(self, self._spec, self.nome_pagina)
            desenhar_rodape(self, self._spec, total)
            super().showPage()
        super().save()


def _logo(c, x, y_topo, largura):
    if not os.path.exists(LOGO):
        return
    altura = largura * 232 / 480
    c.drawImage(LOGO, x, y_topo - altura, width=largura, height=altura, mask="auto")


def desenhar_capa(c, spec):
    w, h = c._pagesize
    altura = 56 * mm
    y0 = h - altura
    c.saveState()
    caminho = c.beginPath()
    caminho.rect(0, y0, w, altura)
    c.clipPath(caminho, stroke=0, fill=0)
    # 115° no CSS: do canto superior esquerdo para o inferior direito.
    ang = math.radians(115)
    cx, cy, r = w / 2, y0 + altura / 2, max(w, altura) / 2
    dx, dy = math.sin(ang) * r, math.cos(ang) * r
    c.linearGradient(cx - dx, cy - dy, cx + dx, cy + dy, (DEGRADE_INICIO, MARINHO), extend=True)
    c.restoreState()

    margem = 15 * mm
    _logo(c, margem, h - 7 * mm, 40 * mm)
    c.setFillColor(BRANCO)
    c.setFont(TEXTO_N, 24)
    c.drawString(margem, y0 + 14 * mm, spec.get("titulo", ""))
    c.setFont(TEXTO, 10)
    c.drawString(margem, y0 + 6.5 * mm, spec.get("periodo", ""))

    logo_cliente = spec.get("logo_cliente")
    if logo_cliente and os.path.exists(logo_cliente):
        img = Image(logo_cliente)
        larg = min(30 * mm, img.imageWidth * 16 * mm / img.imageHeight)
        alt = larg * img.imageHeight / img.imageWidth
        c.drawImage(logo_cliente, w - margem - larg, h - 7 * mm - alt, width=larg, height=alt, mask="auto")
    if spec.get("escopo"):
        c.setFont(MONO, 10)
        c.drawRightString(w - margem, y0 + 6.5 * mm, spec["escopo"])


def desenhar_faixa_interna(c, spec, nome_pagina):
    w, h = c._pagesize
    altura = 14 * mm
    c.setFillColor(MARINHO)
    c.rect(0, h - altura, w, altura, stroke=0, fill=1)
    margem = 15 * mm
    _logo(c, margem, h - 2.5 * mm, 20 * mm)
    c.setFillColor(BRANCO)
    c.setFont(TEXTO_N, 11)
    c.drawString(margem + 25 * mm, h - altura / 2 - 4, nome_pagina or spec.get("titulo", ""))
    if spec.get("escopo"):
        c.setFont(MONO, 9)
        c.drawRightString(w - margem, h - altura / 2 - 3, spec["escopo"])


def desenhar_rodape(c, spec, total):
    w, _ = c._pagesize
    margem = 15 * mm
    partes = [spec.get("relatorio") or spec.get("titulo", ""), spec.get("rede", ""), spec.get("periodo", "")]
    c.setFont(TEXTO, 7.5)
    c.setFillColor(APAGADO)
    c.drawString(margem, 9 * mm, " · ".join(p for p in partes if p))
    c.drawRightString(w - margem, 9 * mm, f"{c._pageNumber} / {total}")


class MarcaPagina(Flowable):
    """Muda o nome que a faixa das páginas internas mostra a partir desta página."""

    def __init__(self, nome):
        super().__init__()
        self.nome = nome

    def wrap(self, *_):
        return 0, 0

    def draw(self):
        self.canv.nome_pagina = self.nome


class Cartoes(Flowable):
    def __init__(self, itens):
        super().__init__()
        self.itens = itens[:5]
        self.gap = 4 * mm
        self.pad = 3.5 * mm

    def _paragrafos(self, item, largura, tam):
        tom = TOM_TEXTO.get(item.get("tendencia", "neutro"), SECUNDARIO)
        valor = item.get("valor", "sem dado")
        ps = [
            Paragraph(item.get("rotulo", ""), estilo("c_rot", fontSize=8, leading=10, textColor=SECUNDARIO)),
            Paragraph(valor, estilo("c_val", fontName=MONO_N, fontSize=tam, leading=tam * 1.25)),
        ]
        if item.get("comparacao"):
            ps.append(Paragraph(item["comparacao"], estilo("c_cmp", fontSize=8, leading=10, textColor=tom)))
        alturas = [p.wrap(largura, 1000)[1] for p in ps]
        return ps, alturas

    def wrap(self, largura_disp, _):
        n = max(1, len(self.itens))
        self.largura_cartao = (largura_disp - self.gap * (n - 1)) / n
        interno = self.largura_cartao - 2 * self.pad
        # Um só tamanho para todos os números da fileira: o maior que cabe em uma linha em todos.
        tam = 24
        while tam > 12 and any(pdfmetrics.stringWidth(i.get("valor", "sem dado"), MONO_N, tam) > interno
                               for i in self.itens):
            tam -= 1
        self.blocos = [self._paragrafos(i, interno, tam) for i in self.itens]
        self.altura = max(sum(a) + 2 * mm for _, a in self.blocos) + 2 * self.pad
        self.largura = largura_disp
        return largura_disp, self.altura

    def draw(self):
        c = self.canv
        for i, (ps, alturas) in enumerate(self.blocos):
            x = i * (self.largura_cartao + self.gap)
            c.setFillColor(BRANCO)
            c.setStrokeColor(BORDA)
            c.setLineWidth(0.8)
            c.roundRect(x, 0, self.largura_cartao, self.altura, 2.5 * mm, stroke=1, fill=1)
            y = self.altura - self.pad
            for p, a in zip(ps, alturas):
                y -= a
                p.drawOn(c, x + self.pad, y)
                y -= 1 * mm


class Caixa(Flowable):
    """Caixa com fundo e filete opcional à esquerda (frase-resumo, qualidade dos dados)."""

    def __init__(self, conteudo, fundo, filete=None, pad=4 * mm):
        super().__init__()
        self.conteudo = conteudo
        self.fundo = fundo
        self.filete = filete
        self.pad = pad

    def wrap(self, largura_disp, altura_disp):
        self.largura = largura_disp
        interno = largura_disp - 2 * self.pad - (1.2 * mm if self.filete else 0)
        self.alturas = [f.wrap(interno, altura_disp)[1] for f in self.conteudo]
        self.altura = sum(self.alturas) + 2 * self.pad + 1.5 * mm * (len(self.conteudo) - 1)
        return largura_disp, self.altura

    def draw(self):
        c = self.canv
        c.setFillColor(self.fundo)
        c.roundRect(0, 0, self.largura, self.altura, 1.5 * mm, stroke=0, fill=1)
        x = self.pad
        if self.filete:
            c.setFillColor(self.filete)
            c.rect(0, 0, 1.2 * mm, self.altura, stroke=0, fill=1)
            x += 1.2 * mm
        y = self.altura - self.pad
        for f, a in zip(self.conteudo, self.alturas):
            y -= a
            f.drawOn(c, x, y)
            y -= 1.5 * mm


class Status(Flowable):
    def __init__(self, status, texto=""):
        super().__init__()
        self.cor = STATUS_COR.get(status, SECUNDARIO)
        self.texto = texto

    def wrap(self, largura_disp, _):
        return largura_disp, 11

    def draw(self):
        self.canv.setFillColor(self.cor)
        self.canv.circle(4, 4, 3.2, stroke=0, fill=1)
        if self.texto:
            self.canv.setFillColor(MARINHO)
            self.canv.setFont(TEXTO, 9)
            self.canv.drawString(11, 1, self.texto)


class Barras(Flowable):
    """Barras horizontais a partir de um eixo central: verde somou, vermelho tirou, maior perda em destaque."""

    def __init__(self, itens):
        super().__init__()
        self.itens = itens
        self.linha = 7 * mm

    def wrap(self, largura_disp, _):
        self.largura = largura_disp
        self.altura = self.linha * len(self.itens) + 2 * mm
        return largura_disp, self.altura

    def draw(self):
        c = self.canv
        rotulo_w = 0.30 * self.largura
        area = self.largura - rotulo_w
        eixo = rotulo_w + area / 2
        meia = area / 2 - 18 * mm  # espaço para o valor escrito ao lado da barra
        maximo = max((abs(i.get("valor", 0)) for i in self.itens), default=0) or 1
        negativos = [i.get("valor", 0) for i in self.itens if i.get("valor", 0) < 0]
        pior = min(negativos) if negativos else None

        c.setStrokeColor(BORDA)
        c.setLineWidth(0.8)
        c.line(eixo, 0, eixo, self.altura)
        for n, item in enumerate(self.itens):
            v = item.get("valor", 0)
            y = self.altura - (n + 1) * self.linha
            destaque = pior is not None and v == pior
            c.setFont(TEXTO_N if destaque else TEXTO, 9)
            c.setFillColor(ROSA if destaque else MARINHO)
            c.drawString(0, y + 2.2 * mm, item.get("rotulo", ""))
            comp = abs(v) / maximo * meia
            c.setFillColor(VERDE_BARRA if v >= 0 else VERMELHO_BARRA)
            x = eixo if v >= 0 else eixo - comp
            c.rect(x, y + 1.2 * mm, comp, self.linha - 2.6 * mm, stroke=0, fill=1)
            c.setFont(MONO_N if destaque else MONO, 8.5)
            c.setFillColor(VERDE_TEXTO if v >= 0 else VERMELHO_TEXTO)
            texto = item.get("texto", str(v))
            if v >= 0:
                c.drawString(eixo + comp + 1.5 * mm, y + 2.2 * mm, texto)
            else:
                c.drawRightString(eixo - comp - 1.5 * mm, y + 2.2 * mm, texto)


def celula(valor, alinhar_direita, cab=False):
    if cab:
        return Paragraph(str(valor), S_CAB_TABELA_D if alinhar_direita else S_CAB_TABELA)
    if isinstance(valor, dict):
        if "status" in valor:
            return Status(valor["status"], valor.get("texto", ""))
        cor = TOM_TEXTO.get(valor.get("tom"))
        base = S_CEL_NUM if alinhar_direita else S_CEL
        s = estilo("cel_x", parent=base, textColor=cor or base.textColor)
        if valor.get("fundo") in ("rosa", "marinho"):
            s = estilo("cel_x2", parent=s, textColor=BRANCO, fontName=MONO_N if alinhar_direita else TEXTO_N)
        partes = [Paragraph(str(valor.get("valor", "")), s)]
        if valor.get("meta"):
            partes.append(Paragraph(valor["meta"], S_META))
        return partes
    return Paragraph("" if valor is None else str(valor), S_CEL_NUM if alinhar_direita else S_CEL)


def tabela(bloco, largura_disp):
    colunas = bloco["colunas"]
    alinh = bloco.get("alinhamento") or ["e"] + ["d"] * (len(colunas) - 1)
    direita = [a in ("d", "r", "direita") for a in alinh]
    dados = [[celula(c, direita[i], cab=True) for i, c in enumerate(colunas)]]
    for linha in bloco.get("linhas", []):
        dados.append([celula(v, direita[i]) for i, v in enumerate(linha)])
    larguras = None
    if bloco.get("larguras"):
        total = sum(bloco["larguras"])
        larguras = [largura_disp * p / total for p in bloco["larguras"]]
    t = Table(dados, colWidths=larguras, repeatRows=1, hAlign="LEFT")
    estilos = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.6, BORDA),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for r, linha in enumerate(bloco.get("linhas", []), start=1):
        for col, v in enumerate(linha):
            if isinstance(v, dict) and v.get("fundo") in FUNDO_CELULA:
                estilos.append(("BACKGROUND", (col, r), (col, r), FUNDO_CELULA[v["fundo"]]))
    if bloco.get("linha_total"):
        estilos += [("LINEABOVE", (0, -1), (-1, -1), 1, MARINHO), ("BACKGROUND", (0, -1), (-1, -1), CREME)]
    t.setStyle(TableStyle(estilos))
    return t


def quadro_acao(bloco):
    linhas = [[Paragraph("O que fazer", S_CAB_TABELA), Paragraph("Quem", S_CAB_TABELA),
               Paragraph("Quanto vale", S_CAB_TABELA_D)]]
    for item in bloco.get("itens", []):
        linhas.append([Paragraph(item.get("o_que", ""), S_CEL), Paragraph(item.get("quem", ""), S_CEL),
                       Paragraph(item.get("quanto", "sem dado"), S_CEL_NUM)])
    t = Table(linhas, colWidths=["60%", "20%", "20%"])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.6, BORDA),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    titulo = Paragraph(espacado(bloco.get("titulo", "Plano de ação")), S_ROTULO_SECAO)
    fundo = ROSA_CLARO if bloco.get("variante") == "rosa" else CREME
    return Caixa([titulo, t], fundo, filete=ROSA)


def montar(spec, largura_util):
    hist = []
    for bloco in spec.get("blocos", []):
        tipo = bloco.get("tipo")
        if tipo == "cartoes":
            hist += [Cartoes(bloco["itens"]), Spacer(1, 5 * mm)]
        elif tipo == "resumo":
            hist += [Caixa([Paragraph(bloco["texto"], estilo("resumo", fontSize=11, leading=15))], CREME, filete=ROSA),
                     Spacer(1, 5 * mm)]
        elif tipo == "secao":
            itens = []
            if bloco.get("rotulo"):
                itens.append(Paragraph(espacado(bloco["rotulo"]), S_ROTULO_SECAO))
            itens.append(Paragraph(bloco["titulo"], S_TITULO_SECAO))
            hist += [CondPageBreak(40 * mm), Spacer(1, 2 * mm)] + itens
        elif tipo == "paragrafo":
            hist += [Paragraph(bloco["texto"], S_TEXTO), Spacer(1, 3 * mm)]
        elif tipo == "tabela":
            hist += [tabela(bloco, largura_util)]
            if bloco.get("nota"):
                hist += [Spacer(1, 1.5 * mm), Paragraph(bloco["nota"], S_NOTA)]
            hist += [Spacer(1, 5 * mm)]
        elif tipo == "barras":
            hist += [KeepTogether([Barras(bloco["itens"])]), Spacer(1, 5 * mm)]
        elif tipo == "acao":
            hist += [quadro_acao(bloco), Spacer(1, 5 * mm)]
        elif tipo == "qualidade":
            s = estilo("qual", fontSize=9, leading=12.5, textColor=ATENCAO_TEXTO)
            conteudo = [Paragraph(espacado("Qualidade dos dados"), estilo("qual_t", parent=S_ROTULO_SECAO, textColor=ATENCAO_TEXTO))]
            conteudo += [Paragraph("• " + i, s) for i in bloco.get("itens", [])]
            hist += [Caixa(conteudo, ATENCAO_FUNDO), Spacer(1, 5 * mm)]
        elif tipo == "imagem":
            img = Image(bloco["caminho"])
            larg = min(largura_util, bloco.get("largura_mm", 999) * mm)
            img.drawWidth, img.drawHeight = larg, larg * img.imageHeight / img.imageWidth
            hist += [img, Spacer(1, 4 * mm)]
        elif tipo == "pagina":
            hist += [PageBreak(), MarcaPagina(bloco.get("titulo", ""))]
        elif tipo == "quebra":
            hist += [PageBreak()]
        else:
            raise SystemExit(f"tipo de bloco desconhecido: {tipo!r}")
    if spec.get("siglas"):
        hist += [Spacer(1, 4 * mm), Paragraph(spec["siglas"], S_NOTA)]
    return hist


def gerar(spec, saida):
    tamanho = landscape(A4) if spec.get("orientacao") == "paisagem" else A4
    w, h = tamanho
    margem = 15 * mm
    capa = Frame(margem, 16 * mm, w - 2 * margem, h - 56 * mm - 22 * mm, id="capa", showBoundary=0)
    interna = Frame(margem, 16 * mm, w - 2 * margem, h - 14 * mm - 22 * mm, id="interna", showBoundary=0)
    doc = BaseDocTemplate(saida, pagesize=tamanho, leftMargin=margem, rightMargin=margem,
                          title=spec.get("titulo", ""), author="AlterVision")
    doc.addPageTemplates([PageTemplate(id="capa", frames=[capa]), PageTemplate(id="interna", frames=[interna])])
    historia = [NextPageTemplate("interna")] + montar(spec, w - 2 * margem)
    doc.build(historia, canvasmaker=lambda *a, **k: CanvasNumerado(*a, spec=spec, **k))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        gerar(json.load(f), sys.argv[2])
    print(sys.argv[2])
