

def projectile(ux, uy, h, T):
    """
    Given initial velocities ux and uy for
    horizontal and vertical velociites respectively as well
    as initial height h. Compute the projectile trajectory
    under Earth's gravity for t seconds
    """

    sx = lambda t: ux*t
    sy = lambda t: uy*t - 4.9*t**2 + h

    xs = [sx(t/25) for t in range(T)]
    ys = [sy(t/25) for t in range(T)]

    return xs, ys
