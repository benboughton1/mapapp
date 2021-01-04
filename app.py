import sys
import os
from qgis import core as qgisCore
from qgis import gui as qgisGui
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from qgis.PyQt.QtCore import Qt


#############################################################################

class MapViewer(QtWidgets.QMainWindow):
    def __init__(self, shapefile):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Map Viewer")

        canvas = qgisGui.QgsMapCanvas()
        # canvas.useImageToRender(False)
        canvas.setCanvasColor(Qt.white)
        canvas.show()

        layer = qgisCore.QgsVectorLayer(shapefile, "layer1", "ogr")
        if not layer.isValid():
            raise IOError("Invalid shapefile")

        project = qgisCore.QgsProject.instance()
        project.addMapLayer(layer)

        canvas.setExtent(layer.extent())
        canvas.setLayers([layer])
        canvas.zoomToFullExtent()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(canvas)

        contents = QtWidgets.QWidget()
        contents.setLayout(layout)
        self.setCentralWidget(contents)

#############################################################################

def main():
    """  Our main program.
    """    
    if getattr(sys, 'frozen', False):
        print("Running In An Application Bundle")
        bundle_dir = sys._MEIPASS
        qgis_prefix_path = bundle_dir
        qgis_plugin_path = bundle_dir + '/qgis_plugins'
    else:
        qgis_prefix_path = 'C:/Users/bboug/miniconda3/pkgs/qgis-3.14.16-py38ha5722f9_2/Library'
        qgis_plugin_path = qgis_prefix_path + '/plugins'

    qgisCore.QgsApplication.setPrefixPath(qgis_prefix_path, True)
    qgisCore.QgsApplication.setPluginPath(qgis_plugin_path)

    app = QtWidgets.QApplication(sys.argv)
    qgisCore.QgsApplication.initQgis()

    viewer = MapViewer('data/gilroy_simple.shp')

    viewer.show()

    app.exec_()

    qgisCore.QgsApplication.exitQgis()

#############################################################################

if __name__ == "__main__":
    print('here')
    main()

