def read_file(filename):
    with open(filename, 'r') as file:
        words = file.read().split(';')
    return words

# filename = 'filePulling.txt'
# words_list = read_file(filename)
# print(words_list)