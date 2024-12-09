import flet as ft

BOLD = ft.FontWeight.BOLD
TEXT_COLOR = ft.Colors.ON_SURFACE
ACCENT2_COLOR = ft.Colors.PRIMARY 
BACKGROUND_COLOR = ft.Colors.SURFACE 
CONTAINER_COLOR = ft.Colors.PRIMARY_CONTAINER
ROOTPATH = './assets'#'./_internal/assets'#'./assets'

# make colours constants
GOLD = '#B49455'
BOLD = ft.FontWeight.BOLD

defualt_theme = {
    'accent': '#E2746D', 
    "text": 'black', #'black'
    "background": '#C6E2FF', #'#C6E2FF'#C6E2FF'#"#ECF1F6"
    'container': 'white',
}
sleek_blue_theme = {
    'accent': '#1E88E5',  # Strong, vibrant blue accent
    'text': '#1A1A1A',  # Almost black text for contrast
    'background': '#E3F2FD',  # Light blue background for a modern, cool look
    'container': '#FFFFFF',  # White container for strong contrast with the background
}
forest_green_theme = {
    'accent': '#388E3C',  # Deep forest green accent
    'text': '#2D2D2D',  # Dark grey for readable text
    'background': '#E8F5E9',  # Light greenish background for a soft, natural feel
    'container': '#FFFFFF',  # White container to provide contrast with the background
}
new_teal_theme = {
    'accent': '#00796B',  # Muted teal for a calm accent
    'text': '#004D40',  # Darker teal for a cohesive text color
    'background': '#E0F2F1',  # Light, soft teal background to match the accent
    'container': '#FFFFFF',  # White container for a clean look
}
new_red_theme = {
    'accent': '#D32F2F',  # Slightly darker red for a less harsh accent
    'text': '#37474F',  # Blue-grey text to complement the red accent
    'background': '#FAFAFA',  # Very light grey background to soften the look
    'container': '#CFD8DC',  # Light blue-grey for a subtle container color
}
soft_lavender_theme = {
    'accent': '#9575CD',  # Soft lavender for a calm, caring vibe
    'text': '#4A4A4A',  # Medium-dark grey for a softer, non-harsh text
    'background': '#F3E5F5',  # Very light lavender for a nurturing and gentle environment
    'container': '#FFFFFF',  # White for clarity and professionalism
}
professional_grey_blue_theme = {
    'accent': '#5C6BC0',  # Soft indigo for a modern, trustworthy accent
    'text': '#1A1A1A',  # Almost black text for strong readability
    'background': '#F0F4C3',  # Very light grey-blue for a professional, clean feel
    'container': '#FFFFFF',  # White container to maintain a clean and modern look
}
new_default_theme = {
    'accent': '#E57373',  # Soft coral-red for a friendly accent
    'text': '#212121',  # Dark grey text for good readability
    'background': '#D0E3FF',  # Slightly darker blue to contrast with the container
    'container': '#FFFFFF',  # White container for strong contrast with the background
}

THEMES_LIST = [
    defualt_theme,
    sleek_blue_theme,
    forest_green_theme,
    new_teal_theme,
    new_red_theme,
    soft_lavender_theme,
    professional_grey_blue_theme,
    new_default_theme
]
# eight maximum