from pathlib import Path
import re

folder_path = Path("./data")
clean_output_file_path = folder_path / "clean_msale.txt"

md_files_path = sorted(folder_path.glob("*.txt"))


def clean_combine(md_files_path, output_file_path):
    # **How the Regex Works**
    # - **`^\d+$`**:
    #   - `^` means the start of the line.
    #   - `\d+` means one or more digits (0-9).
    #   - `$` means the end of the line.
    #   - This matches lines that are *only* numbers (like page numbers).
    # - **`|`**: This means **OR**.
    # - **`^[^\x00-\x7F]$`**:
    #   - `[^\x00-\x7F]` matches any character that is **not** part of the standard English alphabet or keyboard symbols (ASCII).
    #   - Since there are no quantifiers (like `+` or `*`), it looks for **exactly one** character.
    #   - This perfectly catches single 3-byte UTF-8 letters (like a single Korean syllable like `가` or `어`) sitting alone on a line.
    # 2. Create the Regex Pattern
    # ^\d+$             -> Matches a line with only numbers
    # ^[^\x00-\x7F]$   -> Matches a line with exactly one non-English/non-ASCII character
    cleanup_pattern = re.compile(r"^\d+$|^[^\x00-\x7F]$")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        for md_file_path in md_files_path[3:]:
            if md_file_path == output_file_path:
                continue

            with open(md_file_path, "r", encoding="utf-8") as md_file:
                for line in md_file:
                    line = line.strip()
                    if not line:
                        continue
                    if cleanup_pattern.match(line) or line == "":
                        continue

                    output_file.write(line + "\n")

    print(f"All {len(md_files_path)} files are written to {output_file_path}")


clean_combine(md_files_path, clean_output_file_path)
