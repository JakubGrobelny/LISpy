(define x 10)

x

(define pred (> x 3))

(define else true)

(cond
	((= x 13) 1)
	(pred 	  2)
	(else     3))
