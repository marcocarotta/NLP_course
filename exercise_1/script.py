





def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()

    if content1 == content2:
        print("The files are equal.")
    else:
        print("The files are not equal.")

def main():
    # Usage example
    file1 = 'in_example.exb'
    file2 = 'out_example.exb'
    compare_files(file1, file2)

if __name__ == "__main__":
    main()