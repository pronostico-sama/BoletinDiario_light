from pathlib import Path
import numpy as np
import pandas as pd
import os
from reportlab.lib.styles import ParagraphStyle
from PIL import Image
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.colors import Color, white
from pypdf import PdfReader, PdfWriter
from io import BytesIO
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from markdown2 import markdown
import warnings
import utilities as utils
warnings.filterwarnings("ignore", category=UserWarning)


# Define a reference date for calculations
DATE_REF = pd.to_datetime('2025-03-31')

# Directorios de entrada y de salida
dir_sama = os.getenv("NODO")


if dir_sama is None:
    # Set the environment variable DIR to the desired path
    os.environ['SAMA'] = '/home/sgiraldoc4/BoletinDiario_light'

    dir_sama = os.environ.get("NODO")


dir_report_lab = os.path.join(dir_sama, 'report_lab/')



def clean_txt_files(report):
    import os
    if report == '08':
        list_files=['0.obs_goes.txt', '1.manana.txt', '2.tarde.txt',
                    '3.noche.txt', '4.madrugada.txt']
    if report == '16':
        list_files=['0.obs_goes.txt', '1.noche.txt', '2.madrugada.txt',
                    '3.manana.txt', '4.tarde.txt']
        
    path_folder = os.path.join(
        dir_sama, 'report_lab', 'txt_boletin', f'{report}', '')
    # Remove all .txt files in the folder
    for file in os.listdir(path_folder):
        if file.endswith('.txt'):
            os.remove(os.path.join(path_folder, file))
    
    # Create empty files for the specified list
    for file in list_files:
        file_path = os.path.join(path_folder, file)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("")  # Write an empty string to create the file
    print(f"\033[94m\tArchivos limpios de txt creados para reporte {report}\033[0m")
        

def markdown_to_paragraph(md_text, style):
    html_text = markdown(md_text, extras=["fenced-code-blocks",
                                          "break-on-newline"])
    # print('-' * 50)
    # print(html_text)
    # Replace double newlines with paragraph breaks
    html_text = html_text.replace('\n\n', '</p><p>')
    # Remove the opening and closing <p> tags and replace them with line breaks
    html_text = html_text.replace('<p>', '').replace('</p>', '<br />')
    # print('-' * 25)
    # print(html_text)
    return Paragraph(html_text, style)


def draw_paragraph_centered(paragraph, canvas, x, y, width, height, x_factor, y_factor):
    """
    Draw a paragraph vertically centered within a box.
    """
    x, y = x_factor(x), y_factor(y)
    width, height = x_factor(width), y_factor(height)

    _, paragraph_height = paragraph.wrap(width, height)
    y_centered = y + (height - paragraph_height) / 2
    paragraph.drawOn(canvas, x, y_centered)


def draw_figure(canvas, img_path, x, y, width, height, x_factor, y_factor):
    """
    Draw an image on the canvas.
    """
    x, y = x_factor(x), y_factor(y)
    width, height = x_factor(width), y_factor(height)

    if not Path(img_path).exists():
        print(
            f"\033[91m\tError: Image not found: {Path(img_path).name}\033[0m")
        return

    img = Image.open(img_path)
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height

    if width / height > aspect_ratio:
        new_width = height * aspect_ratio
        new_height = height
    else:
        new_width = width
        new_height = width / aspect_ratio

    canvas.drawImage(img_path, x, y, width=new_width, height=new_height)


def create_paragraph_style(name, alignment, font_name, font_size,
                           leading, text_color, x_factor, y_factor):
    """
    Helper function to create a ParagraphStyle.
    """
    return ParagraphStyle(
        name=name,
        alignment=alignment,
        fontName=font_name,
        fontSize=y_factor(font_size),
        leading=y_factor(leading),
        textColor=text_color,
        allowWidows=1, allowOrphans=1
    )


