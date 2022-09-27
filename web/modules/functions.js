var store_row = null,
    store_row_data= null,
    res_data = "",
    res_db = "",
    graph_data = "",
    init_data = "",
    data_interface = "",
    browser_choice = 1,
    tools = null
    init_graph_strain = 0,
    init_graph_dw = 0,
    model_strain_dw = null,
    change_model = 0,
    splash_time = 5000,
    radioValue = 0,
    after_one_fit = 0,
    save_bounds_values_4_restore = "",
    nb_cycle_max_save = 0;
    val2save = "",
    fitting2save = "",
    crystal_choice_select = 0,
    crystal_choice_select_sub = 0,
    dragPointsX = false,
    dragPointsY = false,
    scale_min_strain = 0,
    scale_max_strain = 1,
    scale_min_dw = 0,
    scale_max_dw = 1,
    dw_chart_zoomed = 0,
    strain_chart_zoomed = 0,
    startingValueDrag = 0,
    value2add = 0,
    previous_value = 0,
    isROI = false,
    rectROI = {},
    dragROI = false,
    dragExclude = false,
    cntrlIsPressed = false,
    isSelectedPoints = false,
    SelectedPoints = [],
    rowSelect = 0,
    delete_switch_value = false,
    exclude_region_data = [],
    DateTime = luxon.DateTime;

let table_strain_dw_values = null,
    table_database = null,
    table_exclude_region = null,
    table = null;

let chart_x_start = 0,
    chart_y_start = 0,
    chart_x_end = 0,
    chart_y_end = 0,
    x_start = 0,
    y_start = 0,
    x_end = 0,
    y_end = 0;

var roi_coord = {
    "chart_x_start": 0,
    "chart_x_end": 0,
    "chart_y_start": 0,
    "chart_y_end": 0,
};

var xrd_bounds = {
    "xmin_xrd": 0,
    "xmax_xrd": 0
};

var selectRectExclude = {
    w: 0,
    startX: 0,
    startY: 0
};

var graph_colors_equivalents = {
    "color_strain_modal": "c_strain",
    "color_dw_modal": "c_dw",
    "color_xrd_data_modal": "c_data",
    "color_xrd_fit_modal": "c_fit",
    "color_xrd_live_modal": "c_fit_live",
};

let img_schem_list = {
    0: "Scheme_SingleCrystal.png",
    1: "Scheme_ThinFilm.png",
    2: "Scheme_ThickFilm.png",
    3: "Scheme_ThickFilmAndSubstrate.png"
    },
    par_lattice = ['a', 'b', 'c', 'alpha', 'beta', 'gamma'],
    param_lattice = ['a_lattice', 'b_lattice', 'c_lattice', 'alpha_lattice', 'beta_lattice', 'gamma_lattice'];

const container = document.querySelector("#parameters_pane"),
    click_update_1 = document.getElementById("click_update_1"),
    click_update_2 = document.getElementById("click_update_2"),
    new_project = document.getElementById("new_project"),
    load_project = document.getElementById("load_project"),
    loads_xrd = document.getElementById("loads_xrd"),
    loads_strain = document.getElementById("loads_strain"),
    loads_dw = document.getElementById("loads_dw"),
    save_file = document.getElementById("save_file"),
    save_as_file = document.getElementById("save_as_file"),
    export_fits = document.getElementById("export_fits"),
    menu_file_hide = document.getElementById("menu_file_hide"),
    menu_about_hide = document.getElementById("menu_about_hide"),
    menu_options_hide = document.getElementById("menu_options_hide"),
    path_name = document.getElementById("path_name"),
    current_name = document.getElementById("current_name");
    old_directory = document.getElementById("old_directory");

const radmax_tab = document.getElementById("radmax-tab"),
    about_modal = document.getElementById("about_modal"),
    general_options_modal = document.getElementById("general_options_modal"),
    graph_colors_modal = document.getElementById("graph_colors_modal"),
    sounds_open = document.getElementById("sounds_open"),
    sounds_play = document.getElementById("sounds_play"),
    radmax_use_database = document.getElementById("radmax_use_database"),
    database_panel = document.getElementById("database_pane-tab"),
    radmax_version = document.getElementById("radmax_version"),
    labelImage = document.getElementById("sheme_img"),
    crystal_choice = document.getElementById('crystal_choice_m'),
    crystal_choice_s = document.getElementById('crystal_choice_s'),
    dw_function = document.getElementById('dw_basis_func');

