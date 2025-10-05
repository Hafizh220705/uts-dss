from fastapi import FastAPI, HTTPException
import numpy as np
import pandas as pd

from .schemas import DSSPayload, AHPPayload
from .core.dss_methods import calculate_saw, calculate_wp, calculate_topsis, calculate_ahp_weights

app = FastAPI(title="DSS Calculation API")

@app.post("/calculate-ahp-weights")
def get_ahp_weights(payload: AHPPayload):
    try:
        bobot, cr = calculate_ahp_weights(payload.comparison_matrix)
        
        status = "Konsisten" if cr <= 0.1 else "Tidak Konsisten"
            
        return {
            "calculation_success": True,
            "weights": bobot.tolist(),
            "consistency_ratio": cr,
            "consistency_status": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan saat perhitungan AHP: {e}")

@app.post("/calculate")
def calculate_dss(payload: DSSPayload):
    try:
        criteria_df = pd.DataFrame([c.dict() for c in payload.criteria])
        alternatives_df = pd.DataFrame(payload.alternatives).set_index('alternatif')
        
        criteria_names = criteria_df['Kriteria'].tolist()
        alternatives_df = alternatives_df[criteria_names]

        data = alternatives_df.to_numpy()
        bobot = criteria_df['Bobot'].to_numpy()
        tipe_kriteria = criteria_df['Tipe'].tolist()
        
        if payload.method == 'saw' or payload.method == 'ahp':
            scores, rank_indices = calculate_saw(data, bobot, tipe_kriteria)
        elif payload.method == 'wp':
            scores, rank_indices = calculate_wp(data, bobot, tipe_kriteria)
        elif payload.method == 'topsis':
            scores, rank_indices = calculate_topsis(data, bobot, tipe_kriteria)
        else:
            raise HTTPException(status_code=400, detail=f"Metode '{payload.method}' tidak valid.")

        sorted_alternatives = alternatives_df.index[rank_indices].tolist()
        sorted_scores = scores[rank_indices]

        result = [
            {"Alternatif": alt, "Skor": round(float(score), 4), "Peringkat": i + 1}
            for i, (alt, score) in enumerate(zip(sorted_alternatives, sorted_scores))
        ]

        return {
            "method": payload.method,
            "calculation_success": True,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan saat pemrosesan: {e}")