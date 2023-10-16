import tkinter as tk
import time
from frames import home_frame, user_frame, manager_frame
from handle_code import x_handle
is_Login = False 
import os
from tkinter import ttk
def create_right_frame(color):
    right_frame = tk.Frame(container)
    right_frame.config(bg=color)
    return right_frame

def show_frame(frame_to_show):
    for frame in right_frames:
        if frame != frame_to_show:
            frame.pack_forget()
    frame_to_show.pack(side="right", fill="both", expand=True)
    return frame_to_show

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
def minimize_window():
    root.iconify()
def on_home_click():
    if is_Login != True:
        show_login_frame()
    else:
        global current_right_frame
        current_right_frame = show_frame(home_right_frame)
        update_button_state()

def on_user_click():
    if is_Login != True:
        show_login_frame()
    else:
        global current_right_frame
        current_right_frame = show_frame(user_right_frame)
        update_button_state()

def on_manager_click():
    if is_Login != True:
        show_login_frame()
    else:
        global current_right_frame
        current_right_frame = show_frame(manager_right_frame)
        update_button_state()

def login(event=None):
    # Lấy tên người dùng và mật khẩu từ các ô nhập
    global is_Login
    login_result.config(text="Đang đăng nhập...")
    username = username_entry.get()
    password = password_entry.get()
    # Kiểm tra đăng nhập
    if x_handle.Login(username,password)==True:
        login_window.update_idletasks()  # Cập nhật giao diện ngay lập tức
        login_result.config(text="Đăng nhập thành công")
        login_window.grab_release()  # Cho phép tương tác với cửa sổ khác
        login_window.destroy()  # Đóng cửa sổ login_frame
        # Thay đổi nút "Login" thành tên người dùng và nút "Logout"
        login_button.config(text=f"{username} (Logout)", command=logout)
        is_Login = True
        if save_account_var.get() == 1:
            with open("account.txt", 'w') as file:
                file.write('\n'.join([username, password]))
    else:
        login_result.config(text="Đăng nhập thất bại")

def close_login_frame(event=None):
    login_window.grab_release()  # Cho phép tương tác với cửa sổ khác
    login_window.destroy()  # Đóng cửa sổ login_frame

def show_login_frame():
    global login_window
    login_window = tk.Toplevel(root)
    login_window.title("Đăng nhập")
    center_window(login_window, 400, 180)

    login_frame = ttk.Frame(login_window)
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Tạo các thành phần đăng nhập
    global username_entry, password_entry, login_result, show_password_var, save_account_var
    username_label = ttk.Label(login_frame, text="Tài khoản:")
    username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    username_entry = ttk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=5)
    username_entry.focus_set()  # Thiết lập focus vào username_entry

    password_label = ttk.Label(login_frame, text="Mật khẩu:")
    password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    password_entry = ttk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    password_entry.bind("<Return>", login)  # Bắt sự kiện Enter cho password_entry
    
    show_password_var = tk.IntVar()
    show_password_checkbox = ttk.Checkbutton(login_frame, text="Hiện mật khẩu", variable=show_password_var, command=toggle_show_password)
    show_password_checkbox.grid(row=2, columnspan=2, padx=10, pady=5, sticky="w")
    save_account_var = tk.IntVar()
    save_account_checkbox = ttk.Checkbutton(login_frame, text="Lưu tài khoản", variable=save_account_var)
    save_account_checkbox.grid(row=3, columnspan=2, padx=10, pady=5, sticky="w")

    login_button = ttk.Button(login_frame, text="Đăng nhập X", command=login,width=35)
    login_button.grid(row=4, columnspan=2, padx=10, pady=10)

    login_result = ttk.Label(login_frame, text="")
    login_result.grid(row=5, columnspan=2, padx=10, pady=5)

    login_window.grab_set()  # Chặn tương tác với cửa sổ khác

    # Bắt sự kiện nhấn Enter và Esc
    username_entry.bind("<Return>", login)
    login_window.bind("<Escape>", close_login_frame)
    credentials = save_account()
    if credentials != []:
        username_entry.insert(0, credentials[0])
        password_entry.insert(0, credentials[1])
    

def toggle_show_password():
    if show_password_var.get() == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")
def save_account():
    credentials = []
    if os.path.exists("account.txt"):
        with open("account.txt", 'r') as file:
            credentials = file.read().splitlines()
    return credentials
def clear_right_frame():
    for frame in right_frames:
        frame.pack_forget()
def logout():
    global is_Login
    login_button.config(text="Login", command=show_login_frame)
    x_handle.Logout()
    is_Login = False
    clear_right_frame()

def update_button_state():
    # Kiểm tra xem right_frame hiện tại có được hiển thị hay không và cập nhật trạng thái của các nút
    home_button.config(bg="light blue" if current_right_frame == home_right_frame else "SystemButtonFace")
    user_button.config(bg="light blue" if current_right_frame == user_right_frame else "SystemButtonFace")
    manager_button.config(bg="light blue" if current_right_frame == manager_right_frame else "SystemButtonFace")

# Tạo cửa sổ
root = tk.Tk()
root.geometry("1700x900")
root.title("X data")
# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Tính toán vị trí để đặt cửa sổ giữa màn hình
x = (screen_width - 1700) // 2  # 1000 là chiều rộng của cửa sổ
y = (screen_height - 900) // 2  # 600 là chiều cao của cửa sổ

# Đặt vị trí của cửa sổ giữa màn hình
root.geometry(f"1700x900+{x}+{y}")

# Tạo container frame
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Tạo Nav-bar frame
nav_frame = tk.Frame(container, width=100)
nav_frame.pack(side="left", fill="y")

# Tạo các nút trong Nav-bar
home_button = tk.Button(nav_frame, text="Lấy các bài viết", width=20, command=on_home_click, relief=tk.RAISED)
home_button.pack(pady=2)

# user_button = tk.Button(nav_frame, text="updating", width=20, command=on_user_click, relief=tk.RAISED)
# user_button.pack(pady=2)

# manager_button = tk.Button(nav_frame, text="updating", width=20, command=on_manager_click, relief=tk.RAISED)
# manager_button.pack(pady=2)

# Tạo nút "Login" trong nav_frame
login_button = tk.Button(nav_frame, text="Đăng nhập", width=20, command=show_login_frame)
login_button.pack()

# Tạo các right_frame tương ứng cho từng nút
home_right_frame = home_frame.create_home_frame(container)
user_right_frame = user_frame.create_user_frame(container)
manager_right_frame = manager_frame.create_manager_frame(container)

# Gom các right_frame vào một danh sách
right_frames = [home_right_frame, user_right_frame, manager_right_frame]

# Biến để theo dõi right_frame hiện tại
current_right_frame = None

# Bắt đầu vòng lặp chạy ứng dụng
root.mainloop()
