function showMetaDataInfo(seg_id){
    sidebar.open('home');
    
    $('#segment_info').html('Segment ID: ' + seg_id );
    var meta_data_str = "";

    $('#historyHeatMap').html('');

    d3.json("Data/MetaData/" + seg_id + ".json").then(function(d) {
        var data = d.data;

        meta_data_str += "<div>Variable : IRFroutedRunoff in m3/s</div>";
        meta_data_str += "<div>Length : "+ data.Length.toFixed(2) +"</div>";
        meta_data_str += "<div>Flow Accumulation : "+ data.flow_acc.toFixed(2) +"</div>";

        $('#meta_info_div').html(meta_data_str);
    });
    drawHistoryHeatMapChart(seg_id, 'IRFroutedRunoff');
}