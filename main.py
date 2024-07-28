from webbrowser import open as openurl
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from pypresence import Presence
from tkinter import messagebox
from customtkinter import *
import threading
import CTkCustom
import pystray
import time
import json
import os

RPC = None

appdata_dir = os.getenv('APPDATA')
folder_path = os.path.join(appdata_dir, 'CustomDiscordRPC')
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Load client ID
client_id_path = os.path.join(folder_path, 'client.json')
try:
    os.path.join(os.getenv('APPDATA'), 'CustomDiscordRPC')
    client_id_path = os.path.join(os.getenv('APPDATA'), 'CustomDiscordRPC', 'client.json')
    with open(client_id_path, 'r') as file:
        config = json.load(file)
        client_id = config['client_id']
        client_id_was_found = True
except FileNotFoundError:
    with open(client_id_path, 'w') as file:
        json.dump({"client_id": "1250118752217993267"}, file, indent=4)
        client_id_was_found = False
        client_id = "1250118752217993267"
except Exception as e:
    messagebox.showerror("ERROR OCCURED", f"{e}, file error, contact developer")
    client_id_was_found = False

# start presence
if client_id_was_found:
    try:
        RPC = Presence(client_id)
        RPC.connect()
    except Exception as e:
        messagebox.showerror("ERROR OCCURED", f"{e}")

