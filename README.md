# Convex-Fair
โปรเจกต์เกี่ยวกับการพัฒนาอัลกอริทึมที่ใช้ในการแบ่งพื้นที่ และเส้นรอบรูปให้เท่ากัน โดยมีต้นแบบมาจากงาน An algorithmic approach to convex fair partitions of convex polygons 
โดยภายในงานจะทำการปรับอัลกอริทึมทั้งหมด 3 ส่วน

1.การทำงานของอัลกอริทึม Normal Flow พัฒนาการทำงานของอัลกอริทึม Normal Flow โดยการปรับค่า เดลต้า ภายในอัลกอริทึม กับปรับเปลี่ยนวิธีการหาอนุพันธ์ และการปรับวิธีการปรับค่า Factor ให้ลู่สู่คำตอบของสมการเร็วขึ้นเพื่อลดจำนวนรอบ โดยใช้หลักการ Exponential Search และ Binary Search ซึ่งจะปรับทุก ๆ รอบ iteration 

2.พัฒนาวิธีการหาเซนทรอยด์ในลอยด์อัลกอริทึม เพื่อให้ได้ค่าเซนทรอยด์ที่เหมาะสมสำหรับอัลกอริทึมที่ใช้แบ่งพื้นที่ให้เท่ากัน ซึ่งวิธีการที่ใช้จะแบ่งออกเป็น 2 ส่วน

  1 คือการใช้ฟัซซี่ลอจิก (Fuzzy Logic) ในการหาเซนทรอยด์ของรูปหลายเหลี่ยม ซึ่งใช้วิธีการสร้างกฎที่ครอบคลุม และการเลือกใช้ฟังก์ชันความเป็นสมาชิกที่เหมาะสมสำหรับทั้ง 3 ขั้นตอนในฟัซซี่ลอจิก 
  
  2 คือการใช้ฟังก์ชันความเป็นสมาชิกแบบเกาส์เซียนในการหาเซนทรอยด์ของรูปหลายเหลี่ยม โดยจะใช้ค่าความเป็นสมาชิกแบบเกาส์เซียนร่วมกับการหาค่าเฉลี่ยแบบถ่วงน้ำหนัก และการเลือกใช้ค่าที่เหมาะสมสำหรับรูปหลายเหลี่ยมนั้น ๆ โดย     การหาความสัมพันธ์ของรูปหลายเหลี่ยม กับค่า ซิกม่า ที่สามารถทำให้ค่า ซิกม่า ส่งผลให้อัลกอริทึมสามารถทำงานได้เร็วขึ้น 
งานนี้ยังอยู่ในขั้นตอนการทำงานอยู่

ENG ver.
This project focuses on developing an algorithm for partitioning both area and perimeter equally—building on the paper An Algorithmic Approach to Convex Fair Partitions of Convex Polygons. It comprises three main enhancements:

Normal Flow improvements
We refine the core Normal Flow routine by

tuning its internal Δ parameter,

replacing the finite-difference scheme with a more accurate derivative approximation, and

accelerating convergence of the “factor” update via Exponential Search and Binary Search at every iteration
in order to reduce the total number of iterations.

Enhanced centroid computation in Lloyd’s algorithm
To obtain centroids that are better suited to equal-area (and equal-perimeter) partitions, we explore two complementary approaches:
2.1 Fuzzy-Logic–based centroids
  – Define a comprehensive rule base and select appropriate membership functions for all three fuzzy-logic stages (fuzzification, inference, defuzzification) to pinpoint each polygon’s centroid.
2.2 Gaussian membership–based centroids
  – Use a Gaussian membership function together with weighted averaging to choose a centroid that best fits each shape. We also model the relationship between a polygon’s geometry and the membership standard deviation σ, so that tuning σ further speeds up convergence.

This work is currently ongoing.
