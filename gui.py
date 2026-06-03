# gui.py
import os
import threading
import customtkinter as ctk
from tkinter import messagebox

# Importamos las funciones core que ya desarrollaste en tu pipeline
from clasificar_cli import analizar_pagina_web
from generar_reporte import crear_reporte_pdf

# Configuración estética global (Estilo Moderno / Oscuro)
ctk.set_appearance_mode("System")  # Detecta si el sistema operativo está en modo oscuro
ctk.set_default_color_theme("blue") # Tema azul que alinea con la UNAM

class AppSADOW(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la Ventana Principal
        self.title("SADOW - Sistema Inteligente de Auditoría de Odio Web • UNAM")
        self.geometry("700x520")
        self.resizable(False, False)

        # Paleta de colores institucionales para la GUI
        self.azul_unam = "#002B49"
        self.dorado_unam = "#B38E5D"

        # --- ENCABEZADO INSTITUCIONAL ---
        self.header_frame = ctk.CTkFrame(self, fg_color=self.azul_unam, height=80, corner_radius=0)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO", 
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        self.title_label.pack(pady=(12, 2))

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame, 
            text="FACULTAD DE INGENIERÍA • AUDITORÍA DE ODIO WEB (CNN 1D)", 
            font=ctk.CTkFont(family="Helvetica", size=11),
            text_color=self.dorado_unam
        )
        self.subtitle_label.pack()

        # --- CUERPO DE LA INTERFAZ ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Entrada de la URL
        self.url_label = ctk.CTkLabel(
            self.main_frame, 
            text="Inserte la URL del video de YouTube a auditar:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.url_label.pack(anchor="w", pady=(0, 5))

        self.url_entry = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="https://www.youtube.com/watch?v=...", 
            width=640,
            height=35
        )
        self.url_entry.pack(pady=(0, 15))

        # Botón de Acción Principal
        self.btn_analizar = ctk.CTkButton(
            self.main_frame, 
            text="INICIAR AUDITORÍA E INFERENCIA", 
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.azul_unam,
            hover_color="#00406C",
            height=40,
            command=self.ejecutar_analisis_hilo
        )
        self.btn_analizar.pack(fill="x", pady=(0, 15))

        # Indicador de Progreso (Spinner / ProgressBar)
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, orientation="horizontal", mode="indeterminate")
        self.progress_bar.set(0)

        # --- PANEL DE CUADRO DE MANDO (DASHBOARD KPIs) ---
        self.kpi_frame = ctk.CTkFrame(self.main_frame, height=100)
        self.kpi_frame.pack(fill="x", pady=(5, 15))
        self.kpi_frame.pack_propagate(False)

        # Métrica 1: Total Procesados
        self.kpi1_val = ctk.CTkLabel(self.kpi_frame, text="-", font=ctk.CTkFont(size=24, weight="bold"))
        self.kpi1_val.place(relx=0.15, rely=0.3, anchor="center")
        self.kpi1_lbl = ctk.CTkLabel(self.kpi_frame, text="Comentarios Analizados", font=ctk.CTkFont(size=10))
        self.kpi1_lbl.place(relx=0.15, rely=0.7, anchor="center")

        # Métrica 2: Mensajes de Odio
        self.kpi2_val = ctk.CTkLabel(self.kpi_frame, text="-", font=ctk.CTkFont(size=24, weight="bold"))
        self.kpi2_val.place(relx=0.5, rely=0.3, anchor="center")
        self.kpi2_lbl = ctk.CTkLabel(self.kpi_frame, text="Mensajes de Odio", font=ctk.CTkFont(size=10))
        self.kpi2_lbl.place(relx=0.5, rely=0.7, anchor="center")

        # Métrica 3: Índice Global
        self.kpi3_val = ctk.CTkLabel(self.kpi_frame, text="-", font=ctk.CTkFont(size=24, weight="bold"))
        self.kpi3_val.place(relx=0.85, rely=0.3, anchor="center")
        self.kpi3_lbl = ctk.CTkLabel(self.kpi_frame, text="Índice Global de Odio", font=ctk.CTkFont(size=10))
        self.kpi3_lbl.place(relx=0.85, rely=0.7, anchor="center")

        # Caja de Estado / Veredicto Visual
        self.veredicto_box = ctk.CTkLabel(
            self.main_frame, 
            text="ESTADO DEL SISTEMA: EN ESPERA DE DATOS", 
            height=50,
            corner_radius=6,
            fg_color="#34495E",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.veredicto_box.pack(fill="x", pady=(0, 10))

        # Terminal Log integrada de la GUI
        self.log_textbox = ctk.CTkTextbox(self.main_frame, height=120, font=ctk.CTkFont(family="Courier", size=11))
        self.log_textbox.pack(fill="x")
        self.log_textbox.insert("0.0", ">>> SADOW listo. Inserte un enlace web válido para comenzar...\n")
        self.log_textbox.configure(state="disabled")

    def log(self, texto):
        """Imprime logs internos en la caja de texto embebida"""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f">>> {texto}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def ejecutar_analisis_hilo(self):
        """Lanza el análisis en un hilo secundario para evitar que la GUI se congele"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error de Entrada", "Por favor, proporcione una URL de YouTube válida.")
            return
        
        self.btn_analizar.configure(state="disabled")
        self.progress_bar.pack(fill="x", pady=(0, 15))
        self.progress_bar.start()
        
        # Hilo de ejecución asíncrono
        threading.Thread(target=self.proceso_auditoria, args=(url,), daemon=True).start()

    def proceso_auditoria(self, url):
        try:
            self.log(f"Iniciando peticiones síncronas a la API de Google para: {url}")
            
            # 1. Llamada a tu CNN (clasificar_cli)
            comentarios, conteo_odio, pct_global, datos_tabla = analizar_pagina_web(url)
            
            if not comentarios:
                self.log("Error crítico: No se extrajeron comentarios de la API.")
                self.restablecer_gui()
                return

            # 2. Actualizar KPIs cuantitativas en la GUI
            self.kpi1_val.configure(text=str(len(comentarios)))
            self.kpi2_val.configure(text=str(conteo_odio))
            self.kpi3_val.configure(text=f"{pct_global:.2f}%")

            # 3. Evaluar el umbral del 35% e impactar la UI
            if pct_global > 35.0:
                self.veredicto_box.configure(
                    text=f"VEREDICTO IA: ATAQUE DE ODIO DETECTADO ({pct_global:.2f}%)",
                    fg_color="#C0392B"
                )
                self.log("ALERTA: Nivel de riesgo severo. Cambiando matriz a estado de contingencia.")
            else:
                self.veredicto_box.configure(
                    text=f"VEREDICTO IA: ENTORNO SEGURO - COMUNIDAD SALUDABLE ({pct_global:.2f}%)",
                    fg_color="#27AE60"
                )
                self.log("ÉXITO: Entorno saludable confirmado por análisis de características locales.")

            # 4. Compilar de forma automática el Reporte PDF Exhaustivo (los 50 comentarios)
            self.log("Compilando reporte institucional en PDF (ReportLab)...")
            crear_reporte_pdf(
                url_video=url,
                total_comentarios=len(comentarios),
                total_odio=conteo_odio,
                indice_global=pct_global,
                datos_tabla=datos_tabla
            )
            
            self.log("Proceso terminado con éxito. Reporte guardado en 'outputs/reporte_auditoria.pdf'")
            messagebox.showinfo("Auditoría Finalizada", "El reporte PDF institucional ha sido generado exitosamente en la carpeta 'outputs/'.")

        except Exception as e:
            self.log(f"Fallo en la ejecución del pipeline: {str(e)}")
            messagebox.showerror("Error Crítico", f"Ocurrió un fallo en el backend de la red neuronal:\n{e}")
        
        self.restablecer_gui()

    def restablecer_gui(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.btn_analizar.configure(state="normal")

if __name__ == "__main__":
    app = AppSADOW()
    app.mainloop()