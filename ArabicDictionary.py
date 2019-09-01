# Hanoof Algofari - Last Version - The Concordancer System
import os
import re
from nltk.tokenize import word_tokenize
from nltk.stem.isri import ISRIStemmer


word_dict = {}
stem_dict = {}
file_numbers = {}


def de_noise_arabic(text):
    # Text Prepossessing - Text Normalization
    noise = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ
                         """, re.VERBOSE)
    text = re.sub(noise, '', text)
    return text


def clean_text(text):
    # Text Prepossessing - Noise Removal
    newline_re = r'[\n]+'
    num_chars_ar_re = r'[\""«»,١٢٣٤٥٦٧٨٩٠؟!٪:،؛\[\]\.]+'
    num_chars_en_re = r'[0123456789!"$%&\\\'()*+,-;<>=?@[]^_`{═}—“”•‹|~«°»˓ ̮ ̯]+…'
    white_space_re = r"\s+"

    text = re.sub(newline_re, r' ', text, flags=re.UNICODE)
    text = re.sub(num_chars_ar_re, r'', text, flags=re.UNICODE)
    text = re.sub(num_chars_en_re, r'', text, flags=re.UNICODE)
    text = re.sub(r'[A-Za-z0-9-@:!_#/()]', '', text, flags=re.MULTILINE)
    text = re.sub(white_space_re, r' ', text, flags=re.UNICODE)

    return text


def all_steps(text, steps):
    steps_dict = {'de_noise': de_noise_arabic,
                  'clean': clean_text}

    if len(steps):
        for step in steps:
            text = steps_dict[step](text)

    return text


def build_word_dictionary(file_number, preprocessed_text, stop_words):
    # This method builds the Words Dictionary as follows
    # {'word1':[['file_number', 'word_index'], ['file_number', 'word_index'], ...],
    #  'word2':[['file_number', 'word_index'], ['file_number', 'word_index'], ...], ...}
    i = 0
    words_list = word_tokenize(preprocessed_text)
    for token in words_list:
        if token not in stop_words:

            if not word_dict.get(token):
                sub_list = []
                sub_list.append(file_number)
                sub_list.append(i)
                word_dict[token] = []
                word_dict[token].append(sub_list)

            else:
                sub_list = []
                sub_list.append(file_number)
                sub_list.append(i)
                word_dict[token].append(sub_list)

        i += 1


def build_stem_dictionary(preprocessed_text, stop_words):
    # This method builds the Roots Dictionary as follows
    # {'stemmed_word1': ['derived_word1', 'derived_word2', ...],
    #  'stemmed_word2': ['derived_word1', 'derived_word2', 'derived_word3', ...], ...}
    st = ISRIStemmer()
    words_list = word_tokenize(preprocessed_text)
    for token in words_list:
        if token not in stop_words and token not in ['.']:
            stemmed_token = st.stem(token)
            if not stem_dict.get(stemmed_token):
                stem_dict[stemmed_token] = []
            if not token in stem_dict[stemmed_token]:
                stem_dict[stemmed_token].append(token)


def get_fixed_con(list_of_occurrences):
    # This method will take the occurrences list for a specific word and get all the concordance outputs
    # for each of these occurrence, storing it in a concordances_output list
    # Fixed concordance size (approximately 5 words before and after the specific word)

    concordances_output = []
    for x in range(len(list_of_occurrences)):
        occurrence_list = list_of_occurrences[x]
        file_number = occurrence_list[0]
        word_index = occurrence_list[1]
        file_name = file_numbers[file_number]

        file_data = open("corpus/" + file_name, 'r', encoding='utf-8-sig').read()
        steps = ['de_noise', 'clean']
        preprocessed_text = all_steps(file_data, steps)

        words_list = word_tokenize(preprocessed_text)
        filter_sentence2 = " "
        if word_index > 5:
            filter_sentence2 = " ".join(words_list[word_index - 5:word_index + 6])
        else:
            filter_sentence2 = " ".join(words_list[0:word_index + 6])

        if not filter_sentence2 in concordances_output:
            concordances_output.append(filter_sentence2)
    return concordances_output


def get_changeable_con(list_of_occurrences, size):
    # This method will take the occurrences list for a specific word and get all the concordance outputs
    # for each of these occurrence, storing it in a concordances_output list
    # Changeable concordance size (the user will determine the number of words before and after the specific word)

    concordances_output = []
    for x in range(len(list_of_occurrences)):
        occurrence_list = list_of_occurrences[x]
        file_number = occurrence_list[0]
        word_index = occurrence_list[1]
        file_name = file_numbers[file_number]

        file_data = open("corpus/" + file_name, 'r', encoding='utf-8-sig').read()
        steps = ['de_noise', 'clean']
        preprocessed_text = all_steps(file_data, steps)

        words_list = word_tokenize(preprocessed_text)
        filter_sentence2 = " "
        if word_index > size:
            filter_sentence2 = " ".join(words_list[word_index - size:word_index + size + 1])
        else:
            filter_sentence2 = " ".join(words_list[0:word_index + size + 1])

        if not filter_sentence2 in concordances_output:
            concordances_output.append(filter_sentence2)
    return concordances_output


def printing_word_dict():
    print("No of Arabic Words in the Words Dictionary: " + str(len(word_dict)) + "\n")
    for token in word_dict:
        print("Word : " + token)
        print("Documents and Positions : ")
        print(*word_dict[token])
        print("\n")


def printing_stem_dict():
    print("No of Arabic Roots in the Roots Dictionary: " + str(len(stem_dict)) + "\n")
    for stemmed_word in stem_dict:
        print("Stemmed Word : " + stemmed_word)
        print("Derived Words : ")
        print(*stem_dict[stemmed_word], sep="\n")
        print("\n")


def finding_fixed_con(word):
    st = ISRIStemmer()
    stemmed_word = st.stem(word)
    if stemmed_word == word:
        for token in stem_dict:
            if token == word:
                print("Stemmed Word : " + token)
                for x in range(len(stem_dict[token])):
                    derived_word = stem_dict[token][x]
                    print("Derived Word : ")
                    print(derived_word)
                    print("Sentences : ")
                    occurrences_list = word_dict[derived_word]
                    concordances_output = get_fixed_con(occurrences_list)
                    print(*concordances_output, sep="\n")

    else:
        for token in word_dict:
            if token == word:
                print("Word : " + token)
                print("Stemmed Word : " + stemmed_word)
                print("Sentences : ")
                occurrences_list = word_dict[token]
                concordances_output = get_fixed_con(occurrences_list)
                print(*concordances_output, sep="\n")
                print("\n")
    print("\n")


def finding_changeable_con(word, size):
    st = ISRIStemmer()
    stemmed_word = st.stem(word)
    if stemmed_word == word:
        for token in stem_dict:
            if token == word:
                print("Stemmed Word : " + token)
                for x in range(len(stem_dict[token])):
                    derived_word = stem_dict[token][x]
                    print("Derived Word : ")
                    print(derived_word)
                    print("Sentences : ")
                    occurrences_list = word_dict[derived_word]
                    concordances_output = get_changeable_con(occurrences_list, size)
                    print(*concordances_output, sep="\n")

    else:
        for token in word_dict:
            if token == word:
                print("Word : " + token)
                print("Stemmed Word : " + stemmed_word)
                print("Sentences : ")
                occurrences_list = word_dict[token]
                concordances_output = get_changeable_con(occurrences_list, size)
                print(*concordances_output, sep="\n")
                print("\n")
    print("\n")


def finding_derived_words(stemmed_word):
    for token in stem_dict:
        if token == stemmed_word:
            print("Stemmed Word : " + stemmed_word)
            print("Derived Words : ")
            print(*stem_dict[stemmed_word], sep="\n")
            print("\n")
            break


def main():
    num = 1
    ar_stopwords_list = open('arabic_stop_word.txt', 'r', encoding='utf-8')
    stop_words = ar_stopwords_list.read().split('\n')
    file_names = os.listdir('./corpus')
    for file_name in file_names:
        # Open the file
        if file_name.endswith(".txt"):
            file_numbers[num] = file_name
            file_data = open("corpus/" + file_name, 'r', encoding='utf-8-sig').read()
            steps = ['de_noise', 'clean']
            preprocessed_text = all_steps(file_data, steps)
            build_word_dictionary(num, preprocessed_text, stop_words)
            build_stem_dictionary(preprocessed_text, stop_words)
            num = num + 1

    print("\n\nWelcome to the Concordancer Tool...\n\n"
          "please choose a number from the below list:\n\n"
          "1: To Print the Words Dictionary \n"
          "2: To Print the Roots Dictionary\n"
          "3: To Find all the Concordances for a Specific Word (with a Fixed Window Size = 5)\n"
          "4: To Find all the Concordances for a Specific Word (with a Changeable Window Size)\n"
          "5: To Find all the Derived Words for a Specific Word\n"
          "6: To Exit the Concordancer Tool\n")
    while True:
        choice = input("Enter Your Choice:")
        if choice == "1":
            printing_word_dict()
        elif choice == "2":
            printing_stem_dict()
        elif choice == "3":
            word = input("Please Enter the word:")
            finding_fixed_con(word)
        elif choice == "4":
            word = input("Please Enter the word:")
            size = int(input("Please Enter the Number of Preceding and Subsequent Words:"))
            finding_changeable_con(word, size)
        elif choice == "5":
            word = input("Please Enter the word:")
            finding_derived_words(word)
        elif choice == "6":
            os._exit(1)


if __name__ == '__main__':
    main()
