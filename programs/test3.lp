(define (func x)
    (define (aux y)
        (* y 2))
    (aux (+ 2 x)))

(define f (lambda (x)
    (define g (lambda (y)
        (+ y 2)))
    (+ 2 (g x))))

(let ((x 10)
      (f (lambda (z) (+ z 2))))
    (f x))

