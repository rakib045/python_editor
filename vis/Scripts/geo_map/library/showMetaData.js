function previewMetaDataInfo(seg_id, layer_name, feature){
    
    if(sidebar_library.preview_geofeature != null)
        sidebar_library.preview_geofeature.removeFrom(map_library.map);

    var selection_color = sidebar_library.color_list[0].color;
    for(var i=0; i<sidebar_library.color_list.length; i++)
        if(sidebar_library.color_list[i].available){
            selection_color = sidebar_library.color_list[i].color;
            break;
        }
        
    var geoFeature = L.geoJson(feature, {
        style: function (feature) {            
            return {'color': selection_color, opacity: 0.85, weight : 3, fillOpacity: 0};
        }
    }).addTo(map_library.map);

    //var bounding_points = geoFeature.getBounds();
    //L.rectangle(bounding_points, {color: selection_color, weight: 1, fillOpacity: 0.1}).addTo(map_library.map);
    sidebar_library.preview_geofeature = geoFeature;
    sidebar_library.preview_feature = feature;
    var button_str = "<div>";
    button_str += "<button width='10px' height='10px' style='background-color: "+selection_color+";border: 1px solid black;width: 10px;height: 25px;margin-right: 5px;float: right;' disabled=''></button>"
    button_str += "<a onclick=\'addToSideBar("+seg_id + ',\"' + layer_name +"\",\"" + selection_color + "\")\'";
    button_str += "class='btn btn-outline-primary' target='_blank' title='Pin to Sidebar'><i class='fa fa-thumb-tack'></i></a>";
    button_str += "<a onclick=\'addComparisonTable("+seg_id + ',\"' + layer_name +"\",\"" + selection_color + "\")\'";
    button_str += "class='btn btn-outline-primary' target='_blank' title='Add to Comparison Table' style='margin-left: 5px;'><i class='fa fa-files-o'></i></a>";
    button_str += "</div>";
    sidebar_library.addHTMLToSideBar('preview', button_str);

    var section_preview_div = sidebar_library.appendSectionToPanelIntoSideBar('preview', 'Shape Details', 1000);
    var year_range = [animation_library.start_year, animation_library.end_year];
    var aggregate_val = 'average';

    var meta_data_str = "";

    // Filling empty chart option
    for(var i=0; i < sidebar_library.sidebar_option[layer_name].length; i++)
    {
        if(sidebar_library.sidebar_option[layer_name][i].section_id == undefined)
            sidebar_library.sidebar_option[layer_name][i].section_id = 0;
        if(sidebar_library.sidebar_option[layer_name][i].layer_name == undefined)
            sidebar_library.sidebar_option[layer_name][i].layer_name = layer_name;
    }

    d3.json("Data/MetaData/" + data_library.connecting_id_list[layer_name] + "_" + seg_id + ".json").then(function(d) {
        var data = d.data;

        sidebar_library.openPanelIntoSideBar('preview');

        meta_data_str += appendHTMLTextForMetadata('Primary ID', seg_id, true);
        meta_data_str += "<div>Variable Name : " + data_library.variable_name_list[layer_name] + "</div>";
        meta_data_str += "<div>Layer Name : " + layer_name + "</div>";
        meta_data_str += appendHTMLTextForMetadata('GRU ID', data.GRU_ID, false);
        meta_data_str += appendHTMLTextForMetadata('HRU ID', data.HRU_ID, true);
        meta_data_str += appendHTMLTextForMetadata('Length', data.Length, true);
        meta_data_str += appendHTMLTextForMetadata('Flow Accumulation', data.flow_acc, true);
        meta_data_str += appendHTMLTextForMetadata('Lake Name', data.Lake_name, false);
        meta_data_str += appendHTMLTextForMetadata('Lake Area', data.Lake_area, true);
        meta_data_str += appendHTMLTextForMetadata('HRU Area', data.HRU_area, true);
        meta_data_str += appendHTMLTextForMetadata('Center Latitude', data.center_lat, true);
        meta_data_str += appendHTMLTextForMetadata('Center Longitude', data.center_lon, true);

        $('#' + section_preview_div).html(meta_data_str);

        sidebar_library.sidebar_option[layer_name] = sidebar_library.sidebar_option[layer_name].sort((a, b) => (a.section_id > b.section_id) ? 1 : -1);

        var temp_array_index = [];
        var index = 0;
        var div_id = "";
        for(var i=0; i < sidebar_library.sidebar_option[layer_name].length; i++)
        {            
            if(temp_array_index.indexOf(sidebar_library.sidebar_option[layer_name][i].section_id) == -1)
            {
                div_id = sidebar_library.appendSectionToPanelIntoSideBar('preview', sidebar_library.sidebar_option[layer_name][i].title, 
                    sidebar_library.sidebar_option[layer_name][i].section_id);                
                temp_array_index.push(sidebar_library.sidebar_option[layer_name][i].section_id);
                index++;
            }

            var chart_id = div_id + "_" + sidebar_library.sidebar_option[layer_name][i].section_id + i;
            $('#'+div_id).append("<div id='"+ chart_id +"'></div>");

            if(sidebar_library.sidebar_option[layer_name][i].chart_type == 'Heatmap')
                drawHistoryHeatMapChart('#' + chart_id, seg_id, sidebar_library.sidebar_option[layer_name][i].layer_name, 
                    year_range, sidebar_library.sidebar_option[layer_name][i]);
            else if (sidebar_library.sidebar_option[layer_name][i].chart_type == 'LineChart')
                drawHistoryLineChartChart('#' + chart_id, seg_id, sidebar_library.sidebar_option[layer_name][i].layer_name, 
                    year_range, sidebar_library.sidebar_option[layer_name][i]);
            
            

        }

    });

}

