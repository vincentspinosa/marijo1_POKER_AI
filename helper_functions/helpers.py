import multiprocessing

def force_int_input(question: str) -> int:
    try:
        return int(input(question))
    except:
        return force_int_input(question)
    
def cpu_minus_one():
    cores = multiprocessing.cpu_count()
    if cores <= 2:
        return 1
    return cores - 1
