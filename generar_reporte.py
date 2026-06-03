# generar_reporte.py
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether

def generar_graficas_dinamicas(total_comentarios, total_odio, datos_tabla):
    """
    Genera gráficas estadísticas en tiempo real basadas en los comentarios 
    analizados para inyectarlas directamente en el cuerpo del PDF.
    """
    # Asegurar que el directorio de salida existe
    os.makedirs("outputs", exist_ok=True)
    
    # Paleta de diseño
    color_odio = "#C0392B"
    color_neutro = "#27AE60"
    
    # --- GRÁFICA 1: PASTEL (Distribución Porcentual) ---
    total_neutro = total_comentarios - total_odio
    etiquetas = ['Mensajes Neutros', 'Discurso de Odio']
    valores = [total_neutro, total_odio]
    colores_pie = [color_neutro, color_odio]
    
    plt.figure(figsize=(5, 3.5))
    # Explotar la rebanada de odio si existe para darle énfasis visual
    explode = (0, 0.1) if total_odio > 0 else (0, 0)
    
    plt.pie(valores, explode=explode, labels=etiquetas, colors=colores_pie,
            autopct='%1.1f%%', startangle=140, 
            textprops={'fontsize': 10, 'weight': 'bold'})
    plt.title('Distribución de Sentimiento en el Tablón', fontsize=12, weight='bold', pad=10)
    plt.tight_layout()
    
    ruta_pie = "outputs/dinamica_distribucion.png"
    plt.savefig(ruta_pie, dpi=200)
    plt.close()

    # --- GRÁFICA 2: BARRAS (Top 5 Comentarios más Hostiles) ---
    # Filtrar y ordenar datos: tupla (idx, texto, prob, dictamen) ordenada por prob descendente
    comentarios_ordenados = sorted(datos_tabla, key=lambda x: x[2], reverse=True)[:5]
    
    indices_top = [f"Id #{item[0]}" for item in comentarios_ordenados]
    probabilities_top = [item[2] for item in comentarios_ordenados]
    
    plt.figure(figsize=(5.5, 3.5))
    # Renderizar barras horizontales
    barras = plt.barh(indices_top, probabilities_top, color=color_odio, edgecolor='black', height=0.5)
    
    # Añadir las etiquetas de porcentaje al final de cada barra
    for barra in barras:
        ancho = barra.get_width()
        plt.text(ancho + 1, barra.get_y() + barra.get_height()/2, f'{ancho:.1f}%', 
                 va='center', ha='left', fontsize=9, weight='bold')
                 
    plt.xlim(0, 115) # Margen para que no se corten los textos de porcentaje
    plt.gca().invert_yaxis() # Que el más alto aparezca arriba
    plt.title('Top 5 Publicaciones con Mayor Índice de Hostilidad', fontsize=11, weight='bold', pad=10)
    plt.xlabel('Probabilidad de Odio asignada por la CNN (%)', fontsize=9)
    plt.ylabel('Identificador del Comentario', fontsize=9)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    ruta_barras = "outputs/dinamica_hostiles.png"
    plt.savefig(ruta_barras, dpi=200)
    plt.close()
    
    return ruta_pie, ruta_barras

