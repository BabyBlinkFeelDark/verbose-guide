import random
import time
import math
import concurrent.futures
import multiprocessing
from multiprocessing import Process, Queue
import json
import csv

def generate_data(n):
    for _ in range(n):
        yield random.randint(1, 1000)

def process_number(number):
    return math.factorial(number)

def process_with_threads(data):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_number, data))
    return results

def process_with_multiprocessing_pool(data):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(process_number, data)
    return results

def process_with_multiprocessing_processes(data):
    def worker_func(input_q, output_q):
        while True:
            item = input_q.get()
            if item is None:
                break
            result = process_number(item)
            output_q.put(result)

    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    num_workers = multiprocessing.cpu_count()
    processes = []
    for _ in range(num_workers):
        p = Process(target=worker_func, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    for num in data:
        input_queue.put(num)

    for _ in range(num_workers):
        input_queue.put(None)

    results = []
    for _ in range(len(data)):
        results.append(output_queue.get())

    for p in processes:
        p.join()

    return results

def measure_time(func, data):
    start_time = time.time()
    func(data)
    end_time = time.time()
    return end_time - start_time

def save_time_to_csv(results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Method', 'Time (seconds)'])
        for method, t in results:
            writer.writerow([method, t])


if __name__ == "__main__":
    data = list(generate_data(100000))

    thread_pool_time = measure_time(process_with_threads, data)

    multiprocessing_pool_time = measure_time(process_with_multiprocessing_pool, data)

    multiprocessing_processes_time = measure_time(process_with_multiprocessing_processes, data)

    results = [
        ("Thread Pool", thread_pool_time),
        ("Multiprocessing Pool", multiprocessing_pool_time),
        ("Multiprocessing Processes", multiprocessing_processes_time),
    ]

    save_time_to_csv(results, 'execution_times.csv')

    for method, t in results:
        print(f"{method} Time: {t:.4f} seconds")
