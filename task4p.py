
# import os
# import time
# import multiprocessing as mp
# from multiprocessing import shared_memory
# from pathlib import Path
#
# import numpy as np
#
# STUDENT_ID = "230103189"
# MATRIX_SIZE = 8000
# PHYSICAL_CORES = 14
# SEED = int(STUDENT_ID)
#
# # Shared variables available to each worker process
# _shared_memory = None
# _matrix = None
#
# # =======================================================
# # TASK 1: SPATIAL CACHE PROFILING
# # =======================================================
# # Student ID       : 230103189
# # Logical CPUs     : 20
# # Physical workers : 14
# # Matrix size      : 8000 x 8000
# # Data type        : float64
# # Random seed      : 230103189
# # -------------------------------------------------------
# # Mode A (Row-Major)       : 1233.72 ms
# # Mode B (Column-Major)    : 113.62 ms
# # Cache penalty factor     : 0.09x
# # Mode A sum               : 31997461.136610
# # Mode B sum               : 31997461.136610
# # Sums match               : True
# # =======================================================
# # Output saved to: C:\Users\Ернар\PycharmProjects\PythonProject3\task4p_output.txt
#
# def initialize_worker(shm_name, shape):
#     global _shared_memory, _matrix
#
#     _shared_memory = shared_memory.SharedMemory(name=shm_name)
#     _matrix = np.ndarray(
#         shape, dtype=np.float64, buffer=_shared_memory.buf
#     )
#
#
# def sum_chunk(task):
#     mode, start, end = task
#
#     if mode == "A":
#         # Row-major: traverse contiguous rows
#         return float(np.sum(_matrix[start:end, :]))
#
#     # Column-major/strided: traverse a range of columns
#     return float(np.sum(_matrix[:, start:end]))
#
#
# def main():
#     workers = min(PHYSICAL_CORES, os.cpu_count() or 1)
#     shape = (MATRIX_SIZE, MATRIX_SIZE)
#     matrix_bytes = MATRIX_SIZE * MATRIX_SIZE * 8
#
#     shm = shared_memory.SharedMemory(
#         create=True, size=matrix_bytes
#     )
#
#     matrix = np.ndarray(
#         shape, dtype=np.float64, buffer=shm.buf
#     )
#
#     try:
#         # Generate reproducible data using the student ID seed
#         rng = np.random.default_rng(SEED)
#         matrix[:] = rng.random(shape, dtype=np.float64)
#
#         # Divide rows and columns among all worker processes
#         row_edges = np.linspace(
#             0, MATRIX_SIZE, workers + 1, dtype=int
#         )
#         col_edges = np.linspace(
#             0, MATRIX_SIZE, workers + 1, dtype=int
#         )
#
#         row_tasks = [
#             ("A", int(row_edges[i]), int(row_edges[i + 1]))
#             for i in range(workers)
#         ]
#
#         col_tasks = [
#             ("B", int(col_edges[i]), int(col_edges[i + 1]))
#             for i in range(workers)
#         ]
#
#         with mp.Pool(
#             processes=workers,
#             initializer=initialize_worker,
#             initargs=(shm.name, shape),
#         ) as pool:
#
#             start = time.perf_counter()
#             row_results = pool.map(sum_chunk, row_tasks)
#             time_a = (time.perf_counter() - start) * 1000
#
#             start = time.perf_counter()
#             col_results = pool.map(sum_chunk, col_tasks)
#             time_b = (time.perf_counter() - start) * 1000
#
#         sum_a = sum(row_results)
#         sum_b = sum(col_results)
#         penalty = time_b / time_a if time_a > 0 else float("nan")
#
#         print("=" * 55)
#         print("TASK 1: SPATIAL CACHE PROFILING")
#         print("=" * 55)
#         print(f"Student ID       : {STUDENT_ID}")
#         print(f"Logical CPUs     : {os.cpu_count()}")
#         print(f"Physical workers : {workers}")
#         print(f"Matrix size      : {MATRIX_SIZE} x {MATRIX_SIZE}")
#         print(f"Data type        : float64")
#         print(f"Random seed      : {SEED}")
#         print("-" * 55)
#         print(f"Mode A (Row-Major)       : {time_a:.2f} ms")
#         print(f"Mode B (Column-Major)    : {time_b:.2f} ms")
#         print(f"Cache penalty factor     : {penalty:.2f}x")
#         print(f"Mode A sum               : {sum_a:.6f}")
#         print(f"Mode B sum               : {sum_b:.6f}")
#         print(f"Sums match               : {np.isclose(sum_a, sum_b)}")
#         print("=" * 55)
#
#         output = Path(__file__).with_name("task4p_output.txt")
#         with output.open("w", encoding="utf-8") as file:
#             file.write("TASK 1: SPATIAL CACHE PROFILING\n")
#             file.write(f"Student ID: {STUDENT_ID}\n")
#             file.write(f"Logical CPUs: {os.cpu_count()}\n")
#             file.write(f"Physical workers: {workers}\n")
#             file.write(f"Matrix size: {MATRIX_SIZE} x {MATRIX_SIZE}\n")
#             file.write(f"Mode A (Row-Major): {time_a:.2f} ms\n")
#             file.write(f"Mode B (Column-Major): {time_b:.2f} ms\n")
#             file.write(f"Cache penalty factor: {penalty:.2f}x\n")
#             file.write(f"Mode A sum: {sum_a:.6f}\n")
#             file.write(f"Mode B sum: {sum_b:.6f}\n")
#             file.write(f"Sums match: {np.isclose(sum_a, sum_b)}\n")
#
#         print(f"Output saved to: {output}")
#
#     finally:
#         shm.close()
#         shm.unlink()
#
#
# if __name__ == "__main__":
#     mp.freeze_support()
#     main()

