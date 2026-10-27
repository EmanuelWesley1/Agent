import os
import io
import pandas as pd
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini

load_dotenv(override=True)

def create_dashboard_agent(model_id: str = "gemini-3.8-flash"):
    agent = Agent(
        model=Gemini(id=model_id),
        description="Você é um Engenheiro de Dados e Especialista em BI sênior.",
        instructions=[
            "Analise os dados estatísticos e as amostras da planilha fornecida.",
            "Gere um relatório executivo sucinto e objetivo em Markdown.",
            "Crie um código HTML completo e responsivo para um Dashboard interativo.",
            "Utilize Tailwind CSS (via CDN) para o design e Chart.js (via CDN) para os gráficos.",
            "O dashboard deve conter cartões de KPIs principais e pelo menos dois gráficos visuais dinâmicos que façam sentido com os dados.",
            "IMPORTANTE: Retorne a resposta EXATAMENTE no formato JSON puro, contendo estritamente duas chaves: 'report' (string em markdown) e 'html_dashboard' (string com o código HTML completo)."
        ],
        markdown=False
    )
    return agent

def process_spreadsheet_data(file_bytes: bytes, filename: str) -> str:
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif filename.endswith(('.xls', '.xlsx')):
            xls = pd.ExcelFile(io.BytesIO(file_bytes))
            df = None
            for sheet_name in xls.sheet_names:
                temp_df = pd.read_excel(xls, sheet_name=sheet_name)
                if not temp_df.empty and len(temp_df.columns) > 0:
                    df = temp_df
                    break
            if df is None or df.empty or len(df.columns) == 0:
                raise ValueError("Nenhuma aba válida com dados foi encontrada no arquivo Excel.")
        else:
            raise ValueError("Formato de arquivo não suportado. Use CSV ou Excel.")

        if df.empty or len(df.columns) == 0:
            raise ValueError("O arquivo enviado está vazio ou não possui colunas válidas.")

        summary = {
            "columns": list(df.columns),
            "shape": df.shape,
            "head": df.head(10).to_dict(orient="records"),
            "describe": df.describe(include='all').fillna("").to_dict()
        }
        return str(summary)
    except Exception as e:
        raise ValueError(f"Erro ao processar a planilha: {str(e)}")

def process_googlesheets_link(sheet_url: str) -> str:
    if "/edit" in sheet_url:
        export_url = sheet_url.split("/edit")[0] + "/export?format=csv"
    else:
        export_url = sheet_url
        
    df = pd.read_csv(export_url)
    summary = {
        "columns": list(df.columns),
        "shape": df.shape,
        "head": df.head(10).to_dict(orient="records"),
        "describe": df.describe(include='all').fillna("").to_dict()
    }
    return str(summary)
