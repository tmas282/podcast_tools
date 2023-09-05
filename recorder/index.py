import PySimpleGUI as sg
from audio import Audio
from verificacao import Verificar

sg.theme("DarkAmber")

verificacao = Verificar()

with open("img/icon.png", "rb") as img:
    icon = img.read()
    img.close()
janela = sg.Window(
    title="PodRecorder",
    layout=[
        [sg.Text("PodRecorder", font=("Helvetica", 48), justification="center")],
        [sg.Button("Record")],
    ],
    resizable=True,
    icon=icon
)

while True:
    event, values = janela.read()
    if event == sg.WIN_CLOSED:
        janela.close()
        break
    elif event == "Record":
        janela.close()
        obj = Audio(verificacao.efeitos)
        break
