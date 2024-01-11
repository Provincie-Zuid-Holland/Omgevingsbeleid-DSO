from shapely import wkt


class GMLGeometryGenerator:
    def __init__(self, gml_id: str, geometry: str):
        self._gml_id: str = gml_id
        self._geom = wkt.loads(geometry)

    def generate_xml(self):
        if self._geom.geom_type == "Polygon":
            return self._polygon_to_xml()
        elif self._geom.geom_type == "MultiPolygon":
            return self._multipolygon_to_xml()

    def _polygon_to_xml(self):
        xml_string = f'<gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992">'
        xml_string += self._ring_gml(self._geom.exterior, "exterior")
        for interior in self._geom.interiors:
            xml_string += self._ring_gml(interior, "interior")
        xml_string += "</gml:Polygon>"
        return xml_string

    def _multipolygon_to_xml(self):
        xml_string = f'<gml:MultiSurface srsName="urn:ogc:def:crs:EPSG::28992" gml:id="{self._gml_id}-0">'
        for idx, polygon in enumerate(self._geom.geoms):
            xml_string += "<gml:surfaceMember>"
            xml_string += self._polygon_gml(polygon, f"{self._gml_id}-{idx}")
            xml_string += "</gml:surfaceMember>"
        xml_string += "</gml:MultiSurface>"
        return xml_string

    def _polygon_gml(self, polygon, gml_id):
        xml_string = f"<gml:Polygon>"
        xml_string += self._ring_gml(polygon.exterior, "exterior")
        for interior in polygon.interiors:
            xml_string += self._ring_gml(interior, "interior")
        xml_string += "</gml:Polygon>"
        return xml_string

    def _ring_gml(self, ring, type):
        coords = " ".join([f"{coord[0]} {coord[1]}" for coord in ring.coords])
        xml_string = f"<gml:{type}><gml:LinearRing><gml:posList>{coords}</gml:posList></gml:LinearRing></gml:{type}>"
        return xml_string
