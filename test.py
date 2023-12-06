
import ezdxf


def load_dxf_layers(dxf_file_path):
    try:

        doc = ezdxf.readfile(dxf_file_path)

        layers = [layer.dxf.name for layer in doc.layers]
        return layers
    except IOError:
        print(f"Cannot open file: {dxf_file_path}")
        return []
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file: {dxf_file_path}")
        return []


example_dxf_path = r"C:\C00-100.dxf"
layer_list = load_dxf_layers(example_dxf_path)
print(layer_list)
print('test')