const  modal_wait = document.getElementById("myModal"),
    img = document.getElementById("myImg"),
    modalImg = document.getElementById("img01"),
    captionText = document.getElementById("caption"),
    captionTextWait = document.getElementById("caption_wait"),
    hide_film_thickness = document.getElementById("hide_film_thickness"),
    hide_film_thickness_substrate = document.getElementById("hide_film_thickness_substrate"),
    delete_switch = document.getElementById('DeleteDataSwitch'),
    DragXPoints = document.getElementById('DragXPoints'),
    hide_drag_hor = document.getElementById('hide_drag_hor'),
    drag_hor_strain = document.getElementById('drag_hor_strain'),
    drag_hor_dw = document.getElementById('drag_hor_dw'),
    bubble_strain = document.getElementById('bubble_strain'),
    bubble_dw = document.getElementById('bubble_dw'),
    fitting_options = document.getElementById('fitting_options');

// const strain_dw_values = document.getElementById('strain_dw_values');
const width_left_hide = document.getElementById('width_left_hide'),
    width_right_hide = document.getElementById('width_right_hide'),
    shape_left_hide = document.getElementById('shape_left_hide'),
    shape_right_hide = document.getElementById('shape_right_hide'),
    b_bell_hide = document.getElementById('b_bell_hide'),
    width_left_label = document.getElementById('width_left_label'),
    shape_left_label = document.getElementById('shape_left_label'),
    shape_right_label = document.getElementById('shape_right_label'),
    width_right_label = document.getElementById('width_right_label'),
    spinner_fit_hide = document.getElementById('spinner_fit_hide'),
    parameters_pane_tab = document.getElementById('parameters_pane-tab'),
    fitting_pane_tab = document.getElementById('fitting_pane-tab'),
    geometry_pane_tab = document.getElementById('geometry_pane-tab'),
    database_pane_tab = document.getElementById('database_pane-tab'),
    start_fit_button = document.getElementById('start_fit_button'),
    stop_fit_button = document.getElementById('stop_fit_button'),
    strain_button_restore = document.getElementById('strain_button_restore'),
    dw_button_restore = document.getElementById('dw_button_restore'),
    boh_button_restore = document.getElementById('boh_button_restore'),
    fit_state_hide = document.getElementById('fit_state_hide'),
    fit_residual_hide = document.getElementById('fit_residual_hide'),
    fit_state_error_hide = document.getElementById('fit_state_error_hide'),
    fit_state_success_hide = document.getElementById('fit_state_success_hide'),
    fit_error = document.getElementById('fit_error'),
    gsa_current_cycle = document.getElementById('gsa_current_cycle'),
    nb_cycle_max = document.getElementById('nb_cycle_max'),
    strain_scale = document.getElementById('strain_scale'),
    dw_scale = document.getElementById('dw_scale'),
    fitting_choice = document.getElementById('fitting_choice'),
    resolution_func = document.getElementById('resolution_func'),
    model_strain = document.getElementById('model_strain'),
    modal_fitting_options = document.getElementById('modal_fitting_options'),
    modal_strain_dw_values = document.getElementById('modal_strain_dw_values'),
    color_strain_modal = document.getElementById('color_strain_modal'),
    color_dw_modal = document.getElementById('color_dw_modal'),
    color_xrd_data_modal = document.getElementById('color_xrd_data_modal'),
    color_xrd_fit_modal = document.getElementById('color_xrd_fit_modal'),
    color_xrd_live_modal = document.getElementById('color_xrd_live_modal'),
    modal_change_limits = new bootstrap.Modal(document.getElementById('modal_change_limits')),
    modal_change_basis_function = new bootstrap.Modal(document.getElementById('modal_change_basis_function')),
    modal_export_fit_not_working = new bootstrap.Modal(document.getElementById('modal_export_fit_not_working')),
    modal_load_xrd_before_save_project = new bootstrap.Modal(document.getElementById('modal_load_xrd_before_save_project')),
    modal_directory_no_longer_exist = new bootstrap.Modal(document.getElementById('modal_directory_no_longer_exist')),
    modal_error_delete_data_from_db = new bootstrap.Modal(document.getElementById('modal_error_delete_data_from_db')),
    modal_fit_ending_wrong = new bootstrap.Modal(document.getElementById('modal_fit_ending_wrong')),
    modal_about = new bootstrap.Modal(document.getElementById('modal_about')),
    modal_options = new bootstrap.Modal(document.getElementById('modal_options')),
    modal_colors = new bootstrap.Modal(document.getElementById('modal_colors')),
    modal_check_input_file = new bootstrap.Modal(document.getElementById('modal_check_input_file')),
    modal_open_exclude_region = new bootstrap.Modal(document.getElementById('modal_open_exclude_region')),
    start_exclude_region = document.getElementById('start_exclude_region'),
    end_exclude_region = document.getElementById('end_exclude_region'),
    modal_delete_region = document.getElementById('modal_delete_region'),
    checkboxAllDW = document.getElementsByClassName('checkbox_check_all_dw')[0],
    checkboxAllStrain = document.getElementsByClassName('checkbox_check_all_strain')[0];

