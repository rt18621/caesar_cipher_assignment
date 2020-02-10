import pytest
from caesar_cipher import caesar_encrypt, caesar_decrypt, ret_file_msg, write_msg_to_file
from subprocess import Popen, PIPE
import sys
import re

MODULE_NAME = "caesar_cipher"

"""
Fixtures and helper functions
"""

@pytest.fixture()
def file_eng(tmpdir):
    file = tmpdir.join("test_input_eng.txt")
    file.write("The Answer to the Great Question... Of Life, the Universe and Everything... Is... Forty-two,\nsaid Deep Thought, with infinite majesty and calm.")
    return file
    
@pytest.fixture()
def file_cipher_13(tmpdir):
    file = tmpdir.join("test_input_cipher_13.txt")
    file.write("Gur Nafjre gb gur Terng Dhrfgvba... Bs Yvsr, gur Havirefr naq Rirelguvat... Vf... Sbegl-gjb,\nfnvq Qrrc Gubhtug, jvgu vasvavgr znwrfgl naq pnyz.")
    return file
    
@pytest.fixture()
def file_output(tmpdir):
    file = tmpdir.join("output.txt")
    return file


def run_program(args):
    try:
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
    except OSError:
        args[0] = args[0].strip("./")
        proc = Popen([sys.executable] + args, stdout=PIPE, stderr=PIPE)
    
    stdout, stderr = proc.communicate()
    return normalize_newlines(stdout.decode('utf8')), normalize_newlines(stderr.decode('utf8')), proc.returncode

def normalize_newlines(string):
    return re.sub(r'(\r\n|\r|\n)', '\n', string)
"""
Tests to check cipher functions work
"""
    
@pytest.mark.parametrize("english_text, shift, cipher_text", [
    ["HELLO WORLD!", 0, "HELLO WORLD!"],
    ["HELLO WORLD!", 5, "MJQQT BTWQI!"],
    ["THE QUICK ONYX GOBLIN JUMPS OVER THE LAZY DWARF", 8, "BPM YCQKS WVGF OWJTQV RCUXA WDMZ BPM TIHG LEIZN"],
    ["THE QUICK ONYX GOBLIN JUMPS OVER THE LAZY DWARF", 30, "XLI UYMGO SRCB KSFPMR NYQTW SZIV XLI PEDC HAEVJ"]
])
def test_cipher_encrypt(english_text, shift, cipher_text):
    assert caesar_encrypt(shift, english_text) == cipher_text

    
@pytest.mark.parametrize("english_text, shift, cipher_text", [
    ["HELLO WORLD!", 0, "HELLO WORLD!"],
    ["HELLO WORLD!", 5, "MJQQT BTWQI!"],
    ["THE QUICK ONYX GOBLIN JUMPS OVER THE LAZY DWARF", 8, "BPM YCQKS WVGF OWJTQV RCUXA WDMZ BPM TIHG LEIZN"],
    ["THE QUICK ONYX GOBLIN JUMPS OVER THE LAZY DWARF", 30, "XLI UYMGO SRCB KSFPMR NYQTW SZIV XLI PEDC HAEVJ"]
])
def test_cipher_derypt(english_text, shift, cipher_text):
    assert caesar_decrypt(shift, cipher_text) == english_text
    

"""
Tests to check that case preservation has been implemented
"""
    
def test_case_preservation_encrypt():
    english_text = "The Quick Onyx Goblin Jumps Over The Lazy Dwarf"
    cipher_text = "Ymj Vznhp Tsdc Ltgqns Ozrux Tajw Ymj Qfed Ibfwk"
    assert caesar_encrypt(5, english_text) == cipher_text
    
    
def test_case_preservation_decrypt():
    english_text = "The Quick Onyx Goblin Jumps Over The Lazy Dwarf"
    cipher_text = "Ymj Vznhp Tsdc Ltgqns Ozrux Tajw Ymj Qfed Ibfwk"
    assert caesar_decrypt(5, cipher_text) == english_text

    
"""
Tests for command line usage
"""
    
def test_cli_when_args_missing():
    exp_output_nofile = """usage: 
./caesar_cipher.py (e|d) <shift> <text>

Examples:
./caesar_cipher.py e <shift> <text>
./caesar_cipher.py d <shift> <text>
"""
    exp_output_file = """usage: 
./caesar_cipher.py (e|d) <shift> (<text>|--file <infile>) [--write <outfile>]

Examples:
./caesar_cipher.py e <shift> <text>
./caesar_cipher.py d <shift> <text>
./caesar_cipher.py d <shift> --file <filename>
./caesar_cipher.py d <shift> --file <filename>
"""
    stdout, stderr, returncode = run_program(["./" + MODULE_NAME + ".py"])
    assert returncode != 0
    assert stderr.startswith(exp_output_nofile) or stderr.startswith(exp_output_file)
    
    
