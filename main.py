import re
from translator import Translator

translated_file = open("translated_values.txt", "w+")
not_translated_file = open("not_translated.txt", "w+")


def main():
    input_file_name = "input.txt"
    output_file_name = "output.txt"
    translator = Translator()
    with open(input_file_name) as inputFile, open(output_file_name, "w+") as outputFile:
        for line in inputFile:
            indentation = line[:-len(line.lstrip())]
            if translator.contains_sfmc_line_to_ignore(line.strip()) is True:
                continue
            if translator.contains_sfmc_line(line) is True:
                line = line.strip()
                if is_if_condition(line) is True:
                    translation, translated = translator.translate_if_condition(line)
                    new_line = translation
                    # log to translated or not translated file
                    log_translation(line, translation, translated)
                else:
                    words = line.split()
                    new_line = ""
                    for word in words:
                        if is_sfmc_variable(word) is True:
                            translation, translated = translator.translate_variables(word)
                            # log to translated or not translated file
                            log_translation(word, translation, translated)
                            new_line = new_line + " " + translation
                        elif is_sfmc_redirect(word) is True:
                            translation, translated = translator.translate_redirect(word)
                            # log to translated or not translated file
                            log_translation(word, translation, translated)
                            new_line = new_line + " " + translation
                        elif translator.contains_sfmc_line(word):  # unrecognised SFMC keyword
                            # log to translated or not translated file
                            log_translation(word, word, False)
                        else:
                            new_line = new_line + " " + word
                outputFile.write(indentation + new_line)
                outputFile.write('\n')
            else:
                outputFile.write(line)
    translated_file.close()
    not_translated_file.close()


def has_simple_if_condition(if_condition):
    return "if" in if_condition and \
           ("and" not in if_condition and "or" not in if_condition)


def has_simple_checks(if_condition):
    return "!= 'null'" in if_condition or "not empty" in if_condition or "== 'true'" in if_condition


def is_if_condition(line):
    start = re.escape(r'%%[')
    end = re.escape(']%%')
    if_condition = re.search(start + '(.*?)' + end, line)
    return if_condition is not None


def get_if_condition_line(line):
    start = re.escape(r'%%[')
    end = re.escape(']%%')
    if_condition = re.search(start + '(.*?)' + end, line)
    return if_condition.group(1)


def is_sfmc_variable(word):
    return "%%=v(@" in word


def is_sfmc_redirect(word):
    return "%%=RedirectTo" in word


def log_translation(original, translation, is_translated):
    if is_translated is True:
        translated_file.write(original + "  >>>>  " + translation)
        translated_file.write('\n')
        translated_file.write('\n')
    else:
        not_translated_file.write(original)
        not_translated_file.write('\n')
        not_translated_file.write('\n')


if __name__ == "__main__":
    main()
