**Author Luka Absandze**  
# Scheme Interpreter  

## Functionality 
Support for load, define *(including recursion)*, if, cond, lambda and let expressions  
let expressions by default behave as let* expressions do in kawa  
quote defined lists *'(1 2 3)* are NOT recursive, meaning each expression inside the quoted list will be evaluated, the list as a whole will not be 
instead of *'((1 2) (3 4))* use *'('(1 2) '(3 4))*   
### Implemented Functions:
* \+ 
* \- 
* \*  
* / 
* and
* or 
* cdr
* car
* **Multi layered cdr and car _(eg. caaadr, cdadadr.)_ max of 10 layers, same as kawa 
* cons
* append
* map
* apply 
* eval 
* display 
* null? 
* length 
* = 
* < 
* <= 
* \> 
* \>= 
* equal? 
* zero? 
* remainder 
* quotient 
* newline 
* list 
* positive? 
* negative? 
* odd? 
* even? 
* expt 
* sqrt 
* reverse 
* else 

## Usage
You have 2 options to invoke the interpreter 
> python3 interpreter.py path/to/file/from/this/folder 

will interpret the given file, will only output to console if a display function is used  
> python3 interpreter.py  

launches the interpreter in the console, allowing the user to write code there, will output the result of every evaluated statement  
I've provided 4 test files, code for those files were taken from the freeuni paradigms 2021 repository  
* test.scm and test3.scm test general functionality 
* test2.scm tests the let expression 
* test4.scm tests lambda and load
