"""
This module provides a line graphic that can be drawn to a canvas with leading/trailing circular-nodes/rectangles
"""
from math import atan2, degrees

class LineGraphic():
    def __init__(self, x0, y0, x1, y1, color, hasStartNode=False, hasEndNode=False, hasStartModule=False, hasEndModule=False):
        """Construct the object

        Keyword arguments:
        x0 -- x coordinate of first vertex
        y0 -- y coordinate of first vertex
        x1 -- x coordinate of second vertex
        y1 -- y coordinate of second vertex
        color -- line color. As a hexadecimal or English name
        hasStartNode -- if True, adds a circular node to start of line (default False)
        hasEndNode -- if True, adds a circular node to end of line (default False)
        hasStartModule -- if True, adds a rectangle to start of line (default False)
        hasEndModule -- if True, adds a rectangle to end of line (default False)
        """
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
        """Draws a line to the canvas

        Keyword arguments:
        canvas -- a tkinter Canvas instance (default None)
        stipple -- a color to blend with the background to give impression of opacity (default "")
        """
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
        """Draws either a circle, rectangle, or circular polygon to canvas

        Keyword arguments:
        x -- start point x value
        y -- start point y value
        width -- width of shape
        height -- height of shape
        direction -- direction of shape (0, 1, 2, 3 for up, right, down, left, respectively)
        shape -- name of shape to draw
        stipple -- a color to blend with the background to give impression of opacity (default "")
        canvas -- a tkinter Canvas instance (default None)
        """
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
                canvas.create_oval(x + x0Diff, y + y0Diff, x + x1Diff, y + y1Diff, width=6, outline=self.color)
        else:
            canvas.create_rectangle(x + x0Diff, y + y0Diff, x + x1Diff, y + y1Diff, outline=self.color, stipple=stipple, fill=self.color)
        
    def getOppositeDirection(self, lineDirection):
        """Get the opposite direction of a line

        Keyword arguments:
        lineDirection -- direction of the line
        """
        if (lineDirection == 0):
            return 2
        elif (lineDirection == 1):
            return 3
        elif (lineDirection == 2):
            return 0
        return 1

    def getLineDirectionPrecise(self):
        """Use the angle of a line to determine its direction: 0, 1, 2, 3, 4, 5, 6, 7 for up, up-right, right, down-right, down, down-left, left, up-left respectively"""
        angle = self.getLineAngle()
        if ((angle > 337.5) or (angle <= 22.5)):
            return 2
        if ((angle > 22.5) and (angle <= 67.5)):
            return 1
        if ((angle > 67.5) and (angle <= 112.5)):
            return 0
        if ((angle > 112.5) and (angle <= 157.5)):
            return 7
        if ((angle > 157.5) and (angle <= 202.5)):
            return 6
        if ((angle > 202.5) and (angle <= 247.5)):
            return 5
        if ((angle > 247.5) and (angle <= 292.5)):
            return 4
        if ((angle > 292.5) and (angle <= 337.5)):
            return 3
        return -1
        
    def getLineAngle(self):
        """Get the angle of the line in relation to its angle on a circle"""
        atanDegrees = degrees(atan2((self.y1-self.y0),(self.x1-self.x0)))
        if (atanDegrees < 0):
            return abs(atanDegrees)
        return 180 + (180 - atanDegrees)
    
    def getLineDirection(self):
        """Use the angle of a line to determine its direction: 0, 1, 2, 3 for up, right, down, left, respectively"""
        angle = self.getLineAngle()
        if ((angle > 45.0) & (angle < 135.0)):
            return 0
        if ((angle >= 315.0) or ((angle > 0.0) & (angle <= 45.0))):
            return 1
        if ((angle >= 135.0) & (angle <= 225.0)):
            return 3
        return 2
