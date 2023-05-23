def force_int_input(question: str) -> int:
    try:
        return int(input(question))
    except:
        return force_int_input(question)