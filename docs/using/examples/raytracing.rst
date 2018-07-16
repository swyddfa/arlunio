Basic Raytracing
================

.. code-block:: python

    # coding: utf-8

    # In[36]:


    import numpy as np
    from numpy.linalg import norm
    from stylo import Image, cartesian, polar, circle
    from math import sqrt, floor

    get_ipython().run_line_magic('matplotlib', 'inline')


    # In[51]:


    sphere = circle(0, 0, 0.8, fill=True)

    @cartesian()
    def diffuse(x, y):
        return sphere(x, y)


    # Eye Point
    o = np.array([1, 0, -1])
    light = np.array([1, 2, 0])
    mkcol = lambda v: np.array([v, v, v, 255])

    @diffuse.colormap
    def color(x, y):

        # Get the direction of the ray
        d = np.array([x, y, 1])
        d = d / norm(d)
        od = np.dot(o, d)
        try:
            disc = sqrt(od**2 - (1 - 0.8**2))
        except ValueError:
            return mkcol(0)


        # Get the intersection
        t = min([t for t in [-od - disc, -od + disc] if t >= 0])
        p = o + t*d
        angle = abs(np.dot(p, -t*d))
        c = min(floor(2*angle * 255), 255)

        return mkcol(c)


    # In[52]:


    img = Image(512, 512, background=(0,0,0,255))
    img(diffuse)
    img.show()


    # In[25]:


    a = np.array([1, 2, 1])
    b = np.array([1, 1, 3])
    np.dot(a, b)


    # In[20]:


    a * a