# # =======================================================# # =======================================================
# # =======================================================
# # =======================================================
# # =======================================================
# # =======================================================
# # =======================================================
# ==================================TASK2===================================

# import os
# import time
# import threading
# from concurrent.futures import ThreadPoolExecutor
#
# import numpy as np
#
# STUDENT_ID = 230103189
# TOTAL_POINTS = 40_000_000
# NUM_THREADS = 4
# BATCH_SIZE = 10_000
#
# # One shared PRNG and one mutex for Mode A
# shared_rng = np.random.default_rng(STUDENT_ID)
# rng_lock = threading.Lock()
#
#
# def simulate_shared(points):
#     """All threads share one PRNG protected by a lock."""
#     inside = 0
#
#     while points > 0:
#         n = min(BATCH_SIZE, points)
#
#         # Protect access to the shared generator state
#         with rng_lock:
#             samples = shared_rng.random((n, 2))
#
#         # Count points inside the quarter-circle
#         inside += np.count_nonzero(
#             samples[:, 0] ** 2 + samples[:, 1] ** 2 <= 1.0
#         )
#         points -= n
#
#     return inside
#
#
# def simulate_independent(args):
#     """Each thread uses its own independently seeded PRNG."""
#     thread_index, points = args
#
#     seed = (STUDENT_ID * 10) + thread_index
#     rng = np.random.default_rng(seed)
#     inside = 0
#
#     while points > 0:
#         n = min(BATCH_SIZE, points)
#         samples = rng.random((n, 2))
#
#         inside += np.count_nonzero(
#             samples[:, 0] ** 2 + samples[:, 1] ** 2 <= 1.0
#         )
#         points -= n
#
#     return inside
#
#
# def estimate_pi(inside, total):
#     return 4.0 * inside / total
#
#
# def main():
#     points_per_thread = TOTAL_POINTS // NUM_THREADS
#
#     print("=" * 60)
#     print("TASK 2: PRNG STATE BOTTLENECK")
#     print("=" * 60)
#     print(f"Student ID       : {STUDENT_ID}")
#     print(f"Logical CPUs     : {os.cpu_count()}")
#     print(f"Threads          : {NUM_THREADS}")
#     print(f"Total points     : {TOTAL_POINTS:,}")
#     print("-" * 60)
#
#     # Mode A: shared generator protected by a mutex
#     start = time.perf_counter()
#
#     with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
#         shared_counts = list(
#             executor.map(
#                 simulate_shared,
#                 [points_per_thread] * NUM_THREADS
#             )
#         )
#
#     shared_time = (time.perf_counter() - start) * 1000
#     shared_inside = sum(shared_counts)
#     shared_pi = estimate_pi(shared_inside, TOTAL_POINTS)
#     shared_error = abs(shared_pi - np.pi)
#
#     # Mode B: one generator per thread
#     start = time.perf_counter()
#
#     tasks = [
#         (i, points_per_thread) for i in range(NUM_THREADS)
#     ]
#
#     with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
#         independent_counts = list(
#             executor.map(simulate_independent, tasks)
#         )
#
#     independent_time = (time.perf_counter() - start) * 1000
#     independent_inside = sum(independent_counts)
#     independent_pi = estimate_pi(independent_inside, TOTAL_POINTS)
#     independent_error = abs(independent_pi - np.pi)
#
#     speedup = (
#         shared_time / independent_time
#         if independent_time > 0 else float("nan")
#     )
#
#     print("SHARED PRNG (mutex)")
#     print(f"Computed pi      : {shared_pi:.10f}")
#     print(f"Absolute error   : {shared_error:.10f}")
#     print(f"Wall time        : {shared_time:.2f} ms")
#     print("-" * 60)
#
#     print("INDEPENDENT PRNGs")
#     print(f"Computed pi      : {independent_pi:.10f}")
#     print(f"Absolute error   : {independent_error:.10f}")
#     print(f"Wall time        : {independent_time:.2f} ms")
#     print("-" * 60)
#
#     print(f"Speedup factor   : {speedup:.2f}x")
#     print("=" * 60)
#
#     output_path = os.path.join(
#         os.path.dirname(os.path.abspath(__file__)),
#         "task2_output.txt"
#     )
#
#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write("TASK 2: PRNG STATE BOTTLENECK\n")
#         f.write(f"Student ID: {STUDENT_ID}\n")
#         f.write(f"Logical CPUs: {os.cpu_count()}\n")
#         f.write(f"Threads: {NUM_THREADS}\n")
#         f.write(f"Total points: {TOTAL_POINTS}\n\n")
#
#         f.write("SHARED PRNG (mutex)\n")
#         f.write(f"Computed pi: {shared_pi:.10f}\n")
#         f.write(f"Absolute error: {shared_error:.10f}\n")
#         f.write(f"Wall time: {shared_time:.2f} ms\n\n")
#
#         f.write("INDEPENDENT PRNGs\n")
#         f.write(f"Computed pi: {independent_pi:.10f}\n")
#         f.write(f"Absolute error: {independent_error:.10f}\n")
#         f.write(f"Wall time: {independent_time:.2f} ms\n\n")
#
#         f.write(f"Speedup factor: {speedup:.2f}x\n")
#
#     print(f"Output saved to: {output_path}")
#
#
# if __name__ == "__main__":
#     main()
# ============================================================================================================================================
# =====================================================================================================
# =====================================================================================================
# =====================================================================================================
# =======================================Task3==============================================================

