import requests
import timeit

class LinkTest():
    def test_get_status(self):
        try:
            x = requests.get('http://localhost:8000/d7m4q')
            return x.status_code == 200
        except:
            return False

    def test_post_status(self):
        try:
            x = requests.post('http://localhost:8000/?source=https://guap.ru/')
            return x.status_code == 200
        except:
            return False

# Проверка на одинаковость Хеша для одного и тогоже URL
def Test1():
    print('START: TEST 1')
    url_post = 'http://localhost:8000/?source=https://guap.ru/'

    responses = []

    for i in range(0, 10):
        print('.', end='')
        x = requests.post(url_post)
        responses.append(x.text)

    CHECK = True
    for res in responses:
        if not responses[0] == res:
            CHECK = False

    print('\nRESULT: ', end='')
    if CHECK:
        print('OK')
    else:
        print('NOT')
    print('END')

# Проверка на одинаковость ссылок для Хеш
def Test2():
    print('START: TEST 2')
    url_get = 'http://localhost:8000/d7m4q'

    responses = []

    for i in range(0, 10):
        print('.', end='')
        x = requests.get(url_get)
        responses.append(x.text)

    CHECK = True
    for res in responses:
        if not responses[0] == res:
            CHECK = False

    print('\nRESULT: ', end='')
    if CHECK:
        print('OK')
    else:
        print('NOT')
    print('END\n')

def Benchmark_Test():
    print('START: BENCH TEST')
    print('FOR GET')
    url_get = 'http://localhost:8000/d7m4q'
    start_time = timeit.default_timer()
    x = requests.get(url_get)
    print(timeit.default_timer() - start_time)

    print('FOR POST')
    url_post = 'http://localhost:8000/?source=https://guap.ru/'
    start_time = timeit.default_timer()
    x = requests.post(url_post)
    print(timeit.default_timer() - start_time)


print(LinkTest().test_get_status())
print(LinkTest().test_post_status())

Test1()
Test2()
Benchmark_Test()