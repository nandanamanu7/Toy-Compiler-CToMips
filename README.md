How to run this program:

Create a new project/directory in your IDE that supports python. I recommend Pycharm, since that is what I used, but VSCode also works. Simply create two files, C file with C code below for Fizzbuzz, and a python file in IDE that supports python (I used Pycharm). Create a src directory in your directory and put the C file in that directory. 

TLDR: replace filepaths of c_filepath and asm_filepath in main to your c and asm filepath

Now go ahead, and in the main function in my python source code, replace the file path variables with your respective file paths to your C file for the variable c_filepath, and where you want the asm file to open in for the variable asm_filepath (src directory is what I recommend) (also, alternatively, you can create an empty .asm file and take the filepath of that and put it as the asm_filepath).

Then, you can simply hit run to run the program, and the program should run as expected in your IDE. Check the .asm file post run to see the compiled fizzbuzz code from C to MIPS Assembly, which should run directly in Mars. 
