
var form_initial_params = document.querySelectorAll('.initial_params_form');
var form_fitting_options = document.querySelectorAll('.fitting_options_form');
var form_exclude_region = document.querySelectorAll('.exclude_region_form');

function geometryclick(myval){
    radioValue = myval;
    var pngData = 'img/' + img_schem_list[radioValue];
    labelImage.src = pngData;
    hide_film_thickness.classList.add('d-none');
    hide_film_thickness_substrate.classList.add('d-none');
    if(radioValue == 2){
        hide_film_thickness.classList.remove('d-none');
    }else if (radioValue == 3){
        hide_film_thickness_substrate.classList.remove('d-none');
        lattice_parameters_symmetry(1);
    }
}

// function splash() {
//     var time = splash_time;
//     const rand_number = Math.floor((Math.random() * 100) + 1);
//     const rand_list = [2, 18, 24, 56, 77, 89];
//     const rand_list2 = [5, 11, 32, 67, 81, 83, 92, 99];
//     var test_rand = rand_list.includes(rand_number);
//     var test_rand_image = rand_list2.includes(rand_number);
//     console.log(rand_number)
//     modalImg.src = "img/classic_end.png";
//     captionText.innerHTML = "";
//     captionTextWait.innerHTML = "";
//     if(test_rand){
//         modalImg.src = "img/morpheus_end.png";
//     }
//     if(test_rand_image){
//         const rand_number_image = Math.floor((Math.random() * 5) + 1);
//         console.log(rand_number_image)
//         modalImg.src = "img/random_image/" + photo_links[rand_number_image]['path'];
//         captionTextWait.innerHTML = "One moment please wait, waiting for the threads to die...";
//         captionText.innerHTML = photo_links[rand_number_image]['link'];
//     }
//     modal_wait.style.display = "block";
//     setTimeout(function () {
//         modal_wait.style.display = "none";
//     }, time);
// }

function fitting_options_changes(){
    Array.prototype.slice.call(form_fitting_options)
    .forEach(function (form) {
        if (!form.checkValidity()) {
        }else{
            const main_form = document.forms.namedItem("form_fitting_options");
            const dd = new FormData(main_form);
            fitting2save = Object.fromEntries(dd.entries());
            tmp = ["fitting_options", fitting2save];
            update_fitting_options(tmp);
            // eel.update_fitting_options(tmp)
        }
        form.classList.add('was-validated')
  })
}

resolution_func.addEventListener('change', function(event) {
    if(event.originalEvent === undefined)return;
});

function start_fit(){
    spinner_fit_hide.classList.remove('d-none');
    parameters_pane_tab.classList.add('disabled');
    geometry_pane_tab.classList.add('disabled');
    database_pane_tab.classList.add('disabled');
    start_fit_button.classList.add('disabled');
    stop_fit_button.classList.remove('disabled');
    strain_button_restore.classList.add('disabled');
    dw_button_restore.classList.add('disabled');
    boh_button_restore.classList.add('disabled');
    save_bounds_values_4_restore = table_strain_dw_values.getData();
    fit_state_hide.classList.add('d-none');
    fit_residual_hide.classList.add('d-none');
    nb_cycle_max_save = nb_cycle_max.value;
    Apply_update();
    // eel.launch_worker();
    launch_worker();
}

function stop_fit(){
    parameters_pane_tab.classList.remove('disabled');
    geometry_pane_tab.classList.remove('disabled');
    database_pane_tab.classList.remove('disabled');
    start_fit_button.classList.remove('disabled');
    stop_fit_button.classList.add('disabled');
    strain_button_restore.classList.remove('disabled');
    dw_button_restore.classList.remove('disabled');
    boh_button_restore.classList.remove('disabled');
    // eel.stop_worker();
    stop_worker();
    // splash();
}

function delete_database_data(){

}

function Apply_scale_strain(val){
    Apply_scale(val, "strain");
}

function Apply_scale_dw(val){
    Apply_scale(val, "dw");
}

function Apply_scale(val, type){
    test_fields = read_fields_parameters();
    Array.prototype.slice.call(form_initial_params)
    .forEach(function (form) {
        if (!form.checkValidity()) {
        }else{
            // tmp = [type, val, dw_scale.value, val2save];
            // eel.scale_manual(tmp);
            scale_manual(type, val);
        }
    })
}

