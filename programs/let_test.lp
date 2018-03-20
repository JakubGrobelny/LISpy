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