import flet as ft
from src.config import get_api_key
from src.api.weather_client import WeatherClient

def main(page: ft.Page):
    page.title = "Meteo Dashboard"
    page.padding = 0
    
    # MATERIAL 3 THEME - Profesjonalne "przejrzyste" i miękkie kolory bez oślepiających kontrastów
    # Automatycznie wygeneruje paletę na podstawie nasiona (niebiesko-szary)
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.BLUE_GREY,
        font_family="Inter",
        visual_density=ft.ThemeVisualDensity.COMFORTABLE
    )
    
    saved_theme = page.client_storage.get("theme")
    if saved_theme == "light":
        page.theme_mode = ft.ThemeMode.LIGHT
    else:
        page.theme_mode = ft.ThemeMode.DARK

    page.fonts = {
        "Inter": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Regular.woff2",
        "InterBold": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Bold.woff2"
    }
    
    api_key = get_api_key()
    client = WeatherClient(api_key) if api_key else None

    progress_ring = ft.ProgressRing(visible=False)
    dashboard_content = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
    
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.client_storage.set("theme", "light" if page.theme_mode == ft.ThemeMode.LIGHT else "dark")
        page.update()

    def get_icon_url(icon_code):
        return f"https://openweathermap.org/img/wn/{icon_code}@4x.png"

    last_query = ""

    def load_weather(query):
        nonlocal last_query
        last_query = query
        dashboard_content.controls.clear()
        
        if not client:
            dashboard_content.controls.append(ft.Text("Brak klucza API w pliku .env", color=ft.colors.ERROR))
            page.update()
            return
            
        progress_ring.visible = True
        page.update()
        
        try:
            data = client.get_weather(query)
            
            current_section = ft.Container(
                content=ft.Column([
                    ft.Text(f"{data.city}, {data.country}", size=32, font_family="InterBold", color=ft.colors.ON_BACKGROUND),
                    ft.Row([
                        ft.Image(src=get_icon_url(data.icon), width=120, height=120, fit=ft.ImageFit.CONTAIN),
                        ft.Text(f"{int(data.temperature)}°", size=96, font_family="InterBold", color=ft.colors.ON_BACKGROUND),
                    ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Text(data.description.capitalize(), size=24, color=ft.colors.ON_BACKGROUND),
                    ft.Text(f"Min: {int(data.temperature_min)}° • Max: {int(data.temperature_max)}°", size=16, color=ft.colors.ON_SURFACE_VARIANT)
                ]),
                padding=20
            )
            
            hourly_row = ft.Row(scroll=ft.ScrollMode.ADAPTIVE, spacing=15)
            for hr in data.hourly_forecast:
                hourly_row.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(hr['time'], size=14, color=ft.colors.ON_SURFACE_VARIANT),
                            ft.Image(src=get_icon_url(hr['icon']), width=50, height=50),
                            ft.Text(f"{int(hr['temp'])}°", size=20, font_family="InterBold", color=ft.colors.ON_SURFACE),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        padding=20,
                        border_radius=20
                    )
                )
                
            hourly_section = ft.Column([
                ft.Text("Prognoza Godzinowa", size=20, font_family="InterBold", color=ft.colors.ON_BACKGROUND),
                hourly_row
            ], spacing=10)

            daily_row = ft.Row(scroll=ft.ScrollMode.ADAPTIVE, spacing=15)
            for day in data.daily_forecast:
                daily_row.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(day['day_name'], size=16, font_family="InterBold", color=ft.colors.ON_SURFACE),
                            ft.Text(day['date'], size=12, color=ft.colors.ON_SURFACE_VARIANT),
                            ft.Image(src=get_icon_url(day['icon']), width=60, height=60),
                            ft.Text(f"{int(day['temp_max'])}°", size=18, font_family="InterBold", color=ft.colors.ON_SURFACE),
                            ft.Text(f"{int(day['temp_min'])}°", size=14, color=ft.colors.ON_SURFACE_VARIANT),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        padding=20,
                        border_radius=20,
                        width=120
                    )
                )
                
            daily_section = ft.Column([
                ft.Text("Prognoza Dzienna", size=20, font_family="InterBold", color=ft.colors.ON_BACKGROUND),
                daily_row
            ], spacing=10)
            
            def create_detail_card(title, value, subtext):
                return ft.Container(
                    content=ft.Column([
                        ft.Text(title, size=16, color=ft.colors.ON_SURFACE_VARIANT),
                        ft.Text(value, size=32, font_family="InterBold", color=ft.colors.ON_SURFACE),
                        ft.Text(subtext, size=14, color=ft.colors.ON_SURFACE_VARIANT)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    padding=30,
                    border_radius=20,
                )

            details_grid = ft.ResponsiveRow([
                ft.Column(col={"sm": 12, "md": 6, "xl": 3}, controls=[create_detail_card("Opady", f"{data.precipitation_sum} mm", "Suma dzienna")]),
                ft.Column(col={"sm": 12, "md": 6, "xl": 3}, controls=[create_detail_card("Wiatr", f"{data.wind_speed} m/s", f"Kierunek: {data.wind_deg}°")]),
                ft.Column(col={"sm": 12, "md": 6, "xl": 3}, controls=[create_detail_card("Wschód / Zachód", data.sunrise_str, f"Zachód: {data.sunset_str}")]),
                ft.Column(col={"sm": 12, "md": 6, "xl": 3}, controls=[create_detail_card("Indeks UV", str(int(data.uv_index)), "Wg. API")]),
            ])
            
            dashboard_content.controls.extend([
                current_section,
                ft.Divider(color=ft.colors.TRANSPARENT, height=10),
                hourly_section,
                ft.Divider(color=ft.colors.TRANSPARENT, height=10),
                daily_section,
                ft.Divider(color=ft.colors.TRANSPARENT, height=10),
                ft.Text("Szczegóły Dzisiaj", size=20, font_family="InterBold", color=ft.colors.ON_BACKGROUND),
                details_grid
            ])
            
        except Exception as e:
            dashboard_content.controls.append(ft.Text(f"Błąd wyszukiwania: {str(e)}", color=ft.colors.ERROR))
            
        progress_ring.visible = False
        page.update()

    def search_clicked(e):
        if search_field.value:
            load_weather(search_field.value)

    search_field = ft.TextField(
        hint_text="Szukaj miasta...", 
        border_radius=30, 
        prefix_icon=ft.icons.SEARCH,
        on_submit=search_clicked,
        bgcolor=ft.colors.SURFACE,
        color=ft.colors.ON_SURFACE
    )
    
    sidebar_content = ft.Column([
        ft.Row([
            ft.Icon(ft.icons.CLOUD_CIRCLE, size=40, color=ft.colors.PRIMARY),
            ft.Text("Meteo", size=28, font_family="InterBold", color=ft.colors.ON_SURFACE)
        ], alignment=ft.MainAxisAlignment.START),
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        search_field,
        ft.ElevatedButton("Sprawdź pogodę", on_click=search_clicked, width=250, height=50, 
                          style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25), bgcolor=ft.colors.PRIMARY, color=ft.colors.ON_PRIMARY)),
        progress_ring,
        ft.Container(expand=True), 
        ft.Divider(),
        ft.Row([
            ft.Icon(ft.icons.DARK_MODE, color=ft.colors.ON_SURFACE),
            ft.Text("Ciemny motyw", color=ft.colors.ON_SURFACE),
            ft.Switch(value=(page.theme_mode == ft.ThemeMode.DARK), on_change=toggle_theme)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    ], expand=True)

    sidebar = ft.Container(
        content=sidebar_content,
        width=300,
        bgcolor=ft.colors.SURFACE,
        padding=30,
        border_radius=ft.border_radius.only(top_right=30, bottom_right=30)
    )

    main_area = ft.Container(
        content=dashboard_content,
        expand=True,
        bgcolor=ft.colors.BACKGROUND,
        padding=40
    )

    # ---------------- TUTORIAL SHOWCASE (Wyspa animowana) ----------------
    tutorial_steps = [
        {"text": "Witaj w aplikacji pogoda!\n\nTo jest Twój panel boczny. Wpisz tutaj nazwę miasta i wciśnij enter lub przycisk pod spodem, by sprawdzić prognozę z całego świata.", "top": 140, "left": 310},
        {"text": "Krok 2:\n\nTo jest główny Dashboard. Pigułki z dniami tygodnia oraz kartki statystyk możesz swobodnie przewijać myszką na boki.\nKarty reagują elastycznie na rozmiar okna (Spróbuj go zmienić!).", "top": 150, "left": 600},
        {"text": "Krok 3:\n\nAplikacja obsługuje perfekcyjne, miękkie dla oczu motywy.\nZmień motyw przełącznikiem obok i zobacz jak odcienie gładko dopasowują się do siebie. Koniec tutoriala!", "bottom": 80, "left": 310}
    ]
    current_step = 0
    
    showcase_text = ft.Text(tutorial_steps[0]["text"], size=16, color=ft.colors.ON_PRIMARY_CONTAINER)
    
    def next_tutorial_step(e):
        nonlocal current_step
        current_step += 1
        if current_step < len(tutorial_steps):
            # Animacja wyspy do nowego miejsca
            step = tutorial_steps[current_step]
            showcase_island.top = step.get("top")
            showcase_island.left = step.get("left")
            showcase_island.bottom = step.get("bottom")
            showcase_text.value = step["text"]
            
            # Jeśli to ostatni krok
            if current_step == len(tutorial_steps) - 1:
                next_btn.text = "ZAKOŃCZ"
                
            page.update()
        else:
            # Zakończenie tutoriala - ukrywamy go i zapisujemy by nigdy nie wrócił
            showcase_island.visible = False
            page.client_storage.set("tutorial_completed", True)
            page.update()

    next_btn = ft.ElevatedButton("DALEJ ➔", on_click=next_tutorial_step, 
                                 style=ft.ButtonStyle(bgcolor=ft.colors.PRIMARY, color=ft.colors.ON_PRIMARY))
    
    # Sama animowana "Wyspa" Tutorialu
    showcase_island = ft.Container(
        content=ft.Column([
            ft.Icon(ft.icons.INFO, color=ft.colors.PRIMARY, size=32),
            showcase_text,
            ft.Container(height=10),
            ft.Row([next_btn], alignment=ft.MainAxisAlignment.END)
        ]),
        bgcolor=ft.colors.PRIMARY_CONTAINER,
        width=350,
        padding=25,
        border_radius=20,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.colors.SHADOW),
        top=tutorial_steps[0].get("top"),
        left=tutorial_steps[0].get("left"),
        bottom=tutorial_steps[0].get("bottom"),
        animate_position=ft.animation.Animation(500, ft.AnimationCurve.DECELERATE),
        visible=not page.client_storage.get("tutorial_completed") # Zawsze włączony dla nowych, zepsuty dla weteranów
    )

    def reset_tutorial(e):
        page.client_storage.remove("tutorial_completed")
        nonlocal current_step
        current_step = 0
        step = tutorial_steps[0]
        showcase_island.top = step.get("top")
        showcase_island.left = step.get("left")
        showcase_island.bottom = step.get("bottom")
        showcase_text.value = step["text"]
        next_btn.text = "DALEJ ➔"
        showcase_island.visible = True
        page.update()

    # Dodanie przycisku resetu do sidebaru
    sidebar_content.controls.append(
        ft.TextButton("Resetuj samouczek", on_click=reset_tutorial, style=ft.ButtonStyle(color=ft.colors.OUTLINE))
    )

    # ---------------- BAZOWY UKŁAD (STACK = Warstwy) ----------------
    page.add(
        ft.Stack(
            [
                ft.Row([sidebar, main_area], expand=True, spacing=0),
                showcase_island
            ],
            expand=True
        )
    )

    load_weather("Warszawa")