# import os
# import sys
# import time
# from concurrent.futures import ThreadPoolExecutor
#
# import numpy as np
#
# STUDENT_ID = 230103189
# ARRAY_SIZE = 2_000_000
# NUM_THREADS = 4
#
#
# def compute_local_scan(chunk):
#     """Pass 1: calculate each chunk's inclusive prefix sum."""
#     local_output = np.cumsum(chunk, dtype=np.int64)
#     chunk_sum = int(local_output[-1])
#     return local_output, chunk_sum
#
#
# def apply_offset(args):
#     """Pass 2: add the prefix sum of all previous chunks."""
#     local_output, offset = args
#
#     if offset != 0:
#         local_output += offset
#
#     return local_output
#
#
# def main():
#     rng = np.random.default_rng(STUDENT_ID)
#     data = rng.integers(
#         1, 11, size=ARRAY_SIZE, dtype=np.int64
#     )
#
#     chunks = [
#         chunk for chunk in np.array_split(data, NUM_THREADS)
#     ]
#
#     # Serial inclusive prefix sum
#     start = time.perf_counter()
#     serial_output = np.cumsum(data, dtype=np.int64)
#     serial_time = (time.perf_counter() - start) * 1000
#
#     # Parallel chunked prefix scan
#     start = time.perf_counter()
#
#     with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
#         local_results = list(
#             executor.map(compute_local_scan, chunks)
#         )
#
#         local_outputs = [result[0] for result in local_results]
#         chunk_sums = [result[1] for result in local_results]
#
#         # Offset reduction: calculate each chunk's starting offset
#         offsets = []
#         running_total = 0
#
#         for chunk_sum in chunk_sums:
#             offsets.append(running_total)
#             running_total += chunk_sum
#
#         # Apply offsets to local prefix sums in parallel
#         parallel_output = list(
#             executor.map(
#                 apply_offset,
#                 zip(local_outputs, offsets)
#             )
#         )
#
#     parallel_output = np.concatenate(parallel_output)
#     parallel_time = (time.perf_counter() - start) * 1000
#
#     speedup = (
#         serial_time / parallel_time
#         if parallel_time > 0 else float("nan")
#     )
#
#     # Verify the required final prefix sum
#     verification = (
#         parallel_output[-1] == serial_output[-1]
#     )
#
#     print("=" * 65)
#     print("TASK 3: PARALLEL PREFIX SCAN")
#     print("=" * 65)
#     print(f"Student ID       : {STUDENT_ID}")
#     print(f"Logical CPUs     : {os.cpu_count()}")
#     print(f"Array size       : {ARRAY_SIZE:,}")
#     print(f"Threads          : {NUM_THREADS}")
#     print("-" * 65)
#     print(f"Serial Time      : {serial_time:.2f} ms")
#     print(f"Parallel Time    : {parallel_time:.2f} ms")
#     print(f"Speedup          : {speedup:.2f}x")
#     print(
#         f"Verification     : {'PASS' if verification else 'FAIL'}"
#     )
#     print(f"Serial final sum : {serial_output[-1]}")
#     print(f"Parallel final   : {parallel_output[-1]}")
#     print("=" * 65)
#
#     output_path = os.path.join(
#         os.path.dirname(os.path.abspath(__file__)),
#         "task3_output.txt"
#     )
#
#     with open(output_path, "w", encoding="utf-8") as file:
#         file.write("TASK 3: PARALLEL PREFIX SCAN\n")
#         file.write(f"Student ID: {STUDENT_ID}\n")
#         file.write(f"Logical CPUs: {os.cpu_count()}\n")
#         file.write(f"Array size: {ARRAY_SIZE}\n")
#         file.write(f"Threads: {NUM_THREADS}\n")
#         file.write(f"Serial Time: {serial_time:.2f} ms\n")
#         file.write(f"Parallel Time: {parallel_time:.2f} ms\n")
#         file.write(f"Speedup: {speedup:.2f}x\n")
#         file.write(
#             f"Verification: {'PASS' if verification else 'FAIL'}\n"
#         )
#         file.write(f"Serial final sum: {serial_output[-1]}\n")
#         file.write(f"Parallel final sum: {parallel_output[-1]}\n")
#
#     print(f"Output saved to: {output_path}")
#
#     try:
#         assert parallel_output[-1] == serial_output[-1], (
#             "Parallel final prefix sum does not match serial result!"
#         )
#     except AssertionError as error:
#         print(f"ERROR: {error}", file=sys.stderr)
#         raise SystemExit(1)
#
#
# if __name__ == "__main__":
#     main()
# ============================================================================================================================================
# =====================================================================================================
# =====================================================================================================
# =====================================================================================================
# =======================================Task4==============================================================