function addToSideBar(seg_id, layer_name, color){
    console.log(seg_id + layer_name + color);

    for(var i=0; i<sidebar_library.color_list.length; i++)
        if(sidebar_library.color_list[i].color == color){
            sidebar_library.color_list[i].available = false;
            break;
        }

    sidebar_library.addPanelIntoSideBar(seg_id, 'Segment ID - ' + seg_id, 'fa-thumb-tack', color);
    var obj = {'seg_id': seg_id, 'geofeature': sidebar_library.preview_geofeature}
    sidebar_library.pinned_feature_list.push(obj);
    sidebar_library.preview_geofeature = null;

    var button_str = "<div>";
    button_str += "<button width='10px' height='10px' style='background-color: "+color+";border: 1px solid black;width: 10px;height: 25px;margin-right: 5px;float: right;' disabled=''></button>"
    button_str += "<a onclick=\'removeFromSideBar("+seg_id + ',\"' + layer_name +"\",\"" + color + "\")\'";
    button_str += "class='btn btn-outline-danger' target='_blank' title='Unpin to Sidebar'><i class='fa fa-ban'></i></a>";
    button_str += "<a onclick=\'addComparisonTable("+seg_id + ',\"' + layer_name +"\",\"" + color + "\")\'";
    button_str += "class='btn btn-outline-primary' target='_blank' title='Add to Comparison Table' style='margin-left: 5px;'><i class='fa fa-files-o'></i></a>";
    button_str += "</div>";
    sidebar_library.addHTMLToSideBar(seg_id, button_str);


    var section_preview_div = sidebar_library.appendSectionToPanelIntoSideBar(seg_id, 'Shape Details', 1000);
    var year_range = [animation_library.start_year, animation_library.end_year];

    var meta_data_str = "";

    // Filling empty chart option
    for(var i=0; i < sidebar_library.sidebar_option[layer_name].length; i++)
    {
        if(sidebar_library.sidebar_option[layer_name][i].section_id == undefined)
            sidebar_library.sidebar_option[layer_name][i].section_id = 0;
        if(sidebar_library.sidebar_option[layer_name][i].layer_name == undefined)
            sidebar_library.sidebar_option[layer_name][i].layer_name = layer_name;
    }

    d3.json("Data/MetaData/" + data_library.connecting_id_list[layer_name] + "_" + seg_id + ".json").then(function(d) {
        var data = d.data;

        sidebar_library.openPanelIntoSideBar(seg_id);

        meta_data_str += appendHTMLTextForMetadata('Primary ID', seg_id, true);
        meta_data_str += "<div>Variable Name : " + data_library.variable_name_list[layer_name] + "</div>";
        meta_data_str += "<div>Layer Name : " + layer_name + "</div>";
        meta_data_str += appendHTMLTextForMetadata('GRU ID', data.GRU_ID, false);
        meta_data_str += appendHTMLTextForMetadata('HRU ID', data.HRU_ID, true);
        meta_data_str += appendHTMLTextForMetadata('Length', data.Length, true);
        meta_data_str += appendHTMLTextForMetadata('Flow Accumulation', data.flow_acc, true);
        meta_data_str += appendHTMLTextForMetadata('Lake Name', data.Lake_name, false);
        meta_data_str += appendHTMLTextForMetadata('Lake Area', data.Lake_area, true);
        meta_data_str += appendHTMLTextForMetadata('HRU Area', data.HRU_area, true);
        meta_data_str += appendHTMLTextForMetadata('Center Latitude', data.center_lat, true);
        meta_data_str += appendHTMLTextForMetadata('Center Longitude', data.center_lon, true);

        $('#' + section_preview_div).html(meta_data_str);

        sidebar_library.sidebar_option[layer_name] = sidebar_library.sidebar_option[layer_name].sort((a, b) => (a.section_id > b.section_id) ? 1 : -1);

        var temp_array_index = [];
        var index = 0;
        var div_id = "";
        for(var i=0; i < sidebar_library.sidebar_option[layer_name].length; i++)
        {            
            if(temp_array_index.indexOf(sidebar_library.sidebar_option[layer_name][i].section_id) == -1)
            {
                div_id = sidebar_library.appendSectionToPanelIntoSideBar(seg_id, sidebar_library.sidebar_option[layer_name][i].title, 
                    sidebar_library.sidebar_option[layer_name][i].section_id);                
                temp_array_index.push(sidebar_library.sidebar_option[layer_name][i].section_id);
                index++;
            }

            var chart_id = div_id + "_" + sidebar_library.sidebar_option[layer_name][i].section_id + i;
            $('#'+div_id).append("<div id='"+ chart_id +"'></div>");

            if(sidebar_library.sidebar_option[layer_name][i].chart_type == 'Heatmap')
                drawHistoryHeatMapChart('#' + chart_id, seg_id, sidebar_library.sidebar_option[layer_name][i].layer_name, 
                    year_range, sidebar_library.sidebar_option[layer_name][i]);
            else if (sidebar_library.sidebar_option[layer_name][i].chart_type == 'LineChart')
                drawHistoryLineChartChart('#' + chart_id, seg_id, sidebar_library.sidebar_option[layer_name][i].layer_name, 
                    year_range, sidebar_library.sidebar_option[layer_name][i]);
        }

    });

}

