(defn digits [n]
  (loop [remaining n
         digs '()]
    (if (zero? remaining)
        digs
        (recur (quot remaining 10)
               (cons (rem remaining 10) digs)))))

(defn monotonic? [n]
  (apply <= (digits n)))

(defn digit-sequences [n]
  (partition-by identity (digits n)))

(defn sequence-lengths [n]
  (map count (digit-sequences n)))

(def candidates (range 387638 919123))

(println "Part 1:"
  (->> candidates
       (filter monotonic?)
       (filter #(some (partial >= 2) (sequence-lengths %)))
       (count)))

(println "Part 2"
  (->> candidates
       (filter monotonic?)
       (filter #(some (partial = 2) (sequence-lengths %)))
       (count)))
