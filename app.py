# BLOCO 1 - IMPORTAÇÃO DAS BIBLIOTECAS

import streamlit as st
import streamlit as st
import pandas as pd
import os
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from textwrap import wrap
#usado para negrito
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY
from datetime import datetime

# BLOCO 2 - CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="Sistema de Declarações",
    page_icon="📄",
    layout="wide"
)

# BLOCO 3 - TÍTULO

st.title("📄 Sistema de Declarações CESC")

st.write("Bem-vindo ao sistema.")


# BLOCO 4 - CONFIGURAÇÕES

CAMINHO_EXCEL = "LISTA DE ALUNOS.xlsx"

# BLOCO 5 - LEITURA DA PLANILHA

try:

    df = pd.read_excel(
        CAMINHO_EXCEL,
        sheet_name=1
    )

    st.success(f"✅ Planilha carregada com sucesso! {len(df)} alunos encontrados.")

except Exception as erro:

    st.error("Erro ao abrir a planilha.")

    st.code(str(erro))

    st.stop()

# BLOCO 6 - VISUALIZAR AS COLUNAS

st.subheader("Colunas encontradas")

st.write(df.columns.tolist())

# BLOCO 7 - PESQUISA DO ALUNO

st.subheader("Pesquisar aluno")

nome_pesquisa = st.text_input(
    "Digite o nome do aluno"
)

# BLOCO 8 - FILTRAR ALUNO

if nome_pesquisa:

    resultado = df[
        df["Aluno"].str.contains(
            nome_pesquisa,
            case=False,
            na=False
        )
    ]
# BLOCO 9 - FUNÇÃO GERAR DECLARAÇÃO

def gerar_declaracao(dados_aluno):

    pasta_pdf = "pdfs"

    os.makedirs(pasta_pdf, exist_ok=True)

    nome_arquivo = (
        f"Declaracao_{dados_aluno['nome']}"
        .replace(" ", "_")
        .replace("/", "-")
    ) + ".pdf"

    caminho_pdf = os.path.join(
        pasta_pdf,
        nome_arquivo
    )

    c = canvas.Canvas(caminho_pdf)

    largura = 595
    altura = 842

    # LOGO

    logo = ImageReader("Modelos/LOGO.png")

    c.drawImage(
        logo,
        40,
        altura - 105,
        width=60,
        height=60,
        preserveAspectRatio=True,
        mask="auto"
    )

    # CABEÇALHO

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(
        largura / 2,
        altura - 40,
        "EDUCA CESC LTDA"
    )

    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(
        largura / 2,
        altura - 55,
        "CENTRO EDUCACIONAL SANTO CRISTO"
    )

    c.setFont("Helvetica", 8)
    c.drawCentredString(
        largura / 2,
        altura - 70,
        "CNPJ nº 54.019.265/0001-60"
    )

    c.drawCentredString(
        largura / 2,
        altura - 82,
        "Portaria E/SUBAIR/COR/GRE Nº2316, de 28 de Julho de 2025."
    )

    # TÍTULO

    c.setFont("Helvetica-Bold", 18)

    c.drawCentredString(
        largura / 2,
        altura - 130,
        "Declaração Escolar"
    )

    # CORPO DA DECLARAÇÃO

    styles = getSampleStyleSheet()

    estilo = styles["Normal"]

    estilo.fontName = "Helvetica"
    estilo.fontSize = 12
    estilo.leading = 20
    estilo.alignment = TA_JUSTIFY

    texto = f"""
    Declaramos para os devidos fins que o(a) aluno(a)
    <b>{dados_aluno['nome']}</b>, nascido(a) em
    {dados_aluno['nascimento']}, filho(a) de
    <b>{dados_aluno['mae']}</b> e <b>{dados_aluno['pai']}</b>,
    está regularmente matriculado(a) nesta instituição de ensino,
    cursando a turma <b>{dados_aluno['turma']}</b>.
    """

    paragrafo = Paragraph(texto, estilo)

    largura_texto = largura - 100

    w, h = paragrafo.wrap(
        largura_texto,
        altura
    )

    paragrafo.drawOn(
        c,
        50,
        altura - 180 - h
    )


       # POSIÇÃO ABAIXO DO TEXTO

    y_final = altura - 180 - h - 60

    # DATA

    meses = [
        "janeiro", "fevereiro", "março", "abril",
        "maio", "junho", "julho", "agosto",
        "setembro", "outubro", "novembro", "dezembro"
    ]

    hoje = datetime.now()

    data_extenso = (
        f"Rio de Janeiro, {hoje.day} de "
        f"{meses[hoje.month-1]} de {hoje.year}."
    )

    c.setFont("Helvetica", 12)

    c.drawRightString(
        largura - 50,
        y_final,
        data_extenso
    )

        # ASSINATURA

    assinatura = ImageReader("Modelos/Assinatura.jpg")

    y_ass = y_final - 120

    # Imagem da assinatura
    c.drawImage(
        assinatura,
        205,              # posição horizontal
        y_ass + 20,        # posição vertical
        width=180,         # largura da assinatura
        height=70,         # altura da assinatura
        preserveAspectRatio=True,
        mask="auto"
    )

    # Linha da assinatura
    c.setLineWidth(1)

    c.line(
        185,
        y_ass + 15,
        410,
        y_ass + 15
    )

    # Nome da diretora
    c.setFont("Helvetica-Bold", 12)

    c.drawCentredString(
        largura / 2,
        y_ass,
        "Andréia Souza Pinto"
    )

    # Cargo
    c.setFont("Helvetica", 11)

    c.drawCentredString(
        largura / 2,
        y_ass - 16,
        "Diretora"
    )

    # Escola
    c.drawCentredString(
        largura / 2,
        y_ass - 30,
        "Centro Educacional Santo Cristo"
    )

    c.save()

    return caminho_pdf


