import re
from translator import Translator

def translate():
    input_file_name = "input.txt"
    output_file_name = "output.txt"
    translator = Translator()
    with open(input_file_name) as inputFile, open(output_file_name, "w") as outputFile:
        for line in inputFile:
            indentation = line[:-len(line.lstrip())]
            if translator.contains_sfmc_line(line) is True:
                line = line.strip()
                if is_if_condition(line) is True:
                    variable, translated = translator.translate_if_condition(line)
                    new_line = variable
                    # if not translated. save to not translated file
                else:
                    words = line.split()
                    new_line = ""
                    for word in words:
                        if is_sfmc_variable(word) is True:
                            variable, translated = translator.translate_variables(word)
                            # if not translated. save to not translated file
                            new_line = new_line + " " + variable
                        else:
                            new_line = new_line + " " + word
                outputFile.write(indentation + new_line)
                outputFile.write('\n')
            else:
                outputFile.write(line)


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
