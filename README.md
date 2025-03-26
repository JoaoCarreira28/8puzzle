# Eight Puzzle - Inteligência Artificial

Este é um projeto bimestral da disciplina de **Inteligência Artificial (1º bimestre de 2025)**.

## Enunciado do Projeto

O objetivo deste trabalho é desenvolver uma solução para o **8-Puzzle**, aplicando técnicas de **busca heurística** para encontrar a sequência correta de passos até o estado final desejado pelo usuário.

### Funcionalidades Implementadas:
✅ Definir o estado final do jogo  
✅ Embaralhar as peças para gerar um estado inicial válido  
✅ Escolher o tipo de busca para solucionar o problema:  
   - **Busca Cega (BFS - Busca em Largura)**  
   - **Busca Heurística (A* e Best-First Search)**  
✅ Escolher a profundidade da avaliação heurística (1º nível ou 2º nível)  
✅ Mostrar a sequência de passos da solução  
✅ Exibir estatísticas sobre a busca:  
   - Número de passos necessários  
   - Tempo gasto na busca  
   - Tamanho do caminho da solução encontrada  

### Funções de Avaliação Heurística Implementadas:
- **Quantidade de peças fora do lugar**  
- **Soma das Distâncias Manhattan das peças em relação ao estado final**  

O programa conta com uma **interface gráfica** amigável, permitindo que o usuário interaja de forma intuitiva com o jogo e visualize o progresso da busca.

## Tecnologias Utilizadas

- **Linguagem:** Python  
- **Bibliotecas:** Tkinter (interface gráfica), heapq e deque (estruturas de dados para busca)  

## Autor

👤 **João Victor Carreira Tanaka Silva**  
📌 **RA:** 262319411  
🎓 **Curso:** Sistemas de Informação  

---