function restore_values(val){
    table_strain_dw_values.clearData();
    table_strain_dw_values.updateOrAddData([save_bounds_values_4_restore]);
    var tmp = ["DW", table_strain_dw_values.getData()]
    update_sp_dwp_table(tmp)
    // eel.update_sp_dwp_table(tmp)
    var tmp = ["Strain", table_strain_dw_values.getData()]
    update_sp_dwp_table(tmp)
}

function Apply_update(){
    test_fields = read_fields_parameters();
}

function Send_data_update_project(){
    var tmp = [val2save, table_strain_dw_values.getData()]
    // eel.update_project(tmp)
    update_project(tmp)
}

function read_fields_parameters(){
    Array.prototype.slice.call(form_initial_params)
    .forEach(function (form) {
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
        }else{
            form.classList.remove('was-validated');
            const main_form = document.forms.namedItem("initial_params_form");
            const dd = new FormData(main_form);
            val2save = Object.fromEntries(dd.entries());
            val2save['dw_basis_func'] = dw_function.value;
            val2save['model'] = model_strain_dw;
            val2save['model_strain'] = model_strain_dw;
            val2save['model_dw'] = model_strain_dw;
            val2save['change_model'] = change_model;
            val2save['geometry'] = document.querySelector('input[name="scheme_geometry"]:checked').value;
            val2save['crystal_choice'] = crystal_choice_select;
            val2save['crystal_choice_s'] = crystal_choice_select_sub;
            Send_data_update_project();
        }
    })
}

function load_data_to_interface(){
    Object.entries(res_data[3]).forEach(([key, val]) => {
        try {
            document.getElementsByName(key)[0].value = val;
        } catch (e) {
            // This here can be empty
        }
    });

    fill_dw_basis_function(res_data[4][0])
    dw_function.value = res_data[4][3];
    document.getElementsByName("strain_scale")[0].value = 0.1;
    document.getElementsByName("dw_scale")[0].value = 0.1;
    document.getElementById("resolution_func")[0].selectedIndex = res_data[3]['function_profile'];

    if (res_data[0] == "new_project"){
        crystal_choice_s.value = 'Al2O3';
        crystal_choice.value = 'Al2O3';
        crystal_choice_select = 'Al2O3';
        crystal_choice_select_sub = 'Al2O3';
    }else{
        crystal_choice_s.value = res_data[3]['substrate_name'];
        crystal_choice.value = res_data[3]['crystal_name'];
        crystal_choice_select = res_data[3]['crystal_name'];
        crystal_choice_select_sub = res_data[3]['substrate_name'];
    }
    model_strain_dw = res_data[3]['model'];
    
    load_bounds(res_data[2]);
    load_strain_dw_values(res_data[5]);
}

function load_bounds(val){
    Object.entries(val).forEach(([key, val]) => {
        try {
            if(document.getElementsByName(key).length > 1){
                for (let i = 0; i < document.getElementsByName(key).length; i++) {
                    document.getElementsByName(key)[i].value = val;
                }
            }else{
                document.getElementsByName(key)[0].value = val;
            }
        } catch (e) {
            // This here can be empty
        }
    });
}

function update_fields_interface(){
    Object.entries(res_data[3]).forEach(([key, val]) => {
        if(key == "scheme_geometry"){
            document.querySelector("input[name='scheme_geometry'][value='" + val + "']").checked = true;
            // $("input[name='scheme_geometry'][value='" + val + "']").attr('checked', true);
        }else{
            // $('input[name=' + i + ']').val(val);
            try {
                if(document.getElementsByName(key).length > 1){
                    for (let i = 0; i < document.getElementsByName(key).length; i++) {
                        document.getElementsByName(key)[i].value = val;
                    }
                }else{
                    document.getElementsByName(key)[0].value = val;
                }
            } catch (e) {
                // This here can be empty
            }
        }
    });
    fill_dw_basis_function(res_data[4][0])
    dw_function.value = res_data[4][3];
    document.getElementsByName("damaged_depth")[0].value = res_data[4][2];
    document.getElementsByName("number_slices")[0].value = res_data[4][4];
    crystal_choice_s.value = res_data[3]['substrate_name'];
    crystal_choice.value = res_data[3]['crystal_name'];
    crystal_choice_select = res_data[3]['crystal_name'];
    crystal_choice_select_sub = res_data[3]['substrate_name'];
    model_strain_dw = res_data[3]['model'];
    load_strain_dw_values(res_data[5]);
}

