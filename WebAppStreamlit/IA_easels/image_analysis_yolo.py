from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os

# Caminho para o modelo treinado
model_path = r"C:\Users\Novaes Engenharia\WebAppStreamlit\IA_easels\IAE_src\runs\IAE_model9\weights\best.pt"

# Verificar se o arquivo do modelo existe
if not os.path.exists(model_path):
    print(f"❌ Arquivo do modelo não encontrado no caminho: {model_path}")
    exit()

# Carregar o modelo YOLOv8
try:
    model = YOLO(model_path)
    print(f"✅ Modelo carregado com sucesso: {model_path}")
except Exception as e:
    print(f"❌ Erro ao carregar o modelo: {e}")
    exit()

def analyze_image(image_path):
    """
    Realiza análise de uma imagem usando o modelo YOLOv8 treinado.
    """
    try:
        # Realizar inferência na imagem
        results = model.predict(image_path, conf=0.25)

        # Exibir a imagem com as detecções
        annotated_image = results[0].plot()
        plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.show()

        # Extrair informações das detecções
        detections = results[0].boxes
        detection_results = []
        if len(detections) > 0:
            print("Informações detectadas na imagem:")
            for i, box in enumerate(detections):
                label = model.names[int(box.cls)]
                confidence = box.conf.item()
                bbox = box.xyxy.numpy().astype(int)[0]
                detection_results.append({"label": label, "confidence": confidence, "bbox": bbox})
                print(f"{i+1}. Rótulo: {label}, Confiança: {confidence:.2f}, Caixa delimitadora: {bbox}")
        else:
            print("Nenhuma detecção foi encontrada na imagem.")
        return {"annotated_image": annotated_image, "detections": detection_results}
    except Exception as e:
        print(f"❌ Erro ao analisar a imagem: {e}")
        return None

# Integrando com Streamlit
import streamlit as st

def upload_and_analyze():
    st.title("Analisador de Cavaletes - Upload e Análise")
    st.write("Envie uma imagem para análise e obtenha informações detalhadas.")

    # Upload de imagens
    uploaded_file = st.file_uploader("Selecione uma imagem", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image_path = os.path.join("uploaded_image", uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(image_path, caption=f"Imagem carregada: {uploaded_file.name}", use_column_width=True)

        if st.button("Analisar Imagem"):
            st.write("🔄 Realizando análise da imagem...")
            results = analyze_image(image_path)
            if results:
                st.subheader("Resultados da Análise")
                st.image(results["annotated_image"], caption="Imagem Anotada", use_column_width=True)

                if results["detections"]:
                    st.write("### Detecções:")
                    for detection in results["detections"]:
                        st.write(f"- **Rótulo:** {detection['label']}, **Confiança:** {detection['confidence']:.2f}, **Caixa:** {detection['bbox']}")
                else:
                    st.write("Nenhuma detecção foi encontrada.")
            else:
                st.error("Erro ao realizar a análise da imagem.")

if __name__ == "__main__":
    upload_and_analyze()
