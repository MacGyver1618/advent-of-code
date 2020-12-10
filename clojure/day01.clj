(def input (slurp "input/01.txt"))

(def nums (map #(Integer/valueOf %) (clojure.string/split input #"\n")))

(println "Part 1"
  (->> (for [x nums y nums] (seq [x y]))
       (filter #(== 2020 (reduce + %)))
       (map (partial apply *))
       (first)))

(println "Part 2"
  (->> (for [x nums y nums z nums] (seq [x y z]))
       (filter #(== 2020 (reduce + %)))
       (map (partial apply *))
       (first)))
