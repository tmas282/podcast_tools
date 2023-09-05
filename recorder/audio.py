from datetime import datetime
import pyaudio as pa, wave as wv, PySimpleGUI as sg


class Audio:
    CHUNK = 1024
    FORMAT = pa.paInt16
    CHANNELS = 2
    RATE = 44100
    p = pa.PyAudio()
    stream_output = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=False,
        output=True,
        frames_per_buffer=CHUNK,
    )
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    frames = []
    a_gravar = False
    fx: list[str]
    fx_status = {"a_decorrer": False, "fx": "", "pos": 0}

    def gravar_audio(self, fx=None):
        mic = self.stream.read(self.CHUNK)
        if fx:
            self.fx_status["a_decorrer"] = True
            self.fx_status["fx"] = fx
            self.fx_status["pos"] = 0
        if self.fx_status["a_decorrer"]:
            with wv.open(f"fx/{self.fx_status['fx']}.wav", "rb") as wf:
                if (self.fx_status["pos"] + len(mic)) > wf.getnframes():
                    wf.setpos(pos=self.fx_status["pos"])
                    fx_frame = wf.readframes(wf.getnframes() - self.fx_status["pos"])
                    self.fx_status["a_decorrer"] = False
                else:
                    wf.setpos(pos=self.fx_status["pos"])
                    fx_frame = wf.readframes(len(mic))
                    self.fx_status["pos"] += len(mic)
                wf.close()
            self.frames.append(fx_frame)
            self.stream_output.write(fx_frame)
        else:
            self.frames.append(mic)
            self.stream_output.write(mic)

    def parar_gravacao(self, nome_do_ficheiro: str):
        self.stream.stop_stream()
        self.stream.close()
        self.stream_output.stop_stream()
        self.stream_output.close()
        self.p.terminate()
        wf = wv.open("output/" + nome_do_ficheiro + ".wav", "wb")
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b"".join(self.frames))
        wf.close()

    def __init__(self, fx: list[str]):
        self.fx = fx
        with open("img/icon.png", "rb") as img:
            icon = img.read()
            img.close()
        layout = [
            [
                sg.Text("Is an FX running? False", key="-fx_status-"),
            ],
            [sg.Text("Before start recording, change the name of the audio file.")],
            [sg.InputText("Nome da gravação...", key="-NOME_FICHEIRO-")],
            [
                sg.Button("Gravar", size=(10, 2), key="-GRAVAR-"),
                sg.Text("Duração:"),
                sg.Text("0 seg", key="-DURACAO-"),
            ],
        ]
        temp = []
        for i in fx:
            temp.append(sg.Button(button_text=f"FX: {i}", key=i))
        layout.append(temp)
        janela = sg.Window(
            "Gravador",
            layout=layout,
            resizable=True,
            icon=icon
        )
        while True:
            event, values = janela.read(timeout=1)
            if event == sg.WIN_CLOSED:
                break
            elif event == "-GRAVAR-":
                if self.a_gravar:
                    janela["-GRAVAR-"].update("Gravar")
                    self.a_gravar = False
                    if values["-NOME_FICHEIRO-"] == "Nome da gravação...":
                        self.parar_gravacao("episodio")
                    else:
                        self.parar_gravacao(values["-NOME_FICHEIRO-"])
                    break
                else:
                    janela["-GRAVAR-"].update("Parar")
                    self.a_gravar = True
                    tempo_inicial = datetime.now()
            if self.a_gravar == True:
                janela["-DURACAO-"].update(
                    f"{(datetime.now() - tempo_inicial).seconds} seg"
                )
                passou = False
                for i in fx:
                    if event == i:
                        self.gravar_audio(fx=i)
                        passou = True
                if not passou:
                    self.gravar_audio()
                janela["-fx_status-"].update(
                    f"Is an FX running? {self.fx_status['a_decorrer']}"
                )
        janela.close()
