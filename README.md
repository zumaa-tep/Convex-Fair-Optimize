# สร้างโครงเลี้ยงเซลล์ด้วย Voronoi อย่างทนทานด้วย Fuzzy Centroid และ Adaptive Normal Flow (สรุปจาก m629)

## ภาพรวม
สรุปเวิร์กโฟลว์สำหรับสร้างโครงเลี้ยงเซลล์ที่ประกอบด้วยสองช่วงหลัก  
1) Lloyd algorithm
2) normal flow algorithm

จุดปรับปรุงสำคัญมีสองส่วน  
• เซนทรอยด์แบบฟัซซีที่คำนึงถึงรูปร่าง และเรียนค่าพารามิเตอร์ sigma สำหรับการอัปเดตในขั้นตอน Lloyd  
• ค่า delta ของ normal flow ที่ปรับตามสเกลและขอบขอรูปหลายเหลี่ยม

## องค์ประกอบเด่น
### 1) เซนทรอยด์แบบฟัซซีสำหรับ Lloyd
- แทนที่เซนทรอยด์ของรูปหลายเหลี่ยมด้วยเซนทรอยด์แบบถ่วงน้ำหนัก Gaussian ที่แยกคำนวณตามแกน มีความซับซ้อนเชิงเส้นตามจำนวนจุดยอด  
- ลดความสั่นของจุดศูนย์กลางในเซลล์ที่ถูกตัดขอบหรือมีความเบ้ โดยลดน้ำหนักจุดที่เป็น outlier  
- sigma ควบคุมการเน้นน้ำหนักใกล้ค่าเฉลี่ย และสามารถ “เรียน” ได้จากตัวบ่งชี้รูปร่างเชิงเรขาคณิตที่คำนึงถึงสเกล 10 ตัว เช่น เส้นรอบรูป สถิติมุม ความกลม ความไม่สมมาตรจาก PCA และเส้นทแยง พื้นที่ จำนวนด้าน เป็นต้น  
- หากยังไม่มีโมเดลเรียนรู้ สามารถกวาดค่าสำรวจช่วงแคบเพื่อหาค่าที่เหมาะสมได้

### 2) ก้าวเดินของ normal flow แบบปรับตามสเกล
- ก้าวเดินด้านในเป็นแบบตระหนักต่อความคลาดเคลื่อน และปรับสเกลตามขนาดปัญหา ช่วยให้อัตราส่วนผลต่างมีเสถียรภาพในช่วงค่าพิกัดที่กว้าง  
- ข้อจำกัดที่ขอบป้องกันการก้าวกระโดดข้ามปลายเส้น และรักษาระยะปลอดภัยต่อขอบที่ไม่ได้สัมผัสโดยตรง  
- ค่าที่แนะนำ คือ τ_edge = 0.25 และ τ_clear = 0.4

## ผลลัพธ์โดยสรุป
• ขั้นตอน Lloyd ประหยัดเวลาเด่นที่ 3 ถึง 6 พื้นที่ย่อย โดยไม่ถดถอยที่ 7 ถึง 10  
• ขั้นตอน normal flow ลดเวลาและจำนวนรอบได้มากในช่วงกว้าง โดยเด่นชัดเมื่อจำนวนพื้นที่ย่อยมากกว่าหก  
• ใช้กราฟสเกลลอการิทึมสำหรับแกนเวลาและจำนวนรอบ เพื่อให้อ่านค่าเปรียบเทียบข้ามขนาดได้ง่าย

## แนวทางใช้งานแบบย่อ
1) ในทุกการวนซ้ำของ Lloyd ให้ใช้เซนทรอยด์แบบฟัซซี โดยตั้งค่า sigma = κ × √พื้นที่เซลล์ และเรียนค่า κ จากเวกเตอร์คุณลักษณะ 10 ตัว  
2) ใน normal flow ตั้งก้าวเดินด้านในตามกฎที่ตระหนักต่อความคลาดเคลื่อน แล้วใช้ข้อจำกัดที่ขอบกับจุดที่อยู่บนขอบและจุดยอด เพื่อรักษารูปร่างและข้อกำหนดด้านความพรุน พร้อมทั้งลดจำนวนรอบและเวลา

## วิธีทำซ้ำการเรียนค่า sigma และการทดลอง
• ชุดปรับเทียบประกอบด้วยรูปหลายเหลี่ยมนูน 500 ตัวใน 2 มิติ สุ่มจุด 8 จุด สร้าง convex hull กวาดค่า sigma ตั้งแต่ 1 ถึง 250 และบันทึกตัวชี้วัดการลู่เข้าในขั้นตอน Lloyd  
• การสกัดคุณลักษณะใช้ตัวบ่งชี้ 10 ตัวที่คำนึงถึงสเกล พร้อมการเตรียมข้อมูล เช่น เรียงจุดทวนเข็มนาฬิกา จัดให้อยู่ที่เซนทรอยด์ของพื้นที่ จัดกรอบด้วย PCA และปรับสเกลพื้นที่ให้เป็นมาตรฐาน  
• นโยบายของ normal flow ใช้ก้าวเดินด้านในแบบตระหนักต่อความคลาดเคลื่อน และข้อจำกัดที่ขอบตามค่าที่แนะนำ  
• การรายงานผล ควรพล็อต  
  - เวลาและจำนวนรอบของ Lloyd เทียบกับจำนวนพื้นที่ย่อย โดยใช้แกน y แบบลอการิทึม  
  - เวลา ประสิทธิภาพ และสัดส่วนการลดเวลาเทียบวิธีฐานของ normal flow โดยใช้สเกลลอการิทึมเมื่อเหมาะสม

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
