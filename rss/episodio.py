import csv

API_KEY = "Your api key"


class Episodios:
    CHUNK = 1024
    CHANNELS = 2
    RATE = 44100

    def ver_episodios(self):
        rows = []
        try:
            with open("episodios.csv", "r", encoding="utf-8") as csvfile:
                spamreader = csv.reader(csvfile, delimiter=";")
                for row in spamreader:
                    rows.insert(0, row)
                return rows
        except:
            return rows

    def submeter_episodio(
        self,
        api_key: str,
        nome_ep: str,
        desc_ep: str,
        nome_ficheiro: str,
        ficheiro: bytes,
    ):
        if api_key == API_KEY:
            with open("episodios.csv", "a", encoding="utf-8") as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=";")
                spamwriter.writerow([nome_ep, desc_ep, nome_ficheiro])
                csvfile.close()
            with open(f"public/audio/{nome_ficheiro}.aac", "wb") as audio_file:
                audio_file.write(ficheiro)
                audio_file.close()
            return True
        else:
            return False
