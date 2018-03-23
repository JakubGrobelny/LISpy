# LISpy  
Something resembling LISP interpreter written in python  
  
To launch the program use "python3 lispy.py"  
  
It can run most of LISP stuff except the stuff it can't.  
  
It doesn't care whether the bracket is (, [ or { as long as bracket pairs match.  
  
Also it doesn't understand how strings work so don't bother.  
  
#Special forms:  
  
(define «name» «value») - binds the name to a value in current environment  
(if «condition» «if true» «if false») - evaluates one of the values based on the condition  
(cond («condition» «expression») ... (else «expression»)) - works like if but there can be multiple clauses (else is optional)  
(and «expression» ... «expression») - returns true if all expressions are true  
(or «expression» ... «expression») - returns true if any of the expressions is true  
(lambda («arguments») «expression») - creates a function that returns «expression» and takes «arguments»  
(λ («arguments») «expression») - same as above but with cool greek letter  
(let ((«name» «definition») ...) «expression») - locally binds variables to their definitions and returns a value  
(quote «expression») - returns the input as it is, without evaluation (quoted constants are themselves)  
  
#Constants:  
  
True (also 'true' in stdlib)  
False (also 'false' in stdlib)  
None (also 'null' in stdlib)  
all integers and floats (42 included)  
  
#Built-in procedures:  
  
+, -, *, /, =, >, modulo  
cons - creates new pair  
car - returns the first element form the pair  
cdr - returns the second element from the pair  
list - creates a list from given elements  
list?, pair?, number? - checks whether stuff is list/pair/number  
random - returns random integer from given range  
expt - a^b  
eval - basically this entire python program but inside the python program  
  
#Some extra procedures:  
  
!exit - self explanatory  
!reset-env - deletes everything from the global environment except basic built in procedures.  
!clear - prints 100 newlines to create an illusion of clearing the terminal  
!print-env - prints all the things that exist in current local environment  
  
  
When there is too much recursion it crashes because python is a dummy.  
