def filter_strings(filter_func, string_array):

    return list(filter(filter_func, string_array))



if __name__ == "__main__":
    sample_array = ["apple", "banana", "a test", "hello world", "code", "python", "anaconda", " "]

    # Исключить строки с пробелами
    result1 = filter_strings(lambda s: ' ' not in s, sample_array)
    print("Без пробелов:", result1)

    # Исключить строки, начинающиеся с буквы "a"
    result2 = filter_strings(lambda s: not s.startswith('a'), sample_array)
    print("Не начинаются на 'a':", result2)

    # Исключить строки, длина которых меньше 5
    result3 = filter_strings(lambda s: len(s) >= 5, sample_array)
    print("Длина >= 5:", result3)