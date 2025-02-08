from rest_framework.renderers import BaseRenderer
import json
import xml.etree.ElementTree as ET


class CustomRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return f"Custom formatted data: {json.dumps(data, indent=4)}"


class XMLRenderer(BaseRenderer):
    media_type = 'application/xml'
    format = 'xml'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        root = ET.Element('root')
        self._build_xml(root, data)
        return ET.tostring(root, encoding='unicode')

    def _build_xml(self, parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, key)
                self._build_xml(child, value)
        elif isinstance(data, list):
            for item in data:
                child = ET.SubElement(parent, 'item')
                self._build_xml(child, item)
        else:
            parent.text = str(data)