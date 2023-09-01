import time
import keyboard
import os
from audio import Audio
from verificacao import Verificar
from submit import Submit

verificacao = Verificar()
print(
    """
██████╗░░█████╗░██████╗░  ██████╗░███████╗░█████╗░░█████╗░██████╗░██████╗░███████╗██████╗░
██╔══██╗██╔══██╗██╔══██╗  ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██████╔╝██║░░██║██║░░██║  ██████╔╝█████╗░░██║░░╚═╝██║░░██║██████╔╝██║░░██║█████╗░░██████╔╝
██╔═══╝░██║░░██║██║░░██║  ██╔══██╗██╔══╝░░██║░░██╗██║░░██║██╔══██╗██║░░██║██╔══╝░░██╔══██╗
██║░░░░░╚█████╔╝██████╔╝  ██║░░██║███████╗╚█████╔╝╚█████╔╝██║░░██║██████╔╝███████╗██║░░██║
╚═╝░░░░░░╚════╝░╚═════╝░  ╚═╝░░╚═╝╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝                                                                           
"""
)
print("[0] - Record Podcast Episode")
print("[1] - Send Podcast Episode")
while True:
    if keyboard.is_pressed("0"):
        os.system("cls")
        print(
            "Starting to record... (Press the key 0 to stop)\nThe Fx named 1.wav, 2.wav, etc.. are the binded keys 1,2, etc... respectively"
        )
        print("3 sec")
        time.sleep(1)
        print("2 sec")
        time.sleep(1)
        print("1 sec")
        time.sleep(1)
        print("Starting")
        gravacao = Audio(verificacao.efeitos)
        gravacao.gravar_audio()
        break
    elif keyboard.is_pressed("1"):
        Submit(
            str(input("File name: ")),
            str(input("Episode name: ")),
            str(input("Episode Description: ")),
        )
        break
