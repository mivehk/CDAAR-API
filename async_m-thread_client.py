import requests
import random
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# ======= multi-thread method ===========

"""
The benefit of ProcessPoolExecutor .vs ThreadPoolExecutor depends entirely on whether
the workload is CPU-bound or I/O-bound. In a cohesive explanation, threads are blocked
by Python’s Global Interpreter Lock when they run Python bytecode, which means 
CPU-bound code gets no parallelism with threads.
Processes avoid the GIL because each process has its own interpreter, so CPU-intensive
work scales with the number of cores. [to avoid loop of multiple process importing
modules and running functions, use the guard __name__=‘__main__’, so your function
only runs once when you run `python script.py `]
For I/O-bound operations like HTTP requests, the CPython’s GIL is released during network
waits, and threads are generally faster because they are lightweight and avoid the 
overhead of process creation, pickling[convert object into byte stream to send to 
another process], and inter-process communication. 
In your code, the work is purely network I/O, so ProcessPoolExecutor provides 
no improvement and usually performs worse.

brief: if `I/O bound` then use thread; 
elif cpu-bound GIL block thread so use process with dunder guard
"""


def dna_gen(num: int = 99):
    result_ = "".join(random.choice("ATGC") for _ in range(num))
    return result_


# urls = [f"https://dev15.miveh-nejad.info/RNA/v2/?seq={dna_gen()}" for _ in range(150)]


def fetch_url(url):
    return requests.get(url).text.strip()


def thread_mgmt():
    with ThreadPoolExecutor(max_workers=5) as thread:
        result_ = list(thread.map(fetch_url, urls))
        return result_


# url = ["https://dev15.miveh-nejad.info/RNA/v2/?seq=ATGC"] * 5


if __name__ == "__main__":
    urls = [
        f"https://dev15.miveh-nejad.info/RNA/v2/?seq={dna_gen()}" for _ in range(150)
    ]
    url = ["https://dev15.miveh-nejad.info/RNA/v2/?seq=ATGC"] * 5
    for i in thread_mgmt():
        print(i)


# ======= asynchronous method ===========

"""

asyncio.gather runs multiple async tasks concurrently and returns their results in order
time it takes to run multiple async tasks is as long as the one of the tasks that
is the longest.

async functions are called coroutine, when called they do not run immediately.
it returns suspended object that must be scheduled by an event loop
async/await and yield both pause execution. yield runs synchronously waiting for next
call, async/await provide concurrency while waiting In a concise narrative, yield
creates a generator, while async/await creates a coroutine managed by
an event loop. A generator pauses to produce a sequence of values one at a time,
and the caller drives it by repeatedly asking for the next value.
A coroutine pauses to wait for an asynchronous operation, and the event loop—not
the caller—resumes it when the awaited task completes

async def fetch_url_text(session, url):
    async with session.get(url) as resp:
        result_ = resp.text()
        return await result_

async def fetch_all_urls():
    urls = ["https://dev15.miveh-nejad.info/RNA/v2/?seq=ATGC"] * 3
    async with aiohttp.ClientSession() as session:
        result_ = [fetch_url_text(session, url) for url in urls]
        return await asyncio.gather(*result_)

for item in asyncio.run(fetch_all_urls()):
    print(item)

"""


def dna_gen(num: int = 33):
    res_ = "".join(random.choice("ATGC") for _ in range(num))
    return res_


async def fetch_url(session, url):
    async with session.get(url) as resp:
        return await resp.text()


async def fetch_all_urls():
    urls = [
        f"https://dev15.miveh-nejad.info/RNA/v2/?seq={dna_gen()}" for _ in range(10)
    ]
    async with aiohttp.ClientSession() as session:
        result_ = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*result_)


if __name__ == "__main__":
    # url = ["https://dev15.miveh-nejad.info/RNA/v2/?seq=ATGC"] * 3
    # print(asyncio.run(fetch_all_urls()))
    for i in asyncio.run(fetch_all_urls()):
        print(i)
