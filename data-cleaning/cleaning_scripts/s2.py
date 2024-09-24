import sys
import pandas as pd
import os

CLEANED_FILES_DIR = "./cleaned_files"

def clean(input_filename):
    # Đọc file dữ liệu thô
    print('clean in s2.py')
    df = pd.read_csv(input_filename)

    # Thực hiện các bước làm sạch dữ liệu
    df_cleaned = df.dropna()          # Xóa các hàng có giá trị bị thiếu
    df_cleaned = df_cleaned.drop_duplicates()  # Xóa các hàng trùng lặp

    # Tạo đường dẫn để lưu file đã làm sạch
    cleaned_file_path = os.path.join(CLEANED_FILES_DIR, f"cleaned_{os.path.basename(input_filename)}")

    # Lưu DataFrame đã làm sạch vào CSV
    df_cleaned.to_csv(cleaned_file_path, index=False)
    return df_cleaned

# Lấy argument FILE_PATH từ command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_script1.py FILE_PATH")
    else:
        input_filename = sys.argv[1]
        clean(input_filename)
