import os
import shutil
from converter import markdown_to_html_node
from extracter import extract_title

def main():
    print("Hello, I am starting")
    copy_static_to_public(".")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

def copy_static_to_public(path):
    static_path = path + "/static"
    public_path = path + "/public"
    if os.path.exists(static_path):
        if os.path.exists(public_path): #delete destination path for clean copy
            print("Cleaning destination...")
            shutil.rmtree(public_path)
        file_list = get_all_in_path(static_path)
        print("Copying from static to public...")
        make_dirs_and_files(file_list)
    return

def get_all_in_path(path):
    file_list = []
    if os.path.isdir(path):
        file_list.append(path) #add path
        objs = os.listdir(path)
        for obj in objs:
            file_list.extend(get_all_in_path(path + "/" + obj)) #add file
        return file_list
    else:
        return [path] # a file here
    
def replace_static_with_public_path(path_list):
    replaced_paths = []
    for path in path_list:
        replaced_paths.append(path[:1] + "/public" + path[8:])
    return replaced_paths

def make_dirs_and_files(file_list):
    path_list = sorted(file_list) # make sure directories are handled before enclosed files.
    dest_list = replace_static_with_public_path(path_list)
    for i in range(len(path_list)):
        if os.path.isdir(path_list[i]):
            os.mkdir(dest_list[i])
            print(f"made directory: {dest_list[i]}")
        else:
            shutil.copy(path_list[i], dest_list[i])
            print(f"created a file: {dest_list[i]}")
    return

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    f = open(from_path, "r")
    markdown_in = f.read()
    f.close()
    
    t = open(template_path, "r")
    template = t.read()
    t.close()
    
    content = markdown_to_html_node(markdown_in).to_html()
    title = extract_title(markdown_in)

    new = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    n = open(dest_path, "w")
    n.write(new)
    n.close()

    print("Done generating")

    return

main()