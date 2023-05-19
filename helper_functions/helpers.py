def force_int_input(question):
    answer = input(question)
    try:
        return int(answer)
    except:
        return force_int_input(question)