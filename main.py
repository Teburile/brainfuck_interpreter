import sys
from sys import stdin, stdout
import numpy as np

bf_nums = np.zeros([0x10000000], dtype=np.int16)

bf_loop_brackets = np.zeros([0x1000000], dtype=np.int16)

bf_ptr_index = 0x8000000

bf_execute_index = 0


def bf_add_ptr():
    global bf_ptr_index, bf_execute_index
    bf_ptr_index += 1
    bf_execute_index += 1


def bf_sub_ptr():
    global bf_ptr_index, bf_execute_index
    bf_ptr_index -= 1
    bf_execute_index += 1


def bf_add_num():
    global bf_ptr_index, bf_nums, bf_execute_index
    bf_nums[bf_ptr_index] += 1
    bf_execute_index += 1


def bf_sub_num():
    global bf_ptr_index, bf_nums, bf_execute_index
    bf_nums[bf_ptr_index] -= 1
    bf_execute_index += 1


def bf_in():
    global bf_ptr_index, bf_nums, bf_execute_index
    bf_nums[bf_ptr_index] = ord(stdin.read(1))
    bf_execute_index += 1


def bf_out():
    global bf_ptr_index, bf_nums, bf_execute_index
    # print(bf_nums[bf_ptr_index])
    stdout.write(chr(int(bf_nums[bf_ptr_index])))
    bf_execute_index += 1


def bf_start_loop():
    global bf_ptr_index, bf_nums, bf_execute_index
    if bf_nums[bf_ptr_index] == 0:
        bf_execute_index = bf_loop_brackets[bf_execute_index]
    else:
        bf_execute_index += 1


def bf_end_loop():
    global bf_ptr_index, bf_nums, bf_execute_index
    if bf_nums[bf_ptr_index] == 0:
        bf_execute_index += 1
    else:
        bf_execute_index = bf_loop_brackets[bf_execute_index]


def execute_bf(bf_command: str):
    global bf_execute_index
    while bf_execute_index < len(bf_command):
        cmd = bf_command[bf_execute_index]
        if cmd == '>':
            bf_add_ptr()
        elif cmd == '<':
            bf_sub_ptr()
        elif cmd == '+':
            bf_add_num()
        elif cmd == '-':
            bf_sub_num()
        elif cmd == ',':
            bf_in()
        elif cmd == '.':
            bf_out()
        elif cmd == '[':
            bf_start_loop()
        elif cmd == ']':
            bf_end_loop()
        else:
            bf_execute_index += 1


def read_bf(bf_command):
    global bf_loop_brackets
    left_bracket_indexes = []
    search_index = 0
    while search_index < len(bf_command):
        if bf_command[search_index] == '[':
            left_bracket_indexes.append(search_index)
        elif bf_command[search_index] == ']':
            last_left_bracket_index = left_bracket_indexes.pop()
            bf_loop_brackets[search_index] = last_left_bracket_index
            bf_loop_brackets[last_left_bracket_index] = search_index
        search_index += 1


if __name__ == '__main__':
    file_name = sys.argv[1]
    bf_command = open(file_name, 'r').read()
    read_bf(bf_command)
    execute_bf(bf_command)
