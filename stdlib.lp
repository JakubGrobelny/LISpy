; standard library of LISpy
; Jakub Grobelny
; 2018

;; Constants
(define PI 3.141592653589793)

;; Macros
(define mod modulo)
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

(define map (lambda (xs proc)
                    (if (null? xs)
                        null
                        (cons (proc (car xs)) (map (cdr xs) proc)))))