import pandas as pd
from src.classification_workflow_logic.classification_workflow_handler import ClassificationWorkflowHandler

if __name__ == "__main__":
    # Criar uma instância do ClassificationWorkflowHandler
    classification_handler = ClassificationWorkflowHandler()

    # Ler o arquivo CSV
    df = pd.read_csv('../dataframe/src/Alesp/Alesp_dataframe_part_1.csv',delimiter='|',encoding='utf-8').iloc[0]
    
    # Iterar sobre cada linha do DataFrame
    for index, row in df.iterrows():
        lemmatized_text = row['lemmatized_text']
        extracted_toponyms = row['extracted_toponyms'].strip('[]').replace("'", "").split(', ')

        # Calcular a confiança de ser um toponímico para cada palavra extraída
        for toponym in extracted_toponyms:
            confidence = classification_handler.calculate_toponym_confidence(toponym, lemmatized_text)
            # Imprimir o texto lematizado, a palavra e a porcentagem de confiança em linhas diferentes
            print(f"Texto lematizado: '{lemmatized_text}'")
            print(f"Palavra: '{toponym}'")
            print(f"Porcentagem de confiança: {confidence:.2f}\n")