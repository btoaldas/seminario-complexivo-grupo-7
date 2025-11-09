import joblib
import os


def guardar_archivos_modelo(modelo, encoder, model_path, encoder_path, club_encoding=None):
    """
    Guarda el modelo entrenado, el encoder y opcionalmente el club_encoding
    
    Args:
        modelo: Modelo entrenado (RandomForestRegressor o LinearRegression)
        encoder: OneHotEncoder para variables categóricas
        model_path: Ruta donde guardar el modelo
        encoder_path: Ruta donde guardar el encoder
        club_encoding: Diccionario de Target Encoding para club (opcional)
    
    Returns:
        bool: True si se guardó exitosamente, False si hubo error
    """
    try:
        MODEL_DIR = os.path.dirname(model_path)
        os.makedirs(MODEL_DIR, exist_ok=True)
        
        # Guardar encoder
        joblib.dump(encoder, encoder_path)
        print(f'✓ Encoder guardado en: {encoder_path}')
        
        # Guardar modelo
        joblib.dump(modelo, model_path)
        print(f'✓ Modelo guardado en: {model_path}')
        
        # Guardar club_encoding si existe
        if club_encoding is not None:
            club_encoding_path = os.path.join(MODEL_DIR, "club_encoding_fifa.joblib")
            joblib.dump(club_encoding, club_encoding_path)
            print(f'✓ Club Encoding guardado en: {club_encoding_path}')
        
        return True
    except Exception as e:
        print(f'✗ Error al guardar los archivos: {e}')
        return False