const canvas_strain = document.getElementById("strain_canvas"),
    ctx_strain = canvas_strain.getContext("2d"),
    canvas_dw = document.getElementById("dw_canvas"),
    ctx_dw = canvas_dw.getContext("2d"),
    overlay_strain = document.getElementById('overlay_strain'),
    overlay_dw = document.getElementById('overlay_dw'),
    selectionContextStrain = overlay_strain.getContext('2d'),
    selectionContextDw = overlay_dw.getContext('2d'),
    canvas_xrd = document.getElementById("xrd_graph"),
    overlay_xrd = document.getElementById('overlay_xrd'),
    selectionContextXRD = overlay_xrd.getContext('2d'),
    ctx_xrd = canvas_xrd.getContext("2d"),
    strain_chart = new Chart(canvas_strain, config_strain),
    dw_chart = new Chart(canvas_dw, config_dw),
    xrd_gaph = new Chart(ctx_xrd, config_xrd_gaph),
    graph_coords = document.getElementById('graph_coords_strain_dw'),
    graph_coords_xrd = document.getElementById('graph_coords_xrd');

overlay_strain.width = canvas_strain.width;
overlay_strain.height = canvas_strain.height;
overlay_dw.width = canvas_dw.width;
overlay_dw.height = canvas_dw.height;
overlay_xrd.width = canvas_xrd.width;
overlay_xrd.height = canvas_xrd.height;

stop_fit_button.classList.add('disabled');
modal_delete_region.classList.add('disabled');

const list_crystal_choice = new Choices(crystal_choice, {
    allowHTML: true,
    removeItemButton: true,
    searchEnabled: true,
    placeholderValue: "Choose an element",
    addItems: true,
    removeItems: true,
});

const list_crystal_choice_s = new Choices(crystal_choice_s, {
    allowHTML: true,
    removeItemButton: true,
    searchEnabled: true,
    placeholderValue: "Choose an element",
    addItems: true,
    removeItems: true,
});


function isKeyPressed(event) {
    if (event.ctrlKey) {
        cntrlIsPressed = true;
    } else {
        cntrlIsPressed = false;
    }
}

// Dark theme function
const bootstrap_theme_path = "css/boostrap.min.css",
    tabulator_theme_path = "modules/plug_in/tabulator/css/tabulator_read.min.css",
    bootstrap_theme = document.getElementById("theme_for_bootstrap"),
    theme_bootstrap_choice = document.getElementById("theme_bootstrap_choice"),
    tabulator_theme = document.getElementById("theme_for_tabulator");

theme_bootstrap_choice.addEventListener('change', function(e) {
    change_theme(this.value, 1);
    apply_theme(this.value);
});

function apply_theme(val){
    color_apply = ""; 
    color_grid_apply = ""; 
    color_dark = "#adafae";
    color_not_dark = Chart.defaults.color;
    color_grid = Chart.defaults.borderColor;
    bootstrap_theme.setAttribute("href", bootstrap_theme_path);
    tabulator_theme.setAttribute("href", tabulator_theme_path);
    if(val == 0){
        color_apply = color_not_dark;
        color_grid_apply = color_grid;
    }
    else if (val == 1 || val == 2 || val == 5){
        color_apply = color_dark;
        color_grid_apply = color_dark;
    }else{
        color_apply = color_not_dark;
        color_grid_apply = color_grid;
    }
    config_strain.options.scales.y.ticks.color = color_apply;
    config_strain.options.scales.x.ticks.color = color_apply;
    config_strain.options.scales.x.title.color = color_apply;
    config_strain.options.scales.y.title.color = color_apply;
    config_strain.options.scales.y.grid.color = color_grid_apply;
    config_strain.options.scales.x.grid.color = color_grid_apply;
    strain_chart.update();
    config_dw.options.scales.y.ticks.color = color_apply;
    config_dw.options.scales.x.ticks.color = color_apply;
    config_dw.options.scales.x.title.color = color_apply;
    config_dw.options.scales.y.title.color = color_apply;
    config_dw.options.scales.y.grid.color = color_grid_apply;
    config_dw.options.scales.x.grid.color = color_grid_apply;
    dw_chart.update();
    config_xrd_gaph.options.scales.y.ticks.color = color_apply;
    config_xrd_gaph.options.scales.x.ticks.color = color_apply;
    config_xrd_gaph.options.scales.x.title.color = color_apply;
    config_xrd_gaph.options.scales.y.title.color = color_apply;
    config_xrd_gaph.options.scales.y.grid.color = color_grid_apply;
    config_xrd_gaph.options.scales.x.grid.color = color_grid_apply;
    xrd_gaph.update();
}

