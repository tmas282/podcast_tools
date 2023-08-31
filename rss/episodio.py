import csv
import wave as wv
import pyaudio as pa
from index import API_KEY


class Episodios:
    CHUNK = 1024
    FORMAT = pa.paInt16
    p = pa.PyAudio()
    CHANNELS = 2
    RATE = 44100

    def ver_episodios(self):
        with open("episodios.csv", "r", encoding="utf-8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=";")
            rows = []
            for row in spamreader:
                rows.insert(0,row)
            return rows

    def submeter_episodio(self,api_key: str,nome_ep: str,desc_ep: str,nome_ficheiro: str,ficheiro: bytes):
        if api_key == API_KEY:
            with open("episodios.csv", "a", encoding="utf-8") as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=";")
                spamwriter.writerow([nome_ep, desc_ep, nome_ficheiro])
                csvfile.close()
            wf = wv.open("public/audio/{}.wav".format(nome_ficheiro), "wb")
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(ficheiro)
            wf.close()
            return True
        else:
            return False
