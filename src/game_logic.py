import heapq
from collections import deque
from typing import List, Optional

class EightPuzzle:
    @staticmethod
    def tem_solucao(estado: List[int]) -> bool:
        inversoes = 0
        for i in range(9):
            for j in range(i+1, 9):
                if estado[i] != 0 and estado[j] != 0 and estado[i] > estado[j]:
                    inversoes += 1
        return inversoes % 2 == 0

    @staticmethod
    def heuristica_manhattan(estado: List[int], estado_final: List[int]) -> int:
        distancia = 0
        for indice, num in enumerate(estado):
            if num != 0:
                pos_final = estado_final.index(num)
                linha_atual, coluna_atual = indice // 3, indice % 3
                linha_final, coluna_final = pos_final // 3, pos_final % 3
                distancia += abs(linha_atual - linha_final) + abs(coluna_atual - coluna_final)
        return distancia

    @staticmethod
    def heuristica_pecas_fora(estado: List[int], estado_final: List[int]) -> int:
        return sum(1 for i in range(9) if estado[i] != 0 and estado[i] != estado_final[i])

    @staticmethod
    def obter_movimentos_validos(posicao_vazia: int) -> List[int]:
        movimentos = []
        if posicao_vazia // 3 > 0: movimentos.append(posicao_vazia - 3)
        if posicao_vazia // 3 < 2: movimentos.append(posicao_vazia + 3)
        if posicao_vazia % 3 > 0: movimentos.append(posicao_vazia - 1)
        if posicao_vazia % 3 < 2: movimentos.append(posicao_vazia + 1)
        return movimentos

    @staticmethod
    def a_estrela(estado_inicial: List[int], estado_final: List[int], antecipacao: int = 1, heuristica: str = "manhattan") -> Optional[List[List[int]]]:
        if heuristica == "pecas_fora":
            heuristica_fn = EightPuzzle.heuristica_pecas_fora
        else:
            heuristica_fn = EightPuzzle.heuristica_manhattan

        heap = [(0 + heuristica_fn(estado_inicial, estado_final), 0, tuple(estado_inicial), None)]
        visitados = set()

        while heap:
            f, g, estado, pai = heapq.heappop(heap)
            if list(estado) == estado_final:
                caminho = []
                while pai is not None:
                    caminho.append(list(estado))
                    estado, pai = pai
                caminho.reverse()
                return caminho
            if estado in visitados:
                continue
            visitados.add(estado)
            pos_vazia = estado.index(0)
            for mov in EightPuzzle.obter_movimentos_validos(pos_vazia):
                novo_estado = list(estado)
                novo_estado[pos_vazia], novo_estado[mov] = novo_estado[mov], novo_estado[pos_vazia]
                novo_estado_tuple = tuple(novo_estado)
                if novo_estado_tuple not in visitados:
                    novo_g = g + 1
                    if antecipacao == 1:
                        novo_h = heuristica_fn(novo_estado, estado_final)
                    else:
                        novo_h = EightPuzzle.avaliar_segundo_nivel(novo_estado, estado_final, novo_g, heuristica)
                    novo_f = novo_g + novo_h
                    heapq.heappush(heap, (novo_f, novo_g, novo_estado_tuple, (estado, pai)))
        return None

    @staticmethod
    def avaliar_segundo_nivel(estado: List[int], estado_final: List[int], g_atual: int, heuristica: str = "manhattan") -> float:
        if heuristica == "pecas_fora":
            heuristica_fn = EightPuzzle.heuristica_pecas_fora
        else:
            heuristica_fn = EightPuzzle.heuristica_manhattan

        posicao_vazia = estado.index(0)
        min_f = float('inf')
        for movimento in EightPuzzle.obter_movimentos_validos(posicao_vazia):
            novo_estado = list(estado)
            novo_estado[posicao_vazia], novo_estado[movimento] = novo_estado[movimento], novo_estado[posicao_vazia]
            novo_g = g_atual + 1
            f = novo_g + heuristica_fn(novo_estado, estado_final)
            if f < min_f:
                min_f = f
        return min_f

    @staticmethod
    def melhor_primeiro(estado_inicial: List[int], estado_final: List[int], antecipacao: int = 1, heuristica: str = "manhattan") -> Optional[List[List[int]]]:
        if heuristica == "pecas_fora":
            heuristica_fn = EightPuzzle.heuristica_pecas_fora
        else:
            heuristica_fn = EightPuzzle.heuristica_manhattan

        conjunto_aberto = [(heuristica_fn(estado_inicial, estado_final), tuple(estado_inicial), [])]
        conjunto_fechado = set()
        
        while conjunto_aberto:
            _, atual, caminho = heapq.heappop(conjunto_aberto)
            if list(atual) == estado_final:
                return caminho + [list(atual)]
            if atual in conjunto_fechado:
                continue
            conjunto_fechado.add(atual)
            posicao_vazia = atual.index(0)
            for movimento in EightPuzzle.obter_movimentos_validos(posicao_vazia):
                novo_estado = list(atual)
                novo_estado[posicao_vazia], novo_estado[movimento] = novo_estado[movimento], novo_estado[posicao_vazia]
                if antecipacao == 1:
                    heapq.heappush(conjunto_aberto, (heuristica_fn(novo_estado, estado_final), tuple(novo_estado), caminho + [list(atual)]))
                else:
                    melhor_segundo = EightPuzzle.avaliar_segundo_nivel_melhor_primeiro(novo_estado, estado_final, heuristica)
                    heapq.heappush(conjunto_aberto, (melhor_segundo, tuple(novo_estado), caminho + [list(atual)]))
        return None

    @staticmethod
    def avaliar_segundo_nivel_melhor_primeiro(estado: List[int], estado_final: List[int], heuristica: str = "manhattan") -> float:
        if heuristica == "pecas_fora":
            heuristica_fn = EightPuzzle.heuristica_pecas_fora
        else:
            heuristica_fn = EightPuzzle.heuristica_manhattan

        posicao_vazia = estado.index(0)
        min_h = float('inf')
        for movimento in EightPuzzle.obter_movimentos_validos(posicao_vazia):
            novo_estado = list(estado)
            novo_estado[posicao_vazia], novo_estado[movimento] = novo_estado[movimento], novo_estado[posicao_vazia]
            h = heuristica_fn(novo_estado, estado_final)
            if h < min_h:
                min_h = h
        return min_h

    @staticmethod
    def busca_largura(estado_inicial: List[int], estado_final: List[int]) -> Optional[List[List[int]]]:
        fila = deque([(estado_inicial[:], [])])
        visitados = set()
        while fila:
            estado, caminho = fila.popleft()
            if tuple(estado) in visitados:
                continue
            visitados.add(tuple(estado))
            if estado == estado_final:
                return caminho + [estado]
            posicao_vazia = estado.index(0)
            for movimento in EightPuzzle.obter_movimentos_validos(posicao_vazia):
                novo_estado = estado[:]
                novo_estado[posicao_vazia], novo_estado[movimento] = novo_estado[movimento], novo_estado[posicao_vazia]
                fila.append((novo_estado, caminho + [estado]))
        return None