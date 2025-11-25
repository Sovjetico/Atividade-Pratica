import random
import time
import tkinter as tk
import winsound


# -------------------------------
# CLASSES DAS FRUTAS
# -------------------------------
class Fruta:
    def __init__(self, nome, emoji, chance):
        self.nome = nome
        self.emoji = emoji
        self.chance = chance

    def __str__(self):
        return self.emoji


class Cereja(Fruta):
    def __init__(self):
        super().__init__("Cereja", "🍒", 0.2)


class Limao(Fruta):
    def __init__(self):
        super().__init__("Limão", "🍋", 0.5)


class Melancia(Fruta):
    def __init__(self):
        super().__init__("Melancia", "🍉", 0.3)


# -------------------------------
# CLASSE DO CASSINO
# -------------------------------
class Cassino:
    def __init__(self):
        self.frutas = [Cereja(), Limao(), Melancia()]

    def verificar_resultado(self, roleta):
        if roleta[0].nome == roleta[1].nome == roleta[2].nome:
            return "JACKPOT"
        elif (roleta[0].nome == roleta[1].nome or
              roleta[1].nome == roleta[2].nome or
              roleta[0].nome == roleta[2].nome):
            return "PAR"
        else:
            return "NADA"


# -------------------------------
# CLASSE ROLETA (HERDA DE CASSINO)
# -------------------------------
class Roleta(Cassino):
    def __init__(self):
        super().__init__()

    def girar_roleta(self):
        pesos = [f.chance for f in self.frutas]
        return random.choices(self.frutas, weights=pesos, k=3)


# -------------------------------
# INTERFACE TKINTER
# -------------------------------
class CassinoGUI:
    def __init__(self, root):
        self.roleta = Roleta()
        self.root = root
        self.root.title("🎰 Cassino Python")
        self.root.geometry("400x400")
        self.root.configure(bg="#222")

        # Título
        self.label_titulo = tk.Label(root, text="🎰 Cassino da Sorte 🎰",
                                     font=("Arial", 20, "bold"), fg="gold", bg="#222")
        self.label_titulo.pack(pady=20)

        # Mostrador da roleta
        self.roleta_label = tk.Label(root, text="🍋 🍉 🍒",
                                     font=("Arial", 50), bg="#222")
        self.roleta_label.pack(pady=40)

        # Botão de girar
        self.botao_girar = tk.Button(root, text="GIRAR 🎲", command=self.jogar,
                                     font=("Arial", 16, "bold"), bg="gold", fg="black",
                                     activebackground="#ffcc00", padx=20, pady=10)
        self.botao_girar.pack(pady=10)

        # Resultado
        self.resultado_label = tk.Label(root, text="", font=("Arial", 14, "bold"),
                                        fg="white", bg="#222")
        self.resultado_label.pack(pady=20)

    # ------------------------------------
    # FUNÇÕES PARA TOCAR OS SONS
    # ------------------------------------
    
    def som_inicio(self):
        # Toca o som de início do giro
        winsound.PlaySound("start.wav", winsound.SND_FILENAME)

    def som_vitoria(self):
        # Toca o som de vitória total (JACKPOT)
        winsound.PlaySound("win.wav", winsound.SND_FILENAME)

    def som_parcial(self):
        # Toca o som de vitória parcial (PAR)
        winsound.PlaySound("parcial.wav", winsound.SND_FILENAME)

    def som_derrota(self):
        # Toca o som de derrota
        winsound.PlaySound("lose.wav", winsound.SND_FILENAME)

    # ------------------------------------
    # FUNÇÃO DE ANIMAÇÃO
    # ------------------------------------
    
    def animar_roleta(self, emojis):
        self.som_inicio()

        for _ in range(5):
            self.roleta_label.config(text=" ".join(random.choices(["🍋", "🍉", "🍒"], k=3)))
            self.root.update()
            time.sleep(0.1)

        self.roleta_label.config(text=" ".join(emojis))

    # ------------------------------------
    # FUNÇÃO PRINCIPAL DO JOGO
    # ------------------------------------
    
    def jogar(self):
        roleta_resultado = self.roleta.girar_roleta()
        emojis = [str(f) for f in roleta_resultado]

        self.animar_roleta(emojis)

        resultado = self.roleta.verificar_resultado(roleta_resultado)

        # Exibir texto e tocar som correspondente
        if resultado == "JACKPOT":
            self.resultado_label.config(text="🍀 JACKPOT! Três iguais! Você ganhou o prêmio máximo!", fg="gold")
            self.som_vitoria() # Som de vitória total

        elif resultado == "PAR":
            self.resultado_label.config(text="✨ Duas frutas iguais! Você ganhou um prêmio menor!", fg="yellow")
            self.som_parcial() # Som de vitória parcial

        else:
            self.resultado_label.config(text="💀 Nenhuma combinação... azar, tenta de novo!", fg="white")
            self.som_derrota() # Som de derrota

# -------------------------------
# EXECUTAR O JOGO
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CassinoGUI(root)
    root.mainloop()

