"""Read sprite alpha to derive clipping geometry. Original PNGs stay untouched."""
from collections import deque
from PIL import Image

def hull(points):
 points=sorted(set(points))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lower=[];upper=[]
 for p in points:
  while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
  lower.append(p)
 for p in reversed(points):
  while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
  upper.append(p)
 return lower[:-1]+upper[:-1]

def sprite_hulls(path,frames):
 image=Image.open(path);alpha=image.getchannel('A');pix=alpha.load()
 for frame in frames:
  w,h=frame['w'],frame['h'];ox,oy=frame['x'],frame['y'];step=2
  occupied={(x,y) for y in range(0,h,step) for x in range(0,w,step) if pix[ox+x,oy+y]>80}
  largest=[]
  while occupied:
   start=occupied.pop();q=deque([start]);component=[start]
   while q:
    x,y=q.popleft()
    for dx,dy in [(-2,-2),(0,-2),(2,-2),(-2,0),(2,0),(-2,2),(0,2),(2,2)]:
     n=(x+dx,y+dy)
     if n in occupied:occupied.remove(n);q.append(n);component.append(n)
   if len(component)>len(largest):largest=component
  points=hull(largest)
  # A tiny outset preserves antialiased edges; clipping only removes unrelated neighbors.
  cx=sum(x for x,y in points)/len(points);cy=sum(y for x,y in points)/len(points)
  frame['clip']=[[round(x+(-3 if x<cx else 3),1),round(y+(-3 if y<cy else 3),1)] for x,y in points]
