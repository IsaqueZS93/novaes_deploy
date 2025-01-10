import streamlit as st
from PIL import Image, ImageDraw
import os
import subprocess

# Diretórios base
BASE_DIR = r"C:\Users\Novaes Engenharia\WebAppStreamlit\IA_easels\IAE_data"
TRAIN_IMAGES_DIR = os.path.join(BASE_DIR, "IAE_train")
VAL_IMAGES_DIR = os.path.join(BASE_DIR, "IAE_validation")
TRAIN_LABELS_DIR = os.path.join(BASE_DIR, "IAE_train_rotulos")
VAL_LABELS_DIR = os.path.join(BASE_DIR, "IAE_validation_rotulos")

# Garantir que os diretórios existem
os.makedirs(TRAIN_IMAGES_DIR, exist_ok=True)
os.makedirs(VAL_IMAGES_DIR, exist_ok=True)
os.makedirs(TRAIN_LABELS_DIR, exist_ok=True)
os.makedirs(VAL_LABELS_DIR, exist_ok=True)

# Mapeamento de cores para as classes
CLASS_COLORS = {
    "lacre_azul": "blue",
    "lacre_vermelho": "red",
    "hidrômetro_novo": "green",
    "hidrômetro_velho": "orange",
    "hidrômetro_enterrado": "purple",
    "calçada_danificada": "brown",
    "calçada_ok": "black",
    "muro_danificado": "yellow",
    "entulhos": "gray"
}

# Função para salvar imagem e rótulos no formato YOLO
def save_image_and_labels(image, labels, prefix, filename):
    sanitized_filename = os.path.splitext(filename)[0]  # Remover extensões desnecessárias

    # Diretórios para salvar
    if prefix == "train":
        image_path = os.path.join(TRAIN_IMAGES_DIR, f"{sanitized_filename}.jpg")
        label_path = os.path.join(TRAIN_LABELS_DIR, f"{sanitized_filename}.txt")
    else:  # val
        image_path = os.path.join(VAL_IMAGES_DIR, f"{sanitized_filename}.jpg")
        label_path = os.path.join(VAL_LABELS_DIR, f"{sanitized_filename}.txt")

    # Salvar imagem
    image.save(image_path)

    # Salvar rótulos no formato YOLO
    with open(label_path, "w") as f:
        for label in labels:
            class_id, x1, y1, x2, y2 = label[:5]
            x_center = (x1 + x2) / 2 / image.width
            y_center = (y1 + y2) / 2 / image.height
            width = (x2 - x1) / image.width
            height = (y2 - y1) / image.height
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    st.success(f"Imagem e rótulos salvos no conjunto '{prefix}'.")
    return image_path, label_path

# Função para iniciar validação e rotulagem
def run_validation():
    st.title("IAE: Validação e Rotulagem de Imagens")
    st.write("Carregue uma imagem para adicionar ou ajustar rótulos manualmente.")

    uploaded_image = st.file_uploader("Envie uma imagem", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        image = image.convert("RGB")  # Garantir formato RGB

        # Lista de rótulos
        labels = []

        # Configuração dos rótulos
        num_boxes = st.number_input("Quantos rótulos deseja adicionar?", min_value=1, step=1, value=1)
        for i in range(num_boxes):
            st.write(f"### Rótulo {i + 1}:")
            x1 = st.slider(f"Coordenada X1 do rótulo {i + 1}", 0, image.width, 0)
            y1 = st.slider(f"Coordenada Y1 do rótulo {i + 1}", 0, image.height, 0)
            x2 = st.slider(f"Coordenada X2 do rótulo {i + 1}", x1, image.width, image.width)
            y2 = st.slider(f"Coordenada Y2 do rótulo {i + 1}", y1, image.height, image.height)
            cls = st.selectbox(f"Classe do rótulo {i + 1}", options=list(CLASS_COLORS.keys()), index=0)

            cls_index = list(CLASS_COLORS.keys()).index(cls)
            labels.append([cls_index, x1, y1, x2, y2])

        # Exibir imagem com rótulos
        annotated_image = image.copy()
        draw = ImageDraw.Draw(annotated_image)
        for label in labels:
            _, x1, y1, x2, y2 = label
            color = CLASS_COLORS[list(CLASS_COLORS.keys())[label[0]]]
            draw.rectangle([x1, y1, x2, y2], outline=color, width=2)

        st.image(annotated_image, caption="Imagem com Rótulos", use_column_width=True)

        # Salvar rótulos
        st.subheader("Salvar Rótulos Ajustados")
        prefix = st.selectbox("Salvar em:", ["train", "val"])
        save_button = st.button("Salvar Imagem e Rótulos")

        if save_button:
            save_image_and_labels(image, labels, prefix, uploaded_image.name)

    # Botão para retrainar modelo
    if st.button("Retrainar Modelo"):
        st.write("🔄 Retrainando o modelo...")
        result = subprocess.run(
            ["python", "IAE_train_magic.py"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            st.success("✅ Modelo retrainado com sucesso!")
        else:
            st.error("❌ Erro ao retrainar o modelo.")
            st.error(result.stderr)

if __name__ == "__main__":
    run_validation()
