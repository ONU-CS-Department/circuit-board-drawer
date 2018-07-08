from math import atan2, degrees

class LineGraphic():
    def __init__(self, x0, y0, x1, y1, color, hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color
        self.hasStartNode = hasStartNode
        self.hasEndNode = hasEndNode
        self.hasStartModule = hasStartModule
        self.hasEndModule = hasEndModule

    def drawLine(self, canvas=None, stipple=""):
        canvas.create_line(self.x0, self.y0, self.x1, self.y1, fill=self.color, width=6, stipple=stipple)
        lineDirection = self.getLineDirection()

        nodeSize = 16
        if (stipple != ""): # when node is not transparent
            nodeSize = 19
        
        if self.hasStartNode:
            self.drawVertexShape(self.x0, self.y0, nodeSize, nodeSize, self.getOppositeDirection(lineDirection), "node", stipple, canvas)
        if self.hasEndNode:
            self.drawVertexShape(self.x1, self.y1, nodeSize, nodeSize, lineDirection, "node", stipple, canvas)
        if self.hasStartModule:
            self.drawVertexShape(self.x0, self.y0, 16, 32, self.getOppositeDirection(lineDirection), "module", stipple, canvas)
        if self.hasEndModule:
            self.drawVertexShape(self.x1, self.y1, 16, 32, lineDirection, "module", stipple, canvas)

    def drawVertexShape(self, x, y, width, height, direction, shape, stipple="", canvas=None):
        negator = 1
        if ((direction == 3) | (direction == 0)):
            negator *= -1

        if ((direction == 1) | (direction == 3)):
            x0Diff = 0 * negator
            y0Diff = -1 * width/2 * negator
            x1Diff = height * negator
            y1Diff = width/2 * negator
        else:
            x0Diff = width/2 * negator
            y0Diff = 0 * negator
            x1Diff = -1 * width/2  * negator
            y1Diff = height * negator
        if (shape == "node"): # Returing not for values, but to conserve space on this t-shirt :)
            if (stipple != ""): # create_oval doesn't allow transparency, so we must use "create_polygon" to make 
                canvas.create_polygon(x + x0Diff, y + y0Diff,x + x0Diff, y + y1Diff, x + x1Diff, y + y1Diff, x + x1Diff, y + y0Diff, outline=self.color, smooth=1, stipple=stipple, fill=self.color)
            else:
                canvas.create_oval(x + x0Diff, y + y0Diff, x + x1Diff, y + y1Diff, width=6, stipple=stipple, outline=self.color)
        else:
            canvas.create_rectangle(x + x0Diff, y + y0Diff, x + x1Diff, y + y1Diff, outline=self.color, stipple=stipple, fill=self.color)
        
    def getOppositeDirection(self, lineDirection):
        if (lineDirection == 0):
            return 2
        elif (lineDirection == 1):
            return 3
        elif (lineDirection == 2):
            return 0
        return 1

    # Lines angle is determined by the angle between two vertexes in line
    # Graph quadrant (in direction of circle) ranges: I: 0 to -90 exclusive, II: 90 exclusive to 0, III: 0 to -90 exclusive, IV: 90 exclusive to 0
    def getLineAngle(self):
        atanDegrees = degrees(atan2((self.y1-self.y0),(self.x1-self.x0)))
        if (atanDegrees < 0):
            return abs(atanDegrees)
        return 180 + (180 - atanDegrees)
    
    # 0, 1, 2, 3 for up, right, down, left
    def getLineDirection(self):
        angle = self.getLineAngle()
        if ((angle > 45.0) & (angle < 135.0)):
            return 0
        if ((angle >= 315.0) or ((angle > 0.0) & (angle <= 45.0))):
            return 1
        if ((angle >= 135.0) & (angle <= 225.0)):
            return 3
        return 2