table_strain_dw_values = new Tabulator("#table_strain_dw_values", {
    layout:"fitColumns",
    data: [],
    movableColumns:false,
    resizableRows:false,
    columns:[
        {title:"Index", field:"name", headerSort:false},
        {title:"Depth", field:"x_value", headerSort:false},
        {title:"Strain", field:"strain", headerSort:false, editor:true},
        {
            title: "<input id='checkbox_check_all_strain' class='checkbox_check_all_strain' type='checkbox'/>",
            field: "strain_choice",
            width: "5%",
            headerSort:false,
            formatter: function(cell, formatterParams) {
              if(cell.getValue() == true){
                  return '<input type="checkbox" checked class="checkbox_check_strain">';
              }else{
                  return '<input type="checkbox" class="checkbox_check_strain">';
              }
            },
        },
        {title:"DW", field:"dw", headerSort:false, editor:true},
        {
            title: "<input id='checkbox_check_all_dw' class='checkbox_check_all_dw' type='checkbox'/>",
            field: "dw_choice",
            width: "5%",
            headerSort:false,
            frozen:true,
            formatter: function(cell, formatterParams) {
              if(cell.getValue() == true){
                  return '<input type="checkbox" checked class="checkbox_check_dw">';
              }else{
                  return '<input type="checkbox" class="checkbox_check_dw">';
              }
            },
        }
    ]
});

table_strain_dw_values.on("headerClick", function(event, row){
    var data = table_strain_dw_values.getData();
    if(event.path[0].className == 'checkbox_check_all_strain'){
        var is_checked = false; 
        if(event.path[0].checked){
            is_checked = true
        }
        Object.entries(data).forEach(([key, val]) => {
            val.strain_choice = is_checked;
        })
    }
    if(event.path[0].className == 'checkbox_check_all_dw'){
        var is_checked = false; 
        if(event.path[0].checked){
            is_checked = true
        }
        Object.entries(data).forEach(([key, val]) => {
            val.dw_choice = is_checked;
        })
    }
    table_strain_dw_values.clearData();
    table_strain_dw_values.updateOrAddData([data]);
});

table_strain_dw_values.on("rowClick", function(event, row){
    var store_row_data = row.getData();
    var test_in = 0;
    if(event.path[0].className == 'checkbox_check_strain'){
        if(event.path[0].checked){
            store_row_data.strain_choice = true;
        }else{
            store_row_data.strain_choice = false;
        }
        which_check = 1;
        which_check_class = 'checkbox_check_all_strain';
        test_in = 1;
    }else if(event.path[0].className == 'checkbox_check_dw'){
        if(event.path[0].checked){
            store_row_data.dw_choice = true;
        }else{
            store_row_data.dw_choice = false;
        }
        which_check = 0;
        which_check_class = 'checkbox_check_all_dw';
        test_in = 1;
    }
    if(test_in == 1){
        table_strain_dw_values.updateData([store_row_data]);
        test_checked_all(which_check, which_check_class);
    }
});

function test_checked_all(vv, cl){
    var ar  = []
    var loop = 0
    var data = table_strain_dw_values.getData();
    Object.entries(data).forEach(([key, val]) => {
        var res = val.dw_choice;
        if (vv == 1){
            res = val.strain_choice;
        }
        if(res){
            ar.push(1)
        }
        loop += 1;
    });
    if (Array.isArray(ar) && ar.length) {
        if(ar.length == loop){
            document.getElementById(cl).checked = true;
        }else{
            document.getElementById(cl).checked = false;
        }
    }else{
        document.getElementById(cl).checked = false;
    }
}