function load_strain_dw_values(data){
    table_strain_dw_values.clearData();
    table_strain_dw_values.updateOrAddData(data);
}

function load_xrd(){
    console.log(graph_data)
    if (graph_data[0] == "load_xrd"){
        config_xrd_gaph.data.datasets[0].data = graph_data[3];
        // config_xrd_gaph.data.datasets[1].data = graph_data[1];
        // config_xrd_gaph.data.datasets[0].data = graph_data[2];
        // config_xrd_gaph.data.labels = graph_data[1];
    }
    else if (graph_data[0] == "update_xrd"){
        config_xrd_gaph.data.datasets[1].data = graph_data[3];
        // config_xrd_gaph.data.labels = graph_data[1];
    }
    else if (graph_data[0] == "update_xrd_fit"){
        config_xrd_gaph.data.datasets[1].data = graph_data[3];
        config_xrd_gaph.data.datasets[1].borderColor = 'rgb(255, 0, 0)';
        // config_xrd_gaph.data.labels = graph_data[1];
    }
    console.log(config_xrd_gaph)
    xrd_gaph.update();
}

function load_constraints_graph(){
    // console.log("graph_data[0]", graph_data[0])
    if (graph_data[0] == "load_strain_from_main" || graph_data[0] == "update_strain_graph"){
        config_strain.data.datasets[0].data = graph_data[2];
        config_strain.data.datasets[1].data = graph_data[1];
        config_strain.options.scales.y.min = graph_data[3]['ymin_strain'];
        config_strain.options.scales.y.max = graph_data[3]['ymax_strain'];
        config_strain.options.scales.x.max = graph_data[3]['xmax_strain'];
        config_strain.options.scales.x.min = 0;
        config_strain.options.scales.x.type = 'linear';
        config_strain.options.scales.x.ticks.display = false;
        config_strain.options.plugins.dragData.dragX = dragPointsX;
        config_strain.options.plugins.scales.y.dragData = dragPointsY;
        console.log(config_strain)
        strain_chart.update(config_strain);
        strain_chart.resetZoom();
    }
    else{
        config_dw.data.datasets[0].data = graph_data[2];
        config_dw.data.datasets[1].data = graph_data[1];
        config_dw.options.scales.y.min = graph_data[3]['ymin_dw'];
        config_dw.options.scales.y.max = graph_data[3]['ymax_dw'];
        config_dw.options.scales.x.max = graph_data[3]['xmax_dw'];
        config_dw.options.scales.x.min = 0;
        config_dw.options.scales.x.type = 'linear';
        config_dw.options.plugins.dragData.dragX = dragPointsX;
        config_dw.options.plugins.scales.y.dragData = dragPointsY;
        console.log(config_dw)
        dw_chart.update();
    }
    reset_zoom(1);
}

function change_limits(){
    var ele = document.getElementsByName('change_input_limit');
    var res = "None";
    for(i = 0; i < ele.length; i++) {
        if(ele[i].checked) res=parseInt(ele[i].value)
    }
    if (res == 2){
        spinner_fit_hide.classList.add('d-none');
        parameters_pane_tab.classList.remove('disabled');
        geometry_pane_tab.classList.remove('disabled');
        database_pane_tab.classList.remove('disabled');
        start_fit_button.classList.remove('disabled');
        stop_fit_button.classList.add('disabled');
        strain_button_restore.classList.remove('disabled');
        dw_button_restore.classList.remove('disabled');
        boh_button_restore.classList.remove('disabled');
    }else{
        start_fit_button.classList.add('disabled');
        stop_fit_button.classList.remove('disabled');
        // eel.update_change_limits(res)
        update_change_limits(res)
    }
}

