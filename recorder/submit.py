import requests, os, subprocess


class Submit:
    API_KEY = "your api key"
    URL_ENDPOINT = "your api endpoint"

    def __init__(self, nome_ficheiro: str, nome_episodio: str, desc_episodio: str):
        self.optimize_file(nome_ficheiro)
        self.send_file(
            nome_episodio=nome_episodio,
            nome_ficheiro=nome_ficheiro,
            desc_episodio=desc_episodio,
        )

    def optimize_file(self, nome_ficheiro: str):
        try:
            cmd = [
                "./ffmpeg",
                "-i",
                f"output/{nome_ficheiro}.wav",
                "-c:a",
                "aac",
                f"output/{nome_ficheiro}.aac",
            ]
            subprocess.run(cmd)
            os.remove(f"output/{nome_ficheiro}.wav")
        except:
            pass
        os.system("cls")

    def send_file(self, nome_episodio: str, desc_episodio: str, nome_ficheiro: str):
        audio = open(f"output/{nome_ficheiro}.aac", "rb")
        data = audio.read()
        audio.close()
        headers = {
            "x-api-key": self.API_KEY,
            "name-ep": nome_episodio,
            "desc-ep": desc_episodio,
            "name-file": nome_ficheiro,
            "Content-Type": "audio/aac",
        }
        requests.post(url=self.URL_ENDPOINT, headers=headers, data=data)