# BLOCO 10 - DADOS, FICHA E BOTÃO

if nome_pesquisa:

    resultado = df[
        df["Aluno"].str.contains(
            nome_pesquisa,
            case=False,
            na=False
        )
    ]

    if len(resultado) == 0:

        st.warning("Nenhum aluno encontrado.")

    else:

        for _, aluno in resultado.iterrows():

            dados_aluno = {

                "nome": aluno["Aluno"],
                "nascimento": pd.to_datetime(aluno["Data de Nascimento"]).strftime("%d/%m/%Y"),
                "pai": aluno["Nome do Pai"],
                "mae": aluno["Nome da Mãe"],
                "turma": aluno["Turma"],
                "unidade": aluno["Unidade"],
                "modalidade": aluno["Modalidade escolhida"],
                "email": aluno["E-mail"]

            }

            st.divider()

            st.subheader(dados_aluno["nome"])

            col1, col2 = st.columns(2)

            with col1:

                st.write("**Pai:**", dados_aluno["pai"])
                st.write("**Mãe:**", dados_aluno["mae"])
                st.write("**Turma:**", dados_aluno["turma"])
                st.write("**Modalidade:**", dados_aluno["modalidade"])

            with col2:

                st.write("**Nascimento:**", dados_aluno["nascimento"])
                st.write("**Unidade:**", dados_aluno["unidade"])
                st.write("**E-mail:**", dados_aluno["email"])

            if st.button(
                "📄 Gerar Declaração",
                key=f"declaracao_{dados_aluno['nome']}"
            ):

                caminho_pdf = gerar_declaracao(dados_aluno)

                st.success("Declaração gerada com sucesso!")

                with open(caminho_pdf, "rb") as arquivo:

                    st.download_button(
                        label="⬇️ Baixar declaração",
                        data=arquivo,
                        file_name=os.path.basename(caminho_pdf),
                        mime="application/pdf",
                        key=f"download_{dados_aluno['nome']}"
                    )

