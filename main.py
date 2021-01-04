import re


def translate():
    input_file_name = "input.txt"
    output_file_name = "output.txt"
    with open(input_file_name) as inputFile, open(output_file_name, "w") as outputFile:
        for line in inputFile:
            indentation = line[:-len(line.lstrip())]
            line = line.strip()
            if is_if_condition is True:
                if_condition = get_if_condition_line(line)
                if has_simple_if_condition(if_condition):  # does not have any 'and' or 'or' operators
                    if has_simple_checks(if_condition):  # contains only '!- null' or 'not empty' or 'true'
                        variable = re.search(r'@\w+', if_condition).group().replace("@", "")
                        new_line = "{{#if " + variable + "}}"
                    else:
                        new_line = line
                elif "endif" in line:
                    new_line = "{{/if}}"
                else:
                    new_line = line
            else:
                words = line.split()
                new_line = ""
                for word in words:
                    if "%%=v(@" in word:
                        start = re.escape(r'%%=v(@')
                        end = re.escape(')=%%')
                        content = re.search(start + '(.*?)' + end, word)
                        if content is not None:
                            content = content.group(1)
                            to_replace = '%%=v(@' + content + ')=%%'
                            new_content = "{{" + content + "}}"
                            replaced_content = word.replace(to_replace, new_content)
                            new_line = new_line + " " + replaced_content
                    else:
                        new_line = new_line + " " + word
            outputFile.write(indentation + new_line)
            outputFile.write('\n')


def has_simple_if_condition(if_condition):
    return "if" in if_condition and \
           ("and" not in if_condition and "or" not in if_condition)


def has_simple_checks(if_condition):
    return "!= 'null'" in if_condition or "not empty" in if_condition or "== 'true'" in if_condition


def is_if_condition(line):
    start = re.escape(r'%%[')
    end = re.escape(']%%')
    if_condition = re.search(start + '(.*?)' + end, line)
    return if_condition is not None and "endif" not in if_condition


def get_if_condition_line(line):
    start = re.escape(r'%%[')
    end = re.escape(']%%')
    if_condition = re.search(start + '(.*?)' + end, line)
    return if_condition.group(1)
