import pygame
import sys

pygame.init()

# Inicializa o joystick
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Nenhum joystick encontrado.")
    sys.exit()

# Pega o primeiro joystick disponível
joystick = pygame.joystick.Joystick(0)
joystick.init()

try:
    while True:
        pygame.event.pump()  # Atualiza os eventos

        # Verifica os eventos dos botões
        for i in range(joystick.get_numbuttons()):
            if joystick.get_button(i):
                print(f"Botão {i} pressionado")

        # Verifica os eventos dos eixos
        for i in range(joystick.get_numaxes()):
            axis_value = joystick.get_axis(i)
            if i == 4 or i == 5:  # Índices dos eixos analógicos dos gatilhos para controle Xbox
                if axis_value > -1:
                    print(f"Gatilho {i}: {axis_value}")

        # Adicione este trecho para imprimir os índices dos botões
        for i in range(joystick.get_numbuttons()):
            print(f"Botão {i}: {joystick.get_button(i)}")

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
    sys.exit()