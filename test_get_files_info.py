from functions.get_files_info import get_files_info

result = get_files_info("calculator", ".")
indented_result = result.replace("\n", "\n  ")
print(f"Result for current directory:\n  {indented_result}")

result = get_files_info("calculator", "pkg")
indented_result = result.replace("\n", "\n  ")
print(f"Result for current directory:\n  {indented_result}")

result = get_files_info("calculator", "/bin")
indented_result = result.replace("\n", "\n  ")
print(f"Result for current directory:\n  {indented_result}")

result = get_files_info("calculator", "../")
indented_result = result.replace("\n", "\n  ")
print(f"Result for current directory:\n  {indented_result}")