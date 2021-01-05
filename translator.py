import re


class Translator:

    sfmc_expression_start_regex = re.escape(r'%%[')
    sfmc_expression_end_regex = re.escape(']%%')

    sfmc_variable_start_regex = re.escape(r'%%=v(@')
    sfmc_variable_end_regex = re.escape(')=%%')

    sfmc_redirect_start_regex = re.escape(r'%%=RedirectTo(@')
    sfmc_redirect_end_regex = re.escape(')=%%')

    # stack to store if conditions and unless conditions
    # to know whether to translate to '{{/if}} or {{/unless}}
    if_condition_stack = []

    def contains_sfmc_line(self, line):
        return "%%=" in line or "%%[" in line

    def translate_if_condition(self, line):
        if_condition = self.__get_if_condition_line(line)
        if self.__has_simple_if_condition(if_condition):  # does not have any 'and' or 'or' operators
            if self.__has_unless_format(if_condition):
                variable = re.search(r'@\w+', if_condition).group().replace("@", "")
                new_line = "{{#unless " + variable + "}}"
                self.if_condition_stack.append("unless")
                return new_line, True
            elif self.__has_simple_checks(if_condition):  # contains only '!- null' or 'not empty' or 'true'
                variable = re.search(r'@\w+', if_condition).group().replace("@", "")
                new_line = "{{#if " + variable + "}}"
                self.if_condition_stack.append("if")
                return new_line, True
            else:
                self.if_condition_stack.append(line)
                return line, False

        # Sometimes some %%[endif]%% are in the same line as other text.
        # Checking if endif is not in the same line as the start of the if condition.
        # Reason why checking for "then" value.
        elif "endif" in line and "then" not in line:
            # This ''.join( line.split()) removes all spaces and checks that this is the only word in the line
            if ''.join(line.split()) == "%%[endif]%%" or ''.join(line.split()) == "<!--%%[endif]%%-->":
                last_if = self.if_condition_stack.pop()
                new_line = "{{/unless}}" if "unless" in last_if else "{{/if}}"
                return new_line, True
            else:
                self.if_condition_stack.pop()
                return line, False
        else:
            self.if_condition_stack.append(line)
            return line, False

    def translate_variables(self, word):
        content = self.__extract_sfmc_variable(word)
        if content is not None:
            content = content.group(1)
            to_replace = '%%=v(@' + content + ')=%%'
            new_content = "{{{" + content + "}}}"
            translated_variable = word.replace(to_replace, new_content)
            return translated_variable, True
        return word, False

    def translate_redirect(self, word):
        content = self.__extract_sfmc_redirect(word)
        if content is not None:
            content = content.group(1)
            to_replace = '%%=RedirectTo(@' + content + ')=%%'
            new_content = "{{" + content + "}}"
            translated_variable = word.replace(to_replace, new_content)
            return translated_variable, True
        return word, False

    def __extract_sfmc_variable(self, word):
        start = self.sfmc_variable_start_regex
        end = self.sfmc_variable_end_regex
        return re.search(start + '(.*?)' + end, word)

    def __extract_sfmc_redirect(self, word):
        start = self.sfmc_redirect_start_regex
        end = self.sfmc_redirect_end_regex
        return re.search(start + '(.*?)' + end, word)

    def __get_if_condition_line(self, line):
        start = self.sfmc_expression_start_regex
        end = self.sfmc_expression_end_regex
        if_condition = re.search(start + '(.*?)' + end, line)
        return if_condition.group(1)

    def __has_simple_if_condition(self, if_condition):
        if_condition = if_condition.split()
        return "if" in if_condition and \
               ("and" not in if_condition and "or" not in if_condition and "endif" not in if_condition)

    def __has_simple_checks(self, if_condition):
        return "!= 'null'" in if_condition or "not empty" in if_condition or "== 'true'" in if_condition or "!= ''" in if_condition

    def __has_unless_format(self, if_condition):
        return ("empty" in if_condition and "not empty" not in if_condition) or "== null" in if_condition or "== 'false'" in if_condition