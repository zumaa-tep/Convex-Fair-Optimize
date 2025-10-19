import numpy as np
import time
import pandas as pd
from scipy.spatial import ConvexHull
from matplotlib.path import Path
from numpy.ma.core import sqrt
import os

class Delta_Equipartition_adap:
    def __init__(self,polygon,number_of_regions):
        self.poligon = polygon
        self.number_of_regions = number_of_regions

    def punto_mas_cercano(puntos_iniciales, punto):
        c=0
        dist=(puntos_iniciales[0][0]-punto[0])**2+(puntos_iniciales[0][1]-punto[1])**2
        for i in range(0,np.shape(puntos_iniciales)[0],1):
            if (puntos_iniciales[i][0]-punto[0])**2+(puntos_iniciales[i][1]-punto[1])**2< dist:
                c=i
                dist = (puntos_iniciales[i][0]-punto[0])**2+(puntos_iniciales[i][1]-punto[1])**2
        return(c)

    def puntos_mas_cercanos(puntos_iniciales, punto):
        c=0
        v=[]
        dist=(puntos_iniciales[0][0]-punto[0])**2+(puntos_iniciales[0][1]-punto[1])**2
        for i in range(0,np.shape(puntos_iniciales)[0],1):
            if (puntos_iniciales[i][0]-punto[0])**2+(puntos_iniciales[i][1]-punto[1])**2< dist:
                c=i
                dist = (puntos_iniciales[i][0]-punto[0])**2+(puntos_iniciales[i][1]-punto[1])**2
        v.append(c)
        for i in range(c+1,np.shape(puntos_iniciales)[0],1):
            if (puntos_iniciales[i][0]-punto[0])**2+(puntos_iniciales[i][1]-punto[1])**2 == dist:
                v.append(i)
        return(v)

    def puntos_en_region_n(puntos_iniciales, points,j):
        v=[]
        for i in range(0,np.shape(points)[0]):
            if j in Delta_Equipartition_adap.puntos_mas_cercanos(puntos_iniciales, points[i]):
                v.append(i)
        return(v)

    def segment_segment_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
        d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
        if d:
            uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
            uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
        else:
            return
        if not(0 <= uA <= 1 and 0 <= uB <= 1 ): # เหมือนตัว segment_line_intersect ตัวล่างต่างแค่บรรทัดนี้
            return
        x = Ax1 + uA * (Ax2 - Ax1)
        y = Ay1 + uA * (Ay2 - Ay1)

        return x, y

    def segment_line_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
        d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
        if d:
            uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
            uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
        else:
            return
        if not(0 <= uA <= 1 and 0 <= uB  ):
            return
        x = Ax1 + uA * (Ax2 - Ax1)
        y = Ay1 + uA * (Ay2 - Ay1)

        return x, y



    def weighted_ridge(pt1,pt2):
        a=((sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2))**2)/(2*(sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2)))
        uni=sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2)
        ridge=np.array([pt1[0]+a*((pt2[0]-pt1[0])/uni),pt1[1]+a*((pt2[1]-pt1[1])/uni)])
        dir = pt1-pt2
        dir_perp=np.array([dir[1],-dir[0]])
        vertice=ridge+dir_perp
        return np.array([ridge,vertice])



    def vect_intersect(line1,line2):
        d = (line2[1][1] - line2[0][1]) * (line1[1][0] - line1[0][0]) - (line2[1][0] - line2[0][0]) * (line1[1][1] - line1[0][1])
        if d:
            uA = ((line2[1][0] - line2[0][0]) * (line1[0][1] - line2[0][1]) - (line2[1][1] - line2[0][1]) * (line1[0][0] - line2[0][0])) / d
            uB = ((line1[1][0] - line1[0][0]) * (line1[0][1] - line2[0][1]) - (line1[1][1] - line1[0][1]) * (line1[0][0] - line2[0][0])) / d
            x = line1[0][0] + uA * (line1[1][0] - line1[0][0])
            y = line1[0][1] + uA * (line1[1][1] - line1[0][1])
            return np.array([x, y])
        else:
            return



    def triple_intersect(pt1,pt2,pt3):
        return Delta_Equipartition_adap.vect_intersect(Delta_Equipartition_adap.weighted_ridge(pt1,pt2),Delta_Equipartition_adap.weighted_ridge(pt2,pt3))



    def area(R):
        respuesta=0
        region = np.append(R, np.array([R[0]]),  axis=0)
        for i in range(np.shape(R)[0]):
            respuesta = respuesta + (region[i][0]*region[i+1][1]-region[i+1][0]*region[i][1])/2
        return respuesta



    def centroide(R):
        centrox=0
        centroy=0
        region = np.append(R, np.array([R[0]]),  axis=0)
        for i in range(np.shape(R)[0]):
            centrox = centrox + (region[i][0]+region[i+1][0])*(region[i][0]*region[i+1][1]-region[i+1][0]*region[i][1])
            centroy = centroy + (region[i][1]+region[i+1][1])*(region[i][0]*region[i+1][1]-region[i+1][0]*region[i][1])
        areatotal=Delta_Equipartition_adap.area(R)
        centrox = centrox/(6*areatotal)
        centroy = centroy/(6*areatotal)
        return np.array([[centrox,centroy]])



    def internal_vertices(poligono,sitios):
        poligon = ConvexHull(poligono)
        poligon_path = Path( poligon.points[poligon.vertices] )
        lista=[]
        length_sitios=len(sitios)
        for i in range (0,length_sitios-2,1):
            for j in range (i+1,length_sitios-1,1):
                for k in range (j+1,length_sitios,1):
                    interseccion= Delta_Equipartition_adap.triple_intersect(sitios[i],sitios[j],sitios[k])
                    if poligon_path.contains_point(interseccion) == True:
                        if length_sitios==3:
                            lista.append([i,j,k,interseccion])
                        else:
                            new_sitios=np.delete(sitios,[i,j,k],0)
                            w=True
                            value = np.linalg.norm(interseccion-sitios[i])
                            for q in range(len(new_sitios)):
                                w=w*(value <np.linalg.norm(interseccion-new_sitios[q]))
                            if w==True:
                                lista.append([i,j,k,interseccion])

        df = pd.DataFrame(lista, columns=['l','m','n','inter'])
        if len(lista)==0 :
            vertices = np.empty([0,2])
        else :
            vertices = np.vstack(df['inter'])
        regiones = [ [] for i in range(len(sitios))]
        ridge_vertices=[]
        ridge_points=np.empty([0,2], dtype=np.int32)
        for i in range(0,len(sitios),1):
            regiones[i] = df[(df['l']==i)|(df['m']==i)|(df['n']==i)].index.to_list()
        return vertices, regiones


    def external_vertices(poligono, sitios):
        number_of_regions = np.shape(sitios)[0]
        regiones=[]
        for i in range(0,number_of_regions,1):
            regiones.append(Delta_Equipartition_adap.puntos_en_region_n(sitios,poligono,i))
        return poligono, regiones



    def particion_vertices(external, intermediate, internal):
        regiones=[]
        areas=[]
        perimetros=[]
        convex=[]
        todos_convexos=True
        for n in range(0,len(external[1]),1):
            a=np.empty((0,2))
            a = np.append(a, external[0][external[1][n]],axis=0)
            a = np.append(a, intermediate[0][intermediate[1][n]],axis=0)
            a = np.append(a, internal[0][internal[1][n]],axis=0)
            size = np.shape(a)[0]
            if size != 0:
                zona = ConvexHull(a)
                a = zona.points[zona.vertices]
                regiones.append(a)
                areas.append(zona.volume)
                perimetros.append(zona.area)
            else:
                regiones.append([])
                areas.append(0)
                perimetros.append(0)

        lista_respuesta = []
        lista_respuesta.append(regiones)
        lista_respuesta.append(np.asarray(areas))
        lista_respuesta.append(np.asarray(perimetros))

        return lista_respuesta



    def particion(poligono, sitios):

        poligon = ConvexHull(poligono)
        poligon_path = Path( poligon.points[poligon.vertices] )
        number_of_regions = np.shape(sitios)[0]
        vor = Voronoi(sitios, furthest_site=False)
        regiones=[]

        for i in range(0,number_of_regions,1):
            list= vor.regions[vor.point_region[i]].copy()
            if -1 in list:
                list.remove(-1)
            vert = vor.vertices[list].copy()
            rows_to_remove=[]
            for j in range(0,np.shape(vert)[0],1):
                if poligon_path.contains_point(vert[j]) == False:
                    rows_to_remove.append(j)
            vert = np.delete(vert,rows_to_remove,0)
            a = np.vstack((vert,poligono[Delta_Equipartition_adap.puntos_en_region_n(sitios,poligono,i)]))
            regiones.append(a)

        intermediate_vertices=np.empty((0,2))
        regiones_intermediate=[ [] for i in range(len(sitios))]
        sides_intermediate=[]
        count=0
        for row, side in enumerate(vor.ridge_vertices):
            if side[0]!=-1:
                v1x = vor.vertices[side[0]][0]
                v1y = vor.vertices[side[0]][1]
                v2x = vor.vertices[side[1]][0]
                v2y = vor.vertices[side[1]][1]
                for j in range(-1,np.shape(poligono)[0]-1,1):
                    w1x = poligono[j][0]
                    w1y = poligono[j][1]
                    w2x = poligono[j+1][0]
                    w2y = poligono[j+1][1]
                    if Delta_Equipartition_adap.segment_segment_intersect(v1x,v1y,v2x,v2y,w1x,w1y,w2x,w2y) != None:
                        x , y = Delta_Equipartition_adap.segment_segment_intersect(v1x,v1y,v2x,v2y,w1x,w1y,w2x,w2y)
                        new_intersection = np.array([[x,y]])
                        region_1_to_add = vor.ridge_points[row][0]
                        region_2_to_add = vor.ridge_points[row][1]
                        regiones[region_1_to_add] = np.vstack((regiones[region_1_to_add],new_intersection))
                        regiones[region_2_to_add] = np.vstack((regiones[region_2_to_add],new_intersection))

                        intermediate_vertices = np.append(intermediate_vertices, new_intersection,axis=0)
                        regiones_intermediate[region_1_to_add].append(count)
                        regiones_intermediate[region_2_to_add].append(count)
                        sides_intermediate.append([j,j+1])
                        count=count+1
            else:
                vertex = vor.vertices[side[1]]
                point_1= vor.ridge_points[row][0]
                point_2= vor.ridge_points[row][1]
                normal = vor.points[point_1]-vor.points[point_2]
                dir = np.array([normal[1],-normal[0]])
                sitios_sin = np.delete(sitios,[point_1, point_2],axis=0)
                cercano= Delta_Equipartition_adap.punto_mas_cercano(sitios_sin,vertex)
                if cercano>=min(point_1,point_2):
                    cercano = cercano+1
                if cercano>=max(point_1,point_2):
                    cercano = cercano+1
                if np.linalg.norm(vertex+dir-vor.points[cercano]) < np.linalg.norm(vertex+dir-vor.points[point_1]):
                    dir = -dir
                v1x = vertex[0]
                v1y = vertex[1]
                v2x = (vertex+dir)[0]
                v2y = (vertex+dir)[1]
                for j in range(-1,np.shape(poligono)[0]-1,1):
                    w1x = poligono[j][0]
                    w1y = poligono[j][1]
                    w2x = poligono[j+1][0]
                    w2y = poligono[j+1][1]
                    if Delta_Equipartition_adap.segment_line_intersect(w1x,w1y,w2x,w2y,v1x,v1y,v2x,v2y) != None:
                        x , y = Delta_Equipartition_adap.segment_line_intersect(w1x,w1y,w2x,w2y,v1x,v1y,v2x,v2y)
                        new_intersection = np.array([[x,y]])
                        region_1_to_add = vor.ridge_points[row][0]
                        region_2_to_add = vor.ridge_points[row][1]
                        regiones[region_1_to_add] = np.vstack((regiones[region_1_to_add],new_intersection))
                        regiones[region_2_to_add] = np.vstack((regiones[region_2_to_add],new_intersection))

                        intermediate_vertices = np.append(intermediate_vertices, new_intersection,axis=0)
                        regiones_intermediate[region_1_to_add].append(count)
                        regiones_intermediate[region_2_to_add].append(count)
                        sides_intermediate.append([j,j+1])
                        count=count+1

        areas=[]
        perimetros=[]
        for n in range(0,len(regiones),1):
            if len(regiones[n].tolist()) != 0:
                zona = ConvexHull(regiones[n])
                regiones[n] = zona.points[zona.vertices]
                areas.append(zona.volume)
                perimetros.append(zona.area)
            else:
                areas.append(0)
                perimetros.append(0)
        areas = np.array(areas)
        perimetros = np.array(perimetros)
        lista_respuesta = []
        lista_respuesta.append(regiones)
        lista_respuesta.append(areas)
        lista_respuesta.append(perimetros)
        lista_respuesta.append(intermediate_vertices)
        lista_respuesta.append(regiones_intermediate)
        lista_respuesta.append(sides_intermediate)
        return lista_respuesta

    # ===== Finite-difference step sizing (fast, forward diff) =====
    FD_EPS = float(np.sqrt(np.finfo(float).eps))   # ~1.49e-8 (float64)
    FD_MIN = 1e-10
    FD_MAX = 1e-3

    @staticmethod
    def _bbox_scale(poligono):
        """S = ||max_bound - min_bound|| ของ Convex Hull (กันศูนย์ +1e-12)"""
        hull = ConvexHull(poligono)
        return float(np.linalg.norm(hull.max_bound - hull.min_bound) + 1e-12)

    @classmethod
    def _delta_internal(cls, X_flat, S, delta_override=None):
        """
        delta_i สำหรับพารามิเตอร์ภายใน (รายตัว):
        δ_i = clip( sqrt(eps) * max(|x_i|,1) * S , S*FD_MIN , S*FD_MAX )
        ถ้ามี delta_override: ใช้ค่าคงที่ทุกตัว
        """
        if delta_override is not None:
            return np.full_like(X_flat, float(delta_override), dtype=float)
        base = cls.FD_EPS * np.maximum(np.abs(X_flat), 1.0) * S
        return np.clip(base, cls.FD_MIN * S, cls.FD_MAX * S)

    @classmethod
    def _delta_edge(cls, external, sides_intermediate, S, delta_override=None):
        """
        ก้าวฐานบนเส้น (ก่อน cap รายแถว):
        δ_e_base = clip( sqrt(eps) * median(edge_lengths) , S*FD_MIN , S*FD_MAX )
        คืน (δ_e_base, edge_lengths)
        ถ้ามี delta_override: ใช้เป็นค่า base ตรง ๆ
        """
        if delta_override is not None:
            return float(delta_override), [ ]
        lens = [float(np.linalg.norm(external[0][j1] - external[0][j0]))
                for (j0, j1) in sides_intermediate] if len(sides_intermediate) else []
        Lmed = float(np.median(lens)) if lens else S
        base = cls.FD_EPS * Lmed
        delta_e_base = float(np.clip(base, cls.FD_MIN * S, cls.FD_MAX * S))
        return delta_e_base, lens


    def AP(poligono,number_of_regions,external,intermediate,internal):
        poligon = ConvexHull(poligono)
        area_del_poligono = poligon.volume
        parti=Delta_Equipartition_adap.particion_vertices(external,intermediate,internal)
        a = parti[1]-area_del_poligono/number_of_regions
        b = parti[2]-parti[2].mean()
        return np.array([np.append(a,b)]).transpose()

    @classmethod
    def get_jacap_timings(cls):
        """คืนผลลัพธ์สะสมจากทุกครั้งที่เรียก Jac_AP"""
        return cls.cumulative_jacap_times

    cumulative_jacap_times = {
        'AP_initial': 0.0,
        'internal_loop': 0.0,
        'intermediate_loop': 0.0,
        'total_cpu': 0.0,
        'calls': 0
    }

    def Jac_AP(poligono, number_of_regions, external, intermediate, internal, delta=None):
      """
      Jacobian แบบ forward-diff:
      - internal: ใช้ δ_i แบบ scale-aware ต่อพารามิเตอร์ (หรือใช้ค่า override ถ้าส่ง delta มา)
      - intermediate: ใช้ δ_e แบบ edge-aware ต่อแถว (ทิศตามขอบ + cap ≤ 25% ของความยาวขอบ)
      รองรับ delta=None อย่างถูกต้อง
      """
      import numpy as np, time
      from scipy.spatial import ConvexHull

      t_start = time.process_time()

      # 0) residual ปัจจุบัน
      t0 = time.process_time()
      b = Delta_Equipartition_adap.AP(poligono, number_of_regions, external, intermediate, internal)
      t_ap = time.process_time() - t0

      # 1) สเกลโดเมน S และเวกเตอร์ตัวแปรภายใน
      hull = ConvexHull(poligono)
      S = float(np.linalg.norm(hull.max_bound - hull.min_bound) + 1e-12)

      X = np.array([internal[0].flatten()]).T   # (n,1)
      X_flat = X.ravel()
      n = X_flat.size
      m = b.size

      # 2) internal: สร้าง δ_i
      eps = np.finfo(float).eps
      k = np.sqrt(eps)                           # ~1.49e-8
      if delta is None:
          base = k * np.maximum(np.abs(X_flat), 1.0) * S
          lo, hi = S*1e-10, S*1e-3
          delta_vec = np.clip(base, lo, hi)      # (n,)
      else:
          delta_vec = np.full(n, float(delta), dtype=float)

      # 3) คอลัมน์ฝั่ง internal (forward difference)
      t1 = time.process_time()
      jac = np.empty((m, 0))
      for col in range(n):
          di = float(delta_vec[col])
          base = np.zeros_like(X); base[col, 0] = 1.0
          Xp = X + base * di
          internal_p = [Xp.reshape((int(X.size/2), 2)), internal[1]]
          bp = Delta_Equipartition_adap.AP(poligono, number_of_regions, external, intermediate, internal_p)
          cambio = (bp - b) / di
          jac = np.append(jac, cambio, axis=1)
      t_int = time.process_time() - t1

      # 4) คอลัมน์ฝั่ง intermediate (ทิศตาม segment + cap 25%)
      p = int(intermediate[0].shape[0])
      directions = np.empty((p, 2))
      t2 = time.process_time()
      if p > 0:
          # median edge length
          edge_lengths = []
          for row in range(p):
              i0, i1 = intermediate[2][row][0], intermediate[2][row][1]
              seg = external[0][i1] - external[0][i0]
              edge_lengths.append(float(np.linalg.norm(seg)))
          Lmed = float(np.median(edge_lengths)) if edge_lengths else S

          if delta is None:
              de_base = float(np.clip(k * Lmed, S*1e-10, S*1e-3))
          else:
              de_base = float(delta)

          for row in range(p):
              i0, i1 = intermediate[2][row][0], intermediate[2][row][1]
              inicio = external[0][i0]; final = external[0][i1]
              seg = final - inicio
              seglen = float(np.linalg.norm(seg))
              if seglen <= 1e-15:
                  directions[row] = np.array([1.0, 0.0], dtype=float)
                  di_e = de_base
              else:
                  dirv = (seg / seglen).astype(float)
                  directions[row] = dirv
                  di_e = float(min(de_base, 0.25 * seglen))

              base = np.zeros_like(intermediate[0], dtype=float); base[row] = directions[row]
              inter_p = [intermediate[0].astype(float, copy=False) + base * di_e,
                        intermediate[1], intermediate[2]]

              bp = Delta_Equipartition_adap.AP(poligono, number_of_regions, external, inter_p, internal)
              cambio = (bp - b) / di_e
              jac = np.append(jac, cambio, axis=1)
      t_intm = time.process_time() - t2

      # 5) บันทึกเวลาสะสม (ถ้ามี dict ในคลาส)
      try:
          ct = Delta_Equipartition_adap.cumulative_jacap_times
          ct['AP_initial']        += t_ap
          ct['internal_loop']     += t_int
          ct['intermediate_loop'] += t_intm
          ct['total_cpu']         += (time.process_time() - t_start)
          ct['calls']             += 1
      except Exception:
          pass

      return jac, directions

    def balanceo(poligono, arreglo):
        distancia_max = 0
        punto_1 = np.empty([1,2])
        punto_2 = np.empty([1,2])
        for i in range(0, len(poligono), 1):
            for j in range(i+1, len(poligono), 1):
                if (distancia_max < np.linalg.norm(poligono[i]-poligono[j])):
                    distancia_max = np.linalg.norm(poligono[i]-poligono[j])
                    punto_1 = poligono[i]
                    punto_2 = poligono[j]
        vv= (punto_1-punto_2)/np.linalg.norm(punto_1-punto_2)
        ww= np.array([-vv[1],vv[0]])
        alt_pos =0
        alt_neg =0
        for i in range(0, len(poligono),1 ):
            if (np.dot(poligono[i]-punto_1, ww) > alt_pos):
                alt_pos = np.dot(poligono[i]-punto_1, ww)
            if (np.dot(poligono[i]-punto_1, ww) < alt_neg):
                alt_neg = np.dot(poligono[i]-punto_1, ww)
        distancia_perpendicular = alt_pos - alt_neg
        const = distancia_max/distancia_perpendicular
        nuevo_arreglo=arreglo.copy()
        for j in range(0,len(arreglo),1):
            nuevo_arreglo[j]= arreglo[j] +np.dot(punto_1 - arreglo[j],ww)*(1-const)*ww
        return nuevo_arreglo



    def desbalanceo(poligono, arreglo):
        distancia_max = 0
        punto_1 = np.empty([1,2])
        punto_2 = np.empty([1,2])
        for i in range(0, len(poligono), 1):
            for j in range(i+1, len(poligono), 1):
                if (distancia_max < np.linalg.norm(poligono[i]-poligono[j])):
                    distancia_max = np.linalg.norm(poligono[i]-poligono[j])
                    punto_1 = poligono[i]
                    punto_2 = poligono[j]
        vv= (punto_1-punto_2)/np.linalg.norm(punto_1-punto_2)
        ww= np.array([-vv[1],vv[0]])
        alt_pos =0
        alt_neg =0
        for i in range(0, len(poligono),1 ):
            if (np.dot(poligono[i]-punto_1, ww) > alt_pos):
                alt_pos = np.dot(poligono[i]-punto_1, ww)
            if (np.dot(poligono[i]-punto_1, ww) < alt_neg):
                alt_neg = np.dot(poligono[i]-punto_1, ww)
        distancia_perpendicular = alt_pos - alt_neg
        const = 1/(distancia_max/distancia_perpendicular)
        nuevo_arreglo=arreglo.copy()
        for j in range(0,len(arreglo),1):
            nuevo_arreglo[j]= arreglo[j] +np.dot(punto_1 - arreglo[j],ww)*(1-const)*ww
        return nuevo_arreglo

    def save_regions_to_csv(regiones, filename,
                            trial_id,error_total_normalizado,
                            order,polygon,sigmaa,
                            repetition,save_csv,number_of_regions,t1,t,endlloyd,endnormal,eqq,endtime):
        # ให้แน่ใจว่าโฟลเดอร์มีอยู่
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        rows = []
        rows.append({
                    'num_regions': number_of_regions,
                    'order': order,
                    'eqq': eqq,
                    'polygon': polygon,
                    'error_total': error_total_normalizado,
                    'time': endtime,
                    'time_lloyd':endlloyd,
                    'time_normal':endnormal,
                    'repetition': repetition,
                    'iteration_lloyd':t1,
                    'iteration_Newton': t,
                    'sigma': sigmaa,
                    'time_details':save_csv
                })

        df = pd.DataFrame(rows, columns=[
            'num_regions','order','eqq','polygon','error_total','time','time_lloyd','time_normal','repetition',
            'iteration_lloyd','iteration_Newton','sigma','time_details'
        ])

        # ถ้าไฟล์ยังไม่มี ให้เขียน header ครั้งแรก (mode='a' append)
        write_header = not os.path.exists(filename)
        df.to_csv(filename,
                index=False,
                mode='a',
                header=write_header)

        print(f"Trial {order}: Appended {len(regiones)} regions + summary to {filename}")


    def partition(polygon,number_of_regions,trial_id,round,order,seed):
        os.makedirs('k99', exist_ok=True)
        iteraciones_centroide = 100
        iteraciones_Newton = 200
        numero_de_repetitiones= 2500
        balancear_poligono = True
        alcanzo_resultado=False
        eqq = ['central_diff','factor','muti_fuzz','svr_fuzz','elas_fuzz','nn_pred_fuzz','normal','delta','delta_adap']

        repetition=0

        poligon = ConvexHull(polygon)
        area_del_poligono=poligon.volume
        poligono = poligon.points[poligon.vertices]
        area_del_poligono=poligon.volume

        while (alcanzo_resultado==False) and (repetition < numero_de_repetitiones):

            starttime = time.perf_counter()
            start_cputime = time.process_time()
            stscale = time.perf_counter()
            stscalecpu = time.process_time()
            if (balancear_poligono == True) :
                poligono_original = poligono
                nuevo_poligono = Delta_Equipartition_adap.balanceo(poligono, poligono)
                poligon = ConvexHull(nuevo_poligono)
                poligono = poligon.points[poligon.vertices]
                area_del_poligono=poligon.volume

            rng_sitios = np.random.default_rng(seed[repetition])
            bbox = [poligon.min_bound, poligon.max_bound]
            poligon_path = Path( poligon.points[poligon.vertices] )
            rand_points = np.empty((number_of_regions, 2))
            for i in range(number_of_regions):
              rand_points[i] = np.array([rng_sitios.uniform(bbox[0][0], bbox[1][0]), rng_sitios.uniform(bbox[0][1], bbox[1][1])])
              while poligon_path.contains_point(rand_points[i]) == False:
                rand_points[i] = np.array([rng_sitios.uniform(bbox[0][0], bbox[1][0]), rng_sitios.uniform(bbox[0][1], bbox[1][1])])
            sitios = rand_points
            coordenadas=sitios.copy()
            part = Delta_Equipartition_adap.particion(poligono,coordenadas)
            regiones = part[0]
            centros = np.empty(np.shape(coordenadas))
            endscale = time.perf_counter() - stscale
            endscalecpu = time.process_time() - stscalecpu

            stlloyd = time.perf_counter()
            stlloydcpu = time.process_time()
            for i in range(len(regiones)):
                centros[i]=Delta_Equipartition_adap.centroide(regiones[i])[0]
            coord = coordenadas
            t1=0
            while (t1 < iteraciones_centroide) and (np.linalg.norm(coord-centros) >10**-4):
                part = Delta_Equipartition_adap.particion(poligono,coordenadas)
                regiones = part[0]
                centros = np.empty(np.shape(coordenadas))
                for i in range(len(regiones)):
                    centros[i]=Delta_Equipartition_adap.centroide(regiones[i])[0]
                coord = coordenadas
                coordenadas = centros
                t1=t1+1
                max_progress = 100
                bar_length = 20
                percent = t1 / max_progress * 100
                filled_len = int(percent / 100 * bar_length)
                bar = '0' * filled_len + '-' * (bar_length - filled_len)
                print(f"\r Tr : {order} Iterations lloyd : |{bar}| {percent:.1f}%", end='', flush=True)
            endlloyd = time.perf_counter() - stlloyd
            endlloydcpu = time.process_time() - stlloydcpu

            stex = time.perf_counter()
            stexcpu = time.process_time()
            part = Delta_Equipartition_adap.particion(poligono,coordenadas)
            external=Delta_Equipartition_adap.external_vertices(poligono,coordenadas)
            intermediate=part[3:]
            internal=Delta_Equipartition_adap.internal_vertices(poligono,coordenadas)
            endex = time.perf_counter() - stex
            endexcpu = time.process_time() - stexcpu

            strescale= time.perf_counter()
            strescalecpu = time.process_time()
            if (balancear_poligono == True) :
                internal_new=[]
                internal_new.append(Delta_Equipartition_adap.desbalanceo(poligono_original, internal[0]))
                internal_new.append(internal[1])
                intermediate_new=[]
                intermediate_new.append(Delta_Equipartition_adap.desbalanceo(poligono_original, intermediate[0]))
                intermediate_new.append(intermediate[1])
                intermediate_new.append(intermediate[2])
                external_new=[]
                external_new.append(Delta_Equipartition_adap.desbalanceo(poligono_original, external[0]))
                external_new.append(external[1])

                external =external_new
                intermediate = intermediate_new
                internal = internal_new

                poligono = poligono_original
                poligon = ConvexHull(poligono)
                poligono = poligon.points[poligon.vertices]
                area_del_poligono=poligon.volume

            parti=Delta_Equipartition_adap.particion_vertices(external,intermediate,internal)
            perim=parti[2]
            are=parti[1]
            endrescale = time.perf_counter() - strescale
            endrescalecpu = time.process_time() - strescalecpu

            error_total_normalizado=sum((are/(area_del_poligono/number_of_regions)-1)**2)+sum((perim/perim.mean()-1)**2)
            factor0 = 1
            eta = 10**-4
            t = 0
            count_delta = 0
            stnormal = time.perf_counter()
            stnormalcpu = time.process_time()
            while (t < iteraciones_Newton) and ((error_total_normalizado >10**-16)):

                rutina_factor_inicial_chico = True
                rutina_puntos_en_el_interior = True
                # rutina_achicamiento_vector = False  #Rutina de Mayita
                if count_delta == 14:
                  count_delta = 1

                if (rutina_factor_inicial_chico == True):
                    if (t < 10):
                        factor = factor0*((t+1)/10)
                    else :
                        factor = factor0
                else :
                    factor = factor0

                # if count_delta == 0:
                #   delta = 0.5*(10**-3)
                # elif count_delta > 1 and count_delta <= 10:
                #   delta = 10**-4
                # elif count_delta > 10:
                #   delta = 5*(10**-5)

                # delta = 0.5*(10**-3)

                jacobian = Delta_Equipartition_adap.Jac_AP(poligono,number_of_regions,external,intermediate,internal,delta=None)
                AP_value = Delta_Equipartition_adap.AP(poligono,number_of_regions,external,intermediate,internal)
                X = np.array([internal[0].flatten()]).transpose()
                n = np.size(X)
                p= np.shape(intermediate[0])[0]
                resp = np.linalg.lstsq(jacobian[0],-AP_value,rcond=None)

                if (rutina_puntos_en_el_interior == True) :
                    puntos_intermedios = intermediate[0]+factor*(np.append(resp[0][n:n+p,:],resp[0][n:n+p,:],axis=1)*jacobian[1])
                    puntos_internos = internal[0]+factor*(resp[0][0:n].transpose().reshape((int(np.shape(X)[0]/2),2)))
                    while (np.prod(poligon_path.contains_points(puntos_intermedios, radius=10**-4))*np.prod(poligon_path.contains_points(puntos_internos, radius=10**-4)) == 0) :
                        factor = factor/2
                        puntos_intermedios = intermediate[0]+factor*(np.append(resp[0][n:n+p,:],resp[0][n:n+p,:],axis=1)*jacobian[1])
                        puntos_internos = internal[0]+factor*(resp[0][0:n].transpose().reshape((int(np.shape(X)[0]/2),2)))

                intermediate_new=[]
                intermediate_new.append(intermediate[0]+factor*(np.append(resp[0][n:n+p,:],resp[0][n:n+p,:],axis=1)*jacobian[1]))
                intermediate_new.append(intermediate[1])
                intermediate_new.append(intermediate[2])

                internal_new=[]
                internal_new.append(internal[0]+factor*(resp[0][0:n].transpose().reshape((int(np.shape(X)[0]/2),2))))
                internal_new.append(internal[1])

                parti = Delta_Equipartition_adap.particion_vertices(external,intermediate_new,internal_new)
                error_convexidad = sum(parti[1])-area_del_poligono
                error_convexidad_normalizada = sum(parti[1])/area_del_poligono - 1

                error_total_normalizado = sum((parti[1]/(area_del_poligono/number_of_regions)-1)**2)+sum((parti[2]/parti[2].mean()-1)**2)
                internal = internal_new
                intermediate = intermediate_new

                progress = t + 1
                max_progress = 200
                bar_length = 20
                percent = progress / max_progress * 100
                filled_len = int(percent / 100 * bar_length)
                bar = '0' * filled_len + '-' * (bar_length - filled_len)
                print(f"\r Tr : {order} eqq : {eqq[8]} Iterations Normal Flow : |{bar}| {percent:.1f}%", end='', flush=True)

                if (error_convexidad_normalizada > 1) or (factor < 10**-8): # น่าจะเช็คกรณีลู่ออก กับ ลู่เข้าน้อยเกินไป แต่มันมีด้วยหรอ
                    break
                t = t+1
                count_delta = count_delta+1

            endnormal = time.perf_counter() - stnormal
            endnormalcpu = time.process_time() - stnormalcpu
            parti=Delta_Equipartition_adap.particion_vertices(external,intermediate,internal)
            error_convexidad = sum(parti[1])-area_del_poligono
            sigmaa = 0
            perim=parti[2]
            are=parti[1]
            error_total=sum((are-(area_del_poligono/number_of_regions))**2)+sum((perim-perim.mean())**2)
            error_total_normalizado=sum((are/(area_del_poligono/number_of_regions)-1)**2)+sum((perim/perim.mean()-1)**2)

            if ((error_total_normalizado <= 10**-16)):
                alcanzo_resultado=True
            print('Repetition {}, |%F^c|: Total Error= {},Convexity Error = {}'.format(repetition,error_total,error_convexidad))
            repetition += 1

            endtime = time.perf_counter()- starttime
            end_cputime = time.process_time() - start_cputime
            save_csv = (f'TR : {trial_id}_{round} Total_Time: {endtime} CPU_time : {end_cputime}\n',
                  f'Normal_Flow : {endnormal} Normal_FlowCPU : {endnormalcpu}\n',
                  f'LLoyd : {endlloyd} Lloyd_CPU : {endlloydcpu}\n',
                  f'External : {endex} External_CPU : {endexcpu}\n',
                  f'scale : {endscale} scale_CPU : {endscalecpu}\n',
                  f'rescale : {endrescale} rescale_CPU : {endrescalecpu}\n'
                  ,Delta_Equipartition_adap.get_jacap_timings())
            Delta_Equipartition_adap.save_regions_to_csv(parti[0],os.path.join('k99', f'regions_coordinates_{trial_id}_{round}.csv'),trial_id,
                                    error_total_normalizado,order ,polygon ,sigmaa ,repetition ,save_csv ,number_of_regions ,t1 ,t
                                      ,endlloyd ,endnormal ,eqq[8] ,endtime)

        return parti[0],parti[1],parti[2]
