import freecad
import MeshPart
import Part

input_path = r"c:\Users\jorge\OneDrive\Desktop\SW_parts\Weld_test.STEP"
mesh_filepath = r"c:\Users\jorge\OneDrive\Desktop\SW_parts\Weld_test.stl"

shape = Part.Shape()
shape.read(input_path)

linear_deflection = 0.1
angular_deflection = 0.1
mesh = MeshPart.meshFromShape(
    Shape=shape,
    LinearDeflection=linear_deflection,
    AngularDeflection=angular_deflection,
    Relative=False,
)
mesh.write(mesh_filepath)
