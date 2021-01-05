This script will translate SFMC templates into Handlebars templates.

It's work in progress and it just translates a subset of the SFMC keywords.

#### Translates:
* SFMC variables
* Single if conditions without "and" or "or" operators. (supports translating to `unless`)
* Specific SFMC reserved keywords like "RedirectTo"  

#### Does not Translate:
* If conditions with "and" or "or" operators or "== to Strings" 
  * These ones aren't translated as usually we want to combine those in the backend to reduce the logic in the template.
    
#### Instructions
* The template to be translated has to be pasted into `intput.txt`. 
* The script runs with `python3 main.py`
* The translated template will be written to `output.txt`
* `translated_values.txt` will contain a list of `original >>>> translated` values for reference.
* `not_translated.txt` will contain a list of values that couldn't be translated.
