from ultralytics import YOLO
import os

def validate_labels():
    """
    Verifica se há arquivos de rótulos correspondentes às imagens em treinamento e validação.
    """
    train_images_dir = "C:/Users/Novaes Engenharia/WebAppStreamlit/IA_easels/IAE_data/IAE_train"
    train_labels_dir = "C:/Users/Novaes Engenharia/WebAppStreamlit/IA_easels/IAE_data/IAE_train_rotulos"
    val_images_dir = "C:/Users/Novaes Engenharia/WebAppStreamlit/IA_easels/IAE_data/IAE_validation"
    val_labels_dir = "C:/Users/Novaes Engenharia/WebAppStreamlit/IA_easels/IAE_data/IAE_validation_rotulos"

    def check_dir(image_dir, label_dir, mode):
        # Gera nomes de rótulos corretamente sem adicionar `.txt` extra
        images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
        labels = [os.path.splitext(f)[0] + ".txt" for f in images]
        missing_labels = [f for f in labels if not os.path.exists(os.path.join(label_dir, f))]

        if missing_labels:
            raise FileNotFoundError(f"❌ Rótulos ausentes no conjunto {mode}: {missing_labels}")
        else:
            print(f"✅ Todos os rótulos estão presentes no conjunto {mode}.")

    # Verificar rótulos de treinamento
    check_dir(train_images_dir, train_labels_dir, "treinamento")

    # Verificar rótulos de validação
    check_dir(val_images_dir, val_labels_dir, "validação")

def train_yolo_model():
    """
    Treina o modelo YOLOv8 com base no dataset configurado.
    """
    try:
        model_path = "C:/Users/Novaes Engenharia/WebAppStreamlit/IA_easels/IAE_src/yolov8s.pt"
        data_path = "C:/Users/Novaes Engenharia/WebAppStreamlit/IA_easels/IAE_src/dataset.yaml"
        epochs = 50
        imgsz = 640
        batch_size = 16
        save_period = 5
        project_name = "IAE_model"
        verbose = True

        # Verificar se o modelo base existe
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"❌ Modelo base não encontrado: {model_path}")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"❌ Arquivo de configuração do dataset não encontrado: {data_path}")

        # Validar rótulos
        validate_labels()

        # Carregar o modelo base
        model = YOLO(model_path)
        if verbose:
            print(f"✅ Modelo base '{model_path}' carregado com sucesso.")

        # Treinar o modelo
        print("🛠️ Iniciando treinamento...")
        model.train(
            data=data_path,        # Arquivo de configuração do dataset
            epochs=epochs,         # Número de épocas
            imgsz=imgsz,           # Resolução das imagens
            batch=batch_size,      # Tamanho do batch
            name=project_name,     # Nome do projeto
            save_period=save_period,  # Salva checkpoints a cada `save_period` épocas
            project="C:/Users/Novaes Engenharia/WebAppStreamlit/IA_easels/IAE_src/runs",  # Diretório principal de saída
            verbose=verbose,       # Controle de logs detalhados
        )
        print(f"✅ Treinamento concluído! Pesos finais salvos em 'runs/detect/{project_name}/weights/best.pt'.")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except Exception as e:
        print(f"❌ Erro durante o treinamento: {e}")

if __name__ == "__main__":
    train_yolo_model()
