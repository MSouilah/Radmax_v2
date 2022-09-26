function new_project_launcher() {
    eel.data_ask("new_project")();
}

function change_theme(tmp, val) {
    eel.change_theme(tmp, val);
}

function read_db_data(tmp) {
    eel.read_db_data(tmp);
}

function delete_db_data(tmp) {
    eel.delete_db_data(tmp);
}

function load_DB_initialization(){
    eel.load_DB_initialization();
}

function SaveProject(val, option) {
    Apply_update();
    eel.save_project(val, option)();
}

function update_fitting_options(tmp){
    eel.update_fitting_options(tmp)
}

function launch_worker(){
    eel.launch_worker()
}

function stop_worker(){
    eel.stop_worker()
}

function scale_manual(type, val){
    tmp = [type, val, dw_scale.value, val2save];
    eel.scale_manual(tmp)
}

function update_sp_dwp_table(tmp){
    eel.update_sp_dwp_table(tmp)
}

function update_project(tmp){
    eel.update_project(tmp)
}

function update_change_limits(tmp){
    eel.update_change_limits(tmp)
}

function change_options_working(tmp){
    eel.change_options_working(tmp)
}

function data_ask(tmp){
    eel.data_ask(tmp)
}

function load_projects(name, val){
    eel.load_project(name, val)
}

function load_graph(name, val){
    eel.load_graph(name, val)
}

function on_export_data(){
    eel.on_export_data()
}

function on_update_graph_colors(val){
    eel.update_graph_colors(val, graph_colors);
}

function send_action_drag_horizontaly(val, graph){
    eel.drag_horizontaly(val, graph);
}

window.addEventListener('DOMContentLoaded', () => {
    if(!isElectron()){
        menu_file_hide.classList.remove('d-none');
        menu_about_hide.classList.remove('d-none');
        menu_options_hide.classList.remove('d-none');
    }

    eel.expose(browser)
    function browser(data){
        val = data[1];
        browser_choice = val;
        if (browser_choice == 3){
            window.api.receive("fromMain", (data) => {
                eel.handleinput(data);
            });
            window.api.receive("NewProject", (data) => {
                new_project_launcher();
            });
            window.api.receive("SaveProject", (data) => {
                SaveProject(1, data);
            });
            window.api.receive("SaveCurrentProject", (data) => {
                SaveProject(0, "Nopath");
            });
            window.api.receive("OpenOptionsRadmax", (data) => {
                open_general_option();
            });
            window.api.receive("AboutRadmax", (data) => {
                open_about_modal();
            });
            window.api.receive("load_project_from_main", (data) => {
                eel.load_project("load_project_from_main", data);
            });
            window.api.receive("load_xrd_from_main", (data) => {
                eel.load_graph("load_xrd_from_main", data);
            });
            window.api.receive("load_strain_from_main", (data) => {
                eel.load_graph("load_strain_from_main", data);
            });
            window.api.receive("load_dw_from_main", (data) => {
                eel.load_graph("load_dw_from_main", data);
            });
            window.api.receive("SaveFitData", (data) => {
                eel.on_export_data();
            });
            function read_data_py(){
                eel.data_ask("initialization")
            };
        }
    }

    eel.expose(change_api_title)
    function change_api_title(data){
        if(isElectron()){
            window.api.send("change_title", title);
        }else{
            if (document.title != data[0]) {
                document.title = "RaDMaX 2 - " + data[0];
                path_name.innerHTML = data[1];
                current_name.innerHTML = data[0];
            }
        }
    }

    eel.expose(check_input_file)
    function check_input_file(){
        modal_check_input_file.toggle();
    }

    eel.expose(data_from_py)
    function data_from_py(dat){
        load_and_update_data(dat);
    }

    eel.expose(data_graph_py)
    function data_graph_py(dat){
        load_and_update_graph(dat)
    }

    eel.expose(save_project_js)
    function save_project_js(){
        save_project();
    }

    eel.expose(update_bounds_table)
    function update_bounds_table(data){
        load_strain_dw_values(data[1])
    }

    eel.expose(change_limit_input)
    function change_limit_input(){
        modal_change_limits.toggle();
    }

    eel.expose(result_from_fit)
    function result_from_fit(dat){
        fit_ending_data(dat)
    }

    eel.expose(dataPyDB)
    function dataPyDB(dat){
        res_db = dat;
        load_database();
    }

    eel.expose(update_gsa_counter)
    function update_gsa_counter(dat){
        var tmp = dat[1] + " / " + nb_cycle_max_save;
        gsa_current_cycle.innerHTML = tmp;
    }

    eel.expose(manage_database_using)
    function manage_database_using(val){
        change_database_using(val);
    }

    eel.expose(change_basis_functions)
    function change_basis_functions(val){
        change_basis_functions_number();
    }

    eel.expose(export_fit_not_working)
    function export_fit_not_working(val){
        modal_export_fit_not_working.toggle();
    }
    
    eel.expose(load_xrd_before_save_project)
    function load_xrd_before_save_project(val){
        modal_load_xrd_before_save_project.toggle();
    }

    eel.expose(directory_no_longer_exist)
    function directory_no_longer_exist(val){
        old_directory.innerHTML = val;
        modal_directory_no_longer_exist.toggle();
    }

    eel.expose(res_from_delete)
    function res_from_delete(val){
        if(val){
            delete_row_table();
        }else{
            modal_error_delete_data_from_db.toggle();
        }
    }
    
    

    Mousetrap.bind(['command+k', 'ctrl+k'], function() {
        return false;
    });

    Mousetrap.bind(['command+s', 'ctrl+s'], function() {
        SaveProject(0, "Nopath")
        return false;
    });

    Mousetrap.bind(['command+shift+s', 'ctrl+shift+s'], function() {
        if(isElectron()){
            window.api.send("save_project_to_main");
        }else{
            SaveProject(0, 0)
        }
        return false;
    });
    Mousetrap.bind(['command+u', 'ctrl+u'], function() {
        Apply_update();
        return false;
    });
    Mousetrap.bind(['alt+x'], function() {
        if(isElectron()){
            window.api.send("closeElectronWindow");
        }
        return false;
    });
    Mousetrap.bind(['command+o', 'ctrl+o'], function() {
        if(isElectron()){
            window.api.send("load_project_to_main");
        }else{
            eel.load_project("load_project_web", 0);
        }
        return false;
    });
    Mousetrap.bind(['command+n', 'ctrl+n'], function() {
        new_project_launcher();
        return false;
    });
});