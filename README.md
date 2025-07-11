# Convex-Fair
โปรเจกต์เกี่ยวกับการพัฒนาอัลกอริทึมที่ใช้ในการแบ่งพื้นที่ และเส้นรอบรูปให้เท่ากัน โดยมีต้นแบบมาจากงาน An algorithmic approach to convex fair partitions of convex polygons 
โดยภายในงานจะทำการปรับอัลกอริทึมทั้งหมด 3 ส่วน
1.การทำงานของอัลกอริทึม Normal Flow พัฒนาการทำงานของอัลกอริทึม Normal Flow โดยการปรับค่า เดลต้า ภายในอัลกอริทึม กับปรับเปลี่ยนวิธีการหาอนุพันธ์ และการปรับวิธีการปรับค่า Factor ให้ลู่สู่คำตอบของสมการเร็วขึ้นเพื่อลดจำนวนรอบ โดยใช้หลักการ Exponential Search และ Binary Search ซึ่งจะปรับทุก ๆ รอบ iteration 
2.พัฒนาวิธีการหาเซนทรอยด์ในลอยด์อัลกอริทึม เพื่อให้ได้ค่าเซนทรอยด์ที่เหมาะสมสำหรับอัลกอริทึมที่ใช้แบ่งพื้นที่ให้เท่ากัน ซึ่งวิธีการที่ใช้จะแบ่งออกเป็น 2 lส่วน
  1 คือการใช้ฟัซซี่ลอจิก (Fuzzy Logic) ในการหาเซนทรอยด์ของรูปหลายเหลี่ยม ซึ่งใช้วิธีการสร้างกฎที่ครอบคลุม และการเลือกใช้ฟังก์ชันความเป็นสมาชิกที่เหมาะสมสำหรับทั้ง 3 ขั้นตอนในฟัซซี่ลอจิก 
  2 คือการใช้ฟังก์ชันความเป็นสมาชิกแบบเกาส์เซียนในการหาเซนทรอยด์ของรูปหลายเหลี่ยม โดยจะใช้ค่าความเป็นสมาชิกแบบเกาส์เซียนร่วมกับการหาค่าเฉลี่ยแบบถ่วงน้ำหนัก และการเลือกใช้ค่าที่เหมาะสมสำหรับรูปหลายเหลี่ยมนั้น ๆ โดย     การหาความสัมพันธ์ของรูปหลายเหลี่ยม กับค่า   ที่สามารถทำให้ค่า   ส่งผลให้อัลกอริทึมสามารถทำงานได้เร็วขึ้น 
งานนี้ยังอยู่ในขั้นตอนการทำงานอยู่

The project concerns the development of an algorithm for partitioning both area and perimeter equally, based on the paper An Algorithmic Approach to Convex Fair Partitions of Convex Polygons. It involves three main adaptations:

Normal Flow algorithm
We improve the Normal Flow routine by

tuning its internal ∆ (delta) parameter,

switching to a more accurate derivative approximation method, and

accelerating convergence of the “factor” update via Exponential Search and Binary Search at every iteration
so as to reduce the total number of iterations.

Centroid finding in Lloyd’s algorithm, part I (Fuzzy Logic)
We apply Fuzzy Logic to locate each polygon’s centroid by

defining a comprehensive rule base, and

choosing appropriate membership functions for all three stages of the fuzzy‐logic process (fuzzification, inference, defuzzification).

Centroid finding in Lloyd’s algorithm, part II (Gaussian membership)
We use a Gaussian membership function combined with weighted averaging to select a centroid that best fits each polygon. This also entails establishing the relationship between the polygon’s geometry and the parameter ___, which in turn allows ___—thus enabling the algorithm to run faster.

This work is currently in progress.
