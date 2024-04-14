# -*- coding: windows-1251 -*-
import requests
import time
import re
from functools import wraps
from functools import lru_cache
from random import randint

BOOK_PATH = 'https://www.gutenberg.org/files/2638/2638-0.txt'

def counter(func):
    """
    Äåêîðàòîð, ñ÷èòàþùèé è âûâîäÿùèé êîëè÷åñòâî âûçîâîâ äåêîðèðóåìîé ôóíêöèèааааееав
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0    
    return wrapper

def benchmark(func):
    """
    Äåêîðàòîð, âûâîäÿùèé âðåìÿ, êîòîðîå çàíÿëî âûïîëíåíèå äåêîðèðóåìîé ôóíêöèè
    """
    @wraps(func)

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Âðåìÿ âûïîëíåíèÿ ôóíêöèè {func.__name__}: {end - start}')
        return result
    return wrapper

def logging(func):
    """
    Äåêîðàòîð, êîòîðûé âûâîäèò ïàðàìåòðû ñ êîòîðûìè áûëà âûçâàíà ôóíêöèÿ
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        params = (*args,)
        print(f'Ôóíêöèÿ âûçâàíà ñ ïàðàìåòðàìè:\n{params}')
        return result
    return wrapper

@counter
@logging
@benchmark
def word_count(word, url=BOOK_PATH):
    """
    Ôóíêöèÿ äëÿ ïîñ÷åòà óêàçàííîãî ñëîâà íà html-ñòðàíèöå
    """

    # îòïðàâëÿåì çàïðîñ â áèáëèîòåêó Gutenberg è çàáèðàåì òåêñò
    raw = requests.get(url).text

    # çàìåíÿåì â òåêñòå âñå íåáóêâåííûå ñèìâîëû íà ïðîáåëû
    processed_book = re.sub('[\W]+' , ' ', raw).lower()

    # ñ÷èòàåì
    cnt = len(re.findall(word.lower(), processed_book))

    return f"Cëîâî {word} âñòðå÷àåòñÿ {cnt} ðàç"
    
print(word_count('whole'))
print(f'Ôóíêöèÿ áûëà âûçâàíà: {word_count.calls} ðàç')