def get_resource_path(relative_path):
    """ Get the absolute path to a resource"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def update_rpc():
    """Function to update rpc using data provided"""
    global RPC
    # Validate button URLs and labels
    if RPC is None:
        try:
            client_id_path = os.path.join(os.getenv('APPDATA'), 'CustomDiscordRPC', 'client.json')
            with open(client_id_path, 'r') as file:
                config = json.load(file)
                client_id = config['client_id']
                client_id_was_found = True
        except Exception as e:
            print("error with RPC")
    if rpc_buttons:
        filtered_buttons = []
        for button in rpc_buttons:
            if button.get('label') and button.get('url') and button['url'].startswith(('http://', 'https://')) and len(button['label']) > 2:
                filtered_buttons.append(button)
        if not filtered_buttons:
            filtered_buttons = None
    else:
        filtered_buttons = None
    
    try:
        RPC.update(
            details=rpc_details if rpc_details and len(rpc_details) > 2 else None,  # Title
            state=rpc_state if rpc_state and len(rpc_state) > 2 else None,  # Subtitle
            large_image=rpc_l_img if rpc_l_img and len(rpc_l_img) > 2 else None,  # Image key (must be uploaded in the Discord app)
            large_text=rpc_l_tx if rpc_l_tx and len(rpc_l_tx) > 2 else None,  # Hover text for the large image
            small_image=rpc_s_img if rpc_s_img and len(rpc_s_img) > 2 else None,  # Small image key (must be uploaded in the Discord app)
            small_text=rpc_s_tx if rpc_s_tx and len(rpc_s_tx) > 2 else None,  # Hover text for the small image
            buttons=filtered_buttons # Buttons
            )
    except AttributeError as ar:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        app.destroy()
        messagebox.showerror("ERROR OCCURED", f"error while trying to update discord RPC activity, please check if discord is running and you logged in{e}")
        raise Exception
        sys.exit()

def background_update_rpc():
    """Background process to update rpc every {update_time} seconds"""
    try:
        while True:
            update_rpc()
            time.sleep(update_time)
    except KeyboardInterrupt:
        print("Exiting...")

def create_dir():
    """Function to create directory where data wil be saved"""
    appdata_dir = os.getenv('APPDATA')
    
    if not appdata_dir:
        raise EnvironmentError("APPDATA environment variable not found.")
    global folder_path, file_path, clientid_path
    folder_path = os.path.join(appdata_dir, 'CustomDiscordRPC')
    file_path = os.path.join(folder_path, 'rpc.json')
    clientid_path = os.path.join(folder_path, 'client.json')
    
    os.makedirs(folder_path, exist_ok=True)
    
    initial_data = {
        "rpc_details": "",
        "rpc_state": "",
        "rpc_l_img": "",
        "rpc_l_tx":"",
        "rpc_s_img": "",
        "rpc_s_tx": "",
        "rpc_buttons": [
            {"label": "", "url": ""},
            {"label": "", "url": ""}
        ]
    }
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump(initial_data, file, indent=4)
    else:
        load_rpc_data()

def load_rpc_data():
    """Function to load rpc data if file exist"""
    appdata_dir = os.getenv('APPDATA')
    
    if not appdata_dir:
        raise EnvironmentError("APPDATA environment variable not found.")
    
    folder_path = os.path.join(appdata_dir, 'CustomDiscordRPC')
    file_path = os.path.join(folder_path, 'rpc.json')
    
    if not os.path.exists(file_path):
        messagebox.showerror("ERROR OCCURED", f"{file_path} does not exist")
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    global rpc_details, rpc_state, rpc_l_img, rpc_l_tx, rpc_s_img, rpc_s_tx, rpc_buttons
    rpc_details = data.get('rpc_details', None)
    rpc_state = data.get('rpc_state', None)
    rpc_l_img = data.get('rpc_l_img', None)
    rpc_l_tx = data.get('rpc_l_tx', None)
    rpc_s_img = data.get('rpc_s_img', None)
    rpc_s_tx = data.get('rpc_s_tx', None)
    rpc_buttons = data.get('rpc_buttons', None)

    return rpc_details, rpc_state, rpc_l_img, rpc_l_tx, rpc_s_img, rpc_s_tx, rpc_buttons

def write_variables():
    """Function to process user input from entry boxes"""
    global rpc_details, rpc_state, rpc_l_img, rpc_l_tx, rpc_s_img, rpc_s_tx, rpc_buttons

    rpc_details = details_entry.get() or None
    rpc_state = state_entry.get() or None

    rpc_l_img = large_image_entry.get_image_prompt() or None
    rpc_l_tx = large_image_entry.get_alt_text() or None
    rpc_s_img = small_image_entry.get_image_prompt() or None
    rpc_s_tx = small_image_entry.get_alt_text() or None

    rpc_buttons = [
        {"label": button1_label_entry.get() or None, "url": button1_url_entry.get() or None},
        {"label": button2_label_entry.get() or None, "url": button2_url_entry.get() or None}
    ]

    save_rpc_data()

def save_rpc_data():
    """Function to sort and save data to json file"""
    appdata_dir = os.getenv('APPDATA')
    
    if not appdata_dir:
        raise EnvironmentError("APPDATA environment variable not found.")
    
    folder_path = os.path.join(appdata_dir, 'CustomDiscordRPC')
    file_path = os.path.join(folder_path, 'rpc.json')

    data_to_save = {
        "rpc_details": rpc_details,
        "rpc_state": rpc_state,
        "rpc_l_img": rpc_l_img,
        "rpc_l_tx": rpc_l_tx,
        "rpc_s_img": rpc_s_img,
        "rpc_s_tx": rpc_s_tx,
        "rpc_buttons": rpc_buttons
    }

    filtered_data_to_save = {}

    for key, value in data_to_save.items():
        if value is not None:
            filtered_data_to_save[key] = value

    os.makedirs(folder_path, exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(filtered_data_to_save, file, indent=4)

def update_client_id():
    """Function to update client id"""
    global client_id
    if len(settings_client_id_entry.get().strip()) == 19:
        client_id_entry = {
            "client_id": settings_client_id_entry.get().strip()
            }
        with open(clientid_path, 'w') as f:
            json.dump(client_id_entry, f)
        client_id = settings_client_id_entry.get().strip()
    else:
        messagebox.showerror("ERROR OCCURED", "Invalid Client ID, please enter valid Client ID")

def github_link_(e):
    openurl("https://github.com/kitfc-dev")

def list_files_in_directory(directory):
    """List all files in the given directory."""
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return files
    except Exception as e:
        messagebox.showerror("ERROR OCCURED", "{e}, please check 'Themes' folder")
        return []
    
def change_theme(theme):
    theme_path = f"Themes/{theme}"
    try:
        if os.path.exists(theme_path):
            set_default_color_theme(theme_path)
            with open(os.path.join(folder_path, 'theme.json'), 'w') as theme_file:
                json.dump({"theme": theme_path, "theme_name": theme}, theme_file)
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            messagebox.showerror("ERROR OCCURED", "theme doesn't exist in 'Themes' folder")
    except Exception as e:
        print(f"Failed to change theme. Error: {e}")

def create_image(width, height, color1, color2): # created by chatgpt
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image

def on_show(icon, item):
    app.deiconify()
    icon.stop()

def on_exit(icon, item):
    icon.stop()
    app.quit()

def run_tray():
    icon = pystray.Icon("test_icon")
    image = create_image(64, 64, 'black', 'white')
    icon.icon = image
    icon.menu = pystray.Menu(item('Show', on_show), item('Exit', on_exit))
    icon.run()

def hide_to_tray():
    app.withdraw()
    tray_thread = threading.Thread(target=run_tray, daemon=True)
    tray_thread.start()


if __name__ == "__main__":
    update_time = 3
    create_dir()
    rpc_details, rpc_state, rpc_l_img, rpc_l_tx, rpc_s_img, rpc_s_tx, rpc_buttons = load_rpc_data()

    app = CTk()
    theme_file_path = os.path.join(folder_path, 'theme.json')
    if os.path.exists(theme_file_path):
        with open(theme_file_path, 'r') as theme_file:
            data = json.load(theme_file)
            set_default_color_theme(data.get("theme", None))
            current_theme_nm = data.get("theme_name", None).replace(".json", "")
    else:
        default_theme = "Themes/Blue.json"
        set_default_color_theme(default_theme)
        with open(theme_file_path, 'w') as theme_file:
            json.dump({"theme": default_theme, "theme_name": "Blue"}, theme_file, indent=4)
        current_theme_nm = "Blue"
    app.geometry("500x400")
    app.title("Discord-RPC")
    app.resizable(False, False)


    # Create tabs
    tabview = CTkTabview(master=app)
    tabview.pack(pady=1, padx=1, fill="both", expand=True)
    main_tab = tabview.add("RPC")
    settings_tab = tabview.add("Settings")
    
    app.protocol("WM_DELETE_WINDOW", hide_to_tray)

    # TIP
    tip_label = CTkLabel(master=main_tab, text=f"TIP: enter 3 backspaces where you dont want to have text \n(example: write '   ' in title to dont have title in activity)", font=("Arial", 8))
    tip_label.place(relx=0.5, rely=0.07, anchor="center")

    # ENTRIES
    details_entry = CTkEntry(master=main_tab, placeholder_text="Title for Activity", width=300, )
    details_entry.place(relx=0.5, rely=0.15, anchor="center")

    state_entry = CTkEntry(master=main_tab, placeholder_text="Subtitle for Activity", width=300, )
    state_entry.place(relx=0.5, rely=0.25, anchor="center")

    # IMAGE ENTRIES
    large_image_entry = CTkCustom.AnimatedCheckboxEntry(master=main_tab, checkbox_text="Large Image", entry1_text="promt", entry2_text="alt text")
    large_image_entry.place(relx=0.2, rely=0.45, anchor="center")

    small_image_entry = CTkCustom.AnimatedCheckboxEntry(master=main_tab, checkbox_text="Small Image", entry1_text="promt", entry2_text="alt text")
    small_image_entry.place(relx=0.2, rely=0.75, anchor="center")

    # BUTTONS
    button1_label_entry = CTkEntry(master=main_tab, placeholder_text="Button 1 for Activity", width=150)
    button1_label_entry.place(relx=0.7, rely=0.45, anchor="center")

    button1_url_entry = CTkEntry(master=main_tab, placeholder_text="Button 1 URL for Activity", width=150)
    button1_url_entry.place(relx=0.7, rely=0.55, anchor="center")

    button2_label_entry = CTkEntry(master=main_tab, placeholder_text="Button 2 for Activity", width=150)
    button2_label_entry.place(relx=0.7, rely=0.65, anchor="center")

    button2_url_entry = CTkEntry(master=main_tab, placeholder_text="Button 2 URL for Activity", width=150)
    button2_url_entry.place(relx=0.7, rely=0.75, anchor="center")

    apply_button = CTkButton(master=main_tab, text='Apply Changes', command=write_variables)
    apply_button.place(relx=0.5, rely=0.9, anchor="center")

    # SETTINGS
    settings_client_id_entry = CTkEntry(master=settings_tab, placeholder_text='1250118752217993267', width=170)
    settings_client_id_entry.place(relx=0.4, rely=0.1, anchor='e')

    settings_client_id_button = CTkButton(master=settings_tab, text='Apply Client ID', command=update_client_id)
    settings_client_id_button.place(relx=0.7, rely=0.1, anchor='w')

    theme_combo_box = CTkComboBox(master=settings_tab, values=list_files_in_directory("Themes"), command=change_theme)
    theme_combo_box.place(relx=0.192, rely=0.3, anchor="center")
    
    theme_current_name = CTkLabel(master=settings_tab, text=f"current theme: {current_theme_nm}")
    theme_current_name.place(relx=0.192, rely=0.4, anchor="center")

    hide_to_tray_button = CTkButton(master=settings_tab, text='Hide to Tray', command=hide_to_tray)
    hide_to_tray_button.place(relx=0.192, rely=0.5, anchor="center")

    github_link = CTkLabel(master=settings_tab, text=f'DISCORD-RPC by KITFC-dev (Click to check GitHub)', image=CTkImage(dark_image=Image.open("Image/github_icon.png"), light_image=Image.open("Image/github_icon.png")), cursor="hand2", compound="left")
    github_link.bind("<Button-1>", github_link_)
    github_link.place(relx=0.5, rely=0.95, anchor="center")
    
    background_update = threading.Thread(target=background_update_rpc, daemon=True)
    background_update.start()
    
    # load json entry
    try:
        details_entry.insert(0, f"{rpc_details}")
        state_entry.insert(0, f"{rpc_state}")
        button1_label_entry.insert(0, f"{rpc_buttons[0]['label']}")
        button1_url_entry.insert(0, f"{rpc_buttons[0]['url']}")
        button2_label_entry.insert(0, f"{rpc_buttons[1]['label']}")
        button2_url_entry.insert(0, f"{rpc_buttons[1]['url']}")
    except Exception as e:
        messagebox.showerror("ERROR OCCURED", "Error while loading RPC data")
    if client_id_was_found:
        settings_client_id_entry.insert(0, f"{client_id}")

    app.mainloop()
