(define (reverseDup lst) 
    (let 
        ((reversed (reverse lst))
         (cum (append '("CUUUUUUUUUUM") reversed))
        )
        (append reversed reversed cum)
    )
)
(display (reverseDup '(1 2 3 4 5 6 12093121 123123123123)))