import time


def timing_decorator(func):

    def wrapper(*args, **kwargs):
        start_time = time.time() 
        result = func(*args, **kwargs)  
        end_time = time.time()  
        execution_time = end_time - start_time  
        print(f"Функция '{func.__name__}' выполнилась за {execution_time:.4f} секунд.")
        return result
    return wrapper



@timing_decorator
def sum_numbers(a, b):
    result = a + b
    print(f"Результат сложения: {result}")
    return result


@timing_decorator
def calculate_from_file(input_filename='input.txt', output_filename='output.txt'):
    try:
        with open(input_filename, 'r') as file:
            data = file.read().split()
            a = int(data[0])
            b = int(data[1])
    except FileNotFoundError:
        print(f"Файл {input_filename} не найден.")
        return
    except ValueError:
        print("Ошибка в данных файла. Ожидались два числа.")
        return

    result = a + b  

    with open(output_filename, 'w') as file:
        file.write(str(result))
    print(f"Результат {result} записан в файл {output_filename}")



if __name__ == "__main__":

    sum_numbers(100000000, 256984321)

    calculate_from_file()