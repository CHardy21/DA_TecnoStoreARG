import os
import ast

def get_imports_from_file(filepath):
    """Extrae todos los imports de un archivo Python usando AST."""
    with open(filepath, "r", encoding="utf-8") as f:
        node = ast.parse(f.read(), filename=filepath)
    imports = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(n, ast.ImportFrom):
            if n.module:
                imports.add(n.module.split('.')[0])
    return imports

def get_imports_from_project(root_dir="."):
    """Recorre todos los .py en el proyecto y devuelve los imports únicos."""
    all_imports = set()
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(subdir, file)
                all_imports.update(get_imports_from_file(filepath))
    return sorted(all_imports)

if __name__ == "__main__":
    project_imports = get_imports_from_project("..")  # sube un nivel desde scripts/
    print("Dependencias detectadas en tu proyecto:")
    for imp in project_imports:
        print("-", imp)

    # Preguntar si desea guardar
    choice = input("\n¿Deseás guardar esta lista en un archivo TXT? (s/n): ").strip().lower()
    if choice == "s":
        with open("project_imports.txt", "w", encoding="utf-8") as f:
            for imp in project_imports:
                f.write(f"{imp}\n")
        print("✔️ Lista guardada en project_imports.txt")
    else:
        print("ℹ️ No se guardó ningún archivo.")
