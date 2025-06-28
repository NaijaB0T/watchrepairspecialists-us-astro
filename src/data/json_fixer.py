import json
import re
import argparse
import os

def repair_json(file_path: str, output_path: str, max_attempts: int = 10) -> bool:
    """
    Attempts to validate and repair a broken JSON file by fixing common syntax errors.

    Args:
        file_path (str): The path to the potentially broken JSON file.
        output_path (str): The path to save the repaired JSON file.
        max_attempts (int): The number of repair cycles to attempt before giving up.

    Returns:
        bool: True if the file was successfully repaired and saved, False otherwise.
    """
    print(f"Attempting to validate and repair: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

    for attempt in range(max_attempts):
        print(f"\n--- Repair Attempt #{attempt + 1} ---")
        try:
            # Try to parse the current content
            json.loads(content)
            print("\n✅ Success! JSON is valid.")
            # If successful, write the cleaned content to the output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned JSON saved to: {output_path}")
            return True
        except json.JSONDecodeError as e:
            print(f"JSON Error Found: {e.msg}")
            print(f"Location: Line {e.lineno}, Column {e.colno}")

            fixed = False
            
            # 1. First-pass, aggressive cleaning: comments, pythonic values, single quotes
            # This often fixes issues before we need to do line-by-line analysis.
            new_content = content
            
            # Strip // comments
            new_content = re.sub(r'//.*', '', new_content)
            # Strip /* */ comments
            new_content = re.sub(r'/\*.*?\*/', '', new_content, flags=re.DOTALL)
            
            # Replace Python/JS keywords with JSON equivalents
            new_content = re.sub(r'\bTrue\b', 'true', new_content)
            new_content = re.sub(r'\bFalse\b', 'false', new_content)
            new_content = re.sub(r'\bNone\b', 'null', new_content)
            
            # Cautiously replace single quotes with double quotes
            # This is complex. A simple replace can break strings containing single quotes.
            # We target single quotes that are likely delimiters.
            # This regex finds a single-quoted string that doesn't contain double quotes.
            new_content = re.sub(r"(?<!\\)'(.*?)(?<!\\)'", r'"\1"', new_content)

            if new_content != content:
                print("Applied general fixes: Stripped comments, fixed keywords/quotes.")
                content = new_content
                fixed = True
            
            # 2. Specific fixes based on error message and location
            if not fixed:
                lines = content.splitlines()
                error_line_index = e.lineno - 1
                error_col_index = e.colno - 1

                if "Trailing comma" in e.msg:
                    print("Attempting to fix: Trailing comma")
                    if error_line_index < len(lines):
                        line = lines[error_line_index]
                        # Find the comma before the closing bracket/brace
                        offending_comma_pos = line.rfind(',', 0, error_col_index)
                        if offending_comma_pos != -1:
                            lines[error_line_index] = line[:offending_comma_pos] + line[offending_comma_pos+1:]
                            content = "\n".join(lines)
                            fixed = True

                elif "Expecting ',' delimiter" in e.msg:
                    print("Attempting to fix: Missing comma")
                    # This often means the previous non-empty line is missing a comma
                    if error_line_index > 0:
                        # Find the last non-empty, non-bracket line before the error
                        for i in range(error_line_index - 1, -1, -1):
                            prev_line = lines[i].strip()
                            if prev_line and not prev_line.startswith(('{', '[', '}', ']')):
                                lines[i] = lines[i].rstrip() + ','
                                content = "\n".join(lines)
                                fixed = True
                                break

            if not fixed:
                print("\n❌ Failure! Could not automatically fix the JSON.")
                print("The error might be too complex. Please inspect the file manually near the reported line and column.")
                return False

    print("\n❌ Failure! Reached max repair attempts. Unable to fix the file.")
    return False

def main():
    parser = argparse.ArgumentParser(
        description="A tool to validate and automatically fix common issues in JSON files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("file_path", help="The path to the JSON file to fix.")
    parser.add_argument(
        "-o", "--output",
        help="The path for the repaired output file. Defaults to 'filename_fixed.json'.",
        default=None
    )
    args = parser.parse_args()

    input_path = args.file_path
    if args.output:
        output_path = args.output
    else:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_fixed{ext}"

    repair_json(input_path, output_path)

if __name__ == "__main__":
    main()