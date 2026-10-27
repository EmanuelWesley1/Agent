import time
import json
import traceback
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent import create_dashboard_agent, process_spreadsheet_data, process_googlesheets_link

app = FastAPI(title="AI Dashboard & Report Generator API", version="2.6")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODELS_TO_TRY = ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-1.5-pro"]

@app.post("/api/generate-from-file")
async def generate_from_file(file: UploadFile = File(...)):
    contents = await file.read()
    data_summary = process_spreadsheet_data(contents, file.filename)
    
    prompt = f"""
    Aqui está o resumo estatístico e os dados de amostra da planilha enviada pelo usuário:
    {data_summary}
    
    Por favor, gere o relatório executivo e o código HTML/JS do dashboard interativo em formato JSON.
    """
    
    last_exception = None
    
    for model_id in MODELS_TO_TRY:
        try:
            print(f"Executando agente com o modelo: {model_id}...")
            agent = create_dashboard_agent(model_id=model_id)
            response = agent.run(prompt)
            
            if not response or not response.content:
                raise ValueError("O agente retornou uma resposta vazia.")
                
            content_str = response.content.strip()
            
            # Remove blocos markdown caso a IA envie
            if content_str.startswith("```json"):
                content_str = content_str[7:]
            if content_str.startswith("```"):
                content_str = content_str[3:]
            if content_str.endswith("```"):
                content_str = content_str[:-3]
                
            result_dict = json.loads(content_str.strip())
            
            formatted_result = {
                "report": result_dict.get("report") or result_dict.get("Relatorio") or "Relatório não disponível.",
                "html_dashboard": result_dict.get("html_dashboard") or result_dict.get("html") or "<p>Dashboard não gerado.</p>"
            }
            
            print(f"Sucesso com o modelo: {model_id}!")
            return {"result": formatted_result}
            
        except Exception as e:
            last_exception = str(e)
            print(f"Falha ao tentar {model_id}: {last_exception}")
            time.sleep(1)
            continue

    raise HTTPException(
        status_code=500, 
        detail=f"Não foi possível gerar com nenhum dos modelos configurados. Último erro: {last_exception}"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
