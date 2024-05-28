import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import openpyxl


# Clase Node que representa un nodo en el árbol AVL
class Node:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.left = None
        self.right = None
        self.height = 1


# Clase AVLTree que maneja la lógica del árbol AVL
class AVLTree:
    # Función para insertar un nuevo nodo en el árbol
    def insert(self, root, student_id, name):
        if not root:
            return Node(student_id, name)
        elif student_id < root.student_id:
            root.left = self.insert(root.left, student_id, name)
        else:
            root.right = self.insert(root.right, student_id, name)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        # Rotaciones necesarias para mantener el balance del árbol
        if balance > 1 and student_id < root.left.student_id:
            return self.right_rotate(root)
        if balance < -1 and student_id > root.right.student_id:
            return self.left_rotate(root)
        if balance > 1 and student_id > root.left.student_id:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and student_id < root.right.student_id:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # Función para eliminar un nodo del árbol
    def delete(self, root, student_id):
        if not root:
            return root

        if student_id < root.student_id:
            root.left = self.delete(root.left, student_id)
        elif student_id > root.student_id:
            root.right = self.delete(root.right, student_id)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.get_min_value_node(root.right)
            root.student_id = temp.student_id
            root.name = temp.name
            root.right = self.delete(root.right, temp.student_id)

        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        # Rotaciones necesarias para mantener el balance del árbol
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # Función para buscar un nodo en el árbol por ID de estudiante
    def search(self, root, student_id):
        if not root or root.student_id == student_id:
            return root

        if student_id < root.student_id:
            return self.search(root.left, student_id)
        return self.search(root.right, student_id)

    # Función para obtener el nodo con el valor mínimo en un subárbol
    def get_min_value_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    # Función para realizar una rotación hacia la izquierda
    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    # Función para realizar una rotación hacia la derecha
    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    # Función para obtener la altura de un nodo
    def get_height(self, root):
        if not root:
            return 0
        return root.height

    # Función para obtener el balance de un nodo
    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    # Función para realizar un recorrido inorden del árbol
    def in_order(self, root):
        res = []
        if root:
            res = res + self.in_order(root.left)
            res.append((root.student_id, root.name))
            res = res + self.in_order(root.right)
        return res


# Clase AVLGUI que maneja la interfaz gráfica
class AVLGUI:
    def __init__(self, root):
        self.tree = AVLTree()
        self.root = root
        self.tree_root = None

        self.root.title("AVL Tree Visualizer")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.canvas.pack()

        self.label_id = tk.Label(self.root, text="ID del Estudiante:")
        self.label_id.pack(side=tk.LEFT)
        self.entry_id = tk.Entry(self.root)
        self.entry_id.pack(side=tk.LEFT)
        self.label_name = tk.Label(self.root, text="Nombre del Estudiante:")
        self.label_name.pack(side=tk.LEFT)
        self.entry_name = tk.Entry(self.root)
        self.entry_name.pack(side=tk.LEFT)

        self.insert_button = tk.Button(self.root, text="Agregar estudiante", command=self.insert)
        self.insert_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.root, text="Eliminar estudiante", command=self.delete)
        self.delete_button.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.root, text="Buscar estudiante", command=self.search)
        self.search_button.pack(side=tk.LEFT)

        self.list_button = tk.Button(self.root, text="Listar estudiantes", command=self.list_students)
        self.list_button.pack(side=tk.LEFT)

        self.export_button = tk.Button(self.root, text="Exportar a Excel", command=self.export_to_excel)
        self.export_button.pack(side=tk.LEFT)

    # Función para insertar un estudiante en el árbol
    def insert(self):
        try:
            student_id = int(self.entry_id.get())
            name = self.entry_name.get()
            self.tree_root = self.tree.insert(self.tree_root, student_id, name)
            self.entry_id.delete(0, tk.END)
            self.entry_name.delete(0, tk.END)
            self.display_tree()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter an integer value for ID and a name for the student.")

    # Función para eliminar un estudiante del árbol
    def delete(self):
        try:
            student_id = int(self.entry_id.get())
            self.tree_root = self.tree.delete(self.tree_root, student_id)
            self.entry_id.delete(0, tk.END)
            self.display_tree()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter an integer value for ID.")

    # Función para buscar un estudiante en el árbol
    def search(self):
        try:
            student_id = int(self.entry_id.get())
            student = self.tree.search(self.tree_root, student_id)
            if student:
                messagebox.showinfo("Search Result", f"Student ID: {student.student_id}, Name: {student.name}")
            else:
                messagebox.showinfo("Search Result", f"Student ID {student_id} does not exist in the tree.")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter an integer value for ID.")

    # Función para listar todos los estudiantes en el árbol
    def list_students(self):
        students = self.tree.in_order(self.tree_root)
        if students:
            student_list = "\n".join([f"ID: {student[0]}, Name: {student[1]}" for student in students])
            messagebox.showinfo("List of Students", student_list)
        else:
            messagebox.showinfo("List of Students", "No students found.")

    # Función para exportar la lista de estudiantes a un archivo Excel
    def export_to_excel(self):
        students = self.tree.in_order(self.tree_root)
        if students:
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if file_path:
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet.title = "Estudiantes"
                sheet.append(["ID", "Nombre"])
                for student in students:
                    sheet.append([student[0], student[1]])
                workbook.save(file_path)
                messagebox.showinfo("Export Successful", f"Students have been successfully exported to {file_path}")
        else:
            messagebox.showinfo("Export Failed", "No students found to export.")

    # Función para mostrar el árbol en el lienzo
    def display_tree(self):
        self.canvas.delete("all")
        if self.tree_root:
            self._display_tree(self.tree_root, 400, 50, 200)

    # Función recursiva para dibujar cada nodo del árbol
    def _display_tree(self, node, x, y, x_offset):
        if node:
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white")
            self.canvas.create_text(x, y, text=f"{node.student_id}\n{node.name}")
            if node.left:
                self.canvas.create_line(x, y, x - x_offset, y + 60)
                self._display_tree(node.left, x - x_offset, y + 60, x_offset // 2)
            if node.right:
                self.canvas.create_line(x, y, x + x_offset, y + 60)
                self._display_tree(node.right, x + x_offset, y + 60, x_offset // 2)


if __name__ == "__main__":
    root = tk.Tk()
    gui = AVLGUI(root)
    root.mainloop()
