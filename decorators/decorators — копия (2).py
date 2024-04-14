#!/usr/bin/env python
# coding: utf-8

import requests
import time
import re
from functools import wraps
from functools import lru_cache
from random import randint

BOOK_PATH = 'https://www.gutenberg.org/files/2638/2638-0.txt'

def counter(func):
    """
    Декоратор, считающий и выводящий количество вызовов декорируемой функции
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0    
    return wrapper

def benchmark(func):
    """
    Декоратор, выводящий время, которое заняло выполнение декорируемой функции
    """
    @wraps(func)

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Время выполнения функции {func.__name__}: {end - start}')
        return result
    return wrapper

def logging(func):
    """
    Декоратор, который выводит параметры с которыми была вызвана функция
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        params = (*args,)
        print(f'Функция вызвана с параметрами:\n{params}')
        return result
    return wrapper

@counter
@logging
@benchmark
def word_count(word, url=BOOK_PATH):
    """
    Функция для посчета указанного слова на html-странице
    """

    # отправляем запрос в библиотеку Gutenberg и забираем текст
    raw = requests.get(url).text

    # заменяем в тексте все небуквенные символы на пробелы
    processed_book = re.sub('[\W]+' , ' ', raw).lower()

    # считаем
    cnt = len(re.findall(word.lower(), processed_book))

    return f"Cлово {word} встречается {cnt} раз"
    
print(word_count('whole'))
print(f'Функция была вызвана: {word_count.calls} раз')