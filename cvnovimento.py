import cv2
import mediapipe as mp
import numpy as np
import time

# --- Configurações e Inicializações ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# OpenCV - Captura de Vídeo
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera.")
    exit()

# --- Configurações do Desenho (Cores, etc.) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (0, 165, 255)

draw_color = RED
brush_thickness = 15
eraser_thickness = 50
xp, yp = 0, 0

# --- Interface da Paleta de Cores ---
color_palette_height = 70
color_options = [
    {"color": RED, "name": "R"},
    {"color": GREEN, "name": "G"},
    {"color": BLUE, "name": "B"},
    {"color": YELLOW, "name": "Y"},
    {"color": PURPLE, "name": "P"},
    {"color": ORANGE, "name": "O"},
    {"color": WHITE, "name": "Eraser"},
    {"color": BLACK, "name": "Clear"}
]
num_colors = len(color_options)
color_rect_width = 0  # Será definido após obter wCam

# --- Constantes dos Dedos ---
INDEX_FINGER_TIP_ID = 8
MIDDLE_FINGER_TIP_ID = 12

# --- Variáveis de Controle de Inicialização ---
wCam, hCam = 0, 0  # Serão definidas pelo primeiro frame
canvas = None
initialized = False

try:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignorando frame vazio da câmera.")
            continue

        # Inicialização baseada no primeiro frame bem-sucedido
        if not initialized:
            hCam, wCam, _ = frame.shape
            print(f"Dimensões da câmera: {wCam}x{hCam}")
            # Tentar definir as dimensões da câmera (pode não funcionar em todas as câmeras)
            # cap.set(3, wCam)
            # cap.set(4, hCam)
            # Se você quiser forçar uma resolução específica (e redimensionar se necessário):
            # wCam_target, hCam_target = 1280, 720
            # frame = cv2.resize(frame, (wCam_target, hCam_target))
            # hCam, wCam, _ = frame.shape # Atualiza com as dimensões alvo

            canvas = np.zeros((hCam, wCam, 3), np.uint8)
            color_rect_width = wCam // num_colors
            initialized = True

        if not initialized or canvas is None:  # Garante que o canvas foi criado
            continue

        image = cv2.flip(frame, 1)
        # Se você forçou uma resolução acima, não precisa de resize aqui
        # Caso contrário, se o frame tiver dimensões diferentes do wCam/hCam alvo, redimensione
        # if image.shape[1] != wCam or image.shape[0] != hCam:
        #    image = cv2.resize(image, (wCam, hCam)) # Garante que image e canvas têm o mesmo tamanho

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        # Desenhar a paleta de cores
        for i, option in enumerate(color_options):
            x1_color = i * color_rect_width
            x2_color = (i + 1) * color_rect_width
            cv2.rectangle(image, (x1_color, 0), (x2_color, color_palette_height), option["color"], -1)
            text_color = BLACK if np.mean(option["color"]) > 127 or option["name"] == "Eraser" else WHITE
            if option["name"] == "Clear": text_color = WHITE
            cv2.putText(image, option["name"], (x1_color + 5, color_palette_height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
            if draw_color == option["color"] and option["name"] != "Clear":
                highlight_color = (200, 200, 200) if np.mean(option["color"]) < 10 else (50, 50, 50)
                cv2.rectangle(image, (x1_color, 0), (x2_color, color_palette_height), highlight_color, 4)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                index_finger_tip = landmarks[INDEX_FINGER_TIP_ID]
                ix, iy = int(index_finger_tip.x * wCam), int(index_finger_tip.y * hCam)
                middle_finger_tip = landmarks[MIDDLE_FINGER_TIP_ID]
                mx, my = int(middle_finger_tip.x * wCam), int(middle_finger_tip.y * hCam)

                index_pip_y = landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * hCam
                middle_pip_y = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * hCam
                index_up = iy < index_pip_y
                middle_up = my < middle_pip_y

                indicator_brush_color = BLACK if draw_color == WHITE else draw_color
                cv2.circle(image, (ix, iy), brush_thickness // 2, indicator_brush_color, cv2.FILLED)

                if iy < color_palette_height + 10:
                    xp, yp = 0, 0
                    if index_up and not middle_up:
                        for i, option in enumerate(color_options):
                            x1_color = i * color_rect_width
                            x2_color = (i + 1) * color_rect_width
                            if x1_color < ix < x2_color:
                                if option["name"] == "Clear":
                                    canvas = np.zeros((hCam, wCam, 3), np.uint8)
                                elif option["name"] == "Eraser":
                                    draw_color = WHITE
                                else:
                                    draw_color = option["color"]
                                break
                elif index_up and middle_up and iy > color_palette_height + 10:
                    distance_index_middle = np.sqrt((ix - mx) ** 2 + (iy - my) ** 2)
                    if distance_index_middle < 70:
                        cv2.putText(image, "DESENHANDO", (50, hCam - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                                    cv2.LINE_AA)
                        if xp == 0 and yp == 0: xp, yp = ix, iy
                        current_brush_size = eraser_thickness if draw_color == WHITE else brush_thickness
                        cv2.line(canvas, (xp, yp), (ix, iy), draw_color, current_brush_size)
                        xp, yp = ix, iy
                    else:
                        cv2.putText(image, "MOVENDO", (50, hCam - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                                    cv2.LINE_AA)
                        xp, yp = 0, 0
                elif index_up and not middle_up and iy > color_palette_height + 10:
                    cv2.putText(image, "MOVENDO", (50, hCam - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                                cv2.LINE_AA)
                    xp, yp = 0, 0
                else:
                    xp, yp = 0, 0
        else:
            xp, yp = 0, 0

        # Debug: Verificar dimensões antes da operação crítica
        # print(f"Shape image: {image.shape}, Shape canvas: {canvas.shape}")

        mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        # print(f"Shape mask_inv: {mask_inv.shape}") # Deve ser (hCam, wCam)

        img_bg = cv2.bitwise_and(image, image, mask=mask_inv)
        img_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
        final_image = cv2.add(img_bg, img_fg)

        cv2.imshow("Quadro de Desenho Virtual", final_image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Programa interrompido pelo usuário.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")  # Captura outras exceções
    import traceback

    traceback.print_exc()  # Imprime o traceback completo
finally:
    print("Encerrando...")
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    if 'hands' in locals() and hands:
        hands.close()