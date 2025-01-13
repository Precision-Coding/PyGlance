def parseSTL(filename):
    import struct
    import os

    def is_binary_stl(file_path):
        """
        Determines if the STL file is binary by checking the first 80 bytes for printable ASCII characters.
        """
        with open(file_path, 'rb') as f:
            header = f.read(80)
            return not all(32 <= b <= 126 or b in {9, 10, 13} for b in header)

    def parse_binary_stl(file_path):
        """
        Parses a binary STL file and returns a list of triangles.
        Each triangle is a tuple: (normal, vertex1, vertex2, vertex3).
        """
        with open(file_path, 'rb') as f:
            header = f.read(80)  # Read the 80-byte header
            triangle_count = struct.unpack('<I', f.read(4))[0]  # Number of triangles
            triangles = []

            for _ in range(triangle_count):
                data = f.read(50)  # Each triangle is 50 bytes
                if len(data) < 50:
                    raise ValueError(f"Unexpected end of file while reading triangle data at triangle {_}.")
                normal = struct.unpack('<fff', data[0:12])  # Normal vector
                vertex1 = struct.unpack('<fff', data[12:24])  # Vertex 1
                vertex2 = struct.unpack('<fff', data[24:36])  # Vertex 2
                vertex3 = struct.unpack('<fff', data[36:48])  # Vertex 3
                attribute_byte_count = struct.unpack('<H', data[48:50])[0]  # Attribute byte count (ignored)

                # Store the triangle data
                triangles.append((normal, vertex1, vertex2, vertex3))
        return triangles

    def parse_ascii_stl(file_path):
        """
        Parses an ASCII STL file and returns a list of triangles.
        Each triangle is a tuple: (normal, vertex1, vertex2, vertex3).
        """
        triangles = []
        with open(file_path, 'r') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith('facet normal'):
                parts = line.split()
                normal = tuple(map(float, parts[2:]))
                vertex1 = tuple(map(float, lines[i + 2].strip().split()[1:]))
                vertex2 = tuple(map(float, lines[i + 3].strip().split()[1:]))
                vertex3 = tuple(map(float, lines[i + 4].strip().split()[1:]))
                triangles.append((normal, vertex1, vertex2, vertex3))
                i += 7  # Skip to the next facet
            else:
                i += 1
        return triangles

    # Determine file type and parse accordingly
    if is_binary_stl(filename):
        try:
            return parse_binary_stl(filename)
        except ValueError as e:
            print(f"Error parsing binary STL file: {e}")
            raise
    else:
        try:
            return parse_ascii_stl(filename)
        except Exception as e:
            print(f"Error parsing ASCII STL file: {e}")
            raise

parseSTL("STLFiles/Cube.stl")