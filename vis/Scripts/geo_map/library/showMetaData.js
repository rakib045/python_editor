function showMetaDataInfo(seg_id, layer_name){

    var sidebar = map_library.sidebar;
    var year_range = [animation_library.start_year, animation_library.end_year];
    var aggregate_val = 'average';
    //if(map_library.button_chart_option[layer_name][index].aggreagation_type != undefined)
    //    aggregate_val = map_library.button_chart_option[layer_name][index].aggreagation_type;
    
    $('#segment_info').html(data_library.connecting_id_list[layer_name] + ': ' + seg_id );
    var meta_data_str = "";

    

    d3.json("Data/MetaData/" + data_library.connecting_id_list[layer_name] + "_" + seg_id + ".json").then(function(d) {
        var data = d.data;

        meta_data_str += "<div>Variable Name : " + data_library.variable_name_list[layer_name] + "</div>";
        meta_data_str += "<div>Layer Name : " + layer_name + "</div>";
        meta_data_str += appendHTMLTextForMetadata('Length', data.Length, true);
        meta_data_str += appendHTMLTextForMetadata('Flow Accumulation', data.flow_acc, true);
        meta_data_str += appendHTMLTextForMetadata('Lake Name', data.Lake_name, false);
        meta_data_str += appendHTMLTextForMetadata('Lake Area', data.Lake_area, true);
        meta_data_str += appendHTMLTextForMetadata('HRU Area', data.HRU_area, true);
        meta_data_str += appendHTMLTextForMetadata('Center Latitude', data.center_lat, true);
        meta_data_str += appendHTMLTextForMetadata('Center Longitude', data.center_lon, true);

        $('#meta_info_div').html(meta_data_str);
    });

    sidebar.open('home');

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