function update_contraints_graph(graph, datasetIndex, index, value){
    var x_depth = value.x,
        new_coord = value.y.toFixed(3),
        data = table_strain_dw_values.getData(),
        data_graph_dw = dw_chart.data.datasets[datasetIndex].data,
        data_graph_strain = strain_chart.data.datasets[datasetIndex].data,
        data_graph_read = 0,
        x_value = 0,
        x_coord = 0,
        x_select = 0;
    // console.log(graph, datasetIndex, index, value)
    // console.log(data)
    console.log(strain_chart)
    console.log(dw_chart)
    const zoom_strain = strain_chart.isZoomedOrPanned();
    const zoom_dw = dw_chart.isZoomedOrPanned();
    console.log(zoom_strain, zoom_dw)
    if(dragPointsX){
        Object.entries(data).forEach(([key, val]) => {
            // console.log(key, val)
            // val.strain_choice = is_checked;
            x_value = val.x_value;
            if(x_value == x_depth){
                if(graph == "DW"){
                    val.dw = new_coord;
                }else{
                    val.strain = new_coord;
                }
            }
        })
        // InitialDepth = data[index]['x_value'];
        // valDepth = x_depth - InitialDepth;
        // console.log("InitialDepth", InitialDepth)
        // console.log("valDepth", valDepth)
        // Object.entries(data).forEach(([key, val]) => {
        //     val.x_value = val.x_value + valDepth; 
        // })
    }else{
        console.log("isSelectedPoints", isSelectedPoints)
        if(isSelectedPoints){
            Object.entries(data).forEach(([key, val]) => {
                if(SelectedPoints.includes(parseInt(key))){
                    x_select = val.x_value;
                    data_graph_read = data_graph_strain
                    if(graph == "DW"){
                        data_graph_read = data_graph_dw
                    }
                    Object.entries(data_graph_read).forEach(([kk, vv]) => {
                        x_coord = vv.x;
                        if(x_coord == x_select){
                            if(graph == "DW"){
                                val.dw = vv.y.toFixed(3);
                            }else{
                                val.strain = vv.y.toFixed(3);
                            }
                        }
                    })
                }
            })
        }else{
            Object.entries(data).forEach(([key, val]) => {
                x_value = val.x_value;
                if(x_value == x_depth){
                    if(graph == "DW"){
                        val.dw = new_coord;
                    }else{
                        val.strain = new_coord;
                    }
                }
            })
        }
    }
    table_strain_dw_values.clearData();
    table_strain_dw_values.updateOrAddData([data]);
    var tmp = [graph, table_strain_dw_values.getData(), dragPointsX];
    console.log(tmp)
    dw_chart_zoomed = 0;
    strain_chart_zoomed = 0;
    update_sp_dwp_table(tmp)
}

function OptionsValueChange(){
    var tmp = [radmax_use_database.checked, sounds_open.checked, sounds_play.checked];
    res_data[2]['use_database'] = radmax_use_database.checked;
    res_data[2]['open_with_sound'] = sounds_open.checked;
    res_data[2]['play_sounds'] = sounds_play.checked;
    change_database_using(radmax_use_database.checked);
    // eel.change_options_working(tmp);
    change_options_working(tmp);
}

function change_database_using(val){
    if(val){
        database_panel.classList.remove('d-none');
    }else{
        database_panel.classList.add('d-none');
    }
}

function open_about_modal(){
    radmax_version.innerHTML = "Version: " + res_data[2]['version'] + " - Date: " + res_data[2]['last_modification'];
    modal_about.toggle();
}

function open_general_option(){
    // console.log("res_data", res_data)
    sounds_open.checked = false;
    sounds_play.checked = false;
    radmax_use_database.checked = false;
    if(res_data[2]['open_with_sound']){
        sounds_open.checked = true;
    }
    if(res_data[2]['play_sounds']){
        sounds_play.checked = true;
    }
    if(res_data[2]['use_database']){
        radmax_use_database.checked = true;
    }
    modal_options.toggle();
}

function change_title(val){
    if (browser_choice == 3){
        var title = "New project";
        if (val == 1){
            title = res_data[6];
        }
        window.api.send("change_title", title);
    } 
}

function load_database(){
    if(res_db[0] == "Loading_database"){
        table_database.clearData();
    }
    // console.log(res_db[1])
    table_database.updateOrAddData(res_db[1]);
}

