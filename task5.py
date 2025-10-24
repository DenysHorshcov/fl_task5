
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
    (?P<name>[A-Za-z0-9_'’\-]{{1,22}})             
    {DELIM}
    (?P<cost>[+\-]?(?:\d+(?:\.\d+)?|\.\d+))        
    {DELIM}
    (?P<price>0\.000)                              # 5) ЦІНА = рівно 0.000 (фільтр тут!)
    {DELIM}
    (?P<pos>[1-9]\d*)                              # 6) номер позиції (натуральне)
    \s*$
""", re.VERBOSE)

# Один крок перетворення: цілий рядок -> новий рядок з ; як роздільниками
REPLACEMENT = r"\g<invoice> ; \g<qty> ; \g<name> ; \g<cost> ; \g<price> ; \g<pos>"

def main():
    base_dir   = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, INPUT_FILE)
    output_path= os.path.join(base_dir, OUTPUT_FILE)

    if not os.path.exists(input_path):
        print(f"[ERROR] Файл '{INPUT_FILE}' не знайдено поруч зі скриптом.")
        return

    out_lines = []

    with open(input_path, "r", encoding="utf-8") as fin:
        for line in fin:
            # Відібрані лише ті, що МАТЧАТЬСЯ (і, відповідно, мають price = 0.000)
            if PATTERN.fullmatch(line):
                # Повне перетворення ВИКЛЮЧНО через regex (одним викликом)
                new_line = PATTERN.sub(REPLACEMENT, line)
                out_lines.append(new_line)

    # Записуємо кожен уже-збудований (цілісний) рядок
    with open(output_path, "w", encoding="utf-8") as fout:
        for ln in out_lines:
            fout.write(ln + ("\n" if not ln.endswith("\n") else ""))

    print(f"[INFO] Готово. Створено файл: {OUTPUT_FILE}")
    print(f"[INFO] Кількість рядків із ціною 0.000: {len(out_lines)}")

if __name__ == "__main__":
    main()
