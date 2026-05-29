import webview
import os
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

data_file_path = os.path.join(application_path, 'todos_data.json')
html_file = os.path.join(application_path, 'index.html')

class Api:
    def select_folder(self):
        window = webview.windows[0]
        result = window.create_file_dialog(webview.FOLDER_DIALOG)
        return result[0] if result and len(result) > 0 else ""

    def open_folder(self, path):
        if os.path.exists(path):
            os.startfile(path)
            
    def close_app(self):
        window = webview.windows[0]
        window.destroy()

    def minimize_app(self):
        window = webview.windows[0]
        window.minimize()

    def toggle_maximize_app(self):
        window = webview.windows[0]
        window.toggle_fullscreen() 

    def load_data(self):
        if os.path.exists(data_file_path):
            try:
                with open(data_file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"读取数据失败: {e}")
        return "[]"

    def save_data(self, data_str):
        try:
            with open(data_file_path, 'w', encoding='utf-8') as f:
                f.write(data_str)
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False

    def open_spark_file(self, folder_path):
        if not folder_path or not os.path.exists(folder_path):
            return False
            
        file_path = os.path.join(folder_path, 'spark.md')
        
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("# 灵感记录\n")
            except Exception as e:
                print(f"创建 spark.md 失败: {e}")
                return False
                
        try:
            os.startfile(file_path)
            return True
        except Exception as e:
            print(f"打开 spark.md 失败: {e}")
            return False

if __name__ == '__main__':
    if not os.path.exists(html_file):
        print(f"错误: 找不到文件 {html_file}")
        sys.exit(1)

    api = Api()
    webview.create_window(
        title='桌面待办', 
        url=html_file, 
        js_api=api,
        width=380, 
        height=600,
        frameless=True,      
        easy_drag=False,     # 关闭全局拖拽，改为HTML元素局部控制，防止影响滚动条
        on_top=True,         
        transparent=True     
    )
    webview.start(gui='edgechromium')