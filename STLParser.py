def parseSTL(filename):
    import struct
    with open(filename, 'rb') as f:
        header = f.read(80)  # Read the 80-byte header
        triangle_count = struct.unpack('<I', f.read(4))[0]  # Number of triangles
        triangles = []

        for _ in range(triangle_count):
            # Read each triangle
            normal = struct.unpack('<fff', f.read(12))  # Normal vector
            vertex1 = struct.unpack('<fff', f.read(12))  # Vertex 1
            vertex2 = struct.unpack('<fff', f.read(12))  # Vertex 2
            vertex3 = struct.unpack('<fff', f.read(12))  # Vertex 3
            attribute_byte_count = struct.unpack('<H', f.read(2))[0]  # Attribute byte count (ignored)

            # Store the triangle data
            triangles.append((normal, vertex1, vertex2, vertex3))

        return triangles