function load_and_update_data(dat){
    change_model = 0;
    res_data = dat;
    console.log("res_data", res_data)
    if (res_data[0] == "initialization"){
        fill_crystal(res_data[1]);
        load_data_to_interface();
        apply_theme(res_data[2]['theme']);
        theme_bootstrap_choice.value = res_data[2]['theme'];
    }
    else if (res_data[0] == "new_project"){
        init_graph_strain = 0;
        init_graph_dw = 0;
        load_data_to_interface();
        start_fit_button.classList.add('disabled');
        strain_button_restore.classList.add('disabled');
        dw_button_restore.classList.add('disabled');
        boh_button_restore.classList.add('disabled');
        fit_state_success_hide.classList.add('d-none');
        fit_state_error_hide.classList.add('d-none');
        fit_error.classList.add('d-none');
        document.querySelector("input[name='scheme_geometry'][value='0']").checked = true;
        var pngData = 'img/' + img_schem_list[0];
        labelImage.src = pngData;
        geometryclick(0);
        xrd_gaph.clear();
        change_title(0);
    }
    else if (res_data[0] == "load_project"){
        init_graph_strain = 0;
        init_graph_dw = 0;
        load_data_to_interface();
        document.querySelector("input[name='scheme_geometry'][value='0']").checked = true;
        var pngData = 'img/' + img_schem_list[res_data[3]['geometry']];
        labelImage.src = pngData;
        geometryclick(0);
        change_title(1)
    }
    else if (res_data[0] == "load_project_from_database"){
        init_graph_strain = 0;
        init_graph_dw = 0;
        load_data_to_interface();
        document.querySelector("input[name='scheme_geometry'][value='0']").checked = true;
        var pngData = 'img/' + img_schem_list[res_data[3]['geometry']];
        labelImage.src = pngData;
        geometryclick(0);
        change_title(1)
    }
    else if (res_data[0] == "update"){
        update_fields_interface();
    }
}

function save_project(){
    window.api.send("save_project_to_main");
    spinner_fit_hide.classList.add('d-none');
    parameters_pane_tab.classList.remove('disabled');
    geometry_pane_tab.classList.remove('disabled');
    database_pane_tab.classList.remove('disabled');
    start_fit_button.classList.remove('disabled');
    stop_fit_button.classList.add('disabled');
    strain_button_restore.classList.remove('disabled');
    dw_button_restore.classList.remove('disabled');
    boh_button_restore.classList.remove('disabled');
}

function load_and_update_graph(dat){
    change_model = 0;
    graph_data = dat;
    var res = graph_data[0];
    if (res == "load_xrd" || res == "update_xrd"){
        start_fit_button.classList.remove('disabled');
        load_xrd();
    }
    else if (res == "update_xrd_fit"){
        load_xrd();
    }
    else if (res == "load_strain_from_main" || res == "load_strain_web" || res == "update_strain_graph"){
        load_constraints_graph();
    }
    else if (res == "load_dw_from_main" || res == "load_dw_web" || res == "update_dw_graph"){
        load_constraints_graph();
    }
}

function fit_ending_data(dat){
    parameters_pane_tab.classList.remove('disabled');
    geometry_pane_tab.classList.remove('disabled');
    database_pane_tab.classList.remove('disabled');
    start_fit_button.classList.remove('disabled');
    spinner_fit_hide.classList.add('d-none');
    fit_state_hide.classList.remove('d-none');
    fit_residual_hide.classList.remove('d-none');
    fit_error.innerHTML = dat[1];
    if(dat[0] == "fit_success"){
        fit_state_success_hide.classList.remove('d-none');
        fit_state_error_hide.classList.add('d-none');
        fit_error.style.color = 'Chartreuse';
    }else{
        fit_state_success_hide.classList.add('d-none');
        fit_state_error_hide.classList.remove('d-none');
        fit_error.style.color = 'tomato';
    }
    load_strain_dw_values(dat[2]);
    config_xrd_gaph.data.datasets[1].borderColor = "#9999ff";
    xrd_gaph.update();
    if(after_one_fit == 0){
        after_one_fit = 1;
        strain_button_restore.classList.remove('disabled');
        dw_button_restore.classList.remove('disabled');
        boh_button_restore.classList.remove('disabled');
    }
}

radmax_tab.addEventListener('click', function () {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
})

// delete_switch.addEventListener('change', function () {
//     const hide_delete_database_data = document.getElementById('hide_delete_database_data');
//     if(this.checked){
//         hide_delete_database_data.classList.remove('d-none');
//     }else{
//         table_database.deselectRow();
//         hide_delete_database_data.classList.add('d-none');
//     }
// })

