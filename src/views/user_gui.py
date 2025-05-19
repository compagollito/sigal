import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from datetime import datetime
from tkcalendar import DateEntry
from bson import ObjectId

from user.User import User
from user.UserRepository import UserRepository


class UserGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIGAL")
        self.geometry("1000x550")
        self.configure(bg="#f5f5f5")

        self.user_repository = UserRepository()

        self.colors = {
            "primary": "#7f00ff",
            "secondary": "#2C3E50",
            "accent_green": "#2ecc71",
            "accent_yellow": "#f39c12",
            "danger": "#e74c3c",
            "light_bg": "#f5f5f5",
            "white": "#ffffff",
            "dark_text": "#333333",
            "grey_text": "#777777",
            "blue_link": "#007bff",
        }

        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
        self.option_add("*Font", default_font)

        self.create_top_bar()
        self.create_main_content_area()

        self.populate_data_from_db()
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.edit_selected_user_action)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def create_top_bar(self):
        top_bar = tk.Frame(
            self,
            bg=self.colors["white"],
            height=60,
            relief="solid",
            borderwidth=1,
            highlightbackground="#cccccc",
            highlightthickness=1,
        )
        top_bar.pack(side=tk.TOP, fill=tk.X)
        top_bar.pack_propagate(False)

        app_title = tk.Label(
            top_bar,
            text="SIGAL",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["white"],
            fg=self.colors["dark_text"],
        )
        app_title.pack(side=tk.LEFT, padx=20)

        user_icon_label = tk.Label(
            top_bar,
            text="👤",
            font=("Segoe UI", 18),
            bg=self.colors["white"],
            fg=self.colors["dark_text"],
        )
        user_icon_label.pack(side=tk.RIGHT, padx=20)

    def create_main_content_area(self):
        main_frame = tk.Frame(self, bg=self.colors["light_bg"])
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

        header_frame = tk.Frame(main_frame, bg=self.colors["light_bg"])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        gestion_title = tk.Label(
            header_frame,
            text="👥 Gestión de Usuarios",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["light_bg"],
            fg=self.colors["dark_text"],
        )
        gestion_title.pack(side=tk.LEFT, anchor="w")

        self.stats_cards_frame = tk.Frame(header_frame, bg=self.colors["light_bg"])
        self.stats_cards_frame.pack(side=tk.RIGHT)

        self.stat_labels = {}

        stat_card_info = [
            ("Total de Usuarios", "0", self.colors["accent_green"], "👥"),
            ("Roles", "0", self.colors["accent_yellow"], "🏷️"),
        ]

        for i, (title, value, color, icon_char) in enumerate(stat_card_info):
            card = tk.Frame(
                self.stats_cards_frame,
                bg=self.colors["white"],
                padx=15,
                pady=10,
                relief="solid",
                borderwidth=1,
                highlightbackground="#e0e0e0",
                highlightthickness=1,
            )
            card.grid(row=0, column=i, padx=(0 if i == 0 else 10, 0), sticky="ew")
            icon_label = tk.Label(
                card,
                text=icon_char,
                font=("Segoe UI", 18),
                bg=self.colors["white"],
                fg=color,
            )
            icon_label.grid(row=0, column=0, rowspan=2, padx=(0, 10), sticky="ns")
            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 9),
                bg=self.colors["white"],
                fg=self.colors["grey_text"],
            ).grid(row=0, column=1, sticky="w")
            count_label = tk.Label(
                card,
                text=value,
                font=("Segoe UI", 18, "bold"),
                bg=self.colors["white"],
                fg=self.colors["dark_text"],
            )
            count_label.grid(row=1, column=1, sticky="w")
            self.stat_labels[title] = count_label

        toolbar_frame = tk.Frame(
            main_frame,
            bg=self.colors["white"],
            pady=15,
            padx=15,
            relief="solid",
            borderwidth=1,
            highlightbackground="#e0e0e0",
            highlightthickness=1,
        )
        toolbar_frame.pack(fill=tk.X, pady=(0, 20))

        search_icon = tk.Label(
            toolbar_frame,
            text="🔍",
            font=("Segoe UI", 11),
            bg=self.colors["white"],
            fg=self.colors["grey_text"],
        )
        search_icon.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(toolbar_frame, width=30, font=("Segoe UI", 10))
        self.search_entry.insert(0, "Buscar empleado...")
        self.search_entry.pack(side=tk.LEFT, padx=(0, 15))
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)
        self.search_entry.bind("<KeyRelease>", self.filter_data_from_db)

        self.roles_combo = ttk.Combobox(
            toolbar_frame,
            values=[
                "Todos los roles",
                "Administrador",
                "Personal",
                "Supervisor",
                "Alumno",
            ],
            state="readonly",
            width=20,
            font=("Segoe UI", 10),
        )  # "Alumnos" como en tu código original
        self.roles_combo.current(0)
        self.roles_combo.pack(side=tk.LEFT, padx=(0, 15))
        self.roles_combo.bind("<<ComboboxSelected>>", self.filter_data_from_db)

        self.status_combo = ttk.Combobox(
            toolbar_frame,
            values=["Todos los estatus", "Activo", "Inactivo", "Bloqueado"],
            state="readonly",
            width=20,
            font=("Segoe UI", 10),
        )
        self.status_combo.current(0)
        self.status_combo.pack(side=tk.LEFT, padx=(0, 15))
        self.status_combo.bind("<<ComboboxSelected>>", self.filter_data_from_db)

        style = ttk.Style()
        style.configure(
            "AddUser.TButton",
            font=("Segoe UI", 10, "bold"),
            background=self.colors["primary"],
            foreground=self.colors["white"],
        )
        style.map(
            "AddUser.TButton",
            background=[("active", "#0ce405e6")],
            # foreground=[("active", self.colors["white"])],
        )

        add_button = ttk.Button(
            toolbar_frame,
            text="+ Agregar Usuario",
            style="AddUser.TButton",
            command=self.add_user_action,
        )
        add_button.pack(side=tk.RIGHT)

        table_area_frame = tk.Frame(
            main_frame,
            bg=self.colors["white"],
            relief="solid",
            borderwidth=1,
            highlightbackground="#e0e0e0",
            highlightthickness=1,
        )
        table_area_frame.pack(fill=tk.BOTH, expand=True)

        registro_title = tk.Label(
            table_area_frame,
            text="Registro de Usuarios",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["white"],
            fg=self.colors["dark_text"],
            anchor="w",
        )
        registro_title.pack(fill=tk.X, padx=15, pady=(10, 5))

        tree_frame = tk.Frame(table_area_frame, bg=self.colors["white"])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        columns = (
            "nombre",
            "email",
            "cargo",
            "fecha_ingreso",
            "estado",
        )
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("email", text="Email")
        self.tree.heading("cargo", text="Cargo")
        self.tree.heading("fecha_ingreso", text="Fecha Ingreso")
        self.tree.heading("estado", text="Estado")

        self.tree.column("nombre", width=250, anchor=tk.W)
        self.tree.column("email", width=200, anchor=tk.W)
        self.tree.column("cargo", width=150, anchor=tk.W)
        self.tree.column("fecha_ingreso", width=120, anchor=tk.CENTER)
        self.tree.column("estado", width=100, anchor=tk.CENTER)

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#e0e0e0",
            relief="flat",
        )
        style.map("Treeview.Heading", background=[("active", "#d0d0d0")])
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))

        scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        pagination_frame = tk.Frame(table_area_frame, bg=self.colors["white"])
        pagination_frame.pack(fill=tk.X, padx=15, pady=(5, 10))
        self.results_label = tk.Label(
            pagination_frame,
            text="Mostrando 0-0 de 0 empleados",
            font=("Segoe UI", 9),
            bg=self.colors["white"],
            fg=self.colors["grey_text"],
        )
        self.results_label.pack(side=tk.LEFT)

        page_nav_frame = tk.Frame(pagination_frame, bg=self.colors["white"])
        page_nav_frame.pack(side=tk.RIGHT)

    def on_search_focus_in(self, event):
        if self.search_entry.get() == "Buscar empleado...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground=self.colors["dark_text"])

    def on_search_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Buscar empleado...")
            self.search_entry.config(foreground=self.colors["grey_text"])
            self.filter_data_from_db()

    def populate_data_from_db(
        self, search_term=None, role_filter=None, status_filter=None
    ):
        for item in self.tree.get_children():
            self.tree.delete(item)

        all_db_users = self.user_repository.all_users()

        users_to_display = []
        role_counter = {}

        for user_data in all_db_users:
            user = User.from_dict(user_data)

            display = True
            if search_term and search_term.strip().lower() != "buscar empleado...":
                term = search_term.strip().lower()
                full_name = f"{user.get_first_name()} {user.get_last_name()} {user.get_middle_name() or ''}".lower()
                if term not in full_name and term not in user.get_email().lower():
                    display = False

            if role_filter and role_filter != "Todos los roles":
                if user.get_role() != role_filter:
                    display = False

            if status_filter and status_filter != "Todos los estatus":
                if user.get_status() != status_filter:
                    display = False

            if display:
                users_to_display.append(user)

                # Contar dinámicamente roles
                role = user.get_role()
                role_counter[role] = role_counter.get(role, 0) + 1

        for user in users_to_display:
            full_name = f"{user.get_first_name()} {user.get_last_name()} {user.get_middle_name() or ''}"
            email = user.get_email()
            role = user.get_role()
            reg_date_obj = user.get_registration_date()
            reg_date_str = (
                reg_date_obj.strftime("%d/%m/%Y")
                if isinstance(reg_date_obj, datetime)
                else "N/A"
            )

            status = user.get_status()
            status_display = f"◉ {status}" if status == "Activo" else f"○ {status}"

            self.tree.insert(
                "",
                tk.END,
                values=(full_name, email, role, reg_date_str, status_display),
                iid=str(user.get_id()),
            )

        total = len(users_to_display)
        roles_total = sum(role_counter.values())

        self.update_stats_cards(total=total, admin_count=roles_total, alumnos_count=0)

    def filter_data_from_db(self, event=None):
        search_term = self.search_entry.get().strip()
    
        if search_term == "Buscar empleado...":
            search_term = ""

        role_filter = self.roles_combo.get().strip()
        status_filter = self.status_combo.get().strip()

        if role_filter == "Todos los roles":
            role_filter = None
        if status_filter == "Todos los estatus":
            status_filter = None

        self.populate_data_from_db(search_term, role_filter, status_filter)

    def update_stats_cards(self, total, admin_count, alumnos_count):
        if "Total de Empleados" in self.stat_labels:
            self.stat_labels["Total de Empleados"].config(text=str(total))
        if "Roles" in self.stat_labels:
            self.stat_labels["Roles"].config(text=str(admin_count))
        self.results_label.config(text=f"Mostrando 1-{total} de {total} empleados")

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            self.selected_user_id = selected_items[0]
        else:
            self.selected_user_id = None

    # --- Acciones CRUD y Modales ---
    def add_user_action(self):
        self.open_user_modal(mode="add")

    def edit_selected_user_action(self, event=None):
        if hasattr(self, "selected_user_id") and self.selected_user_id:
            self.open_user_modal(mode="edit", user_id=self.selected_user_id)
        else:
            messagebox.showinfo(
                "Editar Usuario",
                "Por favor, seleccione un usuario de la tabla.",
                parent=self,
            )

    def view_selected_user_action(self):
        if hasattr(self, "selected_user_id") and self.selected_user_id:
            self.open_user_modal(mode="view", user_id=self.selected_user_id)
        else:
            messagebox.showinfo(
                "Ver Usuario",
                "Por favor, seleccione un usuario de la tabla.",
                parent=self,
            )

    def delete_selected_user_action(self):
        if hasattr(self, "selected_user_id") and self.selected_user_id:
            user_data = self.user_repository.find_user_by_id(self.selected_user_id)
            if not user_data:
                messagebox.showerror("Error", "Usuario no encontrado.", parent=self)
                return

            user_obj = User.from_dict(user_data)
            full_name = f"{user_obj.get_first_name()} {user_obj.get_last_name()}"

            if messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar al usuario {full_name}?",
                parent=self,
            ):
                try:
                    if self.user_repository.delete_user(self.selected_user_id):
                        messagebox.showinfo(
                            "Eliminar Usuario",
                            "Usuario eliminado correctamente.",
                            parent=self,
                        )
                        self.populate_data_from_db()
                    else:
                        messagebox.showerror(
                            "Eliminar Usuario",
                            "No se pudo eliminar el usuario.",
                            parent=self,
                        )
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Error al eliminar: {e}", parent=self
                    )
        else:
            messagebox.showinfo(
                "Eliminar Usuario",
                "Por favor, seleccione un usuario de la tabla.",
                parent=self,
            )

    def show_context_menu(self, event):
        # Seleccionar el item bajo el cursor
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)  # Selecciona el item
            self.on_tree_select(None)  # Actualiza self.selected_user_id

            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(
                label="Ver Detalles", command=self.view_selected_user_action
            )
            context_menu.add_command(
                label="Editar", command=self.edit_selected_user_action
            )
            context_menu.add_separator()
            context_menu.add_command(
                label="Eliminar", command=self.delete_selected_user_action
            )
            context_menu.tk_popup(event.x_root, event.y_root)

    def open_user_modal(self, mode="add", user_id=None):
        modal = tk.Toplevel(self)
        modal.grab_set()
        modal.resizable(False, False)
        modal.configure(bg=self.colors["white"])

        user_to_edit = None
        if mode != "add" and user_id:
            user_data_dict = self.user_repository.find_user_by_id(user_id)
            if user_data_dict:
                user_to_edit = User.from_dict(user_data_dict)
            else:
                messagebox.showerror("Error", "Usuario no encontrado.", parent=modal)
                modal.destroy()
                return

        title = "Agregar Usuario"
        if mode == "edit":
            title = "Editar Usuario"
        if mode == "view":
            title = "Detalles del Usuario"
        modal.title(title)

        form_frame = tk.Frame(modal, bg=self.colors["white"], padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Definir campos base (sin password)
        fields = {
            "first_name": {"label": "Nombre(s):", "row": 0, "var": tk.StringVar()},
            "last_name": {"label": "Apellido Paterno:", "row": 1, "var": tk.StringVar()},
            "middle_name": {"label": "Apellido Materno:", "row": 2, "var": tk.StringVar()},
            "email": {"label": "Correo Electrónico:", "row": 3, "var": tk.StringVar()},
            "role": {
                "label": "Rol:",
                "row": 4,
                "var": tk.StringVar(),
                "options": ["Administrador", "Supervisor", "Personal", "Alumno"],
            },
            "registration_date": {
                "label": "Fecha de Ingreso:",
                "row": 5,
                "var": tk.StringVar(),
            },
            "status": {
                "label": "Estado:",
                "row": 6,
                "var": tk.StringVar(),
                "options": ["Activo", "Inactivo", "Bloqueado"],
            },
        }

        # Solo agregar campo de contraseña en modo "add"
        if mode == "add":
            fields["password"] = {"label": "Contraseña:", "row": 4, "var": tk.StringVar()}
            fields["role"]["row"] = 5
            fields["registration_date"]["row"] = 6
            fields["status"]["row"] = 7

        for key, field_info in fields.items():
            tk.Label(
                form_frame,
                text=field_info["label"],
                bg=self.colors["white"],
                anchor="w",
            ).grid(row=field_info["row"], column=0, sticky="w", pady=5, padx=(0, 10))

            if key == "registration_date":
                if mode == "add" or mode == "edit":
                    entry = DateEntry(
                        form_frame,
                        textvariable=field_info["var"],
                        width=18,
                        background='darkblue',
                        foreground='white',
                        borderwidth=2,
                        date_pattern='dd/mm/yyyy'
                    )
                    field_info["var"].set(datetime.now().strftime("%d/%m/%Y"))
                else:
                    value = (
                        user_to_edit.get_registration_date().strftime("%d/%m/%Y")
                        if user_to_edit else ""
                    )
                    field_info["var"].set(value)
                    entry = tk.Entry(
                        form_frame,
                        textvariable=field_info["var"],
                        state="readonly",
                        width=20,
                    )
                    if mode == "view":
                        entry['state'] = 'disabled'
            elif "options" in field_info:
                if mode == "view":
                    if user_to_edit:
                        selected_value = getattr(user_to_edit, f"get_{key}")()
                        field_info["var"].set(selected_value)
                    entry = tk.Entry(
                        form_frame,
                        textvariable=field_info["var"],
                        state="readonly",
                        width=20,
                    )
                else:
                    entry = ttk.Combobox(
                        form_frame,
                        values=field_info["options"],
                        textvariable=field_info["var"],
                        state="readonly",
                        width=18,
                    )
                    if user_to_edit:
                        selected_value = getattr(user_to_edit, f"get_{key}")()
                        field_info["var"].set(selected_value)
            else:
                if user_to_edit and key != "password":  # No cargar contraseña existente
                    field_info["var"].set(getattr(user_to_edit, f"get_{key}")())
                entry = tk.Entry(
                    form_frame,
                    textvariable=field_info["var"],
                    width=20,
                    state="readonly" if mode == "view" else "normal",
                    relief="solid",
                    borderwidth=1,
                    show="*" if key == "password" else None  # Mostrar asteriscos para contraseña
                )
                if mode == "view":
                    entry['state'] = 'disabled'

            entry.grid(row=field_info["row"], column=1, sticky="ew", pady=2)
            fields[key]["entry"] = entry

        form_frame.columnconfigure(1, weight=1)

        buttons_frame = tk.Frame(modal, bg=self.colors["light_bg"], pady=10)
        buttons_frame.pack(fill=tk.X)

        if mode != "view":
            save_button = ttk.Button(
                buttons_frame,
                text="Guardar",
                command=lambda: self.save_user_from_modal(
                    modal, mode, fields, user_id if mode == "edit" else None
                ),
            )
            save_button.pack(side=tk.RIGHT, padx=10)

        cancel_button = ttk.Button(
            buttons_frame,
            text="Cerrar",
            command=modal.destroy,
        )
        cancel_button.pack(side=tk.RIGHT, padx=10)

        modal.update_idletasks()
        width = modal.winfo_width()
        height = modal.winfo_height()
        x = (modal.winfo_screenwidth() // 2) - (width // 2)
        y = (modal.winfo_screenheight() // 2) - (height // 2)
        modal.geometry(f"{width}x{height}+{x}+{y}")

    def save_user_from_modal(self, modal, mode, form_fields, user_id_to_edit=None):
        try:
            user_data = {}
            for key, field_info in form_fields.items():
                if key == "registration_date":
                    user_data[key] = field_info["entry"].get_date()
                elif key == "status":
                    user_data[key] = field_info["var"].get()
                else:
                    user_data[key] = field_info["var"].get()

            user_data["authorized_labs"] = []

            if mode == "edit" and not user_data.get("password"):
                existing_user_data = self.user_repository.find_user_by_id(
                    user_id_to_edit
                )
                user_data["password"] = existing_user_data["password"]

            if mode == "add" and not user_data.get("registration_date"):
                user_data["registration_date"] = datetime.utcnow()

            if user_id_to_edit:
                user_data["_id"] = ObjectId(user_id_to_edit)

            valid_keys = [
                "first_name",
                "last_name",
                "middle_name",
                "email",
                "password",
                "role",
                "authorized_labs",
                "status",
                "registration_date",
                "_id",
            ]
            user_args = {k: user_data[k] for k in valid_keys if k in user_data}

            user_obj = User(**user_args)

            if mode == "add":
                self.user_repository.create_user(user_obj.to_dict())
                messagebox.showinfo(
                    "Éxito", "Usuario agregado correctamente.", parent=modal
                )

            elif mode == "edit":
                data_to_set = user_obj.to_dict()
                data_to_set.pop("_id", None)
                self.user_repository.update_user(user_id_to_edit, data_to_set)
                messagebox.showinfo(
                    "Éxito", "Usuario actualizado correctamente.", parent=modal
                )

            self.populate_data_from_db()
            modal.destroy()

        except Exception as e:
            messagebox.showerror("Error de Validación", str(e), parent=modal)
