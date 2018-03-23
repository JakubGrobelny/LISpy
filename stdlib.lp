; standard library of LISpy
; Jakub Grobelny
; 2018

(define PI 3.141592653589793)

(define mod modulo)

(define % modulo)

(define false False)

(define true True)

(define null None)

(define (null? x)
    (= x null))

(define (1+ x)
    (+ x 1))

(define (1- x)
    (+ x 1))

(define (cadr p)
    (car (cdr p)))

(define (cdar p)
    (cdr (car p)))

(define (caar p)
    (car (car p)))

(define (cddr p)
    (cdr (cdr p)))

(define (cddar p)
    (cdr (cdr (car p))))

(define (caddr p)
    (car (cdr (cdr p))))

(define (cdddar p)
    (cdr (cdr (cdr (car p)))))

(define (append xs ys)
    (if (null? xs)
        ys
        (cons
            (car xs)
            (append (cdr xs) ys))))

(define (map proc xs)
    (if (null? xs)
        null
        (cons 
            (proc (car xs)) 
            (map proc (cdr xs)))))

(define (not p)
    (if p
        false
        true))

(define (>= a b)
    (not (< a b)))

(define (< a b) 
    (and 
        (not (> a b)) 
        (not (= a b))))

(define (<= a b)
    (or (< a b)
        (= a b)))

(define (xor p1 p2)
    (and (or p1 p2)
         (not (and p1 p2))))

(define (range start end)
    (if (> start end)
        null
        (cons start (range (1+ start) end))))

(define (first ls)
    (car ls))

(define (second ls)
    (cadr ls))

(define (third ls)
    (caddr ls))

(define (length ls)
    (define (aux acc ls)
        (if (null? ls)
            acc
            (aux (1+ acc) (cdr ls))))
    (aux 0 ls))

(define (div a b)
    (/ (- a (mod a b)) b))