// var dateFormatter = function(cell, formatterParams){
//     var value = cell.getValue();
//     if(value){
//         value = DateTime.fromSQL(value).toFormat('yyyy-LL-dd HH:mm:ss');
//     }
//     return value;
// }

table_database = new Tabulator("#table_database", {
    layout:"fitDataFill",
    data: [],
    selectable:1,
    pagination:"local",       //paginate the data
    paginationSize:15,         //allow 7 rows per page of data
    movableColumns:false,      //allow column order to be changed
    resizableRows:false,       //allow row order to be changed
    paginationCounter:"rows",
    placeholder: "No data available",
    initialSort:[             //set the initial sort order of the data
        {column:"date", dir:"desc"},
    ],
    columns:[
        {title:"id", field:"id", visible:false},
        {title:"Date", field:"date", sorter:"datetime",
            sorterParams:{
                format:"yyyy-LL-dd HH:mm:ss",
                alignEmptyValues:"top",
            }
        },
        {title:"Exp. name", field:"exp_name"},
        {title:"Crystal name", field:"crys_name"},
        {title:"Fit algo.", field:"fit_algo"},
        {title:"Fit success", field:"fit_success"},
        {title:"Residual", field:"residual"},
        {title:"Geometry", field:"geometry"},
        {title:"Model", field:"model"}
    ]
});

table_database.on("rowClick", function(e, row){
    store_row_data = row.getData();
    if(!delete_switch_value){
        read_db_data(store_row_data['id'])
    }
});

document.getElementById("select-all").addEventListener("click", function(){
    table_database.selectRow();
});

document.getElementById("deselect-all").addEventListener("click", function(){
    table_database.deselectRow();
});

function delete_row_table(){
    table_database.deleteRow(store_row_data['id']);
}

/* <button id="select-all" type="button" class="btn btn-primary">Select All</button>
<button id="deselect-all" type="button" class="btn btn-primary">Deselect All</button> */

table_exclude_region = new Tabulator("#table_exclude_region", {
    height:"311px",
    layout:"fitColumns",
    data: [],
    selectable:1,
    // pagination:"local",       //paginate the data
    paginationSize:15,         //allow 7 rows per page of data
    movableColumns:false,      //allow column order to be changed
    resizableRows:true,       //allow row order to be changed
    initialSort:[             //set the initial sort order of the data
        {column:"exclude_start_region", dir:"asc"}
    ],
    columns:[
        {
            title:"Start region",
            field:"exclude_start_region",
            width:200,
            hozAlign:"left",
            headerHozAlign:"left",
            sorter:"number",
            headerSort:false
        },
        {
            title:"End region",
            field:"exclude_end_region",
            width:200,
            hozAlign:"left",
            headerHozAlign:"left",
            sorter:"number",
            headerSort:false
        },
    ]
});

table_exclude_region.on("rowSelected", function(row){
    rowSelect = row;
    modal_delete_region.classList.remove('disabled');
})

table_exclude_region.on("rowDeselected", function(e){
    rowSelect = 0;
    modal_delete_region.classList.add('disabled');
})

function delete_region(){
    table_exclude_region.deleteRow(rowSelect);
    modal_delete_region.classList.add('disabled');
    draw_region_graph();
}

function validate(evt) {
    var theEvent = evt || window.event;
    // Handle paste
    if (theEvent.type === 'paste') {
        key = evt.clipboardData.getData('text/plain');
    } else {
    // Handle key press
        var key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key);
    }
    var regex = /[0-9]|\./;
    if( !regex.test(key) ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
  }

const allRanges = document.querySelectorAll(".range-wrap");
allRanges.forEach(wrap => {
    const range = wrap.querySelector(".range");
    const bubble = wrap.querySelector(".bubble");

    range.addEventListener("input", () => {
        setBubble(range, bubble);
    });
    setBubble(range, bubble);
});

function setBubble(range, bubble) {
    const val = range.value;
    const min = range.min ? range.min : 0;
    const max = range.max ? range.max : 100;
    const newVal = Number(((val - min) * 100) / (max - min));
    bubble.innerHTML = val;

    // Sorta magic numbers based on size of the native UI thumb
    bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
}

function fill_crystal(res, element) {
    element.clearChoices();
    var val2append = [];
    for (var i = 0; i < res.length; i++) {
        tempappend = new Object();
        tempappend.selected = false;
        if (i == 0) {
            tempappend.selected = true;
        }
        tempappend.value = res[i];
        tempappend.label = res[i];
        val2append.push(tempappend);
    }
    element.setChoices(val2append);
}