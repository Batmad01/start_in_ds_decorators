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
    ���������, ��������� � ��������� ���������� ������� ������������ �������
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0    
    return wrapper

def benchmark(func):
    """
    ���������, ��������� �����, ������� ������ ���������� ������������ �������
    """
    @wraps(func)

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'����� ���������� ������� {func.__name__}: {end - start}')
        return result
    return wrapper

def logging(func):
    """
    ���������, ������� ������� ��������� � �������� ���� ������� �������
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        params = (*args,)
        print(f'������� ������� � �����������:\n{params}')
        return result
    return wrapper

@counter
@logging
@benchmark
def word_count(word, url=BOOK_PATH):
    """
    ������� ��� ������� ���������� ����� �� html-��������
    """

    # ���������� ������ � ���������� Gutenberg � �������� �����
    raw = requests.get(url).text

    # �������� � ������ ��� ����������� ������� �� �������
    processed_book = re.sub('[\W]+' , ' ', raw).lower()

    # �������
    cnt = len(re.findall(word.lower(), processed_book))

    return f"C���� {word} ����������� {cnt} ���"
    
print(word_count('whole'))
print(f'������� ���� �������: {word_count.calls} ���')