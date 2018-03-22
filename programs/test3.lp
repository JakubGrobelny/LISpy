(define (func x)
    (define (aux y)
        (* y 2))
    (aux (+ 2 x)))

(define f (lambda (x)
    (define g (lambda (y)
        (+ y 2)))
    (+ 2 (g x))))

;(let ((x 10)
;      (f (lambda (z) (+ z 2))))
;    (f x))

(define x 3)

(let ((x 2))
    x)

((lambda (a b c)
    (+ a b c))
        1 2 3)

(let ((a 1)
      (b 2)
      (c 3))
    (+ a b c))

(define (letf x)
    (let ((y 3))
        x))

(let ((x 10))
    (let ((y x)
          (z (+ x 2)))
        (+ y z)))

(define (test a)
    (let ((x 10))
        (let ((y x)
              (z (+ x 2)))
            (+ y z a))))