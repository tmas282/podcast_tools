from datetime import datetime
import keyboard
import pyaudio as pa
import wave as wv
import time
import os


class Audio:
    CHUNK = 1024
    FORMAT = pa.paInt16
    CHANNELS = 2
    RATE = 44100
    p = pa.PyAudio()
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    frames = []
    a_gravar = True
    fx: list[str]

    def gravar_audio(self):
        tempo_inicial = datetime.now()
        while self.a_gravar:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            os.system("cls")
            print("Duration: {}seg".format((datetime.now() - tempo_inicial).seconds))
            if keyboard.is_pressed("0"):
                self.parar_gravacao()

            for efeito in self.fx:
                if keyboard.is_pressed(efeito):
                    print("FX running...")
                    self.adicionar_fx(efeito)

    def adicionar_fx(self, fx_nome: str):
        fx = wv.open("fx/" + fx_nome + ".wav", "rb")
        duration_seconds = fx.getnframes() / fx.getframerate()
        self.frames.append(fx.readframes(fx.getnframes()))
        time.sleep(duration_seconds)

    def parar_gravacao(self):
        nome_do_ficheiro = str(input("Record name: "))
        self.a_gravar = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        wf = wv.open("output/" + nome_do_ficheiro + ".wav", "wb")
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b"".join(self.frames))
        wf.close()

    def __init__(self, fx: list[str]):
        self.fx = fx
