(def input (slurp "input/01.txt"))

(def masses (map #(Integer/valueOf %) (clojure.string/split input #"\n")))

(defn fuel-for [mass]
  (- (quot mass 3) 2))

(println "Part 1"
  (reduce + (map fuel-for masses)))

(defn total-fuel-for [mass]
  (reduce + (rest (take-while pos? (iterate fuel-for mass)))))

(println "Part 2"
  (reduce + (map total-fuel-for masses)))
