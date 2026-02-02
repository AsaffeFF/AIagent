from functions.write_file import write_file

def tests():
    test_list = [
        ['lorem.txt','wait, this isn\'t lorem ipsum'],
        ['pkg/morelorem.txt', 'lorem ipsum dolor sit amet'],
        ['/tmp/temp.txt', 'this should not be allowed'],
        ]
    
    for test in test_list:
        print(write_file("calculator", test[0], test[1]))


if __name__ == "__main__":
    tests()