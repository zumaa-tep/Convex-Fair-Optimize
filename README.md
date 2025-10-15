# Convex-Fair
โปรเจกต์เกี่ยวกับการพัฒนาอัลกอริทึมที่ใช้ในการแบ่งพื้นที่ และเส้นรอบรูปให้เท่ากัน โดยมีต้นแบบมาจากงาน An algorithmic approach to convex fair partitions of convex polygons 
โดยภายในงานจะทำการปรับอัลกอริทึมทั้งหมด 3 ส่วน

1.การทำงานของอัลกอริทึม Normal Flow พัฒนาการทำงานของอัลกอริทึม Normal Flow โดยการปรับค่า เดลต้า ภายในอัลกอริทึม กับปรับเปลี่ยนวิธีการหาอนุพันธ์ และการปรับวิธีการปรับค่า Factor ให้ลู่สู่คำตอบของสมการเร็วขึ้นเพื่อลดจำนวนรอบ โดยใช้หลักการ Exponential Search และ Binary Search ซึ่งจะปรับทุก ๆ รอบ iteration 

2.พัฒนาวิธีการหาเซนทรอยด์ในลอยด์อัลกอริทึม เพื่อให้ได้ค่าเซนทรอยด์ที่เหมาะสมสำหรับอัลกอริทึมที่ใช้แบ่งพื้นที่ให้เท่ากัน ซึ่งวิธีการที่ใช้จะแบ่งออกเป็น 2 ส่วน

  1 คือการใช้ฟัซซี่ลอจิก (Fuzzy Logic) ในการหาเซนทรอยด์ของรูปหลายเหลี่ยม ซึ่งใช้วิธีการสร้างกฎที่ครอบคลุม และการเลือกใช้ฟังก์ชันความเป็นสมาชิกที่เหมาะสมสำหรับทั้ง 3 ขั้นตอนในฟัซซี่ลอจิก 
  
  2 คือการใช้ฟังก์ชันความเป็นสมาชิกแบบเกาส์เซียนในการหาเซนทรอยด์ของรูปหลายเหลี่ยม โดยจะใช้ค่าความเป็นสมาชิกแบบเกาส์เซียนร่วมกับการหาค่าเฉลี่ยแบบถ่วงน้ำหนัก และการเลือกใช้ค่าที่เหมาะสมสำหรับรูปหลายเหลี่ยมนั้น ๆ โดย     การหาความสัมพันธ์ของรูปหลายเหลี่ยม กับค่า ซิกม่า ที่สามารถทำให้ค่า ซิกม่า ส่งผลให้อัลกอริทึมสามารถทำงานได้เร็วขึ้น 
งานนี้ยังอยู่ในขั้นตอนการทำงานอยู่

ENG ver.

# Robust Voronoi Based Scaffold Generation with Fuzzy Centroid and Adaptive Normal Flow

## Overview
This repository summarizes the m629 report on a robust scaffold generation pipeline that combines a Voronoi based Lloyd stage with a normal flow projection stage. The pipeline introduces two focused improvements: a morphology aware fuzzy centroid for Lloyd updates and an adaptive geometry respecting step size for normal flow. The control flow and checkpoints are shown in the report.

## Why it matters
Across moderate to large problem sizes, the adaptive normal flow reduces total time and total iterations. Typical time reductions are about 21 to 35 percent for 6 to 15 regions and about 31 to 37 percent for 30 to 100 regions. A small case exception appears at 5 regions where the baseline can be slightly faster, which aligns with the fact that very simple geometries rarely trigger the geometric caps.  
For the Lloyd stage, the learned sigma fuzzy centroid delivers large savings for 3 to 6 regions without regressions at 7 to 10.

## Key contributions
1) **Fuzzy centroid for Lloyd updates**  
   * Replace the polygon centroid with a coordinate separable Gaussian weighted centroid. The approach is linear in the number of vertices and stabilizes updates in boundary clipped or skewed cells by down weighting outliers. Sigma controls emphasis near the mean.  
   * Learn sigma from ten scale aware geometric descriptors which include perimeter, angle statistics, circularity, anisotropy from PCA and diagonals, area, and the number of sides. Use a narrow grid if a learned model is not available.

2) **Adaptive normal flow step size**  
   * Interior forward step is roundoff aware and scaled by problem size, which keeps difference quotients well posed across coordinate magnitudes.  
   * Edge cap prevents jump past endpoints and respects clearance to non incident edges. Recommended parameters are tau_edge equal to 0.25 and tau_clear equal to 0.4.

## Results at a glance
* Lloyd stage shows large savings for 3 to 6 regions with no regressions at 7 to 10.  
* Normal flow shows significant reductions in runtime and iterations over a wide range, especially beyond six regions.  
* Figures in the report include log scale plots for time and iterations to improve readability across sizes.

## Practical recipe
Use the following choices as drop in replacements. No solver refactors are required.  
1) In every Lloyd iteration, use the fuzzy centroid with sigma equal to kappa times the square root of the cell area. Learn kappa from the ten feature vector.  
2) In normal flow, set the interior forward step to the roundoff aware rule, then apply the edge cap for on edge samples and vertices. These choices cut iterations and runtime while preserving geometry and porosity constraints.

## How to reproduce the sigma learning and experiments
* Calibration set contains 500 convex polygons in two dimensions. Sample eight points at random, take the convex hull, sweep sigma from 1 to 250, and record convergence diagnostics for Lloyd.  
* Feature extraction uses ten deterministic, scale aware descriptors with pre processing steps which include counter clockwise ordering, centering at area centroid, PCA frame alignment, and area normalization.  
* Normal flow policies use the roundoff aware interior step and the geometry based edge cap with the recommended tau values.  
* Reporting includes Lloyd runtime and total iterations versus region count on log y axes, and normal flow runtime and efficiency with log scales. Include time reduction relative to the baseline.

## Figures referenced from the report
* Fig. 1 Overall pipeline with two checkpoints  
* Fig. 2 Gaussian membership based centroid  
* Fig. 4 to Fig. 5 Lloyd stage runtime and total iterations on log y  
* Fig. 6 to Fig. 9 Normal flow runtime, total iterations, time reduction in percent, and efficiency
