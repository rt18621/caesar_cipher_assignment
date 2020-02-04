# Assignment 1 - Caesar Cipher with Command Line Input

This is an individual python assignment revisiting the caesar cipher from semester 1 and adapt it to use command line input (CLI). A model solution for the caesar cipher using interactive user input will be available on a github repository.

## Tasks

Your tasks are:

1. Register for the assignment in github classroom and clone the assignment1 repository to have a local copy.

2. Adapt the code so that the cipher now preserves case, e.g. Hello World! -> Mjqqt Btwqi! when encrypted with a shift of 5

3. Change the code so that instead of interactive user input, the code now takes commmand line input (CLI). Your program will be called "caesar_cipher.py" and the CLI should work as follows:

```
$ ./caesar_cipher.py
usage: 
./caesar_cipher.py (e|d) <shift> <text>

Examples:
./caesar_cipher.py e <shift> <text>
./caesar_cipher.py d <shift> <text>
$ ./caesar_cipher.py e 5 Hello World!
Mjqqt Btwqi!
$ ./caesar_cipher.py d 5 Mjqqt Btwqi!
Hello World!
```

In the case that the program is called with too few arguments, the output messages should be considerd as *error* messages. The usage message given above should be printed to the the standard error stream (`stderr`). To do this you write:

```python
print("This is an error message\n", file=sys.stderr)
```

4. Tests are included and can be run by calling `python -m pytest` in the same directory as the "caesar_cipher.py" file. Make sure to run these tests regularly to identify any problems with the code that need fixing.

N.B. The outcome of these tests will be used to mark the assignments. You *must* use the tests or you will end up not following the intructions correctly and your submission will be incorrect in some way. If you have trouble using the tests then ask for help - do *not* simply ignore the tests! 

### Extension

An extension to the assignment is to add file read and write capabilities to the caesar cipher code.

1. Complete the `ret_file_msg` function so that it returns the contents of a file as a string if the file exists, otherwise it returns a `FileNotFoundError`.

2. Complete the `write_msg_to_file` function so that it writes the `msg` string to the specified file.

3. Add these capabilities to the CLI so that it now works:
```
$ ./caesar_cipher.py
usage: 
./caesar_cipher.py (e|d) <shift> (<text>|--file <infile>) [--write <outfile>]

Examples:
./caesar_cipher.py e <shift> <text>
./caesar_cipher.py d <shift> <text>
./caesar_cipher.py d <shift> --file <filename>
./caesar_cipher.py d <shift> --file <filename>
$ ./caesar_cipher.py e 5 Hello World!
Mjqqt Btwqi!
$ ./caesar_cipher.py d 5 Mjqqt Btwqi!
Hello World!
$ ./caesar_cipher.py d 5 Mjqqt Btwqi! --write output1.txt
$ ./caesar_cipher.py e 5 --file input_msg.txt
Mjqqt Btwqi!
$ ./caesar_cipher.py e 5 --file input_msg.txt --write output2.txt
```

## Spec

The only things which should be alterred in the assignment repository are of "caesar_cipher.py" and "README.md". Do not change the test files! 

To ensure the tests will work, make sure:

- Your code file is called "caesar_cipher.py".
- The following functions exist, with unalterred names or argument positions:
    - `caesar_encrypt(shift_value, msg)`
    - `caesar_decrypt(shift_value, msg)`
    - `ret_file_msg(file_name)`
    - `write_msg_to_file(file_name, msg)`

All the above can be checked by running the tests. The tests will fail if the above conditions are not followed.

The README.md file is what someone should read when first taking a look at
your code. It should be a mark down file formatted similarly to this one. It should
contain the following:

- Author and date that the code was created.
- A short description of what the code does
- How to use the code and examples of output

## Submission

The submission deadline is **1200 on Tuesday 18th February**.

To submit your code you need to make sure your final version is pushed back to the github classroom repository by the deadline. 