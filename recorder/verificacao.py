import os


class Verificar:
    pastas = {"fx": False, "output": False}
    efeitos = []

    def verificar_pastas(self):
        try:
            os.mkdir("fx")
            self.pastas["fx"] = True
        except:
            self.pastas["fx"] = True
        try:
            os.mkdir("output")
            self.pastas["output"] = True
        except:
            self.pastas["output"] = True

    def obter_efeitos(self):
        efeitos = os.listdir("fx")
        for i in range(len(efeitos)):
            efeitos[i] = str(efeitos[i]).replace(".wav", "")
        self.efeitos = efeitos

    def __init__(self):
        print("Checking...")
        self.verificar_pastas()
        self.obter_efeitos()
        print("Check complete")
        os.system("cls")
