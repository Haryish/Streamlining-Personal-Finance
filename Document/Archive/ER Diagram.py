import os

# Install ERAlchemy if not already installed
try:
    import eralchemy
except ImportError:
    os.system("pip install eralchemy")

from eralchemy import render_er

# Path to the SQLite database file
db_path = '/mnt/data/db.sqlite3'

# Output file path for the ER diagram
output_path = '/mnt/data/er_diagram.dot'

# Generate ER diagram in DOT format
render_er(f"sqlite:///{db_path}", output_path)

# Convert DOT to image (optional, if Graphviz is installed)
image_path = '/mnt/data/er_diagram.png'
os.system(f"dot -Tpng {output_path} -o {image_path}")

print(f"ER Diagram saved as {output_path} and {image_path}")
