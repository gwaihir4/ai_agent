from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def test():
    # result = get_files_info("calculator", ".")
    # print("Result for current directory:")
    # print(result)
    # print("")

    # result = get_files_info("calculator", "pkg")  testing_dirs
    # print("Result for 'pkg' directory:")
    # print(result)

    # result = get_files_info("calculator", "/bin")
    # print("Result for '/bin' directory:")
    # print(result)

    # result = get_files_info("calculator", "../")
    # print("Result for '../' directory:")
    # print(result)

    # ----------file content tests----------
    # content_result = get_file_content("calculator", "lorem.txt")
    # print (content_result)
    # content_result = get_file_content("calculator", "main.py")
    # print (content_result)
    # content_result = get_file_content("calculator", "pkg/calculator.py")
    # print (content_result)
    # content_result = get_file_content("calculator", "/bin/cat")
    # print (content_result)
    # get_file_content("calculator", "pkg/does_not_exist.py")
    # content_result = get_file_content("calculator", "pkg/does_not_exist.py")
    # print (content_result)

    # write tests
    # content_result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # print (content_result)
    # content_result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # print (content_result)
    # content_result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    # print (content_result),
    
    content_result = run_python_file("calculator", "main.py")
    print (content_result)
    content_result = run_python_file("calculator", "main.py", ["3 + 5"])
    print (content_result)
    content_result = run_python_file("calculator", "tests.py")
    print (content_result)
    content_result = run_python_file("calculator", "../main.py") #(this should return an error)
    print (content_result)
    content_result = run_python_file("calculator", "nonexistent.py") #(this should return an error)
    print (content_result)

if __name__ == "__main__":
    test()