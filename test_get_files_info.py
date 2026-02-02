from functions.get_files_info import get_files_info

tests = ['.', 'pkg', '/bin', '../']


for test in tests:
    print(f"Result for '{test}' directory:")
    print(f"{"\t" + get_files_info("calculator", test).replace("\n","\n\t")}\n")
