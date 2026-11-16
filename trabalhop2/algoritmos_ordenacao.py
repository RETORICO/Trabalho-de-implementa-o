# Trabalho de algoritmos de ordenação
# Fonte de estudo: https://www.freecodecamp.org/portuguese/news/algoritmos-de-ordenacao-explicados-com-exemplos-em-python-java-e-c/
#
# Obs: selection, bubble e insertion demoram bastante com 100.000 elementos.
# Pra testar rápido, troca o TAMANHO_LISTA por 5000.

import random
import sys
import time

TAMANHO_LISTA = 100000
VALOR_MAXIMO = 100000

sys.setrecursionlimit(10000)


# Selection Sort
# Vantagem: simples e faz poucas trocas
# Desvantagem: sempre O(n²), lento em lista grande
def selection_sort(lista):
    a = lista[:]
    n = len(a)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if a[j] < a[menor]:
                menor = j
        a[i], a[menor] = a[menor], a[i]
    return a


# Bubble Sort
# Vantagem: fácil de entender e é estável
# Desvantagem: O(n²) e faz muita troca, o mais lento
def bubble_sort(lista):
    a = lista[:]
    n = len(a)
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                trocou = True
        if not trocou:
            break
    return a


# Insertion Sort
# Vantagem: bom pra lista pequena ou quase ordenada, é estável
# Desvantagem: O(n²) no caso médio e no pior caso
def insertion_sort(lista):
    a = lista[:]
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        while j >= 0 and a[j] > chave:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = chave
    return a


# Merge Sort
# Vantagem: sempre O(n log n) e é estável
# Desvantagem: gasta memória extra
def merge_sort(lista):
    if len(lista) <= 1:
        return lista[:]
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])

    resultado = []
    i = 0
    j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


# Quick Sort
# Vantagem: muito rápido na prática, O(n log n) em média
# Desvantagem: pior caso O(n²) e não é estável (usei pivô aleatório pra evitar)
def quick_sort(lista):
    a = lista[:]
    pilha = [(0, len(a) - 1)]
    while pilha:
        inicio, fim = pilha.pop()
        if inicio >= fim:
            continue
        p = random.randint(inicio, fim)
        a[p], a[fim] = a[fim], a[p]
        pivo = a[fim]
        i = inicio - 1
        for j in range(inicio, fim):
            if a[j] <= pivo:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[fim] = a[fim], a[i + 1]
        pilha.append((inicio, i))
        pilha.append((i + 2, fim))
    return a


# Heap Sort
# Vantagem: sempre O(n log n) e não usa memória extra
# Desvantagem: não é estável e costuma ser mais lento que o quick
def heap_sort(lista):
    a = lista[:]
    n = len(a)

    def heapify(tamanho, raiz):
        while True:
            maior = raiz
            esq = 2 * raiz + 1
            dire = 2 * raiz + 2
            if esq < tamanho and a[esq] > a[maior]:
                maior = esq
            if dire < tamanho and a[dire] > a[maior]:
                maior = dire
            if maior == raiz:
                return
            a[raiz], a[maior] = a[maior], a[raiz]
            raiz = maior

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for fim in range(n - 1, 0, -1):
        a[0], a[fim] = a[fim], a[0]
        heapify(fim, 0)
    return a


# Counting Sort
# Vantagem: O(n + k), muito rápido quando os valores têm intervalo pequeno
# Desvantagem: só funciona com inteiros e gasta memória se o intervalo for grande
def counting_sort(lista):
    if not lista:
        return []
    minimo = min(lista)
    maximo = max(lista)
    contagem = [0] * (maximo - minimo + 1)
    for x in lista:
        contagem[x - minimo] += 1
    for i in range(1, len(contagem)):
        contagem[i] += contagem[i - 1]
    saida = [0] * len(lista)
    for x in reversed(lista):
        contagem[x - minimo] -= 1
        saida[contagem[x - minimo]] = x
    return saida


# Radix Sort
# Vantagem: rápido pra inteiros e é estável
# Desvantagem: só funciona com inteiros (não negativos aqui) e usa memória extra
def radix_sort(lista):
    if not lista:
        return []
    a = lista[:]
    maximo = max(a)
    exp = 1
    while maximo // exp > 0:
        saida = [0] * len(a)
        contagem = [0] * 10
        for x in a:
            contagem[(x // exp) % 10] += 1
        for i in range(1, 10):
            contagem[i] += contagem[i - 1]
        for x in reversed(a):
            d = (x // exp) % 10
            contagem[d] -= 1
            saida[contagem[d]] = x
        a = saida
        exp *= 10
    return a


# Bucket Sort
# Vantagem: quase O(n) quando os valores são bem distribuídos
# Desvantagem: fica lento se muitos valores caírem no mesmo balde
def bucket_sort(lista):
    if not lista:
        return []
    minimo = min(lista)
    maximo = max(lista)
    if minimo == maximo:
        return lista[:]
    qtd_baldes = max(1, len(lista) // 10)
    tamanho = (maximo - minimo + 1) / qtd_baldes
    baldes = [[] for _ in range(qtd_baldes)]
    for x in lista:
        baldes[int((x - minimo) / tamanho)].append(x)
    resultado = []
    for balde in baldes:
        resultado.extend(insertion_sort(balde))
    return resultado


ALGORITMOS = [
    ("Selection Sort", selection_sort),
    ("Bubble Sort", bubble_sort),
    ("Insertion Sort", insertion_sort),
    ("Merge Sort", merge_sort),
    ("Quick Sort", quick_sort),
    ("Heap Sort", heap_sort),
    ("Counting Sort", counting_sort),
    ("Radix Sort", radix_sort),
    ("Bucket Sort", bucket_sort),
]


def main():
    random.seed(42)  # tira essa linha pra lista mudar a cada execução
    original = [random.randint(0, VALOR_MAXIMO) for _ in range(TAMANHO_LISTA)]
    esperado = sorted(original)
    print(f"Lista aleatória com {len(original)} elementos gerada.\n")

    print(f"{'Algoritmo':<16} {'Tempo (s)':>12}  Correto?")
    for nome, funcao in ALGORITMOS:
        inicio = time.perf_counter()
        resultado = funcao(original)
        tempo = time.perf_counter() - inicio
        ok = "sim" if resultado == esperado else "NAO"
        print(f"{nome:<16} {tempo:>12.3f}  {ok}", flush=True)


main()