model_strain.addEventListener('change', function(e) {
    model_strain_dw = model_strain.options[model_strain.selectedIndex].value;
    change_model = 1;
    var pv_parameters = document.getElementById('pv_parameters'),
        strain_function = document.getElementById('strain_function');
    if(model_strain_dw == 2){
        pv_parameters.classList.remove('d-none');
        strain_function.innerHTML = 7;
        fill_dw_basis_function([7]);
        strain_function.disabled = true;
    }else{
        pv_parameters.classList.add('d-none');
        strain_function.disabled = false;
    }
    Apply_update();
});

DragXPoints.addEventListener('change', function () {
    if(this.checked){
        dragPointsX = true;
        dragPointsY = false;
    }else{
        dragPointsX = false;
        dragPointsY = true;
    }
    Apply_update();
})

crystal_choice.addEventListener('change', function(e) {
    crystal_choice_select = crystal_choice.options[crystal_choice.selectedIndex].value;
    Apply_update();
});

crystal_choice_s.addEventListener('change', function(e) {
    crystal_choice_select_sub = crystal_choice_s.options[crystal_choice_s.selectedIndex].value;
    Apply_update();
});

fitting_choice.addEventListener('change', function(event) {
    var res = fitting_choice.options[fitting_choice.selectedIndex].value;
    var gsa_options_hide = document.getElementById('gsa_options_hide');
    if (res == 1){
        gsa_options_hide.classList.add('d-none');
    }else{
        gsa_options_hide.classList.remove('d-none');
    }
});

resolution_func.addEventListener('change', function(e) {
    var res_func = resolution_func.options[resolution_func.selectedIndex].value;
    if (res_func == 0 || res_func == 1){
        width_left_hide.classList.remove('d-none');
        width_right_hide.classList.add('d-none');
        shape_left_hide.classList.add('d-none');
        shape_right_hide.classList.add('d-none');
        b_bell_hide.classList.add('d-none');
        width_left_label.innerHTML = "Width(°)";
    }
    else if (res_func == 2){
        width_left_hide.classList.remove('d-none');
        width_right_hide.classList.add('d-none');
        shape_left_hide.classList.remove('d-none');
        shape_right_hide.classList.add('d-none');
        b_bell_hide.classList.add('d-none');
        width_left_label.innerHTML = "Width(°)";
        shape_left_label.innerHTML = "Shape";
    }
    else if (res_func == 3){
        width_left_hide.classList.remove('d-none');
        width_right_hide.classList.add('d-none');
        shape_left_hide.classList.add('d-none');
        shape_right_hide.classList.add('d-none');
        b_bell_hide.classList.remove('d-none');
        width_left_label.innerHTML = "Width(°)";
    }
    else if (res_func == 4){
        width_left_hide.classList.remove('d-none');
        width_right_hide.classList.remove('d-none');
        shape_left_hide.classList.remove('d-none');
        shape_right_hide.classList.remove('d-none');
        b_bell_hide.classList.add('d-none');
        width_left_label.innerHTML = "Width left(°)";
        width_right_label.innerHTML = "Width right(°)";
        shape_left_label.innerHTML = "Shape left";
        shape_right_label.innerHTML = "Shape right";
    }
    Apply_update();
});

new_project.addEventListener('click', function () {
    data_ask("new_project");
})

load_project.addEventListener('click', function () {
    load_projects("load_project_web", 0);
})

loads_xrd.addEventListener('click', function () {
    load_graph("load_xrd_web", 0);
})

loads_strain.addEventListener('click', function () {
    load_graph("load_strain_web", 0);
})

loads_dw.addEventListener('click', function () {
    load_graph("load_dw_web", 0);
})

save_file.addEventListener('click', function () {
    SaveProject(0, "Nopath");
})

save_as_file.addEventListener('click', function () {
    SaveProject(1, 0);
})

export_fits.addEventListener('click', function () {
    on_export_data();
})

about_modal.addEventListener('click', function () {
    open_about_modal();
})

general_options_modal.addEventListener('click', function () {
    open_general_option();
})

container.addEventListener("click", function(event) {
    Apply_update();    
});

window.onbeforeunload = function() {
    return "Dude, are you sure you want to leave? Think of the kittens!";
}

