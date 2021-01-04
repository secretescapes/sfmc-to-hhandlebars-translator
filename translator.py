import re


class Translator:

    sfmc_expression_start_regex = re.escape(r'%%[')
    sfmc_expression_end_regex = re.escape(']%%')

    sfmc_variable_start_regex = re.escape(r'%%=v(@')
    sfmc_variable_end_regex = re.escape(')=%%')

    def contains_sfmc_line(self, line):
        return "%%=" in line or "%%[" in line

    def translate_if_condition(self, line):
        if_condition = self.__get_if_condition_line(line)
        if self.__has_simple_if_condition(if_condition):  # does not have any 'and' or 'or' operators
            if self.__has_simple_checks(if_condition):  # contains only '!- null' or 'not empty' or 'true'
                variable = re.search(r'@\w+', if_condition).group().replace("@", "")
                new_line = "{{#if " + variable + "}}"
                return new_line, True
            else:
                return line, False
        elif "endif" in line:
            new_line = "{{/if}}"
            return new_line, True
        else:
            return line, False

    def translate_variables(self, word):
        content = self.__extract_sfmc_variable(word)
        if content is not None:
            content = content.group(1)
            to_replace = '%%=v(@' + content + ')=%%'
            new_content = "{{" + content + "}}"
            translated_variable = word.replace(to_replace, new_content)
            return translated_variable, True
        return word, False

    def __extract_sfmc_variable(self, word):
        start = self.sfmc_variable_start_regex
        end = self.sfmc_variable_end_regex
        return re.search(start + '(.*?)' + end, word)

    def __get_if_condition_line(self, line):
        start = self.sfmc_expression_start_regex
        end = self.sfmc_expression_end_regex
        if_condition = re.search(start + '(.*?)' + end, line)
        return if_condition.group(1)

    def __has_simple_if_condition(self, if_condition):
        return "if" in if_condition and \
               ("and" not in if_condition and "or" not in if_condition and "endif" not in if_condition)


    def __has_simple_checks(self, if_condition):
        return "!= 'null'" in if_condition or "not empty" in if_condition or "== 'true'" in if_condition
