import numpy as np


def interCube(vals, dists):
    out = np.zeros(vals[0].shape)
    for i, val in enumerate(vals):
        x, y = dists[i]
        x = 1-np.abs(x)
        y = 1-np.abs(y)
        xx = x**2
        yy = y**2
        out = out + (3 * xx - 2 * xx*x) * (3 * yy - 2 * yy*y) * val
    return out


def bilin(vals, dists):
    v00, v10, v01, v11 = vals
    x, y = np.abs(dists[0])
    v0 = lerp(v00, v10, x)
    v1 = lerp(v01, v11, x)

    return lerp(v0, v1, y)


def lerp(a, b, w):
    return a + w*(b-a)


interpolatefcns = {
    "Cubic": interCube,
    "Linear": bilin
}


def perlin(size, ips=5, octaves=3, persistence=0.5, lacunarity=2.0, offset=None, seed=None, interFunc=interCube):
    """vektorizovane generovani 2D perlinova sumu"""
    if seed is not None:
        np.random.seed(seed)
    sizeX, sizeY = size
    if offset is None:
        offset = (-sizeX/2, -sizeY/2)

    output = np.zeros(size)
    amplitude = 1

    for i in range(octaves):
        output += getOctave(size, ips, offset, interFunc) * amplitude
        amplitude *= persistence
        ips *= lacunarity

    return output


def getOctave(size, ips, offset, inter):
    """vraci jednu oktavu sumu"""
    sizeX, sizeY = size
    side = sizeX/ips
    ix, iy = np.indices(size)
    ix = ix + offset[0]
    iy = iy + offset[1]
    ind = np.array((ix, iy)) / side
    ix, iy = ind

    grid = np.array([np.random.random(size), np.random.random(size)]) * 2 - 1

    gx, gy = grid

    l, t = np.floor(ind)
    l = np.array(l, dtype=np.int)
    t = np.array(t, dtype=np.int)
    r = l + 1
    b = t + 1

    xs = [l, r]
    ys = [t, b]

    dists = []
    gridInds = []

    for y in ys:
        for x in xs:
            gridInds.append(np.array((x, y)))  # which point
            dists.append(np.array((ix - x, iy - y)))  # distance to that point

    grads = []
    for i, ds in enumerate(dists):
        dx, dy = ds
        gix, giy = gridInds[i]

        a = dx * gx[gix, giy] + dy * gy[gix, giy]
        grads.append(a)

    output = inter(grads, dists)

    return output