canvas_strain.addEventListener('mousedown', function(evt) {
    canvas_mousedown(evt, strain_chart, PointInitialColorStrain);
});

canvas_strain.addEventListener('mousemove', function(evt) {
    canvas_mousemove(evt, strain_chart, selectionContextStrain, canvas_strain);
});

canvas_strain.addEventListener('mouseup', function(evt) {
    canvas_mouseup(evt, strain_chart, ctx_strain, PointInitialColorStrain)
});

canvas_dw.addEventListener('mousedown', function(evt) {
    canvas_mousedown(evt, dw_chart, PointInitialColorDW);
});

canvas_dw.addEventListener('mousemove', function(evt) {
    canvas_mousemove(evt, dw_chart, selectionContextDw, canvas_dw);
});

canvas_dw.addEventListener('mouseup', function(evt) {
    canvas_mouseup(evt, dw_chart, ctx_dw, PointInitialColorDW)
});

function canvas_mousedown(evt, chart, color){
    if(evt.altKey){
        reset_selected_points(chart, color);
        rectROI.startX = evt.offsetX;
        rectROI.startY = evt.offsetY;
        chart_x_start = chart.scales.x.getValueForPixel(evt.offsetX);
        chart_y_start = chart.scales.y.getValueForPixel(evt.offsetY);
        dragROI = true;
    }
}

function canvas_mousemove(evt, chart, selectctx, canvas){
    let x = chart.scales.x.getValueForPixel(evt.offsetX);
    let y = chart.scales.y.getValueForPixel(evt.offsetY);
    graph_coords.innerHTML = 'Coordinates: ' + x.toFixed(2) + ',' + y.toFixed(2);

    if(evt.altKey){
        if(dragROI) {
            selectctx.clearRect(0, 0, canvas.width, canvas.height);
            rectROI.w = (evt.offsetX) - rectROI.startX;
            rectROI.h = (evt.offsetY) - rectROI.startY;
            selectctx.strokeStyle = 'red';
            selectctx.strokeRect(rectROI.startX, rectROI.startY, rectROI.w, rectROI.h);
        }
    }
}

function canvas_mouseup(evt, chart, ctx, color){
    if(dragROI){
        dragROI = false;
        rectROI.w = (evt.offsetX) - rectROI.startX;
        rectROI.h = (evt.offsetY) - rectROI.startY;
        ctx.strokeStyle = 'red';
        ctx.strokeRect(rectROI.startX, rectROI.startY, rectROI.w, rectROI.h);

        x_end = evt.offsetX;
        y_end = evt.offsetY;
        chart_x_end = chart.scales.x.getValueForPixel(evt.offsetX);
        chart_y_end = chart.scales.y.getValueForPixel(evt.offsetY);
        
        roi_coord["chart_x_start"] = chart_x_start;
        roi_coord["chart_x_end"] = chart_x_end;
        roi_coord["chart_y_start"] = chart_y_start;
        roi_coord["chart_y_end"] = chart_y_end;
        isROI = true;
        Object.entries(chart.data.datasets[1].data).forEach(([key, val]) => {
            if(val.x >= roi_coord['chart_x_start'] && val.x <= roi_coord['chart_x_end']){
                ind = key;
                var test = chart.data.datasets[1].pointBackgroundColor[ind];
                if(test != PointselectedColor){
                    chart.data.datasets[1].pointBackgroundColor[ind] = PointselectedColor;
                }else{
                    chart.data.datasets[1].pointBackgroundColor[ind] = color;
                }
            }
        })
        chart.update();
        test_selected_points(chart);
    }
}

canvas_xrd.addEventListener('mousedown', function(evt) {
    if(evt.altKey){
        const rect = canvas_xrd.getBoundingClientRect();
        selectRectExclude.startX = evt.clientX - rect.left;
        selectRectExclude.startY = xrd_gaph.chartArea.top;
        dragExclude = true;
    }
});

