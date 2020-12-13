(def input (clojure.string/trim (slurp "input/08.txt")))

(def layers
  (->> input
       (partition 150 150)
       (map (partial apply str))))

(defn digits [layer]
  (vec (for [x (range 3)]
         (count (re-seq (re-pattern (str x)) layer)))))

(println "Part 1"
  (->> layers
       (map digits)
       (sort)
       (first)
       (#(* (nth % 1) (nth % 2)))))

(defn overlay [a b]
  (map #(if (= \2 %1) %2 %1) a b))

(defn output [ch]
  (if (= \1 ch) \* \space))

(println "Part 2")
(->> layers
     (reduce overlay)
     (map output)
     (partition 25 25)
     (run! println))