def crear_reporte_pdf(url_video, total_comentarios, total_odio, indice_global, datos_tabla, ruta_pdf="outputs/reporte_auditoria.pdf"):
    """
    Genera un informe ejecutivo formal en PDF con la hoja de estilos de la UNAM,
    tablas de inferencia, métricas globales, gráficas y un veredicto final automatizado.
    """
    # Asegurar que el directorio de salida existe
    os.makedirs("outputs", exist_ok=True)

    # 0. Lanzar el generador de imágenes dinámicas
    ruta_pie, ruta_barras = generar_graficas_dinamicas(total_comentarios, total_odio, datos_tabla)

    # 1. Configuración del documento
    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # 2. Definición de Paleta de Colores Institucional (UNAM / Ingeniería)
    azul_unam = colors.HexColor("#002B49")
    dorado_unam = colors.HexColor("#B38E5D")
    gris_oscuro = colors.HexColor("#2C3E50")
    gris_claro = colors.HexColor("#F8F9F9")
    rojo_alerta = colors.HexColor("#C0392B")
    verde_seguro = colors.HexColor("#27AE60")
    
    # 3. Estilos Personalizados de Texto
    style_titulo = ParagraphStyle(
        'TituloDoc', parent=styles['Heading1'], fontSize=20, leading=24, textColor=azul_unam, spaceAfter=6, alignment=1
    )
    style_subtitulo = ParagraphStyle(
        'SubtituloDoc', parent=styles['Normal'], fontSize=10, leading=12, textColor=dorado_unam, spaceAfter=15, alignment=1
    )
    style_h2 = ParagraphStyle(
        'SeccionH2', parent=styles['Heading2'], fontSize=13, leading=16, textColor=azul_unam, spaceBefore=14, spaceAfter=8,
        borderColor=dorado_unam, borderWidth=1, borderRadius=2, borderPadding=4
    )
    style_cuerpo = ParagraphStyle(
        'CuerpoTexto', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=gris_oscuro, spaceAfter=8
    )
    style_tabla_header = ParagraphStyle(
        'TableHeader', parent=styles['Normal'], fontSize=9, leading=11, textColor=colors.white, fontName='Helvetica-Bold'
    )
    style_tabla_celda = ParagraphStyle(
        'TableCell', parent=styles['Normal'], fontSize=8.5, leading=11, textColor=gris_oscuro
    )

    # 4. ENCABEZADO INSTITUCIONAL
    story.append(Paragraph("<b>UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO</b>", style_titulo))
    story.append(Paragraph("FACULTAD DE INGENIERÍA • SISTEMA INTELIGENTE DE AUDITORÍA DE ODIO WEB", style_subtitulo))
    
    d_linea = Table([[""]], colWidths=[532], rowHeights=[2])
    d_linea.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), dorado_unam)]))
    story.append(d_linea)
    story.append(Spacer(1, 12))
    
    # 5. RESUMEN EJECUTIVO Y METADATOS
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    estado_ataque = "ALTA PROBABILIDAD (ATAQUE DE ODIO DETECTADO)" if indice_global > 35.0 else "PROBABILIDAD MODERADA (MONITORIZACIÓN SUGERIDA)" if indice_global >= 15.0 else "BAJA PROBABILIDAD (ENTORNO SEGURO)"
    color_estado = rojo_alerta if indice_global > 35.0 else verde_seguro
    
    html_metadatos = f"""
    <b>Fecha de Auditoría:</b> {fecha_actual}<br/>
    <b>Plataforma Objetivo:</b> YouTube Data Stream API v3<br/>
    <b>Enlace del Video Analizado:</b> <font color="blue">{url_video}</font><br/>
    <b>Algoritmo de Inferencia:</b> Word Embeddings + Red Neuronal Convolucional (CNN 1D)<br/>
    <b>Estado de Vulnerabilidad del Sitio:</b> <font color="{color_estado}"><b>{estado_ataque}</b></font>
    """
    story.append(Paragraph(html_metadatos, style_cuerpo))
    story.append(Spacer(1, 8))
    
    # 6. TABLA DE MÉTRICAS MACRO (KPIs)
    kpi_data = [
        [Paragraph("<b>Métrica Analítica</b>", style_tabla_header), Paragraph("<b>Valor Cuantitativo</b>", style_tabla_header)],
        [Paragraph("Total de Comentarios Extraídos en Vivo", style_tabla_celda), Paragraph(str(total_comentarios), style_tabla_celda)],
        [Paragraph("Mensajes con Discurso de Odio Confirmados por IA", style_tabla_celda), Paragraph(str(total_odio), style_tabla_celda)],
        [Paragraph("<b>ÍNDICE DE ODIO GLOBAL CALCULADO</b>", style_tabla_celda), Paragraph(f"<b>{indice_global:.2f}%</b>", style_tabla_celda)]
    ]
    t_kpi = Table(kpi_data, colWidths=[300, 232])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), azul_unam),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, gris_claro]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_kpi)
    
    # 7. SECCIÓN DE ANÁLISIS GRÁFICO DINÁMICO
    story.append(Paragraph("Métricas y Modelación Gráfica del Contenido", style_h2))
    story.append(Paragraph("Las siguientes representaciones visuales desglosan el comportamiento de la sección de comentarios analizada, permitiendo identificar la polaridad del espacio:", style_cuerpo))
    
    # Maquetar las dos gráficas de lado a lado usando una tabla invisible
    img_pie = Image(ruta_pie, width=255, height=178)
    img_barras = Image(ruta_barras, width=265, height=178)
    
    tabla_graficas = Table([[img_pie, img_barras]], colWidths=[266, 266])
    tabla_graficas.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tabla_graficas)
    story.append(Spacer(1, 10))
    
    # 8. SECCIÓN DE INFERENCIAS INDIVIDUALES (TABLA MUESTRA)
    story.append(Paragraph("Muestra Detallada de Clasificación Semántica", style_h2))
    
    header_tabla_muestras = [
        Paragraph("<b>#</b>", style_tabla_header),
        Paragraph("<b>Fragmento del Comentario Real Extraído</b>", style_tabla_header),
        Paragraph("<b>Probabilidad</b>", style_tabla_header),
        Paragraph("<b>Dictamen IA</b>", style_tabla_header)
    ]
    
    cuerpo_tabla_muestras = [header_tabla_muestras]
    # Mostrar solo una muestra de hasta los primeros 10 para no saturar de hojas el PDF
    for idx, texto, prob, dictamen in datos_tabla[:50]:
        texto_corto = texto[:85] + "..." if len(texto) > 85 else texto
        c_dictamen = f"<font color='red'><b>{dictamen}</b></font>" if "ODIO" in dictamen else f"<font color='green'>{dictamen}</font>"
        
        cuerpo_tabla_muestras.append([
            Paragraph(str(idx), style_tabla_celda),
            Paragraph(texto_corto, style_tabla_celda),
            Paragraph(f"{prob:.2f}%", style_tabla_celda),
            Paragraph(c_dictamen, style_tabla_celda)
        ])
        
    t_muestras = Table(cuerpo_tabla_muestras, colWidths=[25, 320, 65, 122])
    t_muestras.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), azul_unam),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, gris_claro]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    
    # Envolver la tabla en un KeepTogether para que se imprima limpia sin romperse a la mitad
    story.append(KeepTogether([t_muestras]))
    story.append(Spacer(1, 14))
    
    # 9. SECCIÓN: VEREDICTO FINAL INSTITUCIONAL
    story.append(Paragraph("Conclusión y Veredicto del Sistema de Auditoría", style_h2))
    
    # Lógica de evaluación basada en el umbral solicitado del 35%
    if indice_global > 35.0:
        titulo_veredicto = "<font color='red'><b>VEREDICTO: ATAQUE DE ODIO DETECTADO</b></font>"
        cuerpo_veredicto = f"""
        El análisis algorítmico automatizado ha determinado que el espacio de interacción de este video 
        <b>está sufriendo un ataque de odio detectado</b>, superando el umbral crítico establecido del 35.0% 
        (Índice Global: {indice_global:.2f}%). Las métricas reflejan hostilidad sistemática y un entorno perjudicial. 
        Se sugiere activar protocolos institucionales de moderación de comentarios.
        """
        color_borde_veredicto = rojo_alerta
    else:
        titulo_veredicto = "<font color='green'><b>VEREDICTO: VIDEO ACEPTADO POR LOS VISORES</b></font>"
        cuerpo_veredicto = f"""
        El análisis algorítmico automatizado concluye que el video <b>es aceptado por los visores</b> y mantiene 
        un entorno seguro. El volumen de interacciones hostiles se sitúa por debajo del límite de riesgo tolerado 
        (Índice Global: {indice_global:.2f}% &le; 35.0%), demostrando una convivencia digital saludable en la sección de comentarios.
        """
        color_borde_veredicto = verde_seguro

    # Estilos específicos para la caja informativa del veredicto
    style_veredicto_titulo = ParagraphStyle(
        'VeredictoTitulo', parent=styles['Normal'], fontSize=11, leading=14, fontName='Helvetica-Bold', spaceAfter=4
    )
    style_veredicto_cuerpo = ParagraphStyle(
        'VeredictoCuerpo', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=gris_oscuro
    )

    # Construcción de la caja visual del veredicto usando una Tabla
    tabla_veredicto_data = [
        [Paragraph(titulo_veredicto, style_veredicto_titulo)],
        [Paragraph(cuerpo_veredicto, style_veredicto_cuerpo)]
    ]
    t_veredicto = Table(tabla_veredicto_data, colWidths=[532])
    t_veredicto.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), gris_claro),
        ('BOX', (0,0), (-1,-1), 1.5, color_borde_veredicto),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    
    # Asegurar que toda la conclusión se mantenga unida y limpia al final de la página
    story.append(KeepTogether([t_veredicto]))
    
    # 10. Construcción final del PDF
    doc.build(story)
    print(f"📄 [PDF COMPILER]: Reporte ejecutivo institucional generado con éxito en '{ruta_pdf}'.")

# --- Bloque de prueba opcional para verificar funcionamiento ---
if __name__ == "__main__":
    # Datos dummy para simular una ejecución directa del script
    mock_comentarios = [
        (1, "Este video es una completa basura, ojalá borren el canal.", 89.5, "DISCURSO_ODIO"),
        (2, "Excelente explicación profesor, me sirvió mucho para mi examen.", 4.2, "NEUTRO"),
        (3, "No puedo creer que alguien apoye esto, son todos unos idiotas.", 91.2, "DISCURSO_ODIO"),
        (4, "Me parece un enfoque interesante, aunque discrepo en el minuto 3.", 12.0, "NEUTRO"),
        (5, "Ojalá se mueran todos los que hicieron este proyecto.", 98.4, "DISCURSO_ODIO"),
    ]
    print("Probando generación con un índice crítico (Ataque)...")
    crear_reporte_pdf("https://youtube.com/watch?v=PruebaOdio", 5, 3, 60.0, mock_comentarios, "outputs/prueba_ataque.pdf")
    
    print("\nProbando generación con un índice saludable (Aceptado)...")
    crear_reporte_pdf("https://youtube.com/watch?v=PruebaOk", 5, 0, 0.0, mock_comentarios, "outputs/prueba_aceptado.pdf")