import numpy as np
from io import StringIO
from pyodide.http import open_url
import json
from js import Bokeh, console, JSON
from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN

def myPlot(x, y):
    p = figure(title="Graph", x_axis_label='time', y_axis_label='particle')
    p.circle(x, y, size=3, line_color="navy", fill_color="orange", fill_alpha=0.5)
    p_json = json.dumps(json_item(p, "graph-area"))
    Element("graph-area").element.innerHTML = ""
    Bokeh.embed.embed_item(JSON.parse(p_json))

def handleCSVStringIO(sIO):
    xList, yList = np.genfromtxt(sIO, delimiter="|", skip_header=1, unpack=True)
    myPlot(xList, yList)

def handleCSVString(csvStr):
    sIO = StringIO(csvStr)
    handleCSVStringIO(sIO)   
        
async def drawGraphOfLocalFile():
    localInputElement = Element("data_local_file").element
    fileList = localInputElement.files.to_py()
    if (len(fileList) == 0):
        return
    for f in fileList:
        textData = await f.text()        
        handleCSVString(textData)

def drawGraphOfUrl():
    urlStr = Element('data_url').element.value
    csvStringIO = open_url(urlStr)
    handleCSVStringIO(csvStringIO)