import multiprocessing as mp
from multiprocessing import shared_memory
from statistics import median
from time import perf_counter
from pathlib import Path
import os
import numpy as np

STUDENT_ID = 230103189
ARRAY_SIZES = [100_000, 1_000_000, 10_000_000]
REPEATS = 3


def receiver(input_queue, result_queue):
    """Receive arrays using IPC or shared memory."""
    while True:
        message = input_queue.get()

        if message is None:
            break

        mode, payload, shape = message

        if mode == "ipc":
            array = payload
            checksum = int(np.sum(array, dtype=np.int64))

        elif mode == "shared":
            shm = shared_memory.SharedMemory(name=payload)
            try:
                array = np.ndarray(
                    shape, dtype=np.int64, buffer=shm.buf
                )
                checksum = int(np.sum(array, dtype=np.int64))
            finally:
                shm.close()

        else:
            raise ValueError(f"Unknown mode: {mode}")

        result_queue.put(checksum)


def benchmark_ipc(array, input_queue, result_queue):
    """Measure sending a serialized array and receiving its acknowledgement."""
    start = perf_counter()

    input_queue.put(("ipc", array, None))
    received_checksum = result_queue.get()

    elapsed_ms = (perf_counter() - start) * 1000
    expected_checksum = int(np.sum(array, dtype=np.int64))

    assert received_checksum == expected_checksum
    return elapsed_ms


