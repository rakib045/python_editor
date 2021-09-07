function showMetaDataInfo(seg_id, layer_name, chart_type, aggregation_type){

    var sidebar = map_library.sidebar;
    var year_range = [animation_library.start_year, animation_library.end_year];
    var aggregate_val = aggregation_type;

    sidebar.open('home');
    
    $('#segment_info').html(data_library.connecting_id_list[layer_name] + ': ' + seg_id );
    var meta_data_str = "";

    $('#historyHeatMap').html('');

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

    if(chart_type == 'Heatmap')
        drawHistoryHeatMapChart(seg_id, layer_name, year_range, aggregate_val);
    else if (chart_type == 'LineChart')
        drawHistoryLineChartChart(seg_id, layer_name, year_range, aggregate_val);
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