function showMetaDataInfo(sidebar, seg_id, layer_name){
    sidebar.open('home');
    
    $('#segment_info').html('Segment ID: ' + seg_id );
    var meta_data_str = "";

    $('#historyHeatMap').html('');

    d3.json("Data/MetaData/" + seg_id + ".json").then(function(d) {
        var data = d.data;

        meta_data_str += "<div>Variable Name : " + data_library.variable_name_list[layer_name] + "</div>";
        meta_data_str += appendHTMLTextForMetadata('Length', data.Length, true);
        meta_data_str += appendHTMLTextForMetadata('Flow Accumulation', data.flow_acc, true);
        meta_data_str += appendHTMLTextForMetadata('Lake Name', data.Lake_name, false);
        meta_data_str += appendHTMLTextForMetadata('Lake Area', data.Lake_area, true);

        $('#meta_info_div').html(meta_data_str);
    });
    drawHistoryHeatMapChart(seg_id, layer_name);
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