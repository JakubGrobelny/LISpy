; should be 42
(let ((a 20)
      (b 22))
    (+ a b))

; should fail
(let ((a 60)
      (b (* (/ a 20) 3)))
    (+ a b))

; should be 69
(let* ((a 60)
      (b (* (/ a 20) 3)))
    (+ a b))

; should be 420 (accidentaly)
(let* ((a (+ 1 b))
       (b 20))
    (* a b))