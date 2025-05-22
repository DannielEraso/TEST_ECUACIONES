NEURAL_SOLV_EQU
import tkinter as tk
from tkinter import messagebox, Toplevel, filedialog
from fractions import Fraction
import numpy as np
from fpdf import FPDF
import matplotlib.pyplot as plt
import datetime
import random
import time

class SistemaEcuacionesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("◆ NEURAL EQUATION SOLVER ◆")
        self.root.geometry("900x950")
        self.root.configure(bg="#000008")
        
        # Configurar cursor cyberpunk
        self.root.config(cursor="dotbox")

        self.tamano = tk.IntVar(value=2)
        self.entradas = []
        self.ultimos_pasos = []
        self.ultimas_soluciones = []
        self.ultima_A = None
        self.ultima_B = None
        self.uso_fracciones = tk.BooleanVar(value=False)
        
        # Variables para efectos de animación
        self.animation_running = False
        self.glow_widgets = []

        # Configurar fuentes cyberpunk
        self.setup_fonts()
        self.crear_encabezado()
        self.menu_tamano()
        
        # Iniciar efectos de fondo
        self.start_background_effects()

    def setup_fonts(self):
        """Configurar fuentes cyberpunk"""
        self.font_title = ("OCR A Extended", 20, "bold")
        self.font_subtitle = ("Courier New", 14, "bold")
        self.font_body = ("Consolas", 11)
        self.font_matrix = ("Courier New", 10, "bold")
        self.font_button = ("Arial Black", 10, "bold")

    def start_background_effects(self):
        """Iniciar efectos de animación de fondo"""
        self.animate_title()
        
    def animate_title(self):
        """Animar el título con efecto de parpadeo"""
        if hasattr(self, 'title_label'):
            colors = ["#00ff41", "#00ffff", "#ff0080", "#ffff00", "#00ff41"]
            current_color = random.choice(colors)
            self.title_label.config(fg=current_color)
        
        # Repetir cada 2 segundos
        self.root.after(2000, self.animate_title)

    def animate_entry_focus(self, widget):
        """Animar entrada cuando obtiene foco"""
        original_bg = widget.cget('bg')
        glow_colors = ["#ff0080", "#00ffff", "#00ff41"]
        
        def glow_effect(step=0):
            if step < 10:
                intensity = abs(5 - step) / 5
                color_index = step % len(glow_colors)
                glow_color = glow_colors[color_index]
                
                # Crear efecto de brillo
                if intensity > 0.5:
                    widget.config(bg=glow_color, relief="ridge", bd=2)
                else:
                    widget.config(bg=original_bg, relief="flat", bd=1)
                
                self.root.after(100, lambda: glow_effect(step + 1))
            else:
                widget.config(bg=original_bg, relief="sunken", bd=1)
        
        glow_effect()

    def animate_button_hover(self, button, enter=True):
        """Animar botones al pasar el mouse"""
        if enter:
            original_bg = button.cget('bg')
            button.config(relief="raised", bd=3)
            
            # Efecto de pulsación
            def pulse():
                for i in range(5):
                    button.config(bg="#ffffff")
                    self.root.update()
                    time.sleep(0.05)
                    button.config(bg=original_bg)
                    self.root.update()
                    time.sleep(0.05)
        else:
            button.config(relief="flat", bd=1)

    def crear_encabezado(self):
        # Frame principal del encabezado con gradiente simulado
        header_frame = tk.Frame(self.root, bg="#000008", height=120)
        header_frame.pack(fill=tk.X, pady=10)
        header_frame.pack_propagate(False)
        
        # Crear efectos de "circuitos"
        circuit_frame = tk.Frame(header_frame, bg="#000008")
        circuit_frame.pack(fill=tk.X)
        
        # Líneas decorativas
        tk.Label(circuit_frame, text="▓" * 50, font=("Courier", 8), 
                bg="#000008", fg="#003300").pack()
        
        # Título principal con efecto neón
        self.title_label = tk.Label(header_frame, 
                                   text="◆◇◆ NEURAL EQUATION SOLVER ◆◇◆",
                                   font=self.font_title, bg="#000008", fg="#00ff41")
        self.title_label.pack(pady=10)
        
        # Subtítulo con efecto de matriz
        subtitle = tk.Label(header_frame, 
                           text="[ SISTEMA DE ECUACIONES LINEALES v2.0 ]",
                           font=("Courier New", 12), bg="#000008", fg="#00ffff")
        subtitle.pack()
        
        # Líneas decorativas inferiores
        tk.Label(circuit_frame, text="▓" * 50, font=("Courier", 8), 
                bg="#000008", fg="#003300").pack(side=tk.BOTTOM)
        
        # Indicadores de estado simulados
        status_frame = tk.Frame(header_frame, bg="#000008")
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        status_indicators = ["● NEURAL NET: ONLINE", "● MATRIX CORE: ACTIVE", "● SOLVER: READY"]
        for i, status in enumerate(status_indicators):
            color = ["#00ff00", "#ffff00", "#00ffff"][i]
            tk.Label(status_frame, text=status, font=("Courier", 8), 
                    bg="#000008", fg=color).pack(side=tk.LEFT, padx=20)

    def menu_tamano(self):
        # Frame principal con borde cyberpunk
        main_frame = tk.Frame(self.root, bg="#000008", relief="ridge", bd=2)
        main_frame.pack(pady=15, padx=20, fill=tk.X)
        
        # Título de sección
        tk.Label(main_frame, text="▼ CONFIGURACIÓN DEL SISTEMA ▼", 
                font=self.font_subtitle, bg="#000008", fg="#ff0080").pack(pady=10)
        
        # Frame para controles
        controls_frame = tk.Frame(main_frame, bg="#000008")
        controls_frame.pack(pady=10)
        
        # Label mejorado
        tk.Label(controls_frame, text="[TAMAÑO DE MATRIZ]:", 
                font=self.font_body, bg="#000008", fg="#00ffff").pack(side=tk.LEFT, padx=10)

        # Radiobuttons con estilo cyberpunk
        radio_frame = tk.Frame(controls_frame, bg="#000008")
        radio_frame.pack(side=tk.LEFT, padx=10)
        
        for i in range(2, 7):
            radio = tk.Radiobutton(radio_frame, text=f"[{i}x{i}]", variable=self.tamano, value=i,
                                  bg="#000008", fg="#00ff80", selectcolor="#330033",
                                  font=self.font_matrix, relief="flat", bd=2,
                                  activebackground="#001100", activeforeground="#00ff00")
            radio.pack(side=tk.LEFT, padx=5)
            
            # Efecto hover para radiobuttons
            radio.bind("<Enter>", lambda e, r=radio: r.config(fg="#ffff00"))
            radio.bind("<Leave>", lambda e, r=radio: r.config(fg="#00ff80"))

        # Checkbox mejorado
        check_frame = tk.Frame(controls_frame, bg="#000008")
        check_frame.pack(side=tk.LEFT, padx=20)
        
        fraction_check = tk.Checkbutton(check_frame, text="[USAR FRACCIONES]", 
                                       variable=self.uso_fracciones,
                                       bg="#000008", fg="#ff8000", selectcolor="#440044",
                                       font=self.font_body, relief="flat",
                                       activebackground="#220000", activeforeground="#ffff00")
        fraction_check.pack()
        
        # Botón principal mejorado
        create_button = tk.Button(main_frame, text="◆ GENERAR MATRIZ ◆", 
                                 command=self.crear_campos,
                                 bg="#ff0080", fg="#ffffff", font=self.font_button,
                                 relief="raised", bd=3, padx=20, pady=5,
                                 activebackground="#ff40a0", activeforeground="#000000",
                                 cursor="hand2")
        create_button.pack(pady=15)
        
        # Efectos hover para el botón principal
        create_button.bind("<Enter>", lambda e: self.animate_button_hover(create_button, True))
        create_button.bind("<Leave>", lambda e: self.animate_button_hover(create_button, False))

    def crear_campos(self):
        # Limpiar widgets anteriores manteniendo encabezado y menú
        for widget in self.root.winfo_children()[1:]:
            widget.destroy()

        self.menu_tamano()

        n = self.tamano.get()
        self.entradas = []

        # Contenedor principal con diseño mejorado
        contenedor = tk.Frame(self.root, bg="#000008", relief="ridge", bd=3)
        contenedor.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Título de la matriz
        title_frame = tk.Frame(contenedor, bg="#000008")
        title_frame.pack(pady=10)
        
        tk.Label(title_frame, text="▼ MATRIZ DE COEFICIENTES [A] | VECTOR [B] ▼",
                font=self.font_subtitle, bg="#000008", fg="#00ffff").pack()
        
        # Indicadores decorativos
        tk.Label(title_frame, text="═" * 60, font=("Courier", 10), 
                bg="#000008", fg="#004400").pack(pady=5)

        # Frame para la matriz con efectos
        matriz_container = tk.Frame(contenedor, bg="#000008", relief="sunken", bd=2)
        matriz_container.pack(pady=20)
        
        matriz_frame = tk.Frame(matriz_container, bg="#001108", padx=20, pady=20)
        matriz_frame.pack()

        # Crear matriz de entrada con animaciones
        for i in range(n):
            fila = []
            
            # Indicador de fila
            tk.Label(matriz_frame, text=f"[{i+1}]", font=self.font_matrix, 
                    bg="#001108", fg="#888888").grid(row=i, column=0, padx=5)
            
            for j in range(n):
                entrada = tk.Entry(matriz_frame, width=8, font=self.font_matrix, 
                                 bg="#001a1a", fg="#00ffff", insertbackground="#00ffff",
                                 relief="sunken", bd=2, justify="center",
                                 highlightbackground="#004444", highlightcolor="#00ffff")
                entrada.grid(row=i, column=j+1, padx=3, pady=3)
                
                # Efectos de entrada
                entrada.bind("<FocusIn>", lambda e, w=entrada: self.animate_entry_focus(w))
                entrada.bind("<KeyPress>", lambda e, w=entrada: w.config(fg="#ffff00"))
                entrada.bind("<KeyRelease>", lambda e, w=entrada: w.config(fg="#00ffff"))
                
                fila.append(entrada)

            # Separador visual
            tk.Label(matriz_frame, text="║", font=("Courier", 16, "bold"), 
                    bg="#001108", fg="#ffff00").grid(row=i, column=n+1, padx=10)

            # Entrada para vector B
            entrada_b = tk.Entry(matriz_frame, width=8, font=self.font_matrix, 
                               bg="#1a0011", fg="#ff80ff", insertbackground="#ff80ff",
                               relief="sunken", bd=2, justify="center",
                               highlightbackground="#440044", highlightcolor="#ff80ff")
            entrada_b.grid(row=i, column=n+2, padx=3, pady=3)
            
            # Efectos para entrada B
            entrada_b.bind("<FocusIn>", lambda e, w=entrada_b: self.animate_entry_focus(w))
            entrada_b.bind("<KeyPress>", lambda e, w=entrada_b: w.config(fg="#ffff00"))
            entrada_b.bind("<KeyRelease>", lambda e, w=entrada_b: w.config(fg="#ff80ff"))
            
            fila.append(entrada_b)
            self.entradas.append(fila)

        # Panel de botones mejorado
        botones_container = tk.Frame(contenedor, bg="#000008", relief="raised", bd=2)
        botones_container.pack(pady=20, fill=tk.X)
        
        tk.Label(botones_container, text="▼ PANEL DE CONTROL ▼", 
                font=self.font_subtitle, bg="#000008", fg="#ff8000").pack(pady=10)
        
        botones_frame = tk.Frame(botones_container, bg="#000008")
        botones_frame.pack(pady=10)

        # Botones con diseño cyberpunk mejorado
        buttons_config = [
            ("◆ MÉTODO CRAMER ◆", self.resolver_cramer, "#00ff80", "#000000"),
            ("◆ GAUSS-JORDAN ◆", self.resolver_gauss, "#0080ff", "#ffffff"),
            ("◆ EXPORTAR PDF ◆", self.guardar_pdf, "#ff0080", "#ffffff"),
            ("◆ EXPORTAR TXT ◆", self.guardar_txt, "#8000ff", "#ffffff"),
            ("◆ GRAFICAR 2x2 ◆", self.graficar, "#ffff00", "#000000")
        ]
        
        for i, (texto, comando, bg_color, fg_color) in enumerate(buttons_config):
            button = tk.Button(botones_frame, text=texto, command=comando,
                             bg=bg_color, fg=fg_color, font=self.font_button,
                             relief="raised", bd=3, padx=15, pady=8,
                             cursor="hand2")
            button.grid(row=i//3, column=i%3, padx=8, pady=8)
            
            # Efectos hover mejorados
            def make_hover_effect(btn, orig_bg, orig_fg):
                def on_enter(e):
                    btn.config(bg="#ffffff", fg="#000000", relief="ridge")
                def on_leave(e):
                    btn.config(bg=orig_bg, fg=orig_fg, relief="raised")
                return on_enter, on_leave
            
            enter_func, leave_func = make_hover_effect(button, bg_color, fg_color)
            button.bind("<Enter>", enter_func)
            button.bind("<Leave>", leave_func)

        # Botón de créditos mejorado
        creditos_button = tk.Button(contenedor, text="◆ ACERCA DE LOS CREADORES ◆", 
                                   command=self.mostrar_creditos,
                                   bg="#6600cc", fg="#ffffff", font=self.font_button,
                                   relief="raised", bd=3, padx=20, pady=5,
                                   cursor="hand2")
        creditos_button.pack(pady=10)
        
        # Efecto para botón de créditos
        creditos_button.bind("<Enter>", lambda e: creditos_button.config(bg="#9933ff"))
        creditos_button.bind("<Leave>", lambda e: creditos_button.config(bg="#6600cc"))

    def obtener_matrices(self):
        n = self.tamano.get()
        A = np.zeros((n, n), dtype=object)
        B = np.zeros(n, dtype=object)

        for i in range(n):
            for j in range(n):
                val = self.entradas[i][j].get().strip()
                if not val:
                    raise ValueError("Faltan datos en la matriz A")
                A[i, j] = Fraction(val) if self.uso_fracciones.get() else float(val)
            val_b = self.entradas[i][n].get().strip()
            if not val_b:
                raise ValueError("Faltan datos en el vector B")
            B[i] = Fraction(val_b) if self.uso_fracciones.get() else float(val_b)
        return A, B

    def resolver_cramer(self):
        try:
            A, B = self.obtener_matrices()
            det_A = np.linalg.det(np.array(A, dtype=float))
            if np.isclose(det_A, 0):
                messagebox.showerror("❌ ERROR DEL SISTEMA ❌", 
                                   "El sistema no tiene solución única (det=0).")
                return

            pasos = [f"MATRIZ A =\n{A}", f"DETERMINANTE(A) = {round(det_A, 4)}"]
            soluciones = []
            for i in range(len(B)):
                Ai = A.copy()
                Ai[:, i] = B
                det_Ai = np.linalg.det(np.array(Ai, dtype=float))
                xi = det_Ai / det_A
                soluciones.append(Fraction(xi).limit_denominator() if self.uso_fracciones.get() else round(xi, 4))
                pasos.append(f"\nMATRIZ A_{i+1} =\n{Ai}")
                pasos.append(f"DETERMINANTE(A_{i+1}) = {round(det_Ai, 4)}")
                pasos.append(f"x{i+1} = {det_Ai}/{det_A} = {soluciones[-1]}")

            self.ultimos_pasos = pasos
            self.ultimas_soluciones = soluciones
            self.ultima_A = A
            self.ultima_B = B

            self.mostrar_resultados(soluciones, pasos, metodo="MÉTODO DE CRAMER")
        except Exception as e:
            messagebox.showerror("❌ ERROR ❌", f"Entrada inválida: {e}")

    def resolver_gauss(self):
        try:
            A, B = self.obtener_matrices()
            pasos = []
            n = len(B)
            M = np.hstack((A.astype(float), B.reshape(-1, 1).astype(float)))
            pasos.append(f"MATRIZ AUMENTADA INICIAL:\n{M}")

            for i in range(n):
                M[i] = M[i] / M[i, i]
                pasos.append(f"\nFILA {i+1} NORMALIZADA:\n{M}")
                for j in range(n):
                    if i != j:
                        M[j] = M[j] - M[j, i] * M[i]
                        pasos.append(f"\nFILA {j+1} ACTUALIZADA:\n{M}")

            soluciones = [Fraction(M[i, -1]).limit_denominator() if self.uso_fracciones.get() else round(M[i, -1], 4) for i in range(n)]
            self.ultimos_pasos = pasos
            self.ultimas_soluciones = soluciones
            self.ultima_A = A
            self.ultima_B = B

            self.mostrar_resultados(soluciones, pasos, metodo="MÉTODO GAUSS-JORDAN")

        except Exception as e:
            messagebox.showerror("❌ ERROR ❌", f"Entrada inválida: {e}")

    def mostrar_resultados(self, soluciones, pasos, metodo):
        ventana = Toplevel(self.root)
        ventana.title("◆ RESULTADOS DEL ANÁLISIS ◆")
        ventana.geometry("800x600")
        ventana.configure(bg="#000010")
        ventana.config(cursor="dotbox")

        # Encabezado de la ventana de resultados
        header = tk.Frame(ventana, bg="#000010", relief="ridge", bd=2)
        header.pack(fill=tk.X, pady=5)
        
        tk.Label(header, text=f"◆◇◆ {metodo} ◆◇◆",
                font=("OCR A Extended", 16, "bold"), bg="#000010", fg="#00ff80").pack(pady=10)
        
        tk.Label(header, text="═" * 50, font=("Courier", 8), 
                bg="#000010", fg="#004400").pack()

        # Área de texto con scroll mejorada
        text_frame = tk.Frame(ventana, bg="#000010")
        text_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        texto = tk.Text(text_frame, wrap="word", font=("Courier New", 10), 
                       bg="#001111", fg="#00ff80", insertbackground="#00ff80",
                       selectbackground="#004400", selectforeground="#ffffff",
                       relief="sunken", bd=3)
        
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=texto.yview,
                               bg="#333333", troughcolor="#111111", 
                               activebackground="#666666")
        texto.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        texto.pack(side="left", expand=True, fill="both")

        # Insertar contenido con formato mejorado
        texto.insert("end", "▼ PROCEDIMIENTO PASO A PASO ▼\n\n", "titulo")
        
        for i, paso in enumerate(pasos):
            texto.insert("end", f"[PASO {i+1}]\n", "paso")
            texto.insert("end", paso + "\n\n", "contenido")

        texto.insert("end", "\n" + "═" * 50 + "\n", "separador")
        texto.insert("end", "✓ SOLUCIÓN ENCONTRADA ✓\n\n", "solucion_titulo")
        
        for i, sol in enumerate(soluciones):
            texto.insert("end", f"► x{i+1} = {sol}\n", "solucion")

        # Configurar tags para colores
        texto.tag_config("titulo", foreground="#ff0080", font=("Courier New", 12, "bold"))
        texto.tag_config("paso", foreground="#ffff00", font=("Courier New", 10, "bold"))
        texto.tag_config("contenido", foreground="#00ffff")
        texto.tag_config("separador", foreground="#008800")
        texto.tag_config("solucion_titulo", foreground="#00ff00", font=("Courier New", 12, "bold"))
        texto.tag_config("solucion", foreground="#ff8080", font=("Courier New", 11, "bold"))
        
        texto.config(state="disabled")

    def guardar_pdf(self):
        if not self.ultimos_pasos:
            messagebox.showwarning("⚠️ ADVERTENCIA ⚠️", "Primero resuelve un sistema.")
            return

        archivo = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                             filetypes=[("PDF files", "*.pdf")])
        if not archivo:
            return

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=11)

        pdf.set_title("Neural Equation Solver - Solución")
        pdf.set_author("Neural Equation Solver v2.0")

        pdf.cell(0, 10, "NEURAL EQUATION SOLVER - PROCEDIMIENTO", ln=True, align='C')
        pdf.cell(0, 10, f"Fecha de análisis: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
        pdf.ln(5)

        for paso in self.ultimos_pasos:
            pdf.multi_cell(0, 8, paso)
            pdf.ln(1)

        pdf.cell(0, 10, "SOLUCION FINAL:", ln=True)
        for i, sol in enumerate(self.ultimas_soluciones):
            pdf.cell(0, 10, f"x{i+1} = {sol}", ln=True)

        pdf.output(archivo)
        messagebox.showinfo("✅ ÉXITO ✅", f"PDF guardado exitosamente en:\n{archivo}")

    def guardar_txt(self):
        """Nueva función para exportar a TXT"""
        if not self.ultimos_pasos:
            messagebox.showwarning("⚠️ ADVERTENCIA ⚠️", "Primero resuelve un sistema.")
            return

        archivo = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text files", "*.txt")])
        if not archivo:
            return

        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("    NEURAL EQUATION SOLVER - REPORTE DETALLADO\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Fecha de análisis: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Tamaño del sistema: {self.tamano.get()}x{self.tamano.get()}\n")
                f.write(f"Modo fracciones: {'Activado' if self.uso_fracciones.get() else 'Desactivado'}\n\n")
                
                f.write("PROCEDIMIENTO PASO A PASO:\n")
                f.write("-" * 40 + "\n\n")
                
                for i, paso in enumerate(self.ultimos_pasos, 1):
                    f.write(f"[PASO {i}]\n")
                    f.write(paso + "\n\n")
                
                f.write("=" * 60 + "\n")
                f.write("SOLUCIÓN FINAL:\n")
                f.write("=" * 60 + "\n")
                
                for i, sol in enumerate(self.ultimas_soluciones):
                    f.write(f"x{i+1} = {sol}\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write("Generado por Neural Equation Solver v2.0\n")
                f.write("Desarrollado por: Danniel Eraso, Jordan Ramon, Erick Cuevas\n")
                f.write("=" * 60 + "\n")

            messagebox.showinfo("✅ ÉXITO ✅", f"Archivo TXT guardado exitosamente en:\n{archivo}")
            
        except Exception as e:
            messagebox.showerror("❌ ERROR ❌", f"Error al guardar archivo TXT: {e}")

    def graficar(self):
        if self.ultima_A is None or self.ultima_B is None:
            messagebox.showwarning("⚠️ ADVERTENCIA ⚠️", "Primero debes resolver el sistema.")
            return

        A = np.array(self.ultima_A, dtype=float)
        B = np.array(self.ultima_B, dtype=float)

        if A.shape != (2, 2):
            messagebox.showinfo("ℹ️ INFORMACIÓN ℹ️", 
                              "La gráfica está disponible solo para sistemas 2x2.")
            return

        x_vals = np.linspace(-10, 10, 400)
        
        # Configurar estilo cyberpunk para matplotlib
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor('#000010')
        ax.set_facecolor('#001122')

        colors = ['#00ff80', '#ff0080', '#00ffff', '#ffff00']
        
        for i in range(2):
            a, b = A[i]
            c = B[i]
            if b != 0:
                y_vals = (c - a * x_vals) / b
                ax.plot(x_vals, y_vals, color=colors[i], linewidth=2, 
                       label=f"Ecuación {i+1}: {a:.2f}x + {b:.2f}y = {c:.2f}")
            else:
                ax.axvline(x=c/a, color=colors[i], linewidth=2, 
                          label=f"Ecuación {i+1}: x = {c/a:.2f}")

        if len(self.ultimas_soluciones) == 2:
            x, y = [float(s) for s in self.ultimas_soluciones]
            ax.plot(x, y, 'o', color='#ff4444', markersize=10, 
                   markeredgecolor='#ffffff', markeredgewidth=2)
            ax.annotate(f"SOLUCIÓN\n({x:.3f}, {y:.3f})", (x, y), 
                       textcoords="offset points", xytext=(15,15),
                       fontsize=10, color='#ffffff', weight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='#ff4444', alpha=0.8))

        ax.set_xlabel("X", color='#00ffff', fontsize=12, weight='bold')
        ax.set_ylabel("Y", color='#00ffff', fontsize=12, weight='bold')
        ax.axhline(0, color='#444444', linewidth=0.8, alpha=0.7)
        ax.axvline(0, color='#444444', linewidth=0.8, alpha=0.7)
        ax.legend(facecolor='#001122', edgecolor='#00ffff', 
                 labelcolor='#ffffff', fontsize=10)
        ax.grid(True, color='#003333', alpha=0.5, linestyle='--')
        ax.set_title("◆ REPRESENTACIÓN GRÁFICA DEL SISTEMA 2x2 ◆", 
                    color='#00ff80', fontsize=14, weight='bold', pad=20)
        
        # Configurar colores de los ejes
        ax.tick_params(colors='#00ffff')
        ax.spines['bottom'].set_color('#00ffff')
        ax.spines['top'].set_color('#00ffff')
        ax.spines['right'].set_color('#00ffff')
        ax.spines['left'].set_color('#00ffff')

        plt.tight_layout()
        plt.show()

    def mostrar_creditos(self):
        ventana = Toplevel(self.root)
        ventana.title("◆ INFORMACIÓN DEL PROYECTO ◆")
        ventana.geometry("500x400")
        ventana.configure(bg="#000008")
        ventana.config(cursor="dotbox")
        
        # Hacer la ventana no redimensionable
        ventana.resizable(False, False)

        # Frame principal con efectos
        main_frame = tk.Frame(ventana, bg="#000008", relief="ridge", bd=3)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Encabezado con animación
        header_frame = tk.Frame(main_frame, bg="#000008")
        header_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(header_frame, text="◆◇◆ NEURAL DEVELOPMENT TEAM ◆◇◆", 
                              font=("OCR A Extended", 14, "bold"),
                              bg="#000008", fg="#00ff80")
        title_label.pack(pady=5)
        
        tk.Label(header_frame, text="═" * 45, font=("Courier", 10), 
                bg="#000008", fg="#004400").pack()

        # Información del proyecto con diseño cyberpunk
        info_frame = tk.Frame(main_frame, bg="#001111", relief="sunken", bd=2)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear texto con efectos
        mensaje_lines = [
            ("🤖 PROYECTO:", "#ff0080", "bold"),
            ("Neural Equation Solver v2.0", "#00ffff", "normal"),
            ("", "", ""),
            ("👨‍💻 DESARROLLADORES:", "#ff0080", "bold"),
            ("◆ Danniel Eraso - Neural Architecture", "#00ff80", "normal"),
            ("◆ Jordan Ramon - Matrix Core Systems", "#00ff80", "normal"), 
            ("◆ Erick Cuevas - UI/UX Cybernetics", "#00ff80", "normal"),
            ("", "", ""),
            ("📅 ESPECIFICACIONES:", "#ff0080", "bold"),
            ("Año de desarrollo: 2025", "#ffff00", "normal"),
            ("Institución: FESC", "#ffff00", "normal"),
            ("Programa: Ingeniería de Software", "#ffff00", "normal"),
            ("", "", ""),
            ("⚡ CARACTERÍSTICAS:", "#ff0080", "bold"),
            ("• Solución por método de Cramer", "#00ffff", "normal"),
            ("• Eliminación Gauss-Jordan", "#00ffff", "normal"),
            ("• Exportación PDF y TXT", "#00ffff", "normal"),
            ("• Visualización gráfica 2D", "#00ffff", "normal"),
            ("• Interfaz cyberpunk animada", "#00ffff", "normal"),
            ("", "", ""),
            ("🔮 STATUS: FULLY OPERATIONAL", "#00ff00", "bold")
        ]

        for line_text, color, weight in mensaje_lines:
            if line_text:
                font_tuple = ("Courier New", 10, weight) if weight == "bold" else ("Courier New", 9)
                label = tk.Label(info_frame, text=line_text, font=font_tuple,
                               justify="left", bg="#001111", fg=color)
                label.pack(anchor="w", padx=20, pady=2)
            else:
                tk.Label(info_frame, text="", bg="#001111").pack(pady=3)

        # Botón de cierre con efecto
        close_button = tk.Button(main_frame, text="◆ CERRAR TRANSMISIÓN ◆", 
                               command=ventana.destroy,
                               bg="#ff4040", fg="#ffffff", font=("Arial Black", 10, "bold"),
                               relief="raised", bd=3, padx=20, pady=5,
                               cursor="hand2")
        close_button.pack(pady=15)
        
        # Efecto hover para botón de cierre
        def on_enter(e):
            close_button.config(bg="#ff8080", relief="ridge")
        def on_leave(e):
            close_button.config(bg="#ff4040", relief="raised")
            
        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)
        
        # Efecto de parpadeo para el título
        def animate_credits_title():
            colors = ["#00ff80", "#ff0080", "#00ffff", "#ffff00"]
            current_color = colors[int(time.time()) % len(colors)]
            title_label.config(fg=current_color)
            ventana.after(1000, animate_credits_title)
        
        animate_credits_title()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEcuacionesApp(root)
    root.mainloop()