function addComparisonTable(seg_id, layer_name, color){

    d3.json("Data/" + data_library.variable_name_list[layer_name] + "/Monthly/id_" + seg_id + ".json").then(function(d) {
        var data = d.data;
        var aggregate_val = "average";

        console.log(data);

        var processed_data = {'name': 'ID-' + seg_id, 'color': color};

        var month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'];
        
        var year_list = Object.keys(data);
        
        var temp_array = [];

        for(var year_index=0; year_index<(year_list.length);year_index++){
            
            for(var month_index=0; month_index < month_list.length; month_index++){
                
                var obj = {};
                obj['date'] = year_list[year_index] + " " + month_list[month_index];
                obj['value'] = data[year_list[year_index]][month_index][aggregate_val];
                temp_array.push(obj);                              
            }
        }

        processed_data['values'] = temp_array;
        sidebar_library.comparison_chart_data.push(processed_data);
        $('#comparisonChart').html('');
        drawMultiSeriesLineChart();
        //$('#accordionExample_comparisonChart').collapse('show');
        
    });

}

function removeFromSideBar(seg_id, layer_name, color){
    //alert(seg_id);
    // Removing selection shape from map
    for(var i=0; i<sidebar_library.pinned_feature_list.length; i++){
        if(sidebar_library.pinned_feature_list[i].seg_id == seg_id){
            sidebar_library.pinned_feature_list[i].geofeature.removeFrom(map_library.map);
        }
    }
    // Making color available
    for(var i=0; i<sidebar_library.color_list.length; i++)
        if(sidebar_library.color_list[i].color == color){
            sidebar_library.color_list[i].available = true;
            break;
        }

    sidebar_library.openPanelIntoSideBar('preview');

    // Removing tab from sidebar
    sidebar_library.removePanelIntoSideBar(seg_id);
}

