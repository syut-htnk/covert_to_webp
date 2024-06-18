import flet as ft
from PIL import Image
import os

def convert_to_webp(image_path, quality):
    try:
        with Image.open(image_path) as img:
            output_path = os.path.splitext(image_path)[0] + ".webp"
            img.save(output_path, "WEBP", quality=quality)
            return f"Converted {image_path} to {output_path} with quality {quality}."
    except Exception as e:
        return f"Failed to convert {image_path}: {e}"

def main(page: ft.Page):
    version = "1.0.0a"
    page.window_width = 512
    page.window_height = 512 + 32
    page.title = "Image to WebP Converter"

    def pick_files_result(e: ft.FilePickerResultEvent):
        conversion_results.controls.clear()
        results = []
        if e.files:
            progress_bar.value = 0  
            total_files = len(e.files)
            progress_increment = 1 / total_files

            loading_message.value = "Loading..."
            loading_spinner.visible = True
            overlay_container.visible = True
            loading_message.update()
            loading_spinner.update()
            overlay_container.update()

            for file in e.files:
                file_path = file.path if hasattr(file, 'path') else file.name
                result = convert_to_webp(file_path, int(quality_slider.value))
                results.append(result)
                
                progress_bar.value += progress_increment
                progress_bar.update()

            selected_files.value = ", ".join(map(lambda f: f.name, e.files))
        else:
            selected_files.value = "terminated."
        
        selected_files.update()
        for result in results:
            conversion_results.controls.append(ft.Text(result))
        conversion_results.update()
        
        progress_bar.value = 1  
        progress_bar.update()

        loading_message.value = ""
        loading_spinner.visible = False
        overlay_container.visible = False
        loading_message.update()
        loading_spinner.update()
        overlay_container.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    conversion_results = ft.ListView(expand=True)  
    quality_label = ft.Text("Quality", style=ft.TextStyle(weight="bold"))
    quality_slider = ft.Slider(min=0, max=100, divisions=100, label="Quality: {value}", value=100)
    progress_label = ft.Text("Progress", style=ft.TextStyle(weight="bold"))
    progress_bar = ft.ProgressBar(width=400)
    author = ft.Text(f"by: Shuto Hatanaka | version: {version}", style=ft.TextStyle(weight="bold", size=10))

    loading_message = ft.Text("Loading...")
    loading_spinner = ft.ProgressRing(visible=False)
    
    overlay_container = ft.Container(
        content=ft.Column(
            [
                loading_spinner,
                loading_message,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        width=page.window_width,
        height=page.window_height,
        visible=False,
    )

    page.overlay.append(pick_files_dialog)
    page.overlay.append(overlay_container)

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=author,
                        alignment=ft.alignment.top_right,
                    ),
                    ft.Container(height=32),
                    ft.Row(
                        [
                            ft.Container(width=16),
                            ft.ElevatedButton(
                                "Pick files",
                                icon=ft.icons.UPLOAD_FILE,
                                on_click=lambda _: pick_files_dialog.pick_files(
                                    allow_multiple=True
                                ),
                            ),
                            selected_files,
                        ],
                    ),
                    ft.Container(height=32),
                    quality_label,
                    quality_slider,
                    ft.Container(height=32),
                    progress_label,
                    ft.Container(height=8),
                    ft.Container(
                        content=progress_bar,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=32),
                    ft.Container(
                        content=conversion_results,
                        alignment=ft.alignment.center,
                        height=100,
                    ),
                    ft.Container(height=8),
                ],
            ),
            alignment=ft.alignment.center,
        )
    )

ft.app(target=main)