import re
import os

INPUT_FILE  = "data.txt"
OUTPUT_FILE = "resoult.txt"  

DELIM = r"""\s*[;:\?]\s*"""

PATTERN = re.compile(rf"""
    ^\s*
    (?P<invoice>[A-Za-z0-9]{{10}})                 
    {DELIM}
    (?P<qty>(?:0|[1-9]\d*)\.\d{{3}})               
    {DELIM}
    (?P<name>[A-Za-z0-9_''\-]{{1,22}})             
    {DELIM}
    (?P<cost>[+\-]?(?:\d+(?:\.\d+)?|\.\d+))        
    {DELIM}
    (?P<price>0\.000)                              
    {DELIM}
    (?P<pos>[1-9]\d*)                              
    \s*$
""", re.VERBOSE)

REPLACEMENT_PATTERN = r"\g<invoice> ; \g<qty> ; \g<name> ; \g<cost> ; \g<price> ; \g<pos>"

def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_directory, INPUT_FILE)
    output_file_path = os.path.join(script_directory, OUTPUT_FILE)

    if not os.path.exists(input_file_path):
        print(f"[ERROR] Файл '{INPUT_FILE}' не знайдено поруч зі скриптом.")
        print("Переконайся, що файл data.txt є в тій же папці!")
        return

    processed_lines = []

    try:
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            line_count = 0
            for current_line in input_file:
                line_count += 1  
                
                if PATTERN.fullmatch(current_line):
                    transformed_line = PATTERN.sub(REPLACEMENT_PATTERN, current_line)
                    processed_lines.append(transformed_line)
                    
    except Exception as error:
        print(f"[ERROR] Помилка при читанні файлу: {error}")
        return

    try:
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            for line_to_write in processed_lines:
                if line_to_write.endswith("\n"):
                    output_file.write(line_to_write)
                else:
                    output_file.write(line_to_write + "\n")
                    
    except Exception as error:
        print(f"[ERROR] Помилка при записі файлу: {error}")
        return

    print(f"[INFO] Готово. Створено файл: {OUTPUT_FILE}")
    print(f"[INFO] Кількість рядків із ціною 0.000: {len(processed_lines)}")
    
    if len(processed_lines) == 0:
        print("[WARNING] Не знайдено жодного рядка з ціною 0.000!")  

if __name__ == "__main__":
    main()