; comment test
(define x 10)

; comment test
x
; comment test
; comment test


(define pred (> x 3))

; comment test
(define else true)

(cond
	((= x 13) 1)
    ; comment test
	(pred 	  2)
	(else     3))
