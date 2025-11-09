from db_code import get_root_folders, add_folder, delete_folder, add_tab, get_all_tabs, get_tab_by_id

#delete_folder(11)
#add_tab("sims", "sims.org", 18)
t = get_all_tabs()
print(t)
t1 = get_tab_by_id(1)
print(t1)