def benchmark_shared(array, input_queue, result_queue):
    """Measure shared-memory allocation, copying, handoff and reading."""
    shm = None

    try:
        start = perf_counter()

        shm = shared_memory.SharedMemory(
            create=True, size=array.nbytes
        )

        shared_array = np.ndarray(
            array.shape, dtype=np.int64, buffer=shm.buf
        )
        shared_array[:] = array

        input_queue.put(("shared", shm.name, array.shape))
        received_checksum = result_queue.get()

        elapsed_ms = (perf_counter() - start) * 1000
        expected_checksum = int(np.sum(array, dtype=np.int64))

        assert received_checksum == expected_checksum
        return elapsed_ms

    finally:
        if shm is not None:
            shm.close()
            shm.unlink()


def main():
    ctx = mp.get_context("spawn")
    input_queue = ctx.Queue()
    result_queue = ctx.Queue()

    worker = ctx.Process(
        target=receiver,
        args=(input_queue, result_queue)
    )
    worker.start()

    results = []

    try:
        print("=" * 76)
        print("TASK 4: MEMORY TRANSFER / IPC OVERHEAD")
        print("=" * 76)
        print(f"Student ID: {STUDENT_ID}")
        print(f"Logical CPUs: {os.cpu_count()}")
        print("Mode: CPU-only multiprocessing")
        print(f"Measurement: median of {REPEATS} runs")
        print("-" * 76)
        print(
            f"{'Array size':>14} | {'IPC Queue (ms)':>16} | "
            f"{'Shared Memory (ms)':>19} | {'Faster path':>12}"
        )
        print("-" * 76)

        for size in ARRAY_SIZES:
            rng = np.random.default_rng(STUDENT_ID + size)
            array = rng.integers(
                1, 101, size=size, dtype=np.int64
            )

            ipc_times = []
            shared_times = []

            for _ in range(REPEATS):
                ipc_times.append(
                    benchmark_ipc(array, input_queue, result_queue)
                )
                shared_times.append(
                    benchmark_shared(
                        array, input_queue, result_queue
                    )
                )

            ipc_ms = median(ipc_times)
            shared_ms = median(shared_times)

            if ipc_ms < shared_ms:
                faster = "IPC Queue"
            elif shared_ms < ipc_ms:
                faster = "Shared Memory"
            else:
                faster = "Equal"

            results.append((size, ipc_ms, shared_ms, faster))

            print(
                f"{size:>14,} | {ipc_ms:>16.2f} | "
                f"{shared_ms:>19.2f} | {faster:>12}"
            )

        print("=" * 76)

        output_path = Path(__file__).with_name("task4_output.txt")
        with output_path.open("w", encoding="utf-8") as file:
            file.write("TASK 4: MEMORY TRANSFER / IPC OVERHEAD\n")
            file.write(f"Student ID: {STUDENT_ID}\n")
            file.write(f"Logical CPUs: {os.cpu_count()}\n")
            file.write(f"Measurements per size: {REPEATS}\n")
            file.write("Times are medians in milliseconds.\n\n")
            file.write(
                "Array size | IPC Queue (ms) | Shared Memory (ms) "
                "| Faster path\n"
            )

            for size, ipc_ms, shared_ms, faster in results:
                file.write(
                    f"{size} | {ipc_ms:.2f} | "
                    f"{shared_ms:.2f} | {faster}\n"
                )

        print(f"Output saved to: {output_path}")

    finally:
        input_queue.put(None)
        worker.join()
        input_queue.close()
        result_queue.close()


if __name__ == "__main__":
    mp.freeze_support()
    main()
