import os
import shutil
from converter import markdown_to_html_node
from extracter import extract_title

def main():
    print("Hello, I am starting")
    copy_static_to_public(".")
    generate_pages_recursive("./content", "./template.html", "./public")

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
    
def replace_paths_part(path_list, replace, new):
    new_list = []
    for path in path_list:
        new_list.append(path.replace(replace, new))
    return new_list

def make_dirs_and_files(file_list):
    path_list = sorted(file_list) # make sure directories are handled before enclosed files.
    dest_list = replace_paths_part(path_list, "static", "public")
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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = get_all_in_path(dir_path_content)
    for direc in dir_list:
        if ".md" in direc:
            direc_destination = replace_paths_part([direc], dir_path_content, dest_dir_path)[0][:-2] + "html"
            parent_dir = "/".join(direc_destination.split("/")[:-1])
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir) # handles also needed parent directories to the parent directory (unlike os.mkdir())
            generate_page(direc, template_path, direc_destination)
    return

main()