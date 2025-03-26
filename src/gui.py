import tkinter as tk
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List
from .game_logic import EightPuzzle

class EightPuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle IA - BSI 🧩")
        self.root.configure(bg="#f5f5f5")
        self.cores_pecas = {
            1: "#3498db", 2: "#da70d6", 3: "#1abc9c",
            4: "#9b59b6", 5: "#f1c40f", 6: "#e74c3c",
            7: "#d35400", 8: "#2ecc71", 0: "#2c3e50"
        }
        self.estado_inicial = [0, 8, 7, 6, 5, 4, 3, 2, 1]
        self.estado_final = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.tabuleiro = self.estado_inicial[:]
        self.botoes = []
        self.configurar_interface()

    def configurar_interface(self):
        frame_principal = tk.Frame(self.root, bg="#f5f5f5", padx=20, pady=20)
        frame_principal.pack(expand=True, fill="both")
        frame_tabuleiro = tk.Frame(frame_principal, bg="#ecf0f1", bd=3, relief="ridge", padx=5, pady=5)
        frame_tabuleiro.pack(pady=(0, 20))
        for i in range(9):
            btn = tk.Button(frame_tabuleiro, text="", font=("Segoe UI", 24, "bold"), width=4, height=2,
                          command=lambda i=i: self.mover_peca(i), bg=self.cores_pecas[0], fg="white",
                          activebackground="#3498db", relief="ridge", borderwidth=3)
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.botoes.append(btn)
        frame_controle = tk.Frame(frame_principal, bg="#f5f5f5")
        frame_controle.pack(fill="x")
        controles = [
            ("🔀 Embaralhar", self.embaralhar_tabuleiro, "#9b59b6"),
            ("🎯 Definir estados", self.definir_estados, "#3498db"),
            ("⚡ Resolver (A*)", self.resolver_a_estrela, "#2ecc71"),
            ("🧩 Resolver (Best-First)", self.resolver_melhor_primeiro, "#e74c3c"),
            ("🔍 Resolver (BFS)", self.resolver_bfs, "#f1c40f")
        ]
        for texto, comando, cor in controles:
            btn = tk.Button(frame_controle, text=texto, command=comando, bg=cor, fg="white",
                          font=("Segoe UI", 12), relief=tk.RAISED, borderwidth=3,
                          activebackground="#bdc3c7", padx=10, pady=5)
            btn.pack(fill="x", pady=3)
        self.atualizar_tabuleiro()

    def atualizar_tabuleiro(self):
        for i in range(9):
            if self.tabuleiro[i] == 0:
                self.botoes[i].config(text="", bg=self.cores_pecas[0], state=tk.DISABLED, relief="sunken")
            else:
                self.botoes[i].config(text=str(self.tabuleiro[i]), bg=self.cores_pecas[self.tabuleiro[i]],
                                    fg="white", state=tk.NORMAL, relief="raised")

    def mover_peca(self, indice):
        indice_vazio = self.tabuleiro.index(0)
        movimentos_validos = {
            0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
            3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
            6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
        }
        if indice in movimentos_validos[indice_vazio]:
            for _ in range(5):
                self.botoes[indice_vazio].config(relief="sunken")
                self.botoes[indice].config(relief="raised")
                self.root.update()
                time.sleep(0.05)
            self.tabuleiro[indice_vazio], self.tabuleiro[indice] = self.tabuleiro[indice], self.tabuleiro[indice_vazio]
            self.atualizar_tabuleiro()
            if self.tabuleiro == self.estado_final:
                self.mostrar_dialogo("Parabéns! 🎉", "Você resolveu o puzzle manualmente!", "success")

    def esta_resolvido(self) -> bool:
        return self.tabuleiro == self.estado_final

    def embaralhar_tabuleiro(self):
        if self.esta_resolvido():
            resposta = self.mostrar_dialogo("Aviso - Puzzle Resolvido",
                                          "O puzzle já está resolvido. Deseja embaralhar novamente?",
                                          "warning", ["Sim", "Não"])
            if resposta != "Sim":
                return
        while True:
            random.shuffle(self.tabuleiro)
            if EightPuzzle.tem_solucao(self.tabuleiro):
                break
        self.estado_inicial = self.tabuleiro.copy()
        self.movimentos = 0
        self.tempo_inicio = None
        self.atualizar_tabuleiro()

    def definir_estados(self):
        dialogo = tk.Toplevel(self.root)
        dialogo.title("🎯 Definir estados")
        dialogo.configure(bg="#f5f5f5")
        frame_inicial = tk.LabelFrame(dialogo, text=" Estado Inicial ", bg="#ffffff", fg="#2c3e50",
                                    font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        frame_inicial.pack(pady=10, padx=10, fill="x")
        tk.Label(frame_inicial, text="Digite 9 números (0-8) separados por espaço:", bg="#ffffff",
                font=("Segoe UI", 10)).pack(pady=5)
        self.entrada_inicial = tk.Entry(frame_inicial, font=("Segoe UI", 10), width=30, relief="solid", borderwidth=1)
        self.entrada_inicial.pack(pady=5)
        self.entrada_inicial.insert(0, " ".join(map(str, self.tabuleiro)))
        frame_final = tk.LabelFrame(dialogo, text=" Estado Final ", bg="#ffffff", fg="#2c3e50",
                                  font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        frame_final.pack(pady=10, padx=10, fill="x")
        tk.Label(frame_final, text="Digite 9 números (0-8) separados por espaço:", bg="#ffffff",
                font=("Segoe UI", 10)).pack(pady=5)
        self.entrada_final = tk.Entry(frame_final, font=("Segoe UI", 10), width=30, relief="solid", borderwidth=1)
        self.entrada_final.pack(pady=5)
        self.entrada_final.insert(0, " ".join(map(str, self.estado_final)))
        frame_botoes = tk.Frame(dialogo, bg="#f5f5f5")
        frame_botoes.pack(pady=10)
        tk.Button(frame_botoes, text="✔ Aplicar", command=self.validar_e_aplicar_estados, bg="#2ecc71", fg="white",
                 font=("Segoe UI", 10, "bold"), relief="raised", borderwidth=2, padx=10).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="✖ Cancelar", command=dialogo.destroy, bg="#e74c3c", fg="white",
                 font=("Segoe UI", 10), relief="raised", borderwidth=2, padx=10).pack(side="left", padx=5)

    def validar_e_aplicar_estados(self):
        try:
            texto_inicial = self.entrada_inicial.get()
            lista_inicial = list(map(int, texto_inicial.split()))
            texto_final = self.entrada_final.get()
            lista_final = list(map(int, texto_final.split()))
            if len(lista_inicial) != 9 or sorted(lista_inicial) != list(range(9)):
                raise ValueError("Estado inicial inválido")
            if len(lista_final) != 9 or sorted(lista_final) != list(range(9)):
                raise ValueError("Estado final inválido")
            if lista_inicial == lista_final:
                self.mostrar_dialogo("Aviso", "O estado inicial já é igual ao estado final!", "warning")
                return
            self.tabuleiro = lista_inicial
            self.estado_final = lista_final
            self.atualizar_tabuleiro()
            self.entrada_inicial.master.master.destroy()
            self.mostrar_dialogo("Sucesso", "Estados atualizados com sucesso!", "success")
        except ValueError as e:
            mensagem_erro = "Erro na entrada:\n"
            if "invalid literal" in str(e):
                mensagem_erro += "Digite apenas números separados por espaços"
            else:
                mensagem_erro += "Ambos os estados devem conter os números de 0 a 8 sem repetições\n"
                mensagem_erro += "Exemplo válido: 1 2 3 4 5 6 7 8 0"
            self.mostrar_dialogo("Erro", mensagem_erro, "error")
        except Exception as e:
            self.mostrar_dialogo("Erro", f"Ocorreu um erro: {str(e)}", "error")

    def resolver_a_estrela(self):
        if self.esta_resolvido():
            self.mostrar_dialogo("Aviso", "O puzzle já está resolvido!", "warning")
            return
        if not EightPuzzle.tem_solucao(self.tabuleiro):
            self.mostrar_dialogo("Erro", "Estado inicial não tem solução!", "error")
            return
        self.criar_dialogo_algoritmo("Nível de Antecipação - A*", "a_estrela")

    def resolver_melhor_primeiro(self):
        if self.esta_resolvido():
            self.mostrar_dialogo("Aviso", "O puzzle já está resolvido!", "warning")
            return
        if not EightPuzzle.tem_solucao(self.tabuleiro):
            self.mostrar_dialogo("Erro", "Estado inicial não tem solução!", "error")
            return
        self.criar_dialogo_algoritmo("Nível de Antecipação - Best-First", "melhor_primeiro")

    def resolver_bfs(self):
        if self.esta_resolvido():
            self.mostrar_dialogo("Aviso", "O puzzle já está resolvido!", "warning")
            return
        if not EightPuzzle.tem_solucao(self.tabuleiro):
            self.mostrar_dialogo("Erro", "Estado inicial não tem solução!", "error")
            return
        inicio_busca = time.time()
        solucao = EightPuzzle.busca_largura(self.tabuleiro, self.estado_final)
        tempo_busca = time.time() - inicio_busca
        if solucao:
            self.animar_solucao(solucao, "BFS", tempo_busca)
        else:
            self.mostrar_dialogo("Erro", "Não foi possível encontrar uma solução!", "error")

    def criar_dialogo_algoritmo(self, titulo: str, tipo_algoritmo: str):
        dialogo = tk.Toplevel(self.root)
        dialogo.title(titulo)
        dialogo.configure(bg="#f5f5f5")
        dialogo.resizable(False, False)
        frame_principal = tk.Frame(dialogo, bg="#f5f5f5", padx=20, pady=10)
        frame_principal.pack(expand=True, fill="both")
        frame_conteudo = tk.LabelFrame(frame_principal, text=f" Configurações para {tipo_algoritmo.replace('_', ' ').title()} ",
                                     bg="#ffffff", fg="#2c3e50", font=("Segoe UI", 10, "bold"), padx=15, pady=15)
        frame_conteudo.pack(fill="x", pady=(0, 15))
        tk.Label(frame_conteudo, text="Nível de Antecipação:", bg="#ffffff", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
        var_valor = tk.IntVar(value=1)
        tk.Radiobutton(frame_conteudo, text="1: Avalia apenas movimentos imediatos", variable=var_valor, value=1, bg="#ffffff").pack(anchor="w")
        tk.Radiobutton(frame_conteudo, text="2: Avalia 2 passos à frente", variable=var_valor, value=2, bg="#ffffff").pack(anchor="w", pady=(0, 10))
        tk.Label(frame_conteudo, text="Heurística:", bg="#ffffff", font=("Segoe UI", 10)).pack(anchor="w", pady=(5, 5))
        var_heuristica = tk.StringVar(value="manhattan")
        tk.Radiobutton(frame_conteudo, text="Distância de Manhattan", variable=var_heuristica, value="manhattan", bg="#ffffff").pack(anchor="w")
        tk.Radiobutton(frame_conteudo, text="Peças Fora do Lugar", variable=var_heuristica, value="pecas_fora", bg="#ffffff").pack(anchor="w")
        frame_botoes = tk.Frame(frame_principal, bg="#f5f5f5")
        frame_botoes.pack(fill="x", pady=(10, 0))
        container_botoes = tk.Frame(frame_botoes, bg="#f5f5f5")
        container_botoes.pack(expand=True)
        tk.Button(container_botoes, text="✔ Aplicar", command=lambda: self.iniciar_algoritmo(dialogo, var_valor, tipo_algoritmo, var_heuristica),
                 bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"), relief="raised", borderwidth=2, padx=15).pack(side="left", padx=5)
        tk.Button(container_botoes, text="✖ Cancelar", command=dialogo.destroy, bg="#e74c3c", fg="white",
                 font=("Segoe UI", 10), relief="raised", borderwidth=2, padx=15).pack(side="left", padx=5)
        dialogo.transient(self.root)
        dialogo.grab_set()
        self.root.wait_window(dialogo)

    def iniciar_algoritmo(self, dialogo, var_valor, tipo_algoritmo, var_heuristica):
        valor = var_valor.get()
        heuristica = var_heuristica.get()
        dialogo.destroy()
        if valor not in [1, 2]:
            self.mostrar_dialogo("Valor inválido", "O nível de antecipação deve ser 1 ou 2", "error")
            return
        inicio_busca = time.time()
        if tipo_algoritmo == "a_estrela":
            solucao = EightPuzzle.a_estrela(self.tabuleiro, self.estado_final, antecipacao=valor, heuristica=heuristica)
            nome_algoritmo = "A*"
        elif tipo_algoritmo == "melhor_primeiro":
            solucao = EightPuzzle.melhor_primeiro(self.tabuleiro, self.estado_final, antecipacao=valor, heuristica=heuristica)
            nome_algoritmo = "Best-First"
        else:
            self.mostrar_dialogo("Erro", "Algoritmo não reconhecido!", "error")
            return
        tempo_busca = time.time() - inicio_busca
        if solucao:
            self.animar_solucao(solucao, f"{nome_algoritmo} ({heuristica.replace('_', ' ').title()}, Nível {valor})", tempo_busca)
        else:
            self.mostrar_dialogo("Erro", "Não foi possível encontrar uma solução!", "error")

    def mostrar_solucao_detalhada(self, solucao, algoritmo, tempo_busca, tempo_animacao):
        dialogo = tk.Toplevel(self.root)
        dialogo.title(f"Solução encontrada - {algoritmo}")
        dialogo.geometry("")
        main_frame = tk.Frame(dialogo, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        stats_frame = tk.LabelFrame(main_frame, text=" Estatísticas ", padx=10, pady=10)
        stats_frame.pack(fill="x", pady=(0, 15))
        tk.Label(stats_frame, text=(
            f"• Passos na solução: {len(solucao)-1}\n"
            f"• Tempo de busca: {tempo_busca:.4f} segundos\n"
            f"• Tempo de animação: {tempo_animacao:.4f} segundos\n"
            f"• Tempo total: {(tempo_busca+tempo_animacao):.4f} segundos"
        ), justify="left").pack(anchor="w")
        container = tk.Frame(main_frame)
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        passos_por_linha = 5
        linha_atual = 0
        coluna_atual = 0
        for passo, estado in enumerate(solucao):
            frame_passo = tk.Frame(scrollable_frame, bd=2, relief="groove", padx=5, pady=5)
            tk.Label(frame_passo, text=f"Passo {passo}", font=('Helvetica', 8, 'bold')).pack()
            mini_frame = tk.Frame(frame_passo)
            for i in range(9):
                row, col = i // 3, i % 3
                num = estado[i]
                color = self.cores_pecas[num]
                fg = "white" if num not in [4, 5, 6] else "black"
                tk.Label(mini_frame, text=str(num) if num != 0 else "", width=2, height=1, bg=color, fg=fg,
                        relief="raised", font=('Helvetica', 8)).grid(row=row, column=col, padx=1, pady=1)
            mini_frame.pack()
            frame_passo.grid(row=linha_atual, column=coluna_atual, padx=5, pady=5, sticky="nw")
            coluna_atual += 1
            if coluna_atual >= passos_por_linha:
                coluna_atual = 0
                linha_atual += 1
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        tk.Button(main_frame, text="Fechar", command=dialogo.destroy, bg="#2ecc71", fg="white",
                font=("Arial", 10)).pack(pady=10)

    def animar_solucao(self, solucao: List[List[int]], algoritmo: str, tempo_busca: float):
        inicio_animacao = time.time()
        for estado in solucao:
            self.tabuleiro = list(estado)
            self.atualizar_tabuleiro()
            self.root.update()
            time.sleep(0.5)
        tempo_animacao = time.time() - inicio_animacao
        self.mostrar_solucao_detalhada(solucao, algoritmo, tempo_busca, tempo_animacao)
        self.gerar_relatorio(algoritmo, len(solucao)-1, tempo_busca)

    def gerar_relatorio(self, algoritmo: str, passos: int, tempo: float):
        try:
            df = pd.read_csv("relatorio_comparacao.csv")
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Data", "Algoritmo", "Passos", "Tempo", "Estado_Inicial", "Estado_Final"])
        nova_linha = {
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Algoritmo": algoritmo,
            "Passos": passos,
            "Tempo": tempo,
            "Estado_Inicial": str(self.estado_inicial),
            "Estado_Final": str(self.estado_final)
        }
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        df.to_csv("relatorio_comparacao.csv", index=False)
        if len(df) >= 3: 
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            df.groupby("Algoritmo")["Tempo"].mean().plot(kind="bar", color="skyblue")
            plt.title("Tempo Médio por Algoritmo")
            plt.ylabel("Segundos")
            plt.subplot(1, 2, 2)
            df.groupby("Algoritmo")["Passos"].mean().plot(kind="bar", color="lightgreen")
            plt.title("Passos Médios por Algoritmo")
            plt.tight_layout()
            plt.savefig("grafico_comparacao.png")
            plt.close()

    def mostrar_dialogo(self, titulo: str, mensagem: str, tipo_dialogo: str = "error", botoes: List[str] = ["OK"]):
        dialogo = tk.Toplevel(self.root)
        dialogo.title(titulo)
        dialogo.configure(bg="#f5f5f5")
        dialogo.resizable(False, False)
        estilos = {
            "error": {"icone": "❌", "cor": "#e74c3c"},
            "success": {"icone": "✔️", "cor": "#2ecc71"},
            "warning": {"icone": "⚠️", "cor": "#f39c12"}
        }
        estilo = estilos.get(tipo_dialogo.lower(), estilos["error"])
        frame_principal = tk.Frame(dialogo, bg="#f5f5f5", padx=20, pady=20)
        frame_principal.pack(expand=True, fill="both")
        tk.Label(frame_principal, text=estilo["icone"], font=("Segoe UI", 24), bg="#f5f5f5", fg=estilo["cor"]).pack(pady=(0, 10))
        tk.Label(frame_principal, text=mensagem, font=("Segoe UI", 11), bg="#f5f5f5", fg="#2c3e50",
                wraplength=300, justify="center").pack(pady=(0, 20))
        frame_botoes = tk.Frame(frame_principal, bg="#f5f5f5")
        frame_botoes.pack()
        for i, texto_botao in enumerate(botoes):
            tk.Button(frame_botoes, text=f"  {texto_botao}  ",
                     command=lambda b=texto_botao: self.ao_clicar_botao_dialogo(dialogo, b),
                     bg=estilo["cor"], fg="white", font=("Segoe UI", 10, "bold"),
                     relief="raised", borderwidth=2, activebackground="#bdc3c7").grid(row=0, column=i, padx=5)
        dialogo.transient(self.root)
        dialogo.grab_set()
        self.root.wait_window(dialogo)
        return getattr(dialogo, 'botao_selecionado', None)

    def ao_clicar_botao_dialogo(self, dialogo, botao):
        dialogo.botao_selecionado = botao
        dialogo.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EightPuzzleGUI(root)
    root.mainloop()