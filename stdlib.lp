; standard library of LISpy
; Jakub Grobelny
; 2018

;; Constants
(define PI 3.141592653589793)

;; Macros
(define mod modulo)
(define % modulo)
(define quit exit)

;; Procedures

(define null? (lambda (x)
                    (= x null)))

(define 1+ (lambda (x)
                    (+ x 1)))

(define 1- (lambda (x)
                    (+ x 1)))

(define cadr (lambda (p)
                    (car (cdr p))))

(define cdar (lambda (p)
                    (cdr (car p))))

(define caar (lambda (p)
                    (car (car p))))

(define cddr (lambda (p)
                    (cdr (cdr p))))

(define append (lambda (xs ys)
                    (if (null? xs)
                        ys
                        (cons (car xs) (append (cdr xs) ys)))))

(define map (lambda (proc xs)
                    (if (null? xs)
                        null
                        (cons (proc (car xs)) (map proc (cdr xs))))))

(define not (lambda (p)
		    (if p false true)))

(define >= (lambda (a b)
		    (if (< a b)
			false
			true)))

(define < (lambda (a b)
		(and (not (> a b))
		     (not (= a b)))))

(define <= (lambda (a b)
		    (or (< a b)
			(= a b))))

(define xor (lambda (p1 p2)
		    (and (or p1 p2)
			 (not (and p1 p2)))))

(define range (lambda (start end)
		    (if (> start end)
			null
			(cons start (range (1+ start) end)))))
