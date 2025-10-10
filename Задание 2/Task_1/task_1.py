def is_palindrome(s:str)->bool:

    cleaned_string = s.replace(" ", "").lower()

    return cleaned_string == cleaned_string[::-1]