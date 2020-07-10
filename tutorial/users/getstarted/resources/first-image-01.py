import arlunio.image as image
import arlunio.shape as shape

w, h = 1920, 1080
img = image.new(w, h, color="darkorange")

sun = shape.Circle(xc=-1.2, yc=0, r=0.6)
img += image.fill(sun(width=w, height=h), foreground="yellow")

hill = shape.Circle(xc=-1, yc=-2.1, r=1.5)
img += image.fill(hill(width=w, height=h), foreground="forestgreen")

hill = shape.Circle(xc=1, yc=-1.8, r=1.3)
img += image.fill(hill(width=w, height=h), foreground="green")