function showMetaDataInfo(seg_id, layer_name){

    var sidebar = sidebar_library.sidebar;
    var year_range = [animation_library.start_year, animation_library.end_year];
    var aggregate_val = 'average';
    //if(map_library.button_chart_option[layer_name][index].aggreagation_type != undefined)
    //    aggregate_val = map_library.button_chart_option[layer_name][index].aggreagation_type;
    
    $('#segment_info').html(data_library.connecting_id_list[layer_name] + ': ' + seg_id );
    var meta_data_str = "";

    

    d3.json("Data/MetaData/" + data_library.connecting_id_list[layer_name] + "_" + seg_id + ".json").then(function(d) {
        var data = d.data;

        meta_data_str += appendHTMLTextForMetadata('Primary ID', seg_id, true);
        meta_data_str += "<div>Variable Name : " + data_library.variable_name_list[layer_name] + "</div>";
        meta_data_str += "<div>Layer Name : " + layer_name + "</div>";
        meta_data_str += appendHTMLTextForMetadata('GRU ID', data.GRU_ID, true);
        meta_data_str += appendHTMLTextForMetadata('HRU ID', data.HRU_ID, true);        
        meta_data_str += appendHTMLTextForMetadata('Length', data.Length, true);
        meta_data_str += appendHTMLTextForMetadata('Flow Accumulation', data.flow_acc, true);
        meta_data_str += appendHTMLTextForMetadata('Lake Name', data.Lake_name, false);
        meta_data_str += appendHTMLTextForMetadata('Lake Area', data.Lake_area, true);
        meta_data_str += appendHTMLTextForMetadata('HRU Area', data.HRU_area, true);
        meta_data_str += appendHTMLTextForMetadata('Center Latitude', data.center_lat, true);
        meta_data_str += appendHTMLTextForMetadata('Center Longitude', data.center_lon, true);

        $('#meta_info_div').html(meta_data_str);
    });

    //sidebar.open('home');

    var total_tab = sidebar._tabitems.length;
    for(var i = 0; i<(total_tab-1); i++)
        sidebar.removePanel('sidebar_id_' + i);

    // Filling empty chart option
    for(var i=0; i < map_library.sidebar_option[layer_name].length; i++)
    {
        if(map_library.sidebar_option[layer_name][i].tab_no == undefined)
            map_library.sidebar_option[layer_name][i].tab_no = 0;
        if(map_library.sidebar_option[layer_name][i].layer_name == undefined)
            map_library.sidebar_option[layer_name][i].layer_name = layer_name;
    }


    map_library.sidebar_option[layer_name] = map_library.sidebar_option[layer_name].sort((a, b) => (a.tab_no > b.tab_no) ? 1 : -1);

    var temp_array_index = [];
    var index = 0;
    for(var i=0; i < map_library.sidebar_option[layer_name].length; i++)
    {
        if(temp_array_index.indexOf(map_library.sidebar_option[layer_name][i].tab_no) == -1)
        {
            var panelContent = {
                id: 'sidebar_id_' + index,                     // UID, used to access the panel
                tab: '<i class="fa fa-gear"></i>',  // content can be passed as HTML string,
                pane: '<div id=\'sidebar_chart_' + map_library.sidebar_option[layer_name][i].tab_no + '\'></div>',        // DOM elements can be passed, too
                title: map_library.sidebar_option[layer_name][i].title,              // an optional pane header
                position: 'top'                  // optional vertical alignment, defaults to 'top'
            };
            sidebar.addPanel(panelContent);
            temp_array_index.push(map_library.sidebar_option[layer_name][i].tab_no);
            index++;
        }

        if(map_library.sidebar_option[layer_name][i].chart_type == 'Heatmap')
            drawHistoryHeatMapChart('#sidebar_chart_' + map_library.sidebar_option[layer_name][i].tab_no, 
                seg_id, map_library.sidebar_option[layer_name][i].layer_name, 
                year_range, map_library.sidebar_option[layer_name][i]);
        else if (map_library.sidebar_option[layer_name][i].chart_type == 'LineChart')
            drawHistoryLineChartChart('#sidebar_chart_' + map_library.sidebar_option[layer_name][i].tab_no, 
                seg_id, map_library.sidebar_option[layer_name][i].layer_name, year_range, 
                map_library.sidebar_option[layer_name][i]);
        
        

    }

    //$('#historyHeatMap').html('');

    //if(map_library.button_chart_type[layer_name][index] == 'Heatmap')
    //    drawHistoryHeatMapChart(seg_id, layer_name, year_range, map_library.button_chart_option[layer_name][index]);
    //else if (map_library.button_chart_type[layer_name][index] == 'LineChart')
    //    drawHistoryLineChartChart(seg_id, layer_name, year_range, map_library.button_chart_option[layer_name][index]);
}

function appendHTMLTextForMetadata(label_name, value, isNumber){
    var temp_text = '';
    if(value != undefined)
    {
        temp_text += "<div>" + label_name + " : ";
        if(isNumber)
            temp_text += value.toFixed(2);
        else
            temp_text += value;

        temp_text += "</div>";
    }
        
    return temp_text;
}