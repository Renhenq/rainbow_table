import os
import hashlib
import random

# função hash H
# calcula sha256 (GBC083 + s)
# recebe texto s, devolve hash
def myHash(s):
    hash_object=hashlib.sha256()
    hash_object.update(b"GBC083")
    hash_object.update(s.encode('utf-8'))
    return hash_object.hexdigest()
    #return hash_object.digest()


# função de redução R
def reduce_(hash_hex, col, wordlist, n_words=2):
    # utiliza + col para ter uma função R para cada coluna
    x = (int(hash_hex, 16) + col)  # converte o hash em número e soma o n. da coluna
    words = []
    for _ in range(n_words):
        words.append(wordlist[x % len(wordlist)]) # divide o número pelo tamanho do Diceware para escolher uma palavra
        x //= len(wordlist) # divide para escolher outra palavra
    return " ".join(words)

# construir uma cadeia (linha da tabela)
def make_chain(start, width, wordlist):
    p = start
    for col in range(width):
        p = reduce_(myHash(p), col, wordlist) # R(H(p))
    return p  # retorna última senha da linha (end)


def lookup(h, table, width, wordlist):
    # loop de width iterações para percorrer a cadeia toda
    for k in range(width - 1, -1, -1):
        # primeira reducao
        x = reduce_(h, k, wordlist)

        # calcula iteracoes de R(H())
        # começa pelo maior valor para calcular o mais próximo do end
        for col in range(k + 1, width):
            x = reduce_(myHash(x), col, wordlist)

        if x in table:
            # recupera os valores da chave x
            p = table[x]
            # reconstroi a cadeia
            for col in range(width):
                # compara proximo hash com o hash h
                if myHash(p) == h:
                    return p
                p = reduce_(myHash(p), col, wordlist)

    return None


def generate_password(wodlist, n_words = 2):
    # gera uma senha com palavras do diceware
    return " ".join(
        random.choice(wordlist)
        for _ in range (n_words)
    )

def build_table(wordlist, height, width):
    table = {}

    for _ in range(height):
        # gera uma palavra para ser o start
        start = generate_password(wordlist)
        # constroi cadeia para descobrir o end
        end = make_chain(start, width, wordlist)

        # se end nao esta na tabela, cria uma chave
        if end not in table:
            table[end] = []

        # adiciona a palavra gerada em start nas palavras que terminam em end
        table[end].append(start)

    return table

# carrega o diceware
def load_diceware(file):
    words =[]

    with open(file, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(maxsplit=1)

            if len(parts) == 2:
                code, word = parts
                words.append(word)

    return words


height = 1000
width = 100

wordlist = load_diceware("diceware.txt")

table = build_table(wordlist, height, width)

print("Cadeias geradas:", height)
print("Endpoints distintos:", len(table))
print("Primeiros endpoints:")

for end, starts in list(table.items())[:5]:
    print(f"Início(s): {starts} | Fim: {end}")

print(len(wordlist))
print(wordlist[:5])