## CODE PROMPTS FOR LLM
code_prompt_1 = "Write a Python script that takes two integers as inputs and returns their greatest common divisor (GCD)."
code_prompt_2 = "Write a Python script that takes a string as input and counts the number of vowels and consonants."
code_prompt_3 = "Write a Python script that takes a string as input and checks if it is a palindrome."
code_prompt_4 = "Write a Python script that takes a list of integers as input and calculates the mean, median, and mode."
code_prompt_5 = "Write a Python script that takes two datetime objects as input and calculates the difference between them in days."
code_prompt_6 = "Write a Python script that takes a string as input and converts it into a datetime object."
code_prompt_7 = "Write a Python script that takes an integer as input and prints the Fibonacci sequence up to that number."
code_prompt_8 = "Write a Python script that takes a string as input and returns the string in reverse order."
code_prompt_9 = "Write a Python script that takes two integers as input and calculates their least common multiple (LCM)."
code_prompt_10 = "Write a Python script that takes a list of integers as input and returns the list sorted in ascending order."
code_prompt_11 = "Write a Python script that takes a string as input and checks if it contains any special characters."
code_prompt_12 = "Write a Python script that takes a datetime object as input and returns the day of the week."
code_prompt_13 = "Write a Python script that takes a string as input and counts the number of words in the string."
code_prompt_14 = "Write a Python script that takes an integer as input and checks if it's a prime number."
code_prompt_15 = "Write a Python script that takes two datetime objects as input and calculates the difference between them in minutes."
code_prompt_16 = "Write a Python script that takes a string as input and converts it to upper case."
code_prompt_17 = "Write a Python script that takes an integer as input and generates a square matrix of that size filled with random numbers."
code_prompt_18 = "Write a Python script that takes a string as input and calculates the frequency of each character."
code_prompt_19 = "Write a Python script that takes a list of integers as input and returns the sum of all the elements in the list."
code_prompt_20 = "Write a Python script that takes a datetime object as input and returns the date in 'Month Day, Year' format."
code_prompts = [code_prompt_1,
                code_prompt_2,
                code_prompt_3,
                code_prompt_4,
                code_prompt_5,
                code_prompt_6,
                code_prompt_7,
                code_prompt_8,
                code_prompt_9,
                code_prompt_10,
                code_prompt_11,
                code_prompt_12,
                code_prompt_13,
                code_prompt_14,
                code_prompt_15,
                code_prompt_16,
                code_prompt_17,
                code_prompt_18,
                code_prompt_19,
                code_prompt_20
                ]

## CODE EXAMPLE ANSWERS (There are many ways to write the same function)
code_answer_1 = """import math

def gcd(a, b):
    return math.gcd(a, b)
"""
code_answer_2 = """def count_vowels_consonants(s):
    vowels = "aeiouAEIOU"
    s = s.replace(" ", "")
    v = sum([1 for char in s if char in vowels])
    c = len(s) - v
    return {"vowels": v, "consonants": c}
"""
code_answer_3 = """def is_palindrome(s):
    return s == s[::-1]
"""
code_answer_4 = """import statistics

def calculate_mean_median_mode(lst):
    mean = statistics.mean(lst)
    median = statistics.median(lst)
    mode = statistics.mode(lst)
    return {"mean": mean, "median": median, "mode": mode}
"""
code_answer_5 = """def date_diff(date1, date2):
    return abs((date2 - date1).days)
"""
code_answer_6 = """from datetime import datetime

def str_to_datetime(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
"""
code_answer_7 = """def fibonacci(n):
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
"""
code_answer_8 = """def reverse_string(s):
    return s[::-1]
"""
code_answer_9 = """def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)
"""
code_answer_10 = """def sort_list(lst):
    return sorted(lst)
"""
code_answer_11 = """import re

def check_special_characters(input_string):
    regex = re.compile('[@_!#$%^&*()<>?/\\|}{~:]')
    if(regex.search(input_string) == None):
        return False
    else:
        return True
"""
code_answer_12 = """import datetime

def get_day_of_week(datetime_object):
    return datetime_object.strftime('%A')
"""
code_answer_13 = """def count_words(input_string):
    return len(input_string.split())
"""
code_answer_14 = """def check_prime(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                return False
        else:
            return True
    else:
        return False
"""
code_answer_15 = """def datetime_difference_in_minutes(datetime1, datetime2):
    difference = datetime2 - datetime1
    return difference.total_seconds() / 60.0
"""
code_answer_16 = """def to_upper_case(input_string):
    return input_string.upper()
"""
code_answer_17 = """import numpy as np

def generate_random_matrix(size):
    return np.random.rand(size, size)
"""
code_answer_18 = """from collections import Counter

def character_frequency(input_string):
    return dict(Counter(input_string))
"""
code_answer_19 = """def sum_of_elements(input_list):
    return sum(input_list)
"""
code_answer_20 = """def get_date_in_format(datetime_object):
    return datetime_object.strftime('%B %d, %Y')
"""
code_answers = [code_answer_1,
                code_answer_2,
                code_answer_3,
                code_answer_4,
                code_answer_5,
                code_answer_6,
                code_answer_7,
                code_answer_8,
                code_answer_9,
                code_answer_10,
                code_answer_11,
                code_answer_12,
                code_answer_13,
                code_answer_14,
                code_answer_15,
                code_answer_16,
                code_answer_17,
                code_answer_18,
                code_answer_19,
                code_answer_20
                ]