canvas_xrd.addEventListener('mousemove', function(evt) {
    
    let x = xrd_gaph.scales.x.getValueForPixel(evt.offsetX);
    let y = xrd_gaph.scales.y.getValueForPixel(evt.offsetY);
    graph_coords_xrd.innerHTML = 'Coordinates: ' + x.toFixed(2) + ',' + y.toFixed(2);

    const rect = canvas_xrd.getBoundingClientRect();
    if(evt.altKey){
        if(dragExclude) {
            console.log(evt)
            selectRectExclude.w = (evt.clientX - rect.left) - selectRectExclude.startX;
            selectionContextXRD.globalAlpha = 0.5;
            selectionContextXRD.clearRect(0, 0, canvas_xrd.width, canvas_xrd.height);
            console.log(xrd_gaph)
            console.log(xrd_gaph.chartArea.bottom - xrd_gaph.chartArea.top)
            selectionContextXRD.fillRect(
                selectRectExclude.startX,
                selectRectExclude.startY,
                selectRectExclude.w,
                xrd_gaph.height
                // xrd_gaph.chartArea.bottom + xrd_gaph.chartArea.top
            );
        }else{
            selectionContextXRD.clearRect(0, 0, canvas_xrd.width, canvas_xrd.height);
            var xline = evt.clientX - rect.left;
            if (xline > xrd_gaph.chartArea.left) {
                selectionContextXRD.fillRect(
                    xline,
                    xrd_gaph.chartArea.top,
                    1,
                    xrd_gaph.chartArea.bottom - xrd_gaph.chartArea.top
                );
            }
        }
    }
});

canvas_xrd.addEventListener('mouseup', function(evt) {
    if(dragExclude){
        dragExclude = false;
    }
});

function open_exclude_region(){
    modal_open_exclude_region.toggle();
}

// function add_region(){
    // var dt = {
    //     "id": 1,
    //     "region_name": 1,
    //     "exclude_start_region": 0,
    //     "exclude_end_region": 10
    // }
    // console.log(dt)
    // table_exclude_region.updateOrAddData([dt]);
// }

function add_region(){
    Array.prototype.slice.call(form_exclude_region)
    .forEach(function (form) {
        if (!form.checkValidity()) {
        }else{
            const main_form = document.forms.namedItem("exclude_region_form");
            const dd = new FormData(main_form);
            fitting2save = Object.fromEntries(dd.entries());
            console.log(fitting2save)
            // var datatoadd = [];
            // var test_region = table_exclude_region.getData();
            // console.log(test_region)
            // if(test_region.length > 0){
            //     var start = parseFloat(fitting2save['start_exclude_region']);
            //     var pos_new_region = -1;
            //     console.log(test_region)
            //     datatoadd = [];
            //     Object.entries(test_region).forEach(([key, val]) => {
            //         var st = parseFloat(val.exclude_start_region);
            //         if(start > st){
            //             pos_new_region = -1;
            //         }else{
            //             pos_new_region = key;
            //         }
            //     })
            //     var dt = {
            //         "exclude_start_region": fitting2save['start_exclude_region'],
            //         "exclude_end_region": fitting2save['end_exclude_region'],
            //     }
            //     console.log("pos_new_region", pos_new_region)
            //     if(pos_new_region == -1){
            //         test_region.push(dt)
            //     }else{
            //         test_region.splice(pos_new_region, 0, dt);
            //     }
            //     datatoadd = [test_region];
            // }else{
            //     var dt = {
            //         "exclude_start_region": fitting2save['start_exclude_region'],
            //         "exclude_end_region": fitting2save['end_exclude_region'],
            //     }
            //     datatoadd = [dt];
            // }
            var dt = {
                "exclude_start_region": fitting2save['start_exclude_region'],
                "exclude_end_region": fitting2save['end_exclude_region'],
            }
            table_exclude_region.updateOrAddData([dt]);
            table_exclude_region.setSort("exclude_start_region", "asc");
            draw_region_graph();
        }
        form.classList.add('was-validated')
  })
}

function draw_region_graph(){
    var test_region = table_exclude_region.getData();
    var datatoadd = [];
    for (let counter = 0; counter < test_region.length; counter++) {
        var annotation = {
            type: 'box',
            backgroundColor: 'rgba(255, 245, 157, 0.2)',
            borderWidth: 0,
            xMax: 0,
            xMin: 0
          };
        annotation.xMin = test_region[counter]['exclude_start_region'];
        annotation.xMax = test_region[counter]['exclude_end_region'];
        datatoadd.push(annotation)
    }
    config_xrd_gaph.options.plugins.annotation.annotations = datatoadd;
    xrd_gaph.update();
}