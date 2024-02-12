import cv2
import pygame

global zoom_factor
zoom_factor = 1.0
global position_x, position_y
position_x, position_y = 0, 0

def zoom(frame, scale=1.0, axis_x=0.0, axis_y=0.0):
    global zoom_factor, position_x, position_y

    height, width = frame.shape[:2]

    new_height, new_width = int(height * scale), int(width * scale)
    zoomed_frame = cv2.resize(frame, (new_width, new_height))

    # Ajusta a posição vertical com base no eixo Y do joystick
    position_y -= int(axis_y * 10 * zoom_factor)

    start_x = (new_width - width) // 2
    start_y = (new_height - height) // 2

    # Ajusta a posição horizontal com base no eixo X do joystick
    position_x -= int(axis_x * 10 * zoom_factor)

    start_x -= position_x
    start_y -= position_y

    start_x = max(min(start_x, new_width - width), 0)
    start_y = max(min(start_y, new_height - height), 0)

    zoomed_frame = zoomed_frame[start_y:start_y + height, start_x:start_x + width]

    return zoomed_frame

def main():
    axis_x = 0
    axis_y = 0
    global zoom_factor, position_x, position_y

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    pygame.init()

    if pygame.joystick.get_count() == 0:
        print("Nenhum joystick encontrado.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Joystick detectado: {joystick.get_name()}")

    ret, frame = cap.read()
    height, width = frame.shape[:2]

    # Criar a janela sem exibi-la
    cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Webcam', 800, int(800 * (height / width)))  # Ajuste o tamanho conforme necessário

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    axis_x = joystick.get_axis(0)
                    axis_y = joystick.get_axis(1)

                    global zoom_factor, position_x, position_y

                    # Atualiza a posição da câmera com base nos eixos do joystick
                    position_x -= int(axis_x * 10 * zoom_factor)
                    position_y -= int(axis_y * 10 * zoom_factor)

                    if joystick.get_axis(5) > -1:
                        zoom_factor += 0.05
                    elif joystick.get_axis(4) > -1:
                        zoom_factor -= 0.05

                    zoom_factor = max(1.0, zoom_factor)

            ret, frame = cap.read()
            zoomed_frame = zoom(frame, zoom_factor, axis_x, axis_y)

            # Redimensionar o frame para se ajustar à janela
            resized_frame = cv2.resize(zoomed_frame, (800, int(800 * (height / width))))  # Ajuste o tamanho conforme necessário

            # Exibir o frame na janela OpenCV
            cv2.imshow('Webcam', resized_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        joystick.quit()
        pygame.quit()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()