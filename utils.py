def format_file_size(size_in_bytes):
    units = ["bytes", "KB", "MB", "GB", "TB"]
    size = float(size_in_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.1f} {units[unit_index]}"


if __name__ == "__main__":
    print(format_file_size(500))
    print(format_file_size(24521))
    print(format_file_size(1048576))
    print(format_file_size(1073741824))