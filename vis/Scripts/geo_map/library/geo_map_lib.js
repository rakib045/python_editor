/**
 * @Desc This library object holds all variables and functions for the basic customization of the geo map.
 * @namespace Map Library
 * @author Rakib Hasan
 * @version 1.0
 */
var map_library = {
    /* all variables */
    
    /**
     * @desc This variable holds the leaflet map object
     * @memberof Map Library
     * @var {object} map
     * @defaultvalue null
     * @example 
     * map_library.map = L.map('mapid');
     * or
     * var mapObj = map_library.map;
     * @author Rakib Hasan
     * @version 1.0
     */
    'map': null,

    /**
     * @desc This variable holds the leaflet sidebar object
     * @memberof Map Library
     * @var {object} sidebar
     * @defaultvalue null
     * @example 
     * map_library.sidebar = L.control.sidebar({ container: 'sidebar' });
     * or
     * var sidebarObj = map_library.sidebar;
     * @author Rakib Hasan
     * @version 1.0
     */
    'sidebar': null,

    /**
     * @desc This variable holds the leaflet printer control object
     * @memberof Map Library
     * @var {object} printer
     * @defaultvalue null
     * @example 
     * map_library.printer = L.easyPrint();
     * or
     * var printerObj = map_library.printer;
     * @author Rakib Hasan
     * @version 1.0
     */
    'printer': null,

    'baseLayers': {
        "Grayscale": null,
        "Streets": null,
        "Satelitte": null
    },
    'overlayMaps': {},
    'layers_list_array': [],
    'color_list_array': {},
    'grade_list_array': {},
    'grade_scale': {},
    'layer_name_list': [],

    'connecting_id_list': {},
    'aggregate_val_list': {},

    'button_display_list': {},
    'button_chart_type': {},
    'button_chart_option': {},

    'default_color_list': [ "#b2df8a", "#a6cee3", "#cab2d6", "#fdbf6f", "#fb9a99", "#33a02c", "#1f78b4", "#6a3d9a", "#ff7f00", "#e31a1c"],
    //'default_color_list': [ '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b', '#02214f', '#000000'],

    /* functions */

    
    /**
     * @desc Initialize the geo map using leaflet js and mapbox. It loads map base layers. It initializes the sidebar and also printer control.
     * @memberof Map Library
     * @function initializeMap
     * @returns {void}
     * @example 
     * map_library.initializeMap();
     * @author Rakib Hasan
     * @version 1.0
     */
    initializeMap : function(){
        
        var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        mbAttrS = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
        mbUrlS = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';

        // Defining map layers
        map_library.baseLayers["Grayscale"] = L.tileLayer(mbUrl, {id: 'mapbox/light-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr});
        map_library.baseLayers["Streets"]  = L.tileLayer(mbUrl, {id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr});
        map_library.baseLayers["Satelitte"] = L.tileLayer(mbUrlS, {id: 'mapbox.streets', attribution: mbAttrS});
        

        if (map_library.map != null) 
            map_library.map == null;

        map_library.map = L.map('mapid', {
            center: [51.312588, -116.021118],
            zoom: 10,
            layers: [map_library.baseLayers["Grayscale"]]
        });
        L.control.layers(map_library.baseLayers).addTo(map_library.map);
        
        map_library.initializeSideBar();
        //animation_library.initializeAnimationControl('anim_1', 'Animation Panel', 'bottomright');
        map_library.initializePrinterControl();
        
    },

    /**
     * @desc Initialize the leaflet Side Bar.
     * @memberof Map Library
     * @function initializeSideBar
     * @returns {void}
     * @example 
     * map_library.initializeSideBar();
     * @author Rakib Hasan
     * @version 1.0
     */
    'initializeSideBar': function(){
        map_library.sidebar = L.control.sidebar({ container: 'sidebar' }).addTo(map_library.map);
        //.open('home');
    },
    
    /* Initialize the leaflet Printer Control */
    'initializePrinterControl': function(){
        map_library.printer = L.easyPrint({
            title: 'Print Map',
      		tileLayer: map_library.baseLayers["Grayscale"],
      		sizeModes: ['Current', 'A4Landscape', 'A4Portrait'],
      		filename: 'myMap',
      		exportOnly: true,
      		hideControlContainer: false,
            className: 'a3CssClass'
		}).addTo(map_library.map);
    },

    /* Draw Maps with geojsons and their corresponding variable data */

    /**
     * @desc Draw the map with proper geojson files
     * @memberof Map Library
     * @function drawMap
     * @param {string} layer_name The name of the layer
     * @param {string} json_files The list of json files separated by comma ','
     * @param {string} variable_name The name of the corresponding variable
     * @param {string} connecting_id The name of the corresponding id which is defined in json (data) files
     * @param {string} aggregate_val The type of aggreagation like 'sum' or 'average'
     * @returns {void}
     * @example 
     * map_library.drawMap();
     * @author Rakib Hasan
     * @version 1.0
     */
    'drawMap': function(layer_name, json_files, variable_name, connecting_id, aggregate_val){
        //json_files = "jeoJSON_al_sk_river_flow_acc_gt_1500.json";
        if( !map_library.layer_name_list.includes(layer_name))
            map_library.layer_name_list.push(layer_name);

        loadingModal.show();

        // Check user is defining any connecting id (geojson and variable id), otherwise choose 'id' as default
        if(connecting_id == undefined)
            map_library.connecting_id_list[layer_name] = 'id';
        else
            map_library.connecting_id_list[layer_name] = connecting_id;
        
        // Check user is defining any aggregation type (geojson and variable id), otherwise choose 'average' as default
        if(aggregate_val == undefined)
            map_library.aggregate_val_list[layer_name] = 'average';
        else if(aggregate_val == 'mean' || aggregate_val == 'average')
            map_library.aggregate_val_list[layer_name] = 'average';
        else if(aggregate_val == 'total' || aggregate_val == 'sum')
            map_library.aggregate_val_list[layer_name] = 'total';
        else
            map_library.aggregate_val_list[layer_name] = aggregate_val;

        if(json_files != "")
        {

            // Split geojson files from string and put it in json_list array
            var json_list_temp = json_files.split(',');
            json_list = [];
            
            for (var k=0; k<json_list_temp.length; k++){
                if(json_list_temp[k] == "" || json_list_temp[k] == undefined)
                    continue;
                else
                    json_list.push(json_list_temp[k]);
            }

            if(json_list.length > 0){

                var actions = [];
                json_list.forEach(function(fName){
                    var temp = d3.json(fName);
                    actions.push(temp);
                });

                // Load all geojson files asynchronously
                Promise.all(actions)
                .then(function(files) {
                        
                        data_library.list_geo_json_data[layer_name] = null;
                        files.forEach(function(file, index){
                            // For first time it initializes several variables
                            if(index == 0){                                
                                data_library.list_geo_json_data[layer_name] = file;
                                data_library.variable_name_list[layer_name] = variable_name;
                                data_library.connecting_id_list[layer_name] = file.id_param_name;
                            }
                            else
                                data_library.list_geo_json_data[layer_name].features = data_library.list_geo_json_data[layer_name].features.concat(file.features);
                        });
                        console.log(data_library.list_geo_json_data[layer_name]);
                        
                        data_library.list_geo_json_data[layer_name].features.forEach(function(data){
                            // For each shape file, it loads its corresponding variable data
                            var temp = d3.json("Data\\"+variable_name+"\\Daily\\id_" + data.properties.id + ".json");
                            if (data_library.list_json_files[layer_name] == undefined)
                                data_library.list_json_files[layer_name] = [];
                            data_library.list_json_files[layer_name].push(temp);
                        });
                        data_library.total_shape_file = data_library.list_json_files[layer_name].length;

                        // It loads all json files, read it and calculate min, max
                        data_library.read_variable_jsons(layer_name, variable_name);                                                
                        

                    }).catch(function(err) {
                        console.log(err);
                    });
                                
            }           

        }


    },

    /* Draw all the shape files/geoJSON features for the corresponding layer */
    'drawShapes': function(layer_name){
        map_library.layers_list_array[layer_name] = new L.FeatureGroup();

        // Loading geoJSON
        data_library.list_geo_json_feature[layer_name] = L.geoJSON(data_library.list_geo_json_data[layer_name], {
                // Data filter method
                filter: function(feature){
                    //if (feature.properties.islake == 0) return true;
                    return true;
                },
                // Update color method
                style: function (feature) {
                    // Selecting the id
                    var c_id = feature.properties.id;
                    // Selecting gray color, if no data found
                    if (data_library.variable_data[layer_name][c_id] == undefined)
                        return {color: 'grey'};
                    
                    // Selecting color for that id from the corresponding variable data based on grading scale with color list
                    cus_color = map_library.color_list_array[layer_name][data_library.getIndexOfGrades(map_library.grade_list_array[layer_name], 
                        data_library.variable_data[layer_name][c_id][animation_library.year][animation_library.day][map_library.aggregate_val_list[layer_name]])];
                    return {color: cus_color, fillOpacity: 0.75};
                },
                // Binding methods for each feature/shape
                onEachFeature: function onEachFeature(feature, layer) {

                    // Adding feature into the layer
                    map_library.layers_list_array[layer_name].addLayer(layer);

                    // Binding click event
                    //layer.on('click', function (e) {
                    //    showMetaDataInfo( map_library.sidebar ,feature.properties.id, layer_name, [animation_library.start_year, animation_library.end_year], map_library.aggregate_val_list[layer_name]);
                    //});
                }
            })
            .bindPopup(function (d) {
                var html_str = "<div>";
                for(var i=0; i<map_library.button_display_list[layer_name].length; i++)
                {
                    html_str += "<h5><button onclick=\"showMetaDataInfo("+ d.feature.properties.id + ", '" + layer_name + "', '" 
                            + i
                            + "')\">" 
                            + map_library.button_display_list[layer_name][i] + "</button></h5><br/>";
                }
                html_str += "</div>";
                return  html_str;
            })
        // Adding it into the geo map
        .addTo(map_library.map);

        // Update layer list array
        map_library.overlayMaps[legend_library.legend_title_list[layer_name]] = map_library.layers_list_array[layer_name];
        map_library.layers_list_array[layer_name].addTo(map_library.map);
        
        // Re/initialize base layer and overlay layers into geo map
        $('.leaflet-control-layers').remove();
        L.control.layers(map_library.baseLayers, map_library.overlayMaps).addTo(map_library.map);

        // Update date and animation panel
        var theDate = new Date(animation_library.year, 0, 1);
        var myNewDate = new Date(theDate);
        theDate.setDate(theDate.getDate() + animation_library.day);

        $('#infoAnimation').html((animation_library.day+1) + "/365 day of " + animation_library.year + " (" + theDate.toDateString() + ")");
    },

    /* Update existing shapes/geoJSON features for the corresponding layer on a specific date */
    'updateChart': function(layer_name, year, day){

        layer_name_list = Object.keys(data_library.list_geo_json_feature);
        for(var i=0; i<layer_name_list.length; i++)
        {
            layer_name = layer_name_list[i];
            data_library.list_geo_json_feature[layer_name].eachLayer(function (layer) { 
                //cus_color = color_list[getIndexOfGrades(layer.feature.properties[variable_name][year][day])]; 
                // Selecting the id
                var c_id = layer.feature.properties.id;
                if (data_library.variable_data[layer_name][c_id] != undefined){
    
                    // Selecting gray color, if no data found
                    if(data_library.variable_data[layer_name][c_id][year] == undefined){
                        layer.setStyle({color : 'grey'});
                    }
                    else{
                        // Selecting color for that id from the corresponding variable data based on grading scale with color list
                        cus_color = map_library.color_list_array[layer_name][data_library.getIndexOfGrades(map_library.grade_list_array[layer_name], 
                            data_library.variable_data[layer_name][c_id][year][day][map_library.aggregate_val_list[layer_name]])];
                        layer.setStyle({color : cus_color});
                    }                
                }
                
            });
        }
        
        
        // Update date and animation panel
        var theDate = new Date(year, 0, 1);
        var myNewDate = new Date(theDate);
        theDate.setDate(theDate.getDate() + day);

        $('#infoAnimation').html((day+1) + "/365 day of " + year + " (" + theDate.toDateString() + ")");
    }

    

};

/**
 * @Desc This library object holds all variables and functions for the basic animation panel.
 * @namespace Animation Library
 * @author Rakib Hasan
 * @version 1.0
 */
var animation_library = {
    /* variables */
    // List of all animation controls and current animation object

    /**
     * @desc List of all animation controls
     * @memberof Animation Library
     * @var {object} animation_control_list
     * @defaultvalue Array of animation control objects
     * @example 
     * var animCtrlObj = animation_library.animation_control_list;
     * @author Rakib Hasan
     * @version 1.0
     */
    'animation_control_list': {},

    /**
     * @desc Running animation control
     * @memberof Animation Library
     * @var {object} anim
     * @defaultvalue null
     * @example 
     * var arunningAimCtrlObj = animation_library.anim;
     * @author Rakib Hasan
     * @version 1.0
     */
    'anim': null,

    /**
     * @desc Start year of animation control panel
     * @memberof Animation Library
     * @var {int} start_year
     * @defaultvalue 2010
     * @example 
     * var anim_start_year = animation_library.start_year;
     * or
     * animation_library.start_year = 2010;
     * @author Rakib Hasan
     * @version 1.0
     */
    'start_year': 2010,

    /**
     * @desc End year of animation control panel
     * @memberof Animation Library
     * @var {int} end_year
     * @defaultvalue 2020
     * @example 
     * var anim_end_year = animation_library.end_year;
     * or
     * animation_library.end_year = 2020;
     * @author Rakib Hasan
     * @version 1.0
     */
    'end_year': 2020,

    // Current day and year position in the running animation
    'year': 2010,
    'day': 0,

    // How many day will be added into the animation for next step
    'day_addition': 1,
    

    /* functions */
    /**
     * @desc Initialize animation control
     * @memberof Animation Library
     * @function initializeAnimationControl
     * @param {string} control_class_name The class name of the animation control panel
     * @param {string} title The title of the animation control panel
     * @param {string} pos The position object of the animation control panel
     * @returns {void}
     * @example 
     * animation_library.initializeAnimationControl();
     * @author Rakib Hasan
     * @version 1.0
     */
    'initializeAnimationControl': function(control_class_name, title, pos){
        animation_library.year = animation_library.start_year;
        animation_library.removeAnimationControl(control_class_name);
            
        animation_library.animation_control_list[control_class_name] = L.control({position: pos});
        animation_library.animation_control_list[control_class_name].onAdd = function(m){
            
            // Generate dynamic DOM for animation panel
            var div = L.DomUtil.create('div', 'info animation ' + control_class_name);
            var str = ""
            str += "<h4>"+ title +"</h4>";
            str += "<p>Date : <span id='infoAnimation'></span></p>";
            str += "<p>Jump to : ";
            str += "<select id='jumpToDay' style='margin-right:2px'>";
            for(var i=1; i<=31; i++)
                str += "<option value=" + i + ">" + i + "</option>"
            str += "</select>";

            str += "<select id='jumpToMonth' style='margin-right:2px'>";
            str += "<option value='0'>Jan</option>";
            str += "<option value='1'>Feb</option>";
            str += "<option value='2'>Mar</option>";
            str += "<option value='3'>Apr</option>";
            str += "<option value='4'>May</option>";
            str += "<option value='5'>Jun</option>";

            str += "<option value='6'>Jul</option>";
            str += "<option value='7'>Aug</option>";
            str += "<option value='8'>Sep</option>";
            str += "<option value='9'>Oct</option>";
            str += "<option value='10'>Nov</option>";
            str += "<option value='11'>Dec</option>";
            str += "</select>";

            str += "<select id='jumpToYear' style='margin-right:2px'>";
            for(var i=animation_library.start_year; i<=animation_library.end_year; i++)
                str += "<option value=" + i + ">" + i + "</option>"
            str += "</select>";

            str += "<button id='jumpToButton' onclick='animation_library.jumpToTheDay()'><i class='fa fa-play' aria-hidden='true'></i>  Go</button>";
            str += "</p>";
            str += "<p>Animation Step : <select id='stepAnimation'>";
            str += "<option value='day'> Day </option>";
            str += "<option value='month'> Month </option>";
            str += "<option value='year'> Year </option>";
            str += "</select></p>";
            str += "<button id='playAnimation' onclick='animation_library.animationNextStep()' style='margin-right: 2px;'><i class='fa fa-play' aria-hidden='true'></i>  Play</button>";
            str += "<button id='pauseAnimation' onclick='animation_library.pauseAnimation()' style='margin-right: 2px;'><i class='fa fa-pause' aria-hidden='true'></i>  Pause</button>";
            str += "<button id='stopAnimation' onclick='animation_library.stopAnimation()' style='margin-right: 2px;'><i class='fa fa-stop' aria-hidden='true'></i>  Stop and Reset</button>";

            div.innerHTML = str;
            return div;
        };
        // Add animation panle to the geo map
        animation_library.animation_control_list[control_class_name].addTo(map_library.map);
    },

    /* Remove an animation control */
    'removeAnimationControl': function(control_class_name){
        var ctrl = $('.'+control_class_name);

        if(ctrl.length > 0)
        {
            delete animation_library.animation_control_list[control_class_name];
            ctrl.remove();
        }                    
    },

    /* Load the data for a specific date */
    'jumpToTheDay': function(){
        var year_text = $('#jumpToYear').val();
        var month_text = $('#jumpToMonth').val();
        var day_text = $('#jumpToDay').val();

        var date = new Date(year_text, month_text, day_text);
        var days = Math.round(parseFloat(date - new Date(year_text, 0, 1))/24/3600/1000);

        animation_library.year = parseInt(year_text);
        animation_library.day = parseInt(days);

        map_library.layer_name_list.forEach(function(l_name, index){
            // Update chart with the specific date's values
            map_library.updateChart(l_name, year_text, days);
        });
        
    },

    /* Chossing animation next step based on daily, monthly and yearly animation and run the animation */
    /* It can also resume a pauses animation */
    'animationNextStep':function(){
        var animation_step = $('#stepAnimation').val();
        animation_library.anim = setTimeout(function(){

            // Check how many days we need to add for our next animation step
            if(animation_step == 'day')
                animation_library.day_addition = 1;
            else if (animation_step == 'year')
                animation_library.day_addition = 365;
            else if (animation_step == 'month')
            {
                var date = new Date(animation_library.year, 0, animation_library.day+1);
                date.setMonth( date.getMonth() + 1 );
                animation_library.day_addition = Math.round(parseFloat(date - new Date(animation_library.year, 0, animation_library.day+1))/24/3600/1000);
            }

            animation_library.day = animation_library.day + animation_library.day_addition;

            // Update day and year
            if(animation_library.day >= 365)
            {
                animation_library.year++;
                animation_library.day = animation_library.day - 365;
            }

            //updateChart(variable_name, animation_library.year, animation_library.day);

            map_library.layer_name_list.forEach(function(l_name, index){
                // Update the map
                map_library.updateChart(l_name, animation_library.year, animation_library.day);
            });

            // Recursive call for running the animation
            animation_library.animationNextStep();
        }, 1000);
    },

    /* Stop the animation and reset it to starting position */
    'stopAnimation':function(){
        animation_library.day = 0;
        animation_library.year = animation_library.start_year;
        clearTimeout(animation_library.anim);
        //drawMap(variable_name, year, day);
        map_library.layer_name_list.forEach(function(l_name, index){
            map_library.updateChart(l_name, animation_library.year, animation_library.day);
        });
    },

    /* Pause the animation */
    'pauseAnimation':function(){
        clearTimeout(animation_library.anim);
    }

};

/* Library for all basics about the panel for legends*/
var legend_library = {
    /* variables */
    /* List of all legend control object, title and position */
    'legend_control_list': {},
    'legend_title_list': {},
    'legend_pos_list': {},

    
    /* functions */
    /* Initialize the legend control */
    'initializeLegendControl': function(control_class_name, title, pos, color_list, legend_text){

        // Check color list items is matched with legend text items
        if(color_list.length == legend_text.length)
        { 
            legend_library.removeLegendControl(control_class_name);
            legend_library.legend_control_list[control_class_name] = L.control({position: pos});
            
            // This method will trigger while adding this legend
            legend_library.legend_control_list[control_class_name].onAdd = function(m){
                var div = L.DomUtil.create('div', 'info legend '+ control_class_name);
                div.innerHTML += "<p>"+ title +"</p>"
                for(var i=0; i<color_list.length; i++)
                {
                    div.innerHTML += '<div style="margin-bottom: 4px;"><i style="background:' + color_list[i] + '; opacity:1"></i>' + legend_text[i] + '</div>';
                }
                return div;
            }
            // Legend is added to the geo map
            legend_library.legend_control_list[control_class_name].addTo(map_library.map); 
        }
        else{
            alert('Color list items should be one item more than legend list items !!');
        }

        
    },

    /* Remove Legend control */
    'removeLegendControl': function(control_class_name){
        var ctrl = $('.'+control_class_name);

        if(ctrl.length > 0)
        {
            delete legend_library.legend_control_list[control_class_name];
            ctrl.remove();
        }                    
    },

    /* Generate and return legend texts */
    'generateLegendTexts': function(grades){
        var legend_texts = [];                
        for(var j=0; j<=grades.length; j++)
        {
            var str_label = "";
            if(j==0)
                str_label += "<= " + grades[j];
            else if(j==grades.length)
                str_label += ">= " + grades[j-1];                                   
            else
                str_label += grades[j-1] + " - " + grades[j];
            
            legend_texts.push(str_label);
        }
        return legend_texts;
    }
};

/* Library for all basics about the map data - geojson, variables data and metadata*/
var data_library = {

    /* variables */
    'file_count': 100,
    'total_shape_file': 0,
    'loaded_shape_files': 0,

    /* lists of all variables names and the connecting ids for that variables with geojson data */
    'variable_name_list': {},
    'connecting_id_list': {},

    'minVal': 1000000,
    'maxVal': -1000000,
    
    /* lists of all json files, geo_json data and geojson features (required for updated shape colors) */
    'list_json_files': {},
    'list_geo_json_data': {},
    'list_geo_json_feature': {},

    /* lists of all variables data */
    'variable_data': {},

    /* functions */
    /* Generate and return grades for linear scale*/
    'getScaleGradesLinear': function(minVal, maxVal, no_steps){
        var steps_len = (maxVal-minVal)/no_steps;
        custom_grades = [];
        var prev_val = minVal;
        for(var i=0; i<no_steps-1; i++)
        {
            var val = Math.round(prev_val + steps_len);
            custom_grades.push(val);
            prev_val = val;
        }
        return custom_grades;
    },

    /* Generate and return grades for logarithmic scale*/
    'getScaleGradesLogarithmic': function(val_min, val_max, log_min, log_max, no_steps){
        custom_grades = [];
        var steps_len = (parseInt(log_max - log_min) / no_steps);
        for (var i = 0; i < no_steps; i++) {
            var d = val_max - parseInt((Math.log(log_min+ i*steps_len) - Math.log(log_min)) / (Math.log(log_max) - Math.log(log_min)) * (val_max - val_min));
            custom_grades.push(d.toFixed(2));
        }
        custom_grades = custom_grades.reverse();
        custom_grades.pop();
        return custom_grades
    },

    /* Get the index of a value from the whole grades */
    'getIndexOfGrades': function(grades, val){
        for(var i=0; i<grades.length; i++)
        {
            if(val <= grades[i])
                return i;
        }
        return i;
    },

    /* Read all json files containing variable data */
    'read_variable_jsons': async function(layer_name, variable_name){
        
        // list of all json files in this tem array
        var temp_jsons = [];
        for(var i=0; i<data_library.list_json_files[layer_name].length; i++)
        {
            if(i<data_library.file_count)
                temp_jsons.push(data_library.list_json_files[layer_name][i]);
            else
                break;
        }
        //console.log(temp_jsons);

        // Loading all json files asynchronously
        await Promise.allSettled(temp_jsons).then(function(files) {
            //console.log(files);

            // temp object holds all file information  
            var temp = {};
            files.forEach(function(file, index){
                //console.log(file.segment_id);      
                if(file.status == 'fulfilled')                          
                    temp[file.value[map_library.connecting_id_list[layer_name]]] = file.value.data;
                else
                    console.log(file.status);                                
            });
            
            for (var attrname in temp) { 
                if (data_library.variable_data[layer_name] == undefined)
                    data_library.variable_data[layer_name] = [];
                data_library.variable_data[layer_name][attrname] = temp[attrname]; 
            }
            
           
            var seg_ids = Object.keys(temp);
            data_library.loaded_shape_files += seg_ids.length;
            //console.log(seg_ids.length);
            var percentage_val = parseInt(data_library.loaded_shape_files/data_library.total_shape_file * 100);

            $('#shapeLoadedFileCount').html(data_library.loaded_shape_files);
            $('#shapeTotalFileCount').html(data_library.total_shape_file);

            $('#loadingProgress').width(percentage_val+'%');
            $('#loadingProgress').attr('aria-valuenow', percentage_val);
            
            // Calculate max and min value from all the json files
            for(var i=0; i<seg_ids.length; i++)
            {
                var temp_data = data_library.variable_data[layer_name][seg_ids[i]];

                //var years = Object.keys(temp_data);
                var years = [];
                for(var index=animation_library.start_year; index <= animation_library.end_year; index++)
                    years.push(index);

                for(var j=0; j<years.length; j++){                    
                    var days_data = [];

                    for(var index=0; index< Object.keys(temp_data[years[j]]).length; index++)
                        days_data.push(temp_data[years[j]][index]['average']);

                    var days = Object.keys(days_data);
                    for( var k=0; k<days.length; k++){
                        
                        var temp_val = days_data[days[k]];
                        if(temp_val < data_library.minVal)
                        data_library.minVal = temp_val;
                        
                        if(temp_val > data_library.maxVal)
                        data_library.maxVal = temp_val;
                    }
                }
            }

            // When all json files read will be completed, it goes inside this block of code
            if(data_library.list_json_files[layer_name].length < data_library.file_count)
            {               
                
                console.log(data_library.minVal);
                console.log(data_library.maxVal);
                //console.log(data_library.variable_data[layer_name].length);

                loadingModal.hide();
                // Check user passed any color_list_array or choose default
                if (map_library.color_list_array[layer_name] == undefined)
                {
                    map_library.color_list_array[layer_name] = map_library.default_color_list;
                }

                // Check user passed any grade_list_array or choose default linear scale
                if (map_library.grade_list_array[layer_name] == undefined)
                {
                    if(map_library.grade_scale[layer_name] == 'logarithmic')
                        map_library.grade_list_array[layer_name] = data_library.getScaleGradesLogarithmic(data_library.minVal, data_library.maxVal, data_library.minVal+1, data_library.maxVal*2/3, map_library.color_list_array[layer_name].length);
                    else
                        map_library.grade_list_array[layer_name] = data_library.getScaleGradesLinear(data_library.minVal, data_library.maxVal, map_library.color_list_array[layer_name].length);
                }

                // Check user passed any legend title or choose layer name as default
                if(legend_library.legend_title_list[layer_name] == undefined){
                    legend_library.legend_title_list[layer_name] = layer_name;
                }

                // Check user passed any legend position or choose bottom left as default
                if(legend_library.legend_pos_list[layer_name] == undefined){
                    legend_library.legend_pos_list[layer_name] = 'bottomleft';
                }
                
                
                // It initializes a legend control
                legend_library.initializeLegendControl('legend_'+layer_name, 
                            legend_library.legend_title_list[layer_name], 
                            legend_library.legend_pos_list[layer_name], 
                            map_library.color_list_array[layer_name], 
                            legend_library.generateLegendTexts(map_library.grade_list_array[layer_name])
                            );

                //setScaleGradesLogarithmic(minVal, maxVal, 1, 61457, color_list.length);
                //setScaleGradesLogarithmic(minVal, maxVal, 1, maxVal*2/3, color_list.length);

                //console.log(custom_grades);

                
                //for(var j=0; j< color_list.length; j++){
                //    layers.push(L.layerGroup());
                //}
                
                // It draws all the shapes for that layer_name
                map_library.drawShapes(layer_name);

                // Reseting min and max value
                data_library.minVal = 1000000;
                data_library.maxVal = -1000000;

                return;
            }
            
            // Remove the filenames from the list that has been read and call the recursive method
            data_library.list_json_files[layer_name].splice(0, data_library.file_count);
            data_library.read_variable_jsons(layer_name, variable_name);
            

        });
    }


}