@pytest.mark.parametrize("invalid_mode", [
    "ff",
    "5",
    "encrypt"
])
def test_cli_invalid_mode_fail(invalid_mode):
    stdout, stderr, returncode = run_program(["./" + MODULE_NAME + ".py", invalid_mode, "3", "hello"])
    assert stderr is not None
    assert returncode != 0

    
@pytest.mark.parametrize("invalid_shift", [
    "ff",
    "5.7"
])
def test_cli_invalid_shift_fail(invalid_shift):
    stdout, stderr, returncode = run_program(["./" + MODULE_NAME + ".py",  "e", invalid_shift, "hello"])
    assert stderr is not None
    assert returncode != 0
    

@pytest.mark.parametrize("mode, shift, text, exp_output", [
    ["e", "0", ["HELLO"], "HELLO"],
    ["e", "5", ["THE QUICK ONYX GOBLIN JUMPS OVER THE LAZY DWARF"], "YMJ VZNHP TSDC LTGQNS OZRUX TAJW YMJ QFED IBFWK"],
    ["e", "5", ["THE", "QUICK", "ONYX", "GOBLIN", "JUMPS", "OVER", "THE", "LAZY", "DWARF"], "YMJ VZNHP TSDC LTGQNS OZRUX TAJW YMJ QFED IBFWK"],
    ["d", "5",["YMJ VZNHP TSDC LTGQNS OZRUX TAJW YMJ QFED IBFWK"], "THE QUICK ONYX GOBLIN JUMPS OVER THE LAZY DWARF"],
    ["e", "36", ["HELLO"], "ROVVY"]
])
def test_cli_with_text_success(mode, shift, text, exp_output):
    stdout, stderr, returncode = run_program(["./" + MODULE_NAME + ".py", mode, shift] + text)
    assert not stderr
    assert stdout == exp_output + "\n"

    
"""
Tests for file reading
"""
def test_file_read_success(file_eng):
    exp_output = "The Answer to the Great Question... Of Life, the Universe and Everything... Is... Forty-two,\nsaid Deep Thought, with infinite majesty and calm."
    assert ret_file_msg(file_eng.strpath) == exp_output
    
    
def test_file_name_error():
    with pytest.raises(FileNotFoundError):
        ret_file_msg("invalid_file_name")

        
def test_cli_with_file_encrypt(file_eng):
    exp_output = ("Gur Nafjre gb gur Terng Dhrfgvba... Bs Yvsr, gur Havirefr naq Rirelguvat... Vf... Sbegl-gjb,\nfnvq Qrrc Gubhtug, jvgu vasvavgr znwrfgl naq pnyz.\n")
    stdout, stderr, returncode = run_program(["./" + MODULE_NAME + ".py", "e", "13", "--file",
                                              file_eng.strpath])
    assert not stderr
    assert stdout == exp_output
    
    
def test_cli_with_file_decrypt(file_cipher_13):
    exp_output = ("The Answer to the Great Question... Of Life, the Universe and Everything... Is... Forty-two,\nsaid Deep Thought, with infinite majesty and calm.\n")
    stdout, stderr, returncode = run_program(["./" + MODULE_NAME + ".py", "d", "13", "--file",
                                              file_cipher_13.strpath])
    assert not stderr
    assert stdout == exp_output
    
    
"""
Tests for file writing
"""
def test_cli_with_text_and_write_encrypt(file_output):
    stdout, stderr, returncode = run_program(["./" + MODULE_NAME + ".py", "e", "5",
                                              "HELLO", "WORLD!", "--write", file_output.strpath])
    assert not stderr
    assert not stdout
    assert file_output.read() == "MJQQT BTWQI!"
    
    
def test_cli_with_text_and_write_decrypt(file_output):
    stdout, stderr, returncode = run_program(["./" + MODULE_NAME + ".py", "d", "5",
                                              "MJQQT", "BTWQI!", "--write", file_output.strpath])
    assert not stderr
    assert not stdout
    assert file_output.read() == "HELLO WORLD!"        
    

def test_cli_with_file_and_write_encrypt(file_eng, file_cipher_13, file_output):
    stdout, stderr, returncode = run_program(["./" + MODULE_NAME + ".py", "e", "13", "--file",
                                              file_eng.strpath, "--write", file_output.strpath])
    assert not stderr
    assert not stdout
    assert file_output.read() == file_cipher_13.read()
    
    
def test_cli_with_file_and_write_decrypt(file_eng, file_cipher_13, file_output):
    stdout, stderr, returncode = run_program(["./" + MODULE_NAME + ".py", "d", "13", "--file",
                                              file_cipher_13.strpath, "--write", file_output.strpath])
    assert not stderr
    assert not stdout
    assert file_output.read() == file_eng.read()
    

