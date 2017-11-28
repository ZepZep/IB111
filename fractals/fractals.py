import math


def project(pos, angle, dist):
    projX = pos[0] + math.cos(angle) * dist
    projY = pos[1] + math.sin(angle) * dist
    return projX, projY


def distance(pos1, pos2):
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)


class Triangle:
    def segment(self, start, end, chir, level):
        points = []
        angleToEnd = math.atan2(end[1] - start[1], end[0] - start[0])

        side = distance(start, end) / 2
        angle = math.pi / 3
        if not chir:
            angle = -angle

        if level == 0:
            return [start, end]

        nextPoint = project(start, angleToEnd + angle, side)
        points.extend(self.segment(start, nextPoint, not chir, level - 1))
        lastPoint = nextPoint

        nextPoint = project(lastPoint, angleToEnd, side)
        points.extend(self.segment(lastPoint, nextPoint, chir, level - 1)[1:])
        lastPoint = nextPoint

        points.extend(self.segment(lastPoint, end, not chir, level - 1)[1:])

        return points

    @staticmethod
    def initial(width, height):
        start = (100, height - 200)
        end = (width - 100, height - 200)
        points = [start, end]
        chirs = [False]

        return points, chirs


class Flake:
    def __init__(self, angle=math.pi / 3):
        self.angle = angle
        self.sideMul = 1 / (2 + 2 * math.cos(angle))

    def segment(self, start, end, chir, level):
        points = []
        angleToEnd = math.atan2(end[1] - start[1], end[0] - start[0])

        side = distance(start, end) * self.sideMul
        angle = self.angle

        if not chir:
            angle = -angle

        if level == 0:
            return [start, end]

        nextPoint = project(start, angleToEnd, side)
        points.extend(self.segment(start, nextPoint, chir, level - 1))
        lastPoint = nextPoint

        nextPoint = project(lastPoint, angleToEnd + angle, side)
        points.extend(self.segment(lastPoint, nextPoint, chir, level - 1)[1:])
        lastPoint = nextPoint

        nextPoint = project(lastPoint, angleToEnd - angle, side)
        points.extend(self.segment(lastPoint, nextPoint, chir, level - 1)[1:])
        lastPoint = nextPoint

        points.extend(self.segment(lastPoint, end, chir, level - 1)[1:])

        return points

    @staticmethod
    def initial(width, height):
        left = (100, height - 200)
        top = (width/2, height-200 - math.sqrt(3)/2*(width - 200))
        right = (width - 100, height - 200)

        points = [left, top, right, left]
        chirs = [False, False, False]

        return points, chirs


class Dragon:
    def segment(self, start, end, chir, level):
        points = []
        angleToEnd = math.atan2(end[1] - start[1], end[0] - start[0])

        side = distance(start, end) / math.sqrt(2)
        angle = math.pi / 4
        if not chir:
            angle = -angle

        if level == 0:
            return [start, end]

        nextPoint = project(start, angleToEnd + angle, side)
        points.extend(self.segment(start, nextPoint, True, level - 1))

        points.extend(self.segment(nextPoint, end, False, level - 1)[1:])

        return points

    @staticmethod
    def initial(width, height):
        left = (100, height/2)
        top = (width / 2, height - 250 - (width - 200) / 2)
        right = (width - 100, height / 2)

        points = [left, right]
        chirs = [True]

        return points, chirs


class Thunder:
    def segment(self, start, end, chir, level):
        points = []
        angleToEnd = math.atan2(end[1] - start[1], end[0] - start[0])

        angle = math.pi / 5
        side = distance(start, end) / 2 / math.cos(angle)
        if not chir:
            angle = -angle

        if level == 0:
            return [start, end]

        nextPoint = project(start, angleToEnd + angle, side)
        points.extend(self.segment(start, nextPoint, not chir, level - 1))
        lastPoint = nextPoint

        nextPoint = project(end, math.pi + angleToEnd + angle, side)
        points.extend(self.segment(lastPoint, nextPoint, chir, level - 1)[1:])
        lastPoint = nextPoint

        points.extend(self.segment(lastPoint, end, not chir, level - 1)[1:])

        return points

    @staticmethod
    def initial(width, height):
        left = (100, height/2)
        right = (width - 100, height / 2)

        points = [left, right]
        chirs = [True]

        return points, chirs

fractalTypes = [("Sierpinski triangle", Triangle()),
                ("Koch snowflake", Flake()),
                ("Angled snowflake", Flake(math.pi * 75 / 180)),
                ("Dragon curve", Dragon()),
                ("Thunder", Thunder())]