def draw_text_from_file(file_path, canvas, x, y, width, height, style, x_factor, y_factor):
    """
    Helper function to read text from a file and draw it on the canvas.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # Replace '-' at the start of each line with '— '
    text = '\n'.join(['— ' + line[1:] if line.startswith('-') else line
                      for line in text.splitlines()])
    # Convert markdown to a paragraph
    paragraph = markdown_to_paragraph(text, style)
    draw_paragraph_centered(paragraph, canvas, x, y,
                            width, height, x_factor, y_factor)


def draw_image_from_path(image_path, canvas, x, y, width, height, x_factor, y_factor):
    """
    Helper function to draw an image on the canvas.
    """
    draw_figure(canvas, image_path, x, y, width, height, x_factor, y_factor)


def draw_rectangle(c, x_i, y_i, width_i, height_i, x_factor, y_factor):
    x_i, y_i, width_i, height_i = x_factor(x_i), y_factor(y_i), \
        x_factor(width_i), y_factor(height_i)
    c.setFillColor(white)
    c.rect(x_i, y_i, width_i, height_i, fill=True, stroke=False)


def report_horizontal_am(date_now, idx, report, dir_report_lab, dir_sama,
                         dir_figures, path_out):
    # Load the existing PDF
    layout_file = f'{dir_report_lab}plantillas/Plant_SinTextoNiMapas_am_horizontal.pdf'
    pdf_reader = PdfReader(layout_file)
    pdf_writer = PdfWriter()

    existing_page = pdf_reader.pages[0]
    page_width = existing_page.mediabox.width
    page_height = existing_page.mediabox.height

    # Define the size of the overlay PDF
    size_x, size_y = 1280, 720
    def x_factor(x): return x * page_width/size_x
    def y_factor(x): return x * page_height/size_y

    blue = Color(17/255, 35/255, 63/255, alpha=1)
    yellow = Color(255/255, 192/255, 0/255, alpha=1)
    gray = Color(89/255, 89/255, 89/255, alpha=1)

    path_fonts = f'{dir_report_lab}/fonts/'

    impact_font = path_fonts + 'impact.ttf'
    pdfmetrics.registerFont(TTFont('Impact', impact_font))

    arial_narrow_bold_font = path_fonts + 'arialnarrow_bold.ttf'
    pdfmetrics.registerFont(TTFont('ArialNarrowBold', arial_narrow_bold_font))

    arial_narrow_font = path_fonts + 'arialnarrow.ttf'
    pdfmetrics.registerFont(TTFont('ArialNarrow', arial_narrow_font))

    # Define styles (particular to the report)
    style_text_gray = create_paragraph_style(
        'JustifyGray', TA_JUSTIFY, 'ArialNarrow', 16, 20, gray, x_factor, y_factor)
    style_text_blue = create_paragraph_style(
        'JustifyBlue', TA_JUSTIFY, 'ArialNarrow', 16, 16, blue, x_factor, y_factor)
    style_text_headers_white = create_paragraph_style(
        'HeadersWhite', TA_CENTER, 'ArialNarrowBold', 18.6, 16, white, x_factor, y_factor)
    style_text_headers_small_white = create_paragraph_style(
        'HeadersSmallWhite', TA_LEFT, 'ArialNarrowBold', 17, 16, white, x_factor, y_factor)

    # Create a new PDF with ReportLab for the overlay
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Define date strings
    date_tomorrow = date_now + pd.Timedelta(days=1)
    str_date_today = date_now.strftime('%d/%m/%Y')
    str_date_today_fig = date_now.strftime('%Y-%m-%d')
    str_date_tomorrow = date_tomorrow.strftime('%d/%m/%Y')
    title_header = f'N°{idx:03} - 8 a.m. {str_date_today}'

    # Draw the title
    c.setFont("ArialNarrowBold", y_factor(26))
    c.setFillColor(white)
    c.drawString(x_factor(435), y_factor(587), title_header)

    # Draw headers
    headers = [
        (f'Jornada: madrugada (1 a.m. - 7 a.m.) - {str_date_today}',
         32.279, 520, 362.133, 20, style_text_headers_white),
        (f'Jornada: mañana (7 a.m. - 1 p.m.) {str_date_today}',
         548, 542.3, 320, 20, style_text_headers_small_white),
        (f'Jornada: tarde (1 p.m. - 7 p.m.) {str_date_today}',
         990, 542.3, 280, 20, style_text_headers_small_white),
        (f'Jornada: noche (7 p.m. - 1 a.m.) {str_date_today}',
         559, 303, 300, 20, style_text_headers_small_white),
        (f'Jornada: madrugada (1 a.m. - 7 a.m.) {str_date_tomorrow}',
         952, 303, 320, 20, style_text_headers_small_white)
    ]

    for text, x, y, width, height, style in headers:
        paragraph = Paragraph(text, style)
        draw_paragraph_centered(paragraph, c, x, y, width,
                                height, x_factor, y_factor)

    # Paths
    path_txt_temp = os.path.join(
        dir_sama, 'report_lab', 'txt_boletin', f'{report}', '')
    


    # -------------------------------------------------------------------------
    # # Observed conditions
    # -------------------------------------------------------------------------
    draw_text_from_file(f'{path_txt_temp}0.obs_goes.txt', c,
                        10.3, 218.7, 405, 101, style_text_gray,
                        x_factor, y_factor)

    draw_image_from_path(f'{dir_figures}{str_date_today_fig}_vis_goes.png',
                         c, 6.667, 324.334, 184.098, 180, x_factor, y_factor)

    draw_image_from_path(f'{dir_figures}{str_date_today_fig}_temp_goes.png',
                         c, 193.267, 324.334, 225.605, 180, x_factor, y_factor)

    # -------------------------------------------------------------------------
    # Forecasts
    # --------------------------------------------------------------------------
    forecast_data = [
        (f'{path_txt_temp}1.manana.txt', 617, 340, 224, 185, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_manana.png',
         426.666, 342.667, 185.211, 180),

        (f'{path_txt_temp}2.tarde.txt', 1044, 339, 224, 185, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_tarde.png',
         853.332, 342.667, 185.211, 180),

        (f'{path_txt_temp}3.noche.txt', 617, 96, 224, 185, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_noche.png',
         426.666, 102.668, 185.211, 180),

        (f'{path_txt_temp}4.madrugada.txt', 1044, 96, 224, 185, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_madrugada.png',
         853.332, 102.668, 185.211, 180)
    ]

    for txt_path, x_txt, y_txt, w_txt, h_txt, style, \
            img_path, x_img, y_img, w_img, h_img in forecast_data:
        draw_text_from_file(txt_path, c, x_txt, y_txt, w_txt,
                            h_txt, style, x_factor, y_factor)
        draw_image_from_path(img_path, c, x_img, y_img,
                             w_img, h_img, x_factor, y_factor)

    c.save()
    packet.seek(0)

    # Merge overlay with existing PDF
    overlay_pdf = PdfReader(packet)
    existing_page.merge_page(overlay_pdf.pages[0])
    pdf_writer.add_page(existing_page)

    # Save the final PDF
    str_date_fileout = date_now.strftime('%Y%m%d')
    file_name_out = f'{idx:03}_BoletinMeteorologico_{str_date_fileout}_{report}_Diaria'
    output_path_pdf = os.path.join(path_out, f'{file_name_out}.pdf')

    with open(output_path_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"PDF created: {file_name_out}")

    # Convert to PNG using ImageMagick
    output_path_png = os.path.join(path_out, f'{file_name_out}.png')
    command = f'convert -density 300 {output_path_pdf} -quality 100 {output_path_png}'
    os.system(command)
    print(f"PNG created: {file_name_out}")


def report_vertical_am(date_now, idx, report, dir_report_lab, dir_sama,
                       dir_figures, path_out):
    # Load the existing PDF
    layout_file = f'{dir_report_lab}plantillas/Plant_SinTextoNiMapac_am_vertical.pdf'
    pdf_reader = PdfReader(layout_file)
    pdf_writer = PdfWriter()

    existing_page = pdf_reader.pages[0]
    page_width = existing_page.mediabox.width
    page_height = existing_page.mediabox.height

    # Define the size of the overlay PDF
    size_x, size_y = 1440, 2560
    def x_factor(x): return x * page_width/size_x
    def y_factor(x): return x * page_height/size_y

    blue = Color(17/255, 35/255, 63/255, alpha=1)
    yellow = Color(255/255, 192/255, 0/255, alpha=1)
    gray = Color(89/255, 89/255, 89/255, alpha=1)

    path_fonts = f'{dir_report_lab}/fonts/'

    impact_font = path_fonts + 'impact.ttf'
    pdfmetrics.registerFont(TTFont('Impact', impact_font))

    arial_narrow_bold_font = path_fonts + 'arialnarrow_bold.ttf'
    pdfmetrics.registerFont(TTFont('ArialNarrowBold', arial_narrow_bold_font))

    arial_narrow_font = path_fonts + 'arialnarrow.ttf'
    pdfmetrics.registerFont(TTFont('ArialNarrow', arial_narrow_font))

    # Define styles (particular to the report)
    style_text_gray = create_paragraph_style(
        'JustifyGray', TA_JUSTIFY, 'ArialNarrow', 37.4, 40, gray,
        x_factor, y_factor)
    style_text_headers_small_white = create_paragraph_style(
        'HeadersSmallWhite', TA_LEFT, 'ArialNarrowBold', 38.7, 16, white,
        x_factor, y_factor)

    # Create a new PDF with ReportLab for the overlay
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Define date strings
    date_tomorrow = date_now + pd.Timedelta(days=1)
    str_date_today = date_now.strftime('%d/%m/%Y')
    str_date_today_fig = date_now.strftime('%Y-%m-%d')
    str_date_tomorrow = date_tomorrow.strftime('%d/%m/%Y')
    title_header = f'N°{idx:03} - 8 a.m. {str_date_today}'

    # Draw the title
    c.setFont("ArialNarrowBold", y_factor(46))
    c.setFillColor(white)
    c.drawString(x_factor(685), y_factor(2340), title_header)

    # Draw headers
    headers = [
        (f'Jornada: madrugada - {str_date_today}',
         896.6, 2285, 503.439, 36.9, style_text_headers_small_white),
        (f'Jornada: mañana (7 a.m. - 1 p.m.) {str_date_today}',
         740, 1920, 672.644, 36.9, style_text_headers_small_white),
        (f'Jornada: tarde (1 p.m. - 7 p.m.) {str_date_today}',
         350, 1510, 640, 36.9, style_text_headers_small_white),
        (f'Jornada: noche (7 p.m. - 1 a.m.) {str_date_today}',
         765, 1112, 680, 36.9, style_text_headers_small_white),
        (f'Jornada: madrugada (1 a.m. - 7 a.m.) {str_date_tomorrow}',
         260, 718, 750, 36.9, style_text_headers_small_white)
    ]

    for text, x, y, width, height, style in headers:
        paragraph = Paragraph(text, style)
        draw_paragraph_centered(paragraph, c, x, y, width,
                                height, x_factor, y_factor)

    # Paths
    path_txt_temp = os.path.join(
        dir_sama, 'report_lab', 'txt_boletin', f'{report}', '')
    # -------------------------------------------------------------------------
    # # Observed conditions
    # -------------------------------------------------------------------------
    draw_text_from_file(f'{path_txt_temp}0.obs_goes.txt', c,
                        657.970, 1956.384, 760.212, 291.126, style_text_gray,
                        x_factor, y_factor)

    draw_image_from_path(f'{dir_figures}{str_date_today_fig}_vis_goes.png',
                         c, 333.454, 1946.857, 317.267, 309.630,
                         x_factor, y_factor)

    draw_image_from_path(f'{dir_figures}{str_date_today_fig}_temp_goesvertical.png',
                         c, 13.333, 1930.983, 319.999, 325.239, x_factor, y_factor)

    # -------------------------------------------------------------------------
    # Forecasts
    # --------------------------------------------------------------------------
    forecast_data = [
        (f'{path_txt_temp}1.manana.txt',
            21.566, 1534.5, 980.224, 342.513, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_manana.png',
            1000, 1490, 411.581, 399.999),

        (f'{path_txt_temp}2.tarde.txt',
            437.6, 1145, 977.982, 330.052, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_tarde.png',
            20, 1085, 411.581, 399.999),

        (f'{path_txt_temp}3.noche.txt',
            21.566, 750, 977.945, 329.644, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_noche.png',
            1000, 686.585, 411.581, 399.999),

        (f'{path_txt_temp}4.madrugada.txt',
            436.783, 326.451, 969.454, 352.508, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_madrugada.png',
            20, 293.650, 411.581, 399.999)
    ]

    for txt_path, x_txt, y_txt, w_txt, h_txt, style, \
            img_path, x_img, y_img, w_img, h_img in forecast_data:
        draw_text_from_file(txt_path, c, x_txt, y_txt, w_txt,
                            h_txt, style, x_factor, y_factor)
        draw_image_from_path(img_path, c, x_img, y_img,
                             w_img, h_img, x_factor, y_factor)

    c.save()
    packet.seek(0)

    # Merge overlay with existing PDF
    overlay_pdf = PdfReader(packet)
    existing_page.merge_page(overlay_pdf.pages[0])
    pdf_writer.add_page(existing_page)

    # Save the final PDF
    str_date_fileout = date_now.strftime('%Y%m%d')
    file_name_out = f'{idx:03}_BoletinMeteorologico_{str_date_fileout}_{report}_Vertical'
    output_path_pdf = os.path.join(path_out, f'{file_name_out}.pdf')

    with open(output_path_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"PDF created: {file_name_out}")

    # Convert to PNG using ImageMagick
    output_path_png = os.path.join(path_out, f'{file_name_out}.png')
    command = f'convert -density 300 {output_path_pdf} -quality 100 {output_path_png}'
    os.system(command)
    print(f"PNG created: {file_name_out}")


def report_horizontal_pm(date_now, idx, report, dir_report_lab, dir_sama,
                         dir_figures, path_out):
    # Load the existing PDF
    layout_file = f'{dir_report_lab}plantillas/Plant_SinTextoNiMapas_pm_horizontal.pdf'
    pdf_reader = PdfReader(layout_file)
    pdf_writer = PdfWriter()

    existing_page = pdf_reader.pages[0]
    page_width = existing_page.mediabox.width
    page_height = existing_page.mediabox.height

    # Define the size of the overlay PDF
    size_x, size_y = 1280, 720
    def x_factor(x): return x * page_width/size_x
    def y_factor(x): return x * page_height/size_y

    blue = Color(17/255, 35/255, 63/255, alpha=1)
    yellow = Color(255/255, 192/255, 0/255, alpha=1)
    gray = Color(89/255, 89/255, 89/255, alpha=1)

    path_fonts = f'{dir_report_lab}/fonts/'

    impact_font = path_fonts + 'impact.ttf'
    pdfmetrics.registerFont(TTFont('Impact', impact_font))

    arial_narrow_bold_font = path_fonts + 'arialnarrow_bold.ttf'
    pdfmetrics.registerFont(TTFont('ArialNarrowBold', arial_narrow_bold_font))

    arial_narrow_font = path_fonts + 'arialnarrow.ttf'
    pdfmetrics.registerFont(TTFont('ArialNarrow', arial_narrow_font))

    # Define styles (particular to the report)
    style_text_gray = create_paragraph_style(
        'JustifyGray', TA_JUSTIFY, 'ArialNarrow', 16, 20, gray,
        x_factor, y_factor)
    style_text_headers_small_white = create_paragraph_style(
        'HeadersSmallWhite', TA_LEFT, 'ArialNarrowBold', 17, 16, white,
        x_factor, y_factor)
    style_text_title_fig_obs = create_paragraph_style(
        'JustifyGray', TA_CENTER, 'ArialNarrow', 14, 16, gray,
        x_factor, y_factor)

    # Create a new PDF with ReportLab for the overlay
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Define date strings
    date_tomorrow = date_now + pd.Timedelta(days=1)
    str_date_today = date_now.strftime('%d/%m/%Y')
    str_date_today_fig = date_now.strftime('%Y-%m-%d')
    str_date_tomorrow = date_tomorrow.strftime('%d/%m/%Y')
    title_header = f'N°{idx:03} - 4 p.m. {str_date_today}'

    # Draw the title
    c.setFont("ArialNarrowBold", y_factor(26))
    c.setFillColor(white)
    c.drawString(x_factor(435), y_factor(587), title_header)

    # Draw headers
    headers = [
        (f'Jornada: noche (7 p.m. - 1 a.m.) {str_date_today}',
         555, 542.3, 300, 20, style_text_headers_small_white),
        (f'Jornada: madrugada (1 a.m. - 7 a.m.) {str_date_tomorrow}',
         955, 542.3, 320, 20, style_text_headers_small_white),
        (f'Jornada: mañana (7 a.m. - 1 p.m.) {str_date_tomorrow}',
         548, 303, 320, 20, style_text_headers_small_white),
        (f'Jornada: tarde (1 p.m. - 7 p.m.) {str_date_tomorrow}',
         995, 303, 280, 20, style_text_headers_small_white)
    ]

    for text, x, y, width, height, style in headers:
        paragraph = Paragraph(text, style)
        draw_paragraph_centered(paragraph, c, x, y, width,
                                height, x_factor, y_factor)

    # Paths
    path_txt_temp = os.path.join(
        dir_sama, 'report_lab', 'txt_boletin', f'{report}', '')
    
    # -------------------------------------------------------------------------
    # # Observed conditions
    # -------------------------------------------------------------------------
    draw_text_from_file(f'{path_txt_temp}0.obs_goes.txt', c,
                        13.533, 221, 397.268, 106.793, style_text_gray,
                        x_factor, y_factor)

    draw_image_from_path(f'{dir_figures}{str_date_today_fig}_vis_goes.png',
                         c, 13.716, 333.403, 179.599, 175.276, x_factor, y_factor)

    draw_image_from_path(f'{dir_figures}{str_date_today_fig}_precipitation_gpm.png',
                         c, 193.333, 327.975, 186.666, 178.693, x_factor, y_factor)

    # Draw white rectangles to cover the original title of the figuress
    draw_rectangle(c, 28.123, 497.454, 163.667, 24.267,  x_factor, y_factor)
    draw_rectangle(c, 214.128, 497.730, 165.808, 24.267,  x_factor, y_factor)

    # Draw the Custume Titles over the figures
    titles_fig_obs = [
        ('Canal visible - GOES-(East)',
         28.123, 497.454, 163.667, 24.267, style_text_title_fig_obs),
        ('Prec. acumulada día anterior',
         214.128, 497.730, 165.808, 24.267, style_text_title_fig_obs)
    ]
    for text, x, y, width, height, style in titles_fig_obs:
        paragraph = Paragraph(text, style)
        draw_paragraph_centered(paragraph, c, x, y, width,
                                height, x_factor, y_factor)

    # -------------------------------------------------------------------------
    # Forecasts
    # --------------------------------------------------------------------------
    forecast_data = [
        (f'{path_txt_temp}1.noche.txt', 615, 340, 224, 185, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_noche.png',
         426.666, 342.667, 185.211, 185),

        (f'{path_txt_temp}2.madrugada.txt', 1044, 339, 224, 185, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_madrugada.png',
         853.332, 342.667, 185.211, 185),

        (f'{path_txt_temp}3.manana.txt', 617, 96, 224, 185, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_manana.png',
         426.666, 102.668, 185.211, 185),

        (f'{path_txt_temp}4.tarde.txt', 1044, 96, 224, 185, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_tarde.png',
         853.332, 102.668, 185.211, 185)
    ]

    for txt_path, x_txt, y_txt, w_txt, h_txt, style, \
            img_path, x_img, y_img, w_img, h_img in forecast_data:
        draw_text_from_file(txt_path, c, x_txt, y_txt, w_txt,
                            h_txt, style, x_factor, y_factor)
        draw_image_from_path(img_path, c, x_img, y_img,
                             w_img, h_img, x_factor, y_factor)

    c.save()
    packet.seek(0)

    # Merge overlay with existing PDF
    overlay_pdf = PdfReader(packet)
    existing_page.merge_page(overlay_pdf.pages[0])
    pdf_writer.add_page(existing_page)

    # Save the final PDF
    str_date_fileout = date_now.strftime('%Y%m%d')
    file_name_out = f'{idx:03}_BoletinMeteorologico_{str_date_fileout}_{report}_Diaria'
    output_path_pdf = os.path.join(path_out, f'{file_name_out}.pdf')

    with open(output_path_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"PDF created: {file_name_out}")

    # Convert to PNG using ImageMagick
    output_path_png = os.path.join(path_out, f'{file_name_out}.png')
    command = f'convert -density 300 {output_path_pdf} -quality 100 {output_path_png}'
    os.system(command)
    print(f"PNG created: {file_name_out}")


def report_vertical_pm(date_now, idx, report, dir_report_lab, dir_sama,
                       dir_figures, path_out):
    # Load the existing PDF
    layout_file = f'{dir_report_lab}plantillas/Plant_SinTextoNiMapas_pm_vertical.pdf'
    pdf_reader = PdfReader(layout_file)
    pdf_writer = PdfWriter()

    existing_page = pdf_reader.pages[0]
    page_width = existing_page.mediabox.width
    page_height = existing_page.mediabox.height

    # Define the size of the overlay PDF
    size_x, size_y = 1440, 2560
    def x_factor(x): return x * page_width/size_x
    def y_factor(x): return x * page_height/size_y

    blue = Color(17/255, 35/255, 63/255, alpha=1)
    yellow = Color(255/255, 192/255, 0/255, alpha=1)
    gray = Color(89/255, 89/255, 89/255, alpha=1)

    path_fonts = f'{dir_report_lab}/fonts/'

    impact_font = path_fonts + 'impact.ttf'
    pdfmetrics.registerFont(TTFont('Impact', impact_font))

    arial_narrow_bold_font = path_fonts + 'arialnarrow_bold.ttf'
    pdfmetrics.registerFont(TTFont('ArialNarrowBold', arial_narrow_bold_font))

    arial_narrow_font = path_fonts + 'arialnarrow.ttf'
    pdfmetrics.registerFont(TTFont('ArialNarrow', arial_narrow_font))

    # Define styles (particular to the report)
    style_text_gray = create_paragraph_style(
        'JustifyGray', TA_JUSTIFY, 'ArialNarrow', 37.4, 40, gray,
        x_factor, y_factor)
    style_text_headers_small_white = create_paragraph_style(
        'HeadersSmallWhite', TA_LEFT, 'ArialNarrowBold', 38.7, 16, white,
        x_factor, y_factor)
    style_text_title_fig_obs = create_paragraph_style(
        'JustifyGray', TA_CENTER, 'ArialNarrow', 16, 16, gray,
        x_factor, y_factor)

    # Create a new PDF with ReportLab for the overlay
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Define date strings
    date_tomorrow = date_now + pd.Timedelta(days=1)
    str_date_today = date_now.strftime('%d/%m/%Y')
    str_date_today_fig = date_now.strftime('%Y-%m-%d')
    str_date_tomorrow = date_tomorrow.strftime('%d/%m/%Y')
    title_header = f'N°{idx:03} - 4 p.m. {str_date_today}'

    # Draw the title
    c.setFont("ArialNarrowBold", y_factor(46))
    c.setFillColor(white)
    c.drawString(x_factor(685), y_factor(2340), title_header)

    # Draw headers
    headers = [
        (f'Jornada: noche (7 p.m. - 1 a.m.) {str_date_today}',
         755, 1920, 680, 36.9, style_text_headers_small_white),
        (f'Jornada: madrugada (1 a.m. - 7 a.m.) {str_date_tomorrow}',
         270, 1510, 750, 36.9, style_text_headers_small_white),
        (f'Jornada: mañana (7 a.m. - 1 p.m.) {str_date_tomorrow}',
         735, 1110, 672.644, 36.9, style_text_headers_small_white),
        (f'Jornada: tarde (1 p.m. - 7 p.m.) {str_date_tomorrow}',
         360, 718, 640, 36.9, style_text_headers_small_white)
    ]

    for text, x, y, width, height, style in headers:
        paragraph = Paragraph(text, style)
        draw_paragraph_centered(paragraph, c, x, y, width,
                                height, x_factor, y_factor)

    # Paths
    path_txt_temp = os.path.join(
        dir_sama, 'report_lab', 'txt_boletin', f'{report}', '')
    # -------------------------------------------------------------------------
    # # Observed conditions
    # -------------------------------------------------------------------------
    draw_text_from_file(f'{path_txt_temp}0.obs_goes.txt', c,
                        691.154, 1953, 724.265, 296, style_text_gray,
                        x_factor, y_factor)

    draw_image_from_path(f'{dir_figures}{str_date_today_fig}_vis_goes.png',
                         c, 6.667, 1953.335, 307.398, 299.999,
                         x_factor, y_factor)
    
    draw_image_from_path(f'{dir_figures}{str_date_today_fig}_precipitation_gpm.png',
                         c, 313.333, 1946.668, 320.351, 306.666, x_factor, y_factor)

    # Draw white rectangles to cover the original title of the figuress
    draw_rectangle(c, 39.695, 2232.140, 260.008, 23.258,  x_factor, y_factor)
    draw_rectangle(c, 350, 2240, 280, 16.5,  x_factor, y_factor)

    # Draw the Custume Titles over the figures
    titles_fig_obs = [
        ('Canal visible - GOES-(East)',
         39.695, 2232.140, 260.008, 23.258, style_text_title_fig_obs),
        ('Precipitación acumulada día anterior',
         350, 2240, 295, 16.5, style_text_title_fig_obs)
    ]
    for text, x, y, width, height, style in titles_fig_obs:
        paragraph = Paragraph(text, style)
        draw_paragraph_centered(paragraph, c, x, y, width,
                                height, x_factor, y_factor)

    # -------------------------------------------------------------------------
    # Forecasts
    # --------------------------------------------------------------------------
    forecast_data = [
        (f'{path_txt_temp}1.noche.txt',
            21.566, 1548, 977.683, 338.479, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_noche.png',
            1000, 1490, 411.581, 399.999),

        (f'{path_txt_temp}2.madrugada.txt',
            437.6, 1145, 977.982, 330.052, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_madrugada.png',
            20, 1085, 411.581, 399.999),

        (f'{path_txt_temp}3.manana.txt',
            21.566, 750, 977.945, 329.644, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_manana.png',
            1000, 686.585, 411.581, 399.999),

        (f'{path_txt_temp}4.tarde.txt',
            436.783, 326.451, 969.454, 352.508, style_text_gray,
         f'{dir_figures}{str_date_today_fig}_precip_ens_tarde.png',
            20, 293.650, 411.581, 399.999)
    ]

    for txt_path, x_txt, y_txt, w_txt, h_txt, style, \
            img_path, x_img, y_img, w_img, h_img in forecast_data:
        draw_text_from_file(txt_path, c, x_txt, y_txt, w_txt,
                            h_txt, style, x_factor, y_factor)
        draw_image_from_path(img_path, c, x_img, y_img,
                             w_img, h_img, x_factor, y_factor)

    c.save()
    packet.seek(0)

    # Merge overlay with existing PDF
    overlay_pdf = PdfReader(packet)
    existing_page.merge_page(overlay_pdf.pages[0])
    pdf_writer.add_page(existing_page)

    # Save the final PDF
    str_date_fileout = date_now.strftime('%Y%m%d')
    file_name_out = f'{idx:03}_BoletinMeteorologico_{str_date_fileout}_{report}_Vertical'
    output_path_pdf = os.path.join(path_out, f'{file_name_out}.pdf')

    with open(output_path_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"PDF created: {file_name_out}")

    # Convert to PNG using ImageMagick
    output_path_png = os.path.join(path_out, f'{file_name_out}.png')
    command = f'convert -density 300 {output_path_pdf} -quality 100 {output_path_png}'
    os.system(command)
    print(f"PNG created: {file_name_out}")
