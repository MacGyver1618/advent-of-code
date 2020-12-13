(def input (slurp "input/03.txt"))

(def wires (map #(clojure.string/split % #",") (clojure.string/split input #"\n")))

(defn increment [direction point]
  (let [diff (case direction
                   :R [ 1  0]
                   :L [-1  0]
                   :U [ 0  1]
                   :D [ 0 -1])]
    (map + point diff)))

(defn instruction->points [point instruction]
  (let [direction (keyword (subs instruction 0 1))
        amount (Integer/valueOf (subs instruction 1))]
    (take amount (rest (iterate (partial increment direction) point)))))

(defn instructions->points [instructions]
  (loop [last-point [0 0]
         points [last-point]
         remaining instructions]
    (if (empty? remaining)
      points
      (let [next-points (instruction->points last-point (first remaining))]
        (recur (last next-points)
               (concat points next-points)
               (rest remaining))))))

(defn manhattan-distance [p1 p2]
  (apply + (map #(Math/abs %) (map - p1 p2))))

(def intersections
  (let [w1 (instructions->points (first wires))
        w2 (instructions->points (second wires))]
    (clojure.set/intersection (set w1) (set w2))))

(println "Part 1"
  (->> intersections
       (map #(manhattan-distance % [0 0]))
       (apply min)))

(defn distance-to [point wire]
  (count (take-while #(not (= point %)) wire)))

(defn total-distance-to [point]
  (+ (distance-to point (first wires))
     (distance-to point (second wires))))

(println "Part 2"
  (->> intersections
       (map total-distance-to)
       (apply min)))
