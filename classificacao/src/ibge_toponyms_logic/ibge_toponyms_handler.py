import os
import pandas as pd

class IbgeToponymsHandler:
    def __init__(self, data_folder='classificacao/src/ibge_toponyms_logic/data/'):
        self.data_folder = data_folder
        self.toponyms = None

    def get_toponyms(self):
        if self.toponyms is None:
            toponyms = set()
            for file_name in os.listdir(self.data_folder):
                if file_name.endswith('.xls'):
                    file_path = os.path.join(self.data_folder, file_name)
                    try:
                        df = pd.read_excel(file_path)
                        toponyms.update(df['NOME_ANTERIOR'].dropna().unique())
                        toponyms.update(df['NOME_ATUAL'].dropna().unique())
                    except Exception as e:
                        print(f"Erro ao ler o arquivo {file_name}: {e}")

            self.toponyms = list(toponyms)

        return self.toponyms

# Exemplo de uso do IbgeToponymsHandler
if __name__ == "__main__":
    toponym_handler = IbgeToponymsHandler()
    toponyms = toponym_handler.get_toponyms()
    print("Lista de toponímicos:")
    for toponym in toponyms:
